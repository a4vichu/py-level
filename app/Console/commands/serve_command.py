from core.console.commands.command import Command
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import webbrowser
import os
from pathlib import Path
import time
import json

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                # Serve welcome page
                template_path = Path(__file__).parent.parent.parent.parent.parent / 'resources' / 'views' / 'welcome.html'
                
                with open(template_path, 'r') as f:
                    template = f.read()
                    
                data = {
                    'message': 'Welcome to the Framework! z',
                    'version': '1.0.0',
                    'status': 'running',
                    'server_info': {
                        'host': self.server.server_address[0],
                        'port': self.server.server_address[1],
                        'thread': threading.current_thread().name,
                        'time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                
                # Replace template variables
                for key, value in data.items():
                    if isinstance(value, dict):
                        value = json.dumps(value)
                    template = template.replace(f'{{{{ {key} }}}}', str(value))
                    
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(template.encode())
            else:
                # Handle other routes
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'500 Internal Server Error: {str(e)}'.encode())

class ServeCommand(Command):
    @property
    def signature(self) -> str:
        return 'serve'
        
    @property
    def description(self) -> str:
        return 'Serve the application using Python threaded server'
        
    def _configure_parser(self):
        self.add_argument('--host', default='127.0.0.1', help='The host to serve on')
        self.add_argument('--port', type=int, default=8000, help='The port to serve on')
        self.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
        self.add_argument('--max-threads', type=int, default=10, help='Maximum number of worker threads')
        
    def handle(self, *args, **kwargs):
        args = self.parse_args(args)
        
        # Create server
        server_address = (args.host, args.port)
        httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
        
        # Print server info
        print(f"Starting threaded server at http://{args.host}:{args.port}")
        print(f"Maximum worker threads: {args.max_threads}")
        print("Press Ctrl+C to stop the server")
        
        # Open browser if not disabled
        if not args.no_browser:
            url = f"http://{args.host}:{args.port}"
            threading.Timer(1.5, lambda: webbrowser.open(url)).start()
        
        try:
            # Start server
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close() 