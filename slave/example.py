import asyncio
import json
import time
from typing import Dict, Any
from .process import SlaveProcess
from .command import Command
from .exceptions import CommandExecutionError

async def example_async_handler(command: Command) -> Dict[str, Any]:
    """Example async command handler"""
    # Simulate some async work
    await asyncio.sleep(1)
    return {
        'message': f'Async command {command.command_type} executed successfully',
        'parameters': command.parameters
    }

def example_sync_handler(command: Command) -> Dict[str, Any]:
    """Example sync command handler"""
    # Simulate some work
    time.sleep(1)
    return {
        'message': f'Sync command {command.command_type} executed successfully',
        'parameters': command.parameters
    }

async def long_running_task(command: Command, process: SlaveProcess) -> Dict[str, Any]:
    """Example of a long-running task with progress updates"""
    total_steps = 5
    
    for step in range(total_steps):
        # Simulate work
        await asyncio.sleep(1)
        
        # Send progress update
        progress = (step + 1) / total_steps
        await process.send_progress_update(
            command.command_id,
            progress,
            f'Processing step {step + 1}/{total_steps}',
            {'current_step': step + 1}
        )
    
    return {
        'message': 'Long-running task completed',
        'total_steps': total_steps
    }

async def main():
    # Create slave process instance
    process = SlaveProcess(debug=True)
    
    # Register command handlers
    process.register_command_handler('sync_command', example_sync_handler)
    process.register_command_handler('async_command', example_async_handler, is_async=True)
    process.register_command_handler(
        'long_running',
        lambda cmd: long_running_task(cmd, process),
        is_async=True
    )
    
    # Example command input simulation
    async def simulate_input():
        commands = [
            {
                'command_id': '1',
                'command_type': 'sync_command',
                'parameters': {'data': 'test1'}
            },
            {
                'command_id': '2',
                'command_type': 'async_command',
                'parameters': {'data': 'test2'}
            },
            {
                'command_id': '3',
                'command_type': 'long_running',
                'parameters': {'data': 'test3'}
            }
        ]
        
        for cmd in commands:
            # Simulate command input
            print(json.dumps(cmd), file=process._stdin)
            await asyncio.sleep(2)
    
    # Run input simulation and process in parallel
    await asyncio.gather(
        simulate_input(),
        process.start()
    )

if __name__ == '__main__':
    asyncio.run(main()) 