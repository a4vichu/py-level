import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import os
import sys
import subprocess

logger = logging.getLogger('slave.live_reload')

class RestartHandler(FileSystemEventHandler):
    def __init__(self, server_process):
        self.server_process = server_process
        self.last_restart = 0
        self.restart_cooldown = 1  # Minimum seconds between restarts

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignore certain file types
        if event.src_path.endswith(('.pyc', '.pyo', '.pyd', '.git')):
            return
            
        current_time = time.time()
        if current_time - self.last_restart < self.restart_cooldown:
            return
            
        self.last_restart = current_time
        logger.info(f"Detected change in {event.src_path}")
        self.restart_server()

    def restart_server(self):
        logger.info("Restarting server...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        
        # Restart the server
        python = sys.executable
        self.server_process = subprocess.Popen([python, '-m', 'slave', 'serve'])

class LiveReload:
    def __init__(self, watch_paths=None):
        self.watch_paths = watch_paths or ['.']
        self.observer = Observer()
        self.server_process = None
        self.handler = None

    def start(self):
        # Start the server initially
        python = sys.executable
        self.server_process = subprocess.Popen([python, '-m', 'slave', 'serve'])
        
        # Set up file watching
        self.handler = RestartHandler(self.server_process)
        
        for path in self.watch_paths:
            self.observer.schedule(self.handler, path, recursive=True)
        
        self.observer.start()
        logger.info(f"Live reload started. Watching: {', '.join(self.watch_paths)}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.observer.stop()
        self.observer.join()
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        logger.info("Live reload stopped") 