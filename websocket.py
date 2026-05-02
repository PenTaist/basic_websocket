#!/usr/bin/env python

# Import libraries
import asyncio, os, platform, socket, json, logging
from datetime import datetime, date, time
from websockets.asyncio.server import serve

# Logs
logger = logging.getLogger(__name__)
logging.basicConfig(filename='websocket.log', level=logging.INFO)
logger.info(f"[{datetime.now()}] WEBSOCKET STARTING...")

# Systems commands
cmds = {
    "Windows": {
        "shutdown": "shutdown /s /t 00",
        "reboot": "shutdown /r /t 00",
        "sleep": "rundll32.exe powrprof.dll, SetSuspendState Sleep",
        "lock": "rundll32.exe user32.dll, LockWorkStation"
    },
    "Linux": {
        "shutdown": "sudo poweroff",
        "reboot": "sudo reboot",
        "sleep": "sudo systemctl suspend",
        "lock": "xdg-screensaver lock"
    }
}

# Messages part
async def echo(websocket):
    async for message in websocket:
        if message == 'ping':
            local_hostname = socket.gethostname()
            ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
            filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
            ip = filtered_ips[:1][0]

            data = {
                "hostname": socket.gethostname(),
                "system": platform.system(),
                "ip": ip
            }

            await websocket.send(json.dumps(data, indent=4))

        if platform.system() == 'Windows':
            if message == 'shutdown':
                os.system(cmds['Windows']['shutdown'])
                logger.info(f"[{datetime.now()}] CMD : shutdown")
            elif message == 'reboot':
                os.system(cmds['Windows']['reboot'])
                logger.info(f"[{datetime.now()}] CMD : reboot")
            elif message == 'sleep':
                os.system(cmds['Windows']['sleep'])
                logger.info(f"[{datetime.now()}] CMD : sleep")
            elif message == 'lock':
                os.system(cmds['Windows']['lock'])
                logger.info(f"[{datetime.now()}] CMD : lock")
            else:
                logger.error(f"[{datetime.now()}] Command not found !")
        elif platform.system() == 'Linux':
            if message == 'shutdown':
                os.system(cmds['Linux']['shutdown'])
                logger.info(f"[{datetime.now()}] CMD : shutdown")
            elif message == 'reboot':
                os.system(cmds['Linux']['reboot'])
                logger.info(f"[{datetime.now()}] CMD : reboot")
            elif message == 'sleep':
                os.system(cmds['Linux']['sleep'])
                logger.info(f"[{datetime.now()}] CMD : sleep")
            elif message == 'lock':
                os.system(cmds['Linux']['lock'])
                logger.info(f"[{datetime.now()}] CMD : lock")
            else:
                logger.error(f"[{datetime.now()}] Command not found !")
        else:
            logger.critical(f"[{datetime.now()}] OS not found !")
            exit()

# Server part
async def main():
    async with serve(echo, "0.0.0.0", 1234) as server:
        logger.info(f"[{datetime.now()}] WEBSOCKET STARTED !")
        await server.serve_forever()

# Start main thread
asyncio.run(main())