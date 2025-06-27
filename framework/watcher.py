import os
import sys
import time
import subprocess

WATCH_EXT = [".py"]
CHECK_INTERVAL = 1

IGNORE_FILES = ["watcher.py"]


def get_all_files():
    """
    Recursively collects all files with specific extensions from a directory, excluding ignored files.
    Returns a dictionary mapping file paths to their last modification times.
    """

    files = {}
    for root, _, filenames in os.walk(sys.argv[-1]):
        for fname in filenames:
            if fname in IGNORE_FILES:
                continue

            if any(fname.endswith(ext) for ext in WATCH_EXT):
                path = os.path.join(root, fname)
                try:
                    files[path] = os.path.getmtime(path)
                except FileNotFoundError:
                    continue

    return files


def start_server():
    """
    Starts the server by launching 'app.py' as a subprocess with the '--noreload' flag.
    Returns:
        subprocess.Popen: The process object for the started server.
    """

    return subprocess.Popen([sys.executable, "app.py", "--noreload"])


def watch():
    """
    Watches for file changes in the project directory and restarts the server when changes are detected.
    Continuously monitors all files returned by `get_all_files()`. If any file is added, removed, or modified,
    the running server process (started by `start_server()`) is killed and restarted. The function prints
    notifications to the console when file changes are detected and handles graceful shutdown on keyboard interrupt.
    """
    prev_files = get_all_files()

    proc = start_server()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)

            curr_files = get_all_files()

            changed = [
                f
                for f in curr_files
                if f not in prev_files or curr_files[f] != prev_files[f]
            ]

            if changed:
                print("🔄 File changes detected:")
                for f in changed:
                    print(f"  - {f}")
                proc.kill()
                proc = start_server()
                prev_files = curr_files

    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        proc.kill()


if __name__ == "__main__":
    watch()
