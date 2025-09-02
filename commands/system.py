import platform
import psutil
import socket
import datetime
import os

def handle_system_command():
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
            "Boot Time": f"{datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}",
            "Current User": f"{os.getlogin()}",
            "Hostname": f"{socket.gethostname()}",
            "IP Address": f"{socket.gethostbyname(socket.gethostname())}",
            "Python Version": platform.python_version()
        }
        
        return "🖥️ System Information:\n" + "\n".join([f"  • {k}: {v}" for k, v in info.items()])
    
    except Exception as e:
        return f"❌ Error getting system information: {e}"

def handle_process_list(limit=10):
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
        
        processes.sort(key=lambda x: x['cpu'] or 0, reverse=True)
        
        result = ["🔄 Running Processes (Top 10 by CPU):"]
        for proc in processes[:limit]:
            result.append(f"  PID {proc['pid']}: {proc['name']} - CPU: {proc['cpu'] or 0:.1f}%, Memory: {proc['memory'] or 0:.1f}%")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"❌ Error getting process list: {e}"

def handle_disk_usage():
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
    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_io_counters()
        
        result = ["🌐 Network Information:"]
        result.append(f"  Bytes Sent: {stats.bytes_sent // (1024**2)}MB")
        result.append(f"  Bytes Received: {stats.bytes_recv // (1024**2)}MB")
        
        for interface, addrs in interfaces.items():
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
    try:
        boot_time = psutil.boot_time()
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"⏰ System Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    
    except Exception as e:
        return f"❌ Error getting uptime: {e}"