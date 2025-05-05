#!/usr/bin/env python
import sys
import os
from pathlib import Path

# Get the absolute path of the project root
project_root = Path(__file__).parent.absolute()

# Change to the project root directory
os.chdir(project_root)

# Add the project root to Python path
sys.path.append(str(project_root))
sys.path.append(str(project_root / 'app'))

from core.console.kernel import ConsoleKernel
from core.foundation.application import Application
from core.database.orm.model import Model
from core.utils.logger import Logger

def main():
    try:
        app = Application()
        kernel = ConsoleKernel()
        
        # Register built-in commands
        from app.console.commands.make_controller import MakeControllerCommand
        from app.console.commands.make_model import MakeModelCommand
        from app.console.commands.make_middleware import MakeMiddlewareCommand
        from app.console.commands.make_provider import MakeProviderCommand
        from app.console.commands.make_command import MakeCommandCommand
        from app.console.commands.make_migration import MakeMigrationCommand
        from app.console.commands.make_service import MakeServiceCommand
        from app.console.commands.make_service_model import MakeServiceModelCommand
        from app.console.commands.make_service_controller import MakeServiceControllerCommand
        from app.console.commands.make_event import MakeEventCommand
        from app.console.commands.make_service_event import MakeServiceEventCommand
        from app.console.commands.migrate import MigrateCommand
        from app.console.commands.migrate_rollback import MigrateRollbackCommand
        from app.console.commands.migrate_reset import MigrateResetCommand
        from app.console.commands.migrate_refresh import MigrateRefreshCommand
        from app.console.commands.migrate_status import MigrateStatusCommand
        from app.console.commands.migrate_service import MigrateServiceCommand
        from app.console.commands.db_seed import DbSeedCommand
        from app.console.commands.cache_clear import CacheClearCommand
        from app.console.commands.queue_work import QueueWorkCommand
        from app.console.commands.queue_listen import QueueListenCommand
        from app.console.commands.queue_restart import QueueRestartCommand
        from app.console.commands.route_list import RouteListCommand
        from app.console.commands.serve_command import ServeCommand
        from app.console.commands.watch import WatchCommand
        from app.console.commands.tinker import TinkerCommand
        from app.console.commands.help import HelpCommand
        from app.console.commands.remove_service import RemoveServiceCommand
        
        # Register commands
        kernel.register(MakeControllerCommand)
        kernel.register(MakeModelCommand)
        kernel.register(MakeMiddlewareCommand)
        kernel.register(MakeProviderCommand)
        kernel.register(MakeCommandCommand)
        kernel.register(MakeMigrationCommand)
        kernel.register(MakeServiceCommand)
        kernel.register(MakeServiceModelCommand)
        kernel.register(MakeServiceControllerCommand)
        kernel.register(MakeEventCommand)
        kernel.register(MakeServiceEventCommand)
        kernel.register(MigrateCommand)
        kernel.register(MigrateRollbackCommand)
        kernel.register(MigrateResetCommand)
        kernel.register(MigrateRefreshCommand)
        kernel.register(MigrateStatusCommand)
        kernel.register(MigrateServiceCommand)
        kernel.register(DbSeedCommand)
        kernel.register(CacheClearCommand)
        kernel.register(QueueWorkCommand)
        kernel.register(QueueListenCommand)
        kernel.register(QueueRestartCommand)
        kernel.register(RouteListCommand)
        kernel.register(ServeCommand)
        kernel.register(WatchCommand)
        kernel.register(TinkerCommand)
        kernel.register(HelpCommand)
        kernel.register(RemoveServiceCommand)
        
        # Run the command
        kernel.run(sys.argv[1:])
    except Exception as e:
        logger = Logger()
        logger.error(f"An error occurred: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == '__main__':
    main() 