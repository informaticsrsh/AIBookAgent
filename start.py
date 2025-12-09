import subprocess
import webbrowser
import os
import time

def main():
    """
    Starts the backend server and opens the frontend in a web browser.
    """
    server_process = None
    try:
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
        server_process.wait()
    except KeyboardInterrupt:
        print("Stopping backend server...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            server_process.wait()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
