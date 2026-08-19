import psutil
import os
import signal
import time

def kill_processes(process_names):
    print("Attempting to kill processes:", process_names)
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pinfo = proc.info
            cmdline = " ".join(pinfo['cmdline']) if pinfo['cmdline'] else ''

            for name in process_names:
                if name in pinfo['name'] or name in cmdline:
                    print(f"Killing process {pinfo['pid']}: {pinfo['name']} - {cmdline}")
                    try:
                        os.kill(pinfo['pid'], signal.SIGTERM)
                        time.sleep(0.1) # Give a short moment for the process to terminate
                    except ProcessLookupError:
                        print(f"Process {pinfo['pid']} already terminated.")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("Process killing attempt complete.")

if __name__ == "__main__":
    # List of process names (or parts of command lines) to kill
    processes_to_kill = [
        "orchestrator.py",
        "login_runner.py",
        "monitor_runner.py",
        "booking_runner.py",
        "chrome", # To catch any lingering Chrome instances
    ]
    kill_processes(processes_to_kill)
