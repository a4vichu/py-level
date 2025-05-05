# Implementation Details

## Core Classes Implementation

### 1. SlaveProcess Class

The main process class that handles command execution:

```python
class SlaveProcess:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.command_validator = CommandValidator()
        self.response_formatter = ResponseFormatter()
        self.command_handlers: Dict[str, Callable] = {}
        self.async_command_handlers: Dict[str, Callable] = {}
        self.running = False
        self.command_queue = asyncio.Queue()

    async def start(self):
        """Start the process and handle commands"""
        self.running = True
        while self.running:
            command = await self.command_queue.get()
            await self._process_command(command)

    async def _process_command(self, command: Command):
        """Process a single command"""
        try:
            handler = self._get_handler(command.command_type)
            result = await self._execute_handler(handler, command)
            self._send_response(Response.success(command.command_id, result))
        except Exception as e:
            self._send_error_response(command.command_id, str(e))
```

### 2. Command Class

Represents a command to be executed:

```python
class Command:
    def __init__(
        self,
        command_id: str,
        command_type: str,
        parameters: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ):
        self.command_id = command_id
        self.command_type = command_type
        self.parameters = parameters
        self.timestamp = timestamp or datetime.utcnow()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Command':
        """Create command from dictionary"""
        required = ['command_id', 'command_type', 'parameters']
        for field in required:
            if field not in data:
                raise ValidationError(f"Missing {field}")
        return cls(**data)
```

### 3. BaseController Class

Base class for all controllers:

```python
class BaseController(ABC):
    def __init__(self):
        self.request: Optional[Dict[str, Any]] = None
        self.response: Dict[str, Any] = {
            'status': 'success',
            'data': None,
            'error': None
        }

    @abstractmethod
    async def handle(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the request"""
        pass

    def validate(self, rules: Dict[str, Any]) -> bool:
        """Validate request against rules"""
        if not self.request:
            return False
        for field, rule in rules.items():
            if not self._validate_field(field, rule):
                return False
        return True
```

## Command Implementation

### 1. CLI Commands

Using Click for command implementation:

```python
@click.group()
def cli():
    """Main CLI entry point"""
    pass

@cli.command()
@click.option('--port', default=8000)
@click.option('--workers', default=4)
def serve(port: int, workers: int):
    """Start the server"""
    process = SlaveProcess()
    process.start(port=port, workers=workers)
```

### 2. Controller Commands

Controller creation and management:

```python
def create_controller(name: str, methods: List[str]) -> None:
    """Create a new controller"""
    template = Template(CONTROLLER_TEMPLATE)
    content = template.render(name=name, methods=methods)
    
    controller_path = _get_controller_path(name)
    with open(controller_path, 'w') as f:
        f.write(content)
```

## Configuration Management

### 1. Config Class

Configuration management implementation:

```python
class Config:
    def __init__(self, config_file: str = None):
        self.config_file = config_file or 'config.json'
        self._config: Dict[str, Any] = {}
        self._load()

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with environment variable override"""
        env_key = f"SLAVE_{key.upper()}"
        return os.getenv(env_key) or self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set config value"""
        self._config[key] = value
        self._save()
```

## Async Implementation

### 1. Command Queue

Asynchronous command queue handling:

```python
class CommandQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self._running = False

    async def start(self):
        """Start processing commands"""
        self._running = True
        while self._running:
            command = await self.queue.get()
            try:
                await self._process_command(command)
            finally:
                self.queue.task_done()

    async def stop(self):
        """Stop processing commands"""
        self._running = False
        await self.queue.join()
```

### 2. Async Controller Methods

Example of async controller implementation:

```python
class UserController(BaseController):
    async def get(self, request: Dict[str, Any]) -> Dict[str, Any]:
        user_id = request.get('id')
        if not user_id:
            return self.error("Missing user ID")
            
        # Simulate async database query
        user = await self.db.fetch_user(user_id)
        return self.success(user)
```

## Error Handling

### 1. Exception Hierarchy

Custom exception classes:

```python
class SlaveProcessError(Exception):
    """Base exception for all slave process errors"""
    pass

class ValidationError(SlaveProcessError):
    """Raised when validation fails"""
    pass

class CommandError(SlaveProcessError):
    """Raised when command execution fails"""
    pass
```

### 2. Error Response

Error response handling:

```python
def _send_error_response(self, command_id: str, error: str):
    """Send error response"""
    response = Response(
        command_id=command_id,
        status='error',
        error=error
    )
    self._send_response(response)
```

## Testing Implementation

### 1. Unit Tests

Example of unit test implementation:

```python
class TestSlaveProcess:
    @pytest.fixture
    def process(self):
        return SlaveProcess(debug=True)

    async def test_command_execution(self, process):
        command = Command(
            command_id='test',
            command_type='echo',
            parameters={'message': 'hello'}
        )
        result = await process._process_command(command)
        assert result['message'] == 'hello'
```

### 2. Integration Tests

Example of integration test:

```python
class TestControllerIntegration:
    async def test_controller_workflow(self):
        # Create controller
        create_controller('TestController', ['get'])
        
        # Send request
        process = SlaveProcess()
        response = await process.handle_request({
            'controller': 'TestController',
            'method': 'get',
            'parameters': {'id': 1}
        })
        
        assert response['status'] == 'success'
``` 