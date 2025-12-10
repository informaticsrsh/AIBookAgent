import subprocess
import webbrowser
import os
import time
import sys

def check_and_install_dependencies():
    """
    Checks if the required packages are installed and installs them if they are not.
    """
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("Required packages not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
            print("Packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            print("Please install the required packages manually by running: pip install -r backend/requirements.txt")
            sys.exit(1)

def main():
    """
    Starts the backend server and opens the frontend in a web browser.
    """
    check_and_install_dependencies()
    server_process = None
    try:
        # Start the backend server using python -m uvicorn for cross-platform compatibility
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd="backend"
        )
        print("Starting backend server...")
        time.sleep(3)  # Give the server a moment to start

        # Open the application in the default web browser
        url = "http://127.0.0.1:8000"
        webbrowser.open(url)
        print(f"Opening application at: {url}")

        # Wait for the server process to terminate
        server_process.wait()
    except KeyboardInterrupt:
        print("\nStopping the server...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            server_process.wait()
        print("Server has been shut down.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
