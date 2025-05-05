import logging
import socketserver
import json
import os
from http.server import SimpleHTTPRequestHandler
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs
from .process import SlaveProcess
import uuid
from core.services.template_engine import TemplateEngine
from core.facade.template import Template
from core.foundation.application import Application
from core.http.request import Request

logger = logging.getLogger('slave.server')

class RouterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.process = kwargs.pop('process', None)
        self.template_engine = TemplateEngine()
        self.app = Application()
        self.router = self.app.make('router')
        # Set up static file directory
        self.static_dir = os.path.join(os.getcwd(), 'public')
        if not os.path.exists(self.static_dir):
            os.makedirs(self.static_dir)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        request = None
        try:
            # Parse URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query = parse_qs(parsed_url.query)

            # Create and set current request
            request = Request(
                app=self.app,
                method='GET',
                path=path,
                headers=dict(self.headers)
            )
            request.set_current()

            # Check if this is a static file request
            if path.startswith('/static/'):
                self.serve_static_file(path[7:])  # Remove /static/ prefix
                return

            # Find route
            route = self.router.find_route('GET', path)
            if route:
                # Execute route action
                response = route.action()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                return
            else:
                self.send_error(404, "Route not found")
        except Exception as e:
            logger.error(f"Error handling GET request: {str(e)}")
            self.send_error(500, str(e))
        finally:
            # Clear current request
            if request:
                request.clear_current()

    def do_POST(self):
        """Handle POST requests"""
        try:
            # Parse URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path

            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read request body
            body = self.rfile.read(content_length).decode()
            
            # Parse JSON body if content type is application/json
            if self.headers.get('Content-Type') == 'application/json':
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    self.send_error(400, "Invalid JSON in request body")
                    return
            
            # Find route
            route = self.router.find_route('POST', path)
            if route:
                # Execute route action
                response = route.action()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                return

            # If no route found, send 404
            self.send_error(404, "Route not found")
            
        except Exception as e:
            logger.error(f"Error handling POST request: {str(e)}")
            self.send_error(500, str(e))

    def handle_health(self):
        """Handle health check request"""
        response = {
            'status': 'healthy',
            'queue_size': self.process.get_queue_size()
        }
        self.send_json_response(response)

    def handle_metrics(self):
        """Handle metrics request"""
        response = {
            'status': 'success',
            'metrics': {
                'queue_size': self.process.get_queue_size(),
                'commands_processed': len(self.process.command_handlers),
                'uptime': 'TODO'  # TODO: Add uptime tracking
            }
        }
        self.send_json_response(response)

    def serve_static_file(self, path: str):
        """Serve a static file"""
        file_path = os.path.join(self.static_dir, path)
        
        # Prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(self.static_dir)):
            self.send_error(403, "Access denied")
            return
            
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Set content type based on file extension
            ext = os.path.splitext(path)[1]
            content_type = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.ico': 'image/x-icon'
            }.get(ext.lower(), 'application/octet-stream')
                
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            logger.error(f"Error serving static file: {str(e)}")
            self.send_error(500, str(e))

    def send_json_response(self, data: Dict[str, Any]):
        """Send a JSON response"""
        response = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

class RouterServer:
    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        workers: int = 4,
        process: Optional[SlaveProcess] = None
    ):
        self.host = host
        self.port = port
        self.workers = workers
        self.process = process or SlaveProcess()
        
        # Create server class
        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            allow_reuse_address = True
            
        # Create handler class that includes process
        def handler(*args, **kwargs):
            return RouterHandler(*args, process=self.process, **kwargs)
            
        self.server = ThreadedTCPServer((self.host, self.port), handler)

    def start(self):
        """Start the server"""
        try:
            logger.info(f"Starting server on {self.host}:{self.port} with {self.workers} workers")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down server")
            self.server.shutdown()
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise 