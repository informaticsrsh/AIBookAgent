import subprocess
import webbrowser
import os
import time

def main():
    """
    Starts the backend server and opens the frontend in a web browser.
    """
    # Start the backend server
    server_process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="backend"
    )
    print("Starting backend server...")
    time.sleep(5)  # Give the server a moment to start

    # Open the frontend in the default web browser
    frontend_path = os.path.abspath(os.path.join("frontend", "index.html"))
    webbrowser.open(f"file://{frontend_path}")
    print(f"Opening frontend at: file://{frontend_path}")

    # Keep the script running until the server is terminated
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("Stopping backend server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()
