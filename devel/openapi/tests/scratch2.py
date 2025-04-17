response = {
    "monit": {
        "general": {
            "enabled": "0",
            "interval": "120",
            "startdelay": "120",
            "mailserver": {"127.0.0.1": {"value": "127.0.0.1", "selected": 1}},
            "port": "25",
            "username": "",
            "password": "",
            "ssl": "0",
            "sslversion": {
                "auto": {"value": "AUTO", "selected": 1},
                "tlsv1": {"value": "TLSV1", "selected": 0},
                "tlsv11": {"value": "TLSV11", "selected": 0},
                "tlsv12": {"value": "TLSV12", "selected": 0},
                "tlsv13": {"value": "TLSV13", "selected": 0},
            },
            "sslverify": "1",
            "logfile": "",
            "statefile": "",
            "eventqueuePath": "",
            "eventqueueSlots": "",
            "httpdEnabled": "0",
            "httpdUsername": "root",
            "httpdPassword": "",
            "httpdPort": "2812",
            "httpdAllow": [],
            "mmonitUrl": "",
            "mmonitTimeout": "5",
            "mmonitRegisterCredentials": "1",
        },
        "alert": [],
        "service": {
            "8f977162-3282-4872-bf54-82791bd70666": {
                "enabled": "1",
                "name": "RootFs",
                "description": "",
                "type": {
                    "process": {"value": "Process", "selected": 0},
                    "file": {"value": "File", "selected": 0},
                    "fifo": {"value": "Fifo", "selected": 0},
                    "filesystem": {"value": "Filesystem", "selected": 1},
                    "directory": {"value": "Directory", "selected": 0},
                    "host": {"value": "Remote Host", "selected": 0},
                    "system": {"value": "System", "selected": 0},
                    "custom": {"value": "Custom", "selected": 0},
                    "network": {"value": "Network", "selected": 0},
                },
                "pidfile": "",
                "match": "",
                "path": "/",
                "timeout": "300",
                "starttimeout": "30",
                "address": "",
                "interface": {"": {"value": "None", "selected": 1}},
                "start": "",
                "stop": "",
                "tests": {
                    "682d6561-4db7-406e-9a56-208984a92754": {
                        "value": "ChangedStatus",
                        "selected": 0,
                    },
                    "23dc85be-4e80-41e5-8612-7aa1f62047ad": {
                        "value": "CPUUsage",
                        "selected": 0,
                    },
                    "a6029e92-3873-4bfa-ba52-eb68be3c7b9a": {
                        "value": "LoadAvg1",
                        "selected": 0,
                    },
                    "6f25db22-34c4-42cd-a9de-bcada8107563": {
                        "value": "LoadAvg5",
                        "selected": 0,
                    },
                    "72697d50-18e2-48fa-9db0-7e8f6a7f1a8f": {
                        "value": "LoadAvg15",
                        "selected": 0,
                    },
                    "2c8be678-17ff-4a83-a959-bbd2f26c0622": {
                        "value": "MemoryUsage",
                        "selected": 0,
                    },
                    "267de4b4-e5db-49d1-b2d9-2c8bfbe3275c": {
                        "value": "NonZeroStatus",
                        "selected": 0,
                    },
                    "54b2a5bd-5bce-44c4-b439-a0b16700c95f": {
                        "value": "SpaceUsage",
                        "selected": 1,
                    },
                },
                "depends": {
                    "bb870126-d7cc-46ed-8280-da75823376de": {
                        "value": "carp_status_change",
                        "selected": 0,
                    },
                    "0ebe95bd-42c7-4c06-acea-32413afe7341": {
                        "value": "gateway_alert",
                        "selected": 0,
                    },
                    "8f977162-3282-4872-bf54-82791bd70666": {
                        "value": "RootFs",
                        "selected": 0,
                    },
                },
                "polltime": "",
            },
            "bb870126-d7cc-46ed-8280-da75823376de": {
                "enabled": "0",
                "name": "carp_status_change",
                "description": "",
                "type": {
                    "process": {"value": "Process", "selected": 0},
                    "file": {"value": "File", "selected": 0},
                    "fifo": {"value": "Fifo", "selected": 0},
                    "filesystem": {"value": "Filesystem", "selected": 0},
                    "directory": {"value": "Directory", "selected": 0},
                    "host": {"value": "Remote Host", "selected": 0},
                    "system": {"value": "System", "selected": 0},
                    "custom": {"value": "Custom", "selected": 1},
                    "network": {"value": "Network", "selected": 0},
                },
                "pidfile": "",
                "match": "",
                "path": "/usr/local/opnsense/scripts/OPNsense/Monit/carp_status",
                "timeout": "300",
                "starttimeout": "30",
                "address": "",
                "interface": {"": {"value": "None", "selected": 1}},
                "start": "",
                "stop": "",
                "tests": {
                    "682d6561-4db7-406e-9a56-208984a92754": {
                        "value": "ChangedStatus",
                        "selected": 1,
                    },
                    "23dc85be-4e80-41e5-8612-7aa1f62047ad": {
                        "value": "CPUUsage",
                        "selected": 0,
                    },
                    "a6029e92-3873-4bfa-ba52-eb68be3c7b9a": {
                        "value": "LoadAvg1",
                        "selected": 0,
                    },
                    "6f25db22-34c4-42cd-a9de-bcada8107563": {
                        "value": "LoadAvg5",
                        "selected": 0,
                    },
                    "72697d50-18e2-48fa-9db0-7e8f6a7f1a8f": {
                        "value": "LoadAvg15",
                        "selected": 0,
                    },
                    "2c8be678-17ff-4a83-a959-bbd2f26c0622": {
                        "value": "MemoryUsage",
                        "selected": 0,
                    },
                    "267de4b4-e5db-49d1-b2d9-2c8bfbe3275c": {
                        "value": "NonZeroStatus",
                        "selected": 0,
                    },
                    "54b2a5bd-5bce-44c4-b439-a0b16700c95f": {
                        "value": "SpaceUsage",
                        "selected": 0,
                    },
                },
                "depends": {
                    "bb870126-d7cc-46ed-8280-da75823376de": {
                        "value": "carp_status_change",
                        "selected": 0,
                    },
                    "0ebe95bd-42c7-4c06-acea-32413afe7341": {
                        "value": "gateway_alert",
                        "selected": 0,
                    },
                    "8f977162-3282-4872-bf54-82791bd70666": {
                        "value": "RootFs",
                        "selected": 0,
                    },
                },
                "polltime": "",
            },
            "0ebe95bd-42c7-4c06-acea-32413afe7341": {
                "enabled": "0",
                "name": "gateway_alert",
                "description": "",
                "type": {
                    "process": {"value": "Process", "selected": 0},
                    "file": {"value": "File", "selected": 0},
                    "fifo": {"value": "Fifo", "selected": 0},
                    "filesystem": {"value": "Filesystem", "selected": 0},
                    "directory": {"value": "Directory", "selected": 0},
                    "host": {"value": "Remote Host", "selected": 0},
                    "system": {"value": "System", "selected": 0},
                    "custom": {"value": "Custom", "selected": 1},
                    "network": {"value": "Network", "selected": 0},
                },
                "pidfile": "",
                "match": "",
                "path": "/usr/local/opnsense/scripts/OPNsense/Monit/gateway_alert",
                "timeout": "300",
                "starttimeout": "30",
                "address": "",
                "interface": {"": {"value": "None", "selected": 1}},
                "start": "",
                "stop": "",
                "tests": {
                    "682d6561-4db7-406e-9a56-208984a92754": {
                        "value": "ChangedStatus",
                        "selected": 0,
                    },
                    "23dc85be-4e80-41e5-8612-7aa1f62047ad": {
                        "value": "CPUUsage",
                        "selected": 0,
                    },
                    "a6029e92-3873-4bfa-ba52-eb68be3c7b9a": {
                        "value": "LoadAvg1",
                        "selected": 0,
                    },
                    "6f25db22-34c4-42cd-a9de-bcada8107563": {
                        "value": "LoadAvg5",
                        "selected": 0,
                    },
                    "72697d50-18e2-48fa-9db0-7e8f6a7f1a8f": {
                        "value": "LoadAvg15",
                        "selected": 0,
                    },
                    "2c8be678-17ff-4a83-a959-bbd2f26c0622": {
                        "value": "MemoryUsage",
                        "selected": 0,
                    },
                    "267de4b4-e5db-49d1-b2d9-2c8bfbe3275c": {
                        "value": "NonZeroStatus",
                        "selected": 1,
                    },
                    "54b2a5bd-5bce-44c4-b439-a0b16700c95f": {
                        "value": "SpaceUsage",
                        "selected": 0,
                    },
                },
                "depends": {
                    "bb870126-d7cc-46ed-8280-da75823376de": {
                        "value": "carp_status_change",
                        "selected": 0,
                    },
                    "0ebe95bd-42c7-4c06-acea-32413afe7341": {
                        "value": "gateway_alert",
                        "selected": 0,
                    },
                    "8f977162-3282-4872-bf54-82791bd70666": {
                        "value": "RootFs",
                        "selected": 0,
                    },
                },
                "polltime": "",
            },
        },
        "test": {
            "2c8be678-17ff-4a83-a959-bbd2f26c0622": {
                "name": "MemoryUsage",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 1},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "memory usage is greater than 75%",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "23dc85be-4e80-41e5-8612-7aa1f62047ad": {
                "name": "CPUUsage",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 1},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "cpu usage is greater than 75%",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "a6029e92-3873-4bfa-ba52-eb68be3c7b9a": {
                "name": "LoadAvg1",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 1},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "loadavg (1min) is greater than 8",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "6f25db22-34c4-42cd-a9de-bcada8107563": {
                "name": "LoadAvg5",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 1},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "loadavg (5min) is greater than 6",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "72697d50-18e2-48fa-9db0-7e8f6a7f1a8f": {
                "name": "LoadAvg15",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 1},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "loadavg (15min) is greater than 4",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "54b2a5bd-5bce-44c4-b439-a0b16700c95f": {
                "name": "SpaceUsage",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 0},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 1},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 0},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "space usage is greater than 75%",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "682d6561-4db7-406e-9a56-208984a92754": {
                "name": "ChangedStatus",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 0},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 1},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "changed status",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
            "267de4b4-e5db-49d1-b2d9-2c8bfbe3275c": {
                "name": "NonZeroStatus",
                "type": {
                    "Existence": {"value": "Existence", "selected": 0},
                    "SystemResource": {"value": "System Resource", "selected": 0},
                    "ProcessResource": {"value": "Process Resource", "selected": 0},
                    "ProcessDiskIO": {"value": "Process Disk I/O", "selected": 0},
                    "FileChecksum": {"value": "File Checksum", "selected": 0},
                    "Timestamp": {"value": "Timestamp", "selected": 0},
                    "FileSize": {"value": "File Size", "selected": 0},
                    "FileContent": {"value": "File Content", "selected": 0},
                    "FilesystemMountFlags": {
                        "value": "Filesystem Mount Flags",
                        "selected": 0,
                    },
                    "SpaceUsage": {"value": "Space Usage", "selected": 0},
                    "InodeUsage": {"value": "Inode Usage", "selected": 0},
                    "DiskIO": {"value": "Disk I/O", "selected": 0},
                    "Permisssion": {"value": "Permission", "selected": 0},
                    "UID": {"value": "UID", "selected": 0},
                    "GID": {"value": "GID", "selected": 0},
                    "PID": {"value": "PID", "selected": 0},
                    "PPID": {"value": "PPID", "selected": 0},
                    "Uptime": {"value": "Uptime", "selected": 0},
                    "ProgramStatus": {"value": "Program Status", "selected": 1},
                    "NetworkInterface": {"value": "Network Interface", "selected": 0},
                    "NetworkPing": {"value": "Network Ping", "selected": 0},
                    "Connection": {"value": "Connection", "selected": 0},
                    "Custom": {"value": "Custom", "selected": 0},
                },
                "condition": "status != 0",
                "action": {
                    "alert": {"value": "Alert", "selected": 1},
                    "restart": {"value": "Restart", "selected": 0},
                    "start": {"value": "Start", "selected": 0},
                    "stop": {"value": "Stop", "selected": 0},
                    "exec": {"value": "Execute", "selected": 0},
                    "unmonitor": {"value": "Unmonitor", "selected": 0},
                },
                "path": "",
            },
        },
    }
}
schema = {
    "type": "object",
    "properties": {
        "monit": {
            "type": "object",
            "properties": {
                "general": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "string"},
                        "interval": {"type": "string"},
                        "startdelay": {"type": "string"},
                        "mailserver": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "selected": {"type": "integer", "enum": [0, 1]},
                                },
                                "required": ["value", "selected"],
                            },
                        },
                        "port": {"type": "string"},
                        "username": {"type": "string"},
                        "password": {"type": "string"},
                        "ssl": {"type": "string"},
                        "sslversion": {
                            "type": "object",
                            "properties": {
                                "auto": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["AUTO"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "tlsv1": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["TLSV1"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "tlsv11": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["TLSV11"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "tlsv12": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["TLSV12"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "tlsv13": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["TLSV13"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                            },
                            "additionalProperties": False,
                        },
                        "sslverify": {"type": "string"},
                        "logfile": {"type": "string"},
                        "statefile": {"type": "string"},
                        "eventqueuePath": {"type": "string"},
                        "eventqueueSlots": {"type": "string"},
                        "httpdEnabled": {"type": "string"},
                        "httpdUsername": {"type": "string"},
                        "httpdPassword": {"type": "string"},
                        "httpdPort": {"type": "string"},
                        "httpdAllow": {"type": "array", "items": {"type": "string"}},
                        "mmonitUrl": {"type": "string"},
                        "mmonitTimeout": {"type": "string"},
                        "mmonitRegisterCredentials": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
                "alert": {
                    "type": "object",
                    "additionalProperties": {
                        "enabled": {"type": "string"},
                        "recipient": {"type": "string"},
                        "noton": {"type": "string"},
                        "events": {
                            "type": "object",
                            "properties": {
                                "SelectOptions": {
                                    "type": "object",
                                    "properties": {
                                        "action": {"type": "string"},
                                        "checksum": {"type": "string"},
                                        "bytein": {"type": "string"},
                                        "byteout": {"type": "string"},
                                        "connection": {"type": "string"},
                                        "content": {"type": "string"},
                                        "data": {"type": "string"},
                                        "exec": {"type": "string"},
                                        "fsflags": {"type": "string"},
                                        "gid": {"type": "string"},
                                        "icmp": {"type": "string"},
                                        "instance": {"type": "string"},
                                        "invalid": {"type": "string"},
                                        "link": {"type": "string"},
                                        "nonexist": {"type": "string"},
                                        "packetin": {"type": "string"},
                                        "packetout": {"type": "string"},
                                        "permission": {"type": "string"},
                                        "pid": {"type": "string"},
                                        "ppid": {"type": "string"},
                                        "resource": {"type": "string"},
                                        "saturation": {"type": "string"},
                                        "size": {"type": "string"},
                                        "speed": {"type": "string"},
                                        "status": {"type": "string"},
                                        "timeout": {"type": "string"},
                                        "timestamp": {"type": "string"},
                                        "uid": {"type": "string"},
                                        "uptime": {"type": "string"},
                                    },
                                    "additionalProperties": False,
                                }
                            },
                            "additionalProperties": False,
                        },
                        "format": {"type": "string"},
                        "reminder": {"type": "string"},
                        "description": {"type": "string"},
                    },
                },
                "service": {
                    "type": "object",
                    "additionalProperties": {
                      "type": "object",
                      "properties": {
                        "enabled": {"type": "string"},
                        "name": {"type": "string"},
                        # "description": {"type": "string"},
                        # "type": {
                        #     "type": "object",
                        #     "properties": {
                        #         "process": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {
                        #                     "type": "string",
                        #                     "enum": ["Process"],
                        #                 },
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "file": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {"type": "string", "enum": ["File"]},
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "fifo": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {"type": "string", "enum": ["Fifo"]},
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "filesystem": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {
                        #                     "type": "string",
                        #                     "enum": ["Filesystem"],
                        #                 },
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "directory": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {
                        #                     "type": "string",
                        #                     "enum": ["Directory"],
                        #                 },
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "host": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {
                        #                     "type": "string",
                        #                     "enum": ["Remote Host"],
                        #                 },
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "system": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {"type": "string", "enum": ["System"]},
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "custom": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {"type": "string", "enum": ["Custom"]},
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #         "network": {
                        #             "type": "object",
                        #             "properties": {
                        #                 "value": {
                        #                     "type": "string",
                        #                     "enum": ["Network"],
                        #                 },
                        #                 "selected": {"type": "integer", "enum": [0, 1]},
                        #             },
                        #             "required": ["value", "selected"],
                        #         },
                        #     },
                        #     "additionalProperties": False,
                        # },
                        "pidfile": {"type": "string"},
                        "match": {"type": "string"},
                        "path": {"type": "string"},
                        "timeout": {"type": "string"},
                        "starttimeout": {"type": "string"},
                        "address": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "selected": {"type": "integer", "enum": [0, 1]},
                                },
                                "required": ["value", "selected"],
                            },
                        },
                        "interface": {
                            "type": "object",
                            "properties": {
                                "AddParentDevices": {"type": "string"},
                                "filters": {
                                    "type": "object",
                                    "properties": {
                                        "enable": {"type": "string"},
                                        "ipaddr": {"type": "string"},
                                    },
                                    "additionalProperties": False,
                                },
                            },
                            "additionalProperties": False,
                        },
                        "start": {"type": "string"},
                        "stop": {"type": "string"},
                        "tests": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "selected": {"type": "integer"},
                                },
                                "additionalProperties": False,
                            },
                        },
                        "depends": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "selected": {"type": "integer"},
                                },
                                "additionalProperties": False,
                            },
                        },
                        "polltime": {"type": "string"},
                      }
                    },
                },
                "test": {
                    "type": "object",
                    "additionalProperties": {
                        # "name": {"type": "string"},
                        "type": {
                            "type": "object",
                            "properties": {
                                "Existence": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Existence"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "SystemResource": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["System Resource"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "ProcessResource": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Process Resource"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "ProcessDiskIO": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Process Disk I/O"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "FileChecksum": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["File Checksum"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "Timestamp": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Timestamp"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "FileSize": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["File Size"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "FileContent": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["File Content"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "FilesystemMountFlags": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Filesystem Mount Flags"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "SpaceUsage": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Space Usage"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "InodeUsage": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Inode Usage"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "DiskIO": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Disk I/O"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "Permisssion": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Permission"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "UID": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["UID"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "GID": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["GID"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "PID": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["PID"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "PPID": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["PPID"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "Uptime": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["Uptime"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "ProgramStatus": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Program Status"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "NetworkInterface": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Network Interface"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "NetworkPing": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Network Ping"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "Connection": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Connection"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "Custom": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["Custom"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                            },
                            "additionalProperties": False,
                        },
                        "condition": {"type": "string"},
                        "action": {
                            "type": "object",
                            "properties": {
                                "alert": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["Alert"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "restart": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Restart"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "start": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["Start"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "stop": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "string", "enum": ["Stop"]},
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "exec": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Execute"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                                "unmonitor": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "enum": ["Unmonitor"],
                                        },
                                        "selected": {"type": "integer", "enum": [0, 1]},
                                    },
                                    "required": ["value", "selected"],
                                },
                            },
                            "additionalProperties": False,
                        },
                        "path": {"type": "string"},
                    },
                },
            },
            "additionalProperties": False,
            "x-config-xpath": ".//OPNsense/monit",
        }
    },
}
