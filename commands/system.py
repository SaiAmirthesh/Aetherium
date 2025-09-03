import platform
import psutil
import socket
import datetime
import os
import subprocess
import time
from datetime import datetime, timedelta

def handle_system_command():
    """Get comprehensive system information"""
    try:
        info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Cores": f"{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical",
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "Memory": f"{psutil.virtual_memory().used // (1024**2)}MB used / {psutil.virtual_memory().total // (1024**2)}MB total ({psutil.virtual_memory().percent}%)",
            "Disk": f"{psutil.disk_usage('/').used // (1024**3)}GB used / {psutil.disk_usage('/').total // (1024**3)}GB total ({psutil.disk_usage('/').percent}%)",
            "Boot Time": f"{datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}",
            "Current User": f"{os.getlogin()}",
            "Hostname": f"{socket.gethostname()}",
            "IP Address": f"{socket.gethostbyname(socket.gethostname())}",
            "Python Version": platform.python_version()
        }
        
        return "🖥️ System Information:\n" + "\n".join([f"  • {k}: {v}" for k, v in info.items()])
    
    except Exception as e:
        return f"❌ Error getting system information: {e}"

def handle_process_list(limit=15):
    """List running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'cpu': info['cpu_percent'],
                    'memory': info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu'] or 0, reverse=True)
        
        result = ["🔄 Running Processes (Top 15 by CPU):"]
        for i, proc in enumerate(processes[:limit]):
            result.append(f"  {i+1:2d}. PID {proc['pid']:5} : {proc['name'][:25]:25} - CPU: {proc['cpu'] or 0:5.1f}%, Memory: {proc['memory'] or 0:5.1f}%")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"❌ Error getting process list: {e}"

def handle_disk_usage():
    """Show disk usage information"""
    try:
        partitions = psutil.disk_partitions()
        result = ["💾 Disk Usage:"]
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                result.append(
                    f"  {partition.device} ({partition.mountpoint}): "
                    f"{usage.used // (1024**3)}GB / {usage.total // (1024**3)}GB "
                    f"({usage.percent}%) - {partition.fstype}"
                )
            except PermissionError:
                continue
        
        return "\n".join(result)
    
    except Exception as e:
        return f"❌ Error getting disk usage: {e}"

def handle_network_info():
    """Show network information"""
    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_io_counters()
        
        result = ["🌐 Network Information:"]
        result.append(f"  Bytes Sent: {stats.bytes_sent // (1024**2)}MB")
        result.append(f"  Bytes Received: {stats.bytes_recv // (1024**2)}MB")
        
        for interface, addrs in interfaces.items():
            if interface != 'Loopback Pseudo-Interface 1':  # Skip loopback
                result.append(f"  Interface: {interface}")
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        result.append(f"    IPv4: {addr.address} (Netmask: {addr.netmask})")
                    elif addr.family == socket.AF_INET6:
                        result.append(f"    IPv6: {addr.address}")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"❌ Error getting network information: {e}"

def handle_system_uptime():
    """Show system uptime with detailed information"""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime = timedelta(seconds=uptime_seconds)
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Get additional system info
        boot_datetime = datetime.fromtimestamp(boot_time)
        current_time = datetime.now()
        
        result = [
            "⏰ System Uptime:",
            f"  • Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
            f"  • Boot Time: {boot_datetime.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  • Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  • Total Seconds: {int(uptime_seconds)}",
            f"  • Total Hours: {uptime_seconds/3600:.1f}"
        ]
        
        return "\n".join(result)
    
    except Exception as e:
        return f"❌ Error getting uptime: {e}"

def handle_users_logged_in():
    """Show users currently logged in"""
    try:
        if platform.system() == "Windows":
            # For Windows - try multiple methods
            try:
                # Method 1: wmic
                result = subprocess.run(
                    ["wmic", "computersystem", "get", "username"], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        username = lines[1].strip()
                        if username:
                            return f"👥 Current User: {username}"
                
                # Method 2: whoami
                result = subprocess.run(
                    ["whoami"], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                if result.returncode == 0:
                    username = result.stdout.strip()
                    return f"👥 Current User: {username}"
                
                # Method 3: environment variable
                username = os.getenv('USERNAME') or os.getenv('USER')
                if username:
                    return f"👥 Current User: {username}"
                
                return "👥 Current User: Unknown (could not determine)"
                
            except Exception:
                # Fallback to environment variable
                username = os.getenv('USERNAME') or os.getenv('USER')
                if username:
                    return f"👥 Current User: {username}"
                return "👥 Current User: Unknown (could not determine)"
        else:
            # For Linux/Mac
            result = subprocess.run(
                ["who"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return f"👥 Logged in Users:\n{result.stdout}"
            else:
                return "👥 Current User: Unknown (could not determine)"
                
    except Exception as e:
        return f"❌ Error getting user information: {e}"

def handle_environment_variables():
    """Show environment variables"""
    try:
        env_vars = []
        for key, value in os.environ.items():
            if not key.startswith(('_', '.')) and len(key) < 20:  # Filter some variables
                env_vars.append(f"  {key}: {value}")
        
        return "🌍 Environment Variables (selected):\n" + "\n".join(env_vars[:20])
    
    except Exception as e:
        return f"❌ Error getting environment variables: {e}"

def handle_running_services():
    """Show running services"""
    try:
        if platform.system() == "Windows":
            # Windows services
            result = subprocess.run(
                ["sc", "query", "state=", "all"], 
                capture_output=True, 
                text=True, 
                shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                running_services = [line for line in lines if "RUNNING" in line]
                return f"🔧 Running Services:\n" + "\n".join(running_services[:15])
            else:
                return "❌ Could not retrieve services information"
        else:
            # Linux services
            result = subprocess.run(
                ["service", "--status-all"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return f"🔧 Services Status:\n{result.stdout}"
            else:
                return "❌ Could not retrieve services information"
                
    except Exception as e:
        return f"❌ Error getting services: {e}"