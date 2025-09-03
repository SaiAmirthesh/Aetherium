"""
Aetherium Commands Module
"""

from .system import (
    handle_system_command,
    handle_process_list,
    handle_disk_usage,
    handle_network_info,
    handle_system_uptime,
    handle_users_logged_in,
    handle_environment_variables,
    handle_running_services
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

COMMAND_HANDLERS = {
    'system': handle_system_command,
    'processes': handle_process_list,
    'disk': handle_disk_usage,
    'network': handle_network_info,
    'uptime': handle_system_uptime,
    'users': handle_users_logged_in,
    'environment': handle_environment_variables,
    'services': handle_running_services,
    'list_files': list_files,
    'create_file': create_file,
    'read_file': read_file,
    'delete_file': delete_file,
    'create_dir': create_directory,
    'delete_dir': delete_directory,
    'execute': execute_command,
    'file_info': get_file_info
}