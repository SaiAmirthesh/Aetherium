"""
Aetherium Commands Module - Contains all command handlers for the CLI.
"""

# Import all command functions to make them easily accessible
from .system import (
    handle_system_command,
    handle_process_list,
    handle_disk_usage,
    handle_network_info,
    handle_system_uptime
)

from .file_ops import (
    list_files,
    create_file,
    read_file,
    delete_file,
    create_directory,
    delete_directory,
    execute_command,
    get_file_info
)

# Optional: Create a dictionary for easy command mapping
COMMAND_HANDLERS = {
    'system': handle_system_command,
    'processes': handle_process_list,
    'disk': handle_disk_usage,
    'network': handle_network_info,
    'uptime': handle_system_uptime,
    'list_files': list_files,
    'create_file': create_file,
    'read_file': read_file,
    'delete_file': delete_file,
    'create_dir': create_directory,
    'delete_dir': delete_directory,
    'execute': execute_command,
    'file_info': get_file_info
}

VERSION = "1.0.0"