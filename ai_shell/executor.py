import subprocess

def execute_command(cmd):
    """
    Executes a shell command on Windows and returns its output or error.
    """
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error executing command: {str(e)}"