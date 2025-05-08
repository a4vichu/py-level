import os
import click
import logging
import asyncio
from typing import Optional
from .process import SlaveProcess
from .config import Config
from .exceptions import SlaveProcessError
from .server import RouterServer
from .live_reload import LiveReload

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('slave.cli')

# Global process instance
process: Optional[SlaveProcess] = None
config = Config()

@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug mode')
def cli(debug):
    """Slave server command line interface"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

# Server Commands
@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--port', default=8000, help='Port to listen on')
@click.option('--workers', default=4, help='Number of worker processes')
def serve(host: str, port: int, workers: int):
    """Start the slave server"""
    try:
        process = SlaveProcess(debug=logging.getLogger().level == logging.DEBUG)
        server = RouterServer(
            host=host,
            port=port,
            workers=workers,
            process=process
        )
        server.start()
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise click.ClickException(str(e))

@cli.command()
def stop():
    """Stop the slave server"""
    global process
    if process and process.running:
        asyncio.run(process.stop())
        logger.info("Server stopped")
    else:
        logger.warning("No running server found")

@cli.command()
def status():
    """Check server status"""
    global process
    if process:
        status = "Running" if process.running else "Stopped"
        queue_size = process.get_queue_size()
        click.echo(f"Server Status: {status}")
        click.echo(f"Command Queue Size: {queue_size}")
    else:
        click.echo("Server Status: Not initialized")

@cli.command()
def restart():
    """Restart the slave server"""
    global process
    if process and process.running:
        asyncio.run(process.stop())
        logger.info("Server stopped")
    
    # Get current config
    port = config.get('port', 8000)
    workers = config.get('workers', 4)
    host = config.get('host', '127.0.0.1')
    
    # Restart server
    process = SlaveProcess(debug=logging.getLogger().level == logging.DEBUG)
    logger.info(f"Restarting server on {host}:{port} with {workers} workers")
    asyncio.run(process.start())

@cli.command()
@click.option('--watch', multiple=True, help='Paths to watch for changes')
def dev(watch):
    """Start the slave server with live reload"""
    try:
        # If no watch paths specified, watch the current directory
        watch_paths = watch if watch else ['.']
        
        # Start live reload
        live_reload = LiveReload(watch_paths=watch_paths)
        live_reload.start()
    except Exception as e:
        logger.error(f"Failed to start development server: {str(e)}")
        raise click.ClickException(str(e))

# Controller Commands
@cli.group()
def make():
    """Create new components"""
    pass

@make.command('controller')
@click.argument('name')
@click.option('--methods', default='get,post,put,delete', help='HTTP methods to implement')
def make_controller(name: str, methods: str):
    """Create a new controller"""
    from .controllers import create_controller
    try:
        methods_list = [m.strip().lower() for m in methods.split(',')]
        create_controller(name, methods_list)
        logger.info(f"Created controller: {name}")
    except Exception as e:
        logger.error(f"Failed to create controller: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('list:controllers')
def list_controllers():
    """List all controllers"""
    from .controllers import list_controllers
    try:
        controllers = list_controllers()
        if controllers:
            click.echo("Available controllers:")
            for controller in controllers:
                click.echo(f"  - {controller}")
        else:
            click.echo("No controllers found")
    except Exception as e:
        logger.error(f"Failed to list controllers: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('remove:controller')
@click.argument('name')
def remove_controller(name: str):
    """Remove a controller"""
    from .controllers import remove_controller
    try:
        remove_controller(name)
        logger.info(f"Removed controller: {name}")
    except Exception as e:
        logger.error(f"Failed to remove controller: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('make:model')
@click.argument('name')
@click.option('-m', '--migration', is_flag=True, help='Create a migration file')
@click.option('-c', '--controller', is_flag=True, help='Create a controller')
def make_model(name: str, migration: bool, controller: bool):
    """Create a new model with optional migration and controller"""
    try:
        # Import here to avoid circular imports
        from .models import create_model
        from .controllers import create_controller
        from .migrations import create_migration
        
        # Create the model
        create_model(name)
        logger.info(f"Created model: {name}")
        
        # Create migration if requested
        if migration:
            create_migration(name)
            logger.info(f"Created migration for model: {name}")
            
        # Create controller if requested
        if controller:
            create_controller(name, ['get', 'post', 'put', 'delete'])
            logger.info(f"Created controller for model: {name}")
            
    except Exception as e:
        logger.error(f"Failed to create model components: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('make:request')
@click.argument('name')
def make_request(name: str):
    """Create a new form request class"""
    try:
        # Convert name to proper format
        name = name.replace('-', '_').replace(' ', '_')
        class_name = ''.join(word.capitalize() for word in name.split('_'))
        if not class_name.endswith('Request'):
            class_name += 'Request'

        # Create the request file
        request_path = os.path.join('app', 'requests', f"{name}.py")
        os.makedirs(os.path.dirname(request_path), exist_ok=True)

        template = f'''from core.http.request import Request

class {class_name}(Request):
    """
    Form request for {name}
    """
    def rules(self):
        return {{
            # Define your validation rules here
            # Example:
            # 'email': ['required', 'email'],
            # 'password': ['required', 'string', 'min:8'],
        }}

    def messages(self):
        return {{
            # Define your custom error messages here
            # Example:
            # 'email.required': 'Please provide your email address',
            # 'password.min': 'Password must be at least 8 characters',
        }}

    def authorize(self):
        return True
'''

        with open(request_path, 'w') as f:
            f.write(template)

        logger.info(f"Created request class: {request_path}")
        click.echo(f"Request class created successfully: {request_path}")
    except Exception as e:
        logger.error(f"Failed to create request class: {str(e)}")
        raise click.ClickException(str(e))

# Configuration Commands
@cli.group()
def config():
    """Manage server configuration"""
    pass

@config.command('set')
@click.argument('key_value')
def config_set(key_value: str):
    """Set a configuration value (format: key=value)"""
    try:
        key, value = key_value.split('=', 1)
        config.set(key.strip(), value.strip())
        logger.info(f"Set config {key}={value}")
    except ValueError:
        raise click.ClickException("Invalid format. Use: key=value")
    except Exception as e:
        logger.error(f"Failed to set config: {str(e)}")
        raise click.ClickException(str(e))

@config.command('get')
@click.argument('key')
def config_get(key: str):
    """Get a configuration value"""
    try:
        value = config.get(key)
        if value is not None:
            click.echo(f"{key}={value}")
        else:
            click.echo(f"No value set for {key}")
    except Exception as e:
        logger.error(f"Failed to get config: {str(e)}")
        raise click.ClickException(str(e))

@config.command('list')
def config_list():
    """List all configurations"""
    try:
        configs = config.list_all()
        if configs:
            click.echo("Current configuration:")
            for key, value in configs.items():
                click.echo(f"  {key}={value}")
        else:
            click.echo("No configurations set")
    except Exception as e:
        logger.error(f"Failed to list configs: {str(e)}")
        raise click.ClickException(str(e))

# Process Management Commands
@cli.group()
def process():
    """Manage worker processes"""
    pass

@process.command('start')
@click.argument('worker_name')
def process_start(worker_name: str):
    """Start a worker process"""
    try:
        # Implementation for starting a worker process
        logger.info(f"Starting worker: {worker_name}")
        click.echo(f"Started worker: {worker_name}")
    except Exception as e:
        logger.error(f"Failed to start worker: {str(e)}")
        raise click.ClickException(str(e))

@process.command('stop')
@click.argument('worker_name')
def process_stop(worker_name: str):
    """Stop a worker process"""
    try:
        # Implementation for stopping a worker process
        logger.info(f"Stopping worker: {worker_name}")
        click.echo(f"Stopped worker: {worker_name}")
    except Exception as e:
        logger.error(f"Failed to stop worker: {str(e)}")
        raise click.ClickException(str(e))

@process.command('list')
def process_list():
    """List all worker processes"""
    try:
        # Implementation for listing worker processes
        click.echo("Active workers:")
        # Add actual worker listing logic here
    except Exception as e:
        logger.error(f"Failed to list workers: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('migrate')
@click.option('--force', is_flag=True, help='Force the operation to run in production')
@click.option('--database', default=None, help='Database connection to use')
def migrate(force: bool, database: str):
    """Run the database migrations"""
    try:
        from core.database.migrations import Migration
        migration = Migration(database)
        migration.up()
        logger.info("✓ Migrations completed successfully")
    except Exception as e:
        logger.error(f"Failed to run migrations: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('migrate:refresh')
@click.option('--force', is_flag=True, help='Force the operation to run in production')
@click.option('--database', default=None, help='Database connection to use')
def migrate_refresh(force: bool, database: str):
    """Refresh all migrations by rolling back and re-running them"""
    try:
        from core.database.migrations import Migration
        migration = Migration(database)
        migration.refresh()
        logger.info("✓ Migrations refreshed successfully")
    except Exception as e:
        logger.error(f"Failed to refresh migrations: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('migrate:rollback')
@click.option('--steps', default=1, help='Number of migrations to rollback')
@click.option('--force', is_flag=True, help='Force the operation to run in production')
@click.option('--database', default=None, help='Database connection to use')
def migrate_rollback(steps: int, force: bool, database: str):
    """Rollback the last N migrations"""
    try:
        from core.database.migrations import Migration
        migration = Migration(database)
        migration.rollback(steps)
        logger.info(f"✓ Rolled back {steps} migration(s) successfully")
    except Exception as e:
        logger.error(f"Failed to rollback migrations: {str(e)}")
        raise click.ClickException(str(e))

@cli.command('migrate:fresh')
@click.option('--force', is_flag=True, help='Force the operation to run in production')
@click.option('--database', default=None, help='Database connection to use')
def migrate_fresh(force: bool, database: str):
    """Drop all tables and re-run all migrations"""
    try:
        from core.database.migrations import Migration
        migration = Migration(database)
        migration.fresh()
        logger.info("✓ Database refreshed successfully")
    except Exception as e:
        logger.error(f"Failed to refresh database: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli() 