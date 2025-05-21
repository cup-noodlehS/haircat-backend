#!/usr/bin/env python
"""
Development server script for running Django with WebSockets support.
"""
import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def main():
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Check if Daphne is installed
    try:
        import daphne
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "daphne", "channels[daphne]"])
    
    # Start the Daphne server
    print("Starting development server with WebSocket support...")
    server_proc = subprocess.Popen([
        sys.executable, "-m", "daphne", 
        "-b", "0.0.0.0", 
        "-p", "8000", 
        "haircat.asgi:application"
    ])
    
    try:
        print("\nDevelopment server is running at http://127.0.0.1:8000/")
        print("WebSocket endpoint is available at ws://127.0.0.1:8000/ws/webhooks/")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_proc.send_signal(signal.SIGTERM)
        server_proc.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main() 