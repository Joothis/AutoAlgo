
import subprocess
import sys

def run_shell_command(command: str, timeout: int = None) -> dict:
    """
    Executes a shell command and returns its output.

    Args:
        command: The command to execute.
        timeout: Optional timeout in seconds.

    Returns:
        A dictionary containing stdout, stderr, and the return code.
    """
    try:
        # Using sys.executable to ensure we use the same python interpreter
        # that is running the script.
        if command.startswith("py -m"):
            command = command.replace("py -m", f'{sys.executable} -m', 1)

        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=False,
            timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired as e:
        return {
            "stdout": e.stdout or "",
            "stderr": f"TimeoutExpired: Command '{e.cmd}' ran for more than {e.timeout} seconds.",
            "returncode": -1 # Using a specific code for timeout
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1
        }
