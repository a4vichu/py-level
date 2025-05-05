import asyncio
import json
import sys
import logging
import uuid
from typing import Dict, Any, Optional, Callable, Coroutine
from datetime import datetime
from .command import Command, CommandValidator
from .response import Response, ResponseFormatter
from .exceptions import (
    SlaveProcessError,
    ValidationError,
    CommandError,
    CommandTimeoutError,
    InvalidStateError
)

logger = logging.getLogger('slave.process')

class SlaveProcess:
    """Main slave process class that handles command execution"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.command_validator = CommandValidator()
        self.response_formatter = ResponseFormatter()
        self.command_handlers: Dict[str, Callable] = {
            'GET': self._handle_get,
            'POST': self._handle_post
        }
        self.async_command_handlers: Dict[str, Callable] = {}
        self.running = False
        self.command_queue = asyncio.Queue()
        
        # Configure logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SlaveProcess')
        
    def register_command_handler(
        self,
        command_type: str,
        handler: Callable[[Command], Dict[str, Any]],
        is_async: bool = False
    ):
        """Register a command handler"""
        self.command_validator.register_command_type(command_type)
        if is_async:
            self.async_command_handlers[command_type] = handler
        else:
            self.command_handlers[command_type] = handler
            
    async def start(self):
        """Start the slave process"""
        self.running = True
        self.logger.info("Slave process started")
        
        try:
            while self.running:
                command_str = await self._read_input()
                if command_str:
                    await self._process_command(command_str)
        except Exception as e:
            self.logger.error(f"Fatal error in slave process: {str(e)}")
            raise
        finally:
            self.running = False
            self.logger.info("Slave process stopped")
            
    async def stop(self):
        """Stop the slave process"""
        self.running = False
        self.logger.info("Stopping slave process...")
        
    async def _read_input(self) -> Optional[str]:
        """Read input from stdin"""
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
        except Exception as e:
            self.logger.error(f"Error reading input: {str(e)}")
            return None
            
    async def _process_command(self, command_str: str):
        """Process a command string"""
        try:
            # Validate and parse command
            command = self.command_validator.validate(command_str.strip())
            
            # Queue command for execution
            await self.command_queue.put(command)
            
            # Send pending response
            self._send_response(
                Response.pending(command.command_id)
            )
            
            # Execute command
            if command.command_type in self.async_command_handlers:
                handler = self.async_command_handlers[command.command_type]
                result = await handler(command)
            elif command.command_type in self.command_handlers:
                handler = self.command_handlers[command.command_type]
                result = await asyncio.get_event_loop().run_in_executor(
                    None, handler, command
                )
            else:
                raise CommandError(f"No handler for command type: {command.command_type}")
                
            # Send success response
            self._send_response(
                Response.success(command.command_id, result)
            )
            
        except ValidationError as e:
            self.logger.warning(f"Validation error: {str(e)}")
            self._send_error_response(command_str, str(e))
            
        except CommandError as e:
            self.logger.error(f"Command execution error: {str(e)}")
            self._send_error_response(command_str, str(e))
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self._send_error_response(command_str, "Internal error occurred")
            
    def _send_response(self, response: Response):
        """Send a response to stdout"""
        try:
            print(response.to_json(), flush=True)
        except Exception as e:
            self.logger.error(f"Error sending response: {str(e)}")
            
    def _send_error_response(self, command_str: str, error_message: str):
        """Send an error response"""
        try:
            # Try to extract command_id from the command string
            command_id = str(uuid.uuid4())  # Default to random UUID
            try:
                data = json.loads(command_str)
                if isinstance(data, dict) and 'command_id' in data:
                    command_id = data['command_id']
            except:
                pass
                
            response = Response.error(command_id, error_message)
            self._send_response(response)
            
        except Exception as e:
            self.logger.error(f"Error sending error response: {str(e)}")
            
    async def send_progress_update(
        self,
        command_id: str,
        progress: float,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Send a progress update for a long-running command"""
        response = Response.pending(
            command_id,
            {
                'progress': progress,
                'status': status,
                **(details or {})
            }
        )
        self._send_response(response)
        
    def get_queue_size(self) -> int:
        """Get the current size of the command queue"""
        return self.command_queue.qsize()
        
    async def wait_for_queue_empty(self, timeout: Optional[float] = None):
        """Wait for the command queue to be empty"""
        try:
            if timeout is not None:
                await asyncio.wait_for(
                    self._wait_queue_empty(),
                    timeout=timeout
                )
            else:
                await self._wait_queue_empty()
        except asyncio.TimeoutError:
            raise CommandTimeoutError("Timeout waiting for queue to empty")
            
    async def _wait_queue_empty(self):
        """Helper method to wait for queue to be empty"""
        while not self.command_queue.empty():
            await asyncio.sleep(0.1)
            
    def handle_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a command"""
        try:
            # Validate command
            command = self.command_validator.validate(command_data)
            
            # Process command
            if command.command_type == 'GET':
                response = self.handle_get_command(command)
            elif command.command_type == 'POST':
                response = self.handle_post_command(command)
            else:
                response = Response.error(
                    command.command_id,
                    f"Unsupported command type: {command.command_type}"
                ).to_dict()
                
            return response
            
        except Exception as e:
            logger.error(f"Error handling command: {str(e)}")
            return Response.error(
                command_data.get('command_id', 'unknown'),
                str(e)
            ).to_dict()
            
    def handle_get_command(self, command: Command) -> Dict[str, Any]:
        """Handle GET command"""
        try:
            # For now, just return a success response
            return {
                'command_id': command.command_id,
                'status': 'success',
                'data': {
                    'message': 'GET command processed successfully',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error in handle_get_command: {str(e)}")
            return {
                'command_id': command.command_id,
                'status': 'error',
                'error': str(e)
            }
        
    def handle_post_command(self, command: Command) -> Dict[str, Any]:
        """Handle POST command"""
        # For now, just return a success response
        return Response.success(
            command.command_id,
            {'message': 'POST command processed successfully'}
        ).to_dict()
        
    def _handle_get(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GET command"""
        return {
            'path': command['command_id'],
            'params': command['parameters'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
    def _handle_post(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Handle POST command"""
        return {
            'path': command['command_id'],
            'body': command['parameters'].get('body'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
    def register_handler(self, command_type: str, handler: Callable) -> None:
        """Register a new command handler"""
        if command_type in self.command_handlers:
            logger.warning(f"Overwriting existing handler for {command_type}")
        self.command_handlers[command_type] = handler 