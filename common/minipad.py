import re
import threading
import requests
import serial
import serial
import serial.tools.list_ports


class MinipadController:
    def __init__(self):
        self.DEVMODE = False
        self.MINIPAD = None
        self.MINIPAD_DATA = {}
        self.VID, self.PID = [0x0727]*2
        self.BAUDRATE = 115200
        self.REPO_DATA = {}
        self.CMD_LIST = []
        self.TOTAL_CMD_COUNTS = 0
        self.DATA_PATTERN = r"GET hkey(\d+)\.(\w+)=(\w+)"
        self.FIRMWARE_PATTERN = r"\d+\.\d+\.\d+(\-\w+)?"

        self.thread = None

    def connect_minipad(self):
        self.MINIPAD = serial.Serial(
            port=self.get_minipad(),
            baudrate=self.BAUDRATE
        )
        print("connected!")
        return self.MINIPAD

    def get_minipad(self):
        ports = serial.tools.list_ports.comports()

        for port in ports:
            if port.vid == self.VID and port.pid == self.PID:
                return port.device

        return None
    
    def send_command_async(self, cmd):
        if self.MINIPAD is None or not self.MINIPAD.is_open:
            self.MINIPAD = self.connect_minipad()
            
        self.MINIPAD.write(cmd.encode())
        res = self.MINIPAD.read_until().decode()
        print(f"sent -> {cmd}")

    def send_command(self, cmd):
        if self.MINIPAD is None or not self.MINIPAD.is_open:
            self.MINIPAD = self.connect_minipad()

        self.MINIPAD.write(cmd.encode())
        print(f"sent -> {cmd}")

    def multiple_send_command(self, cmds, status=None, display=None):
        if not self.thread == None:
            if self.thread.is_alive():
                self.thread = None
            
        self.MINIPAD.close()
        self.MINIPAD = self.connect_minipad()
        self.MINIPAD.timeout = 1

        self.TOTAL_CMD_COUNTS = 0

        def send_command(cmd):
            self.TOTAL_CMD_COUNTS = self.TOTAL_CMD_COUNTS + 1

            if not cmd == None:
                print("send command -> " + cmd, end=" ")
                self.MINIPAD.write(cmd.encode())
                res = self.MINIPAD.read_until().decode()
                print(f"| done!")

            if status:
                if self.TOTAL_CMD_COUNTS >= len(cmds):
                    status.configure(text=f"진행중인 작업이 없습니다.")

                    if display:
                        for ele in display:
                            ele.configure(state="normal")
                else:
                    status.configure(text=f"{len(cmds) - self.TOTAL_CMD_COUNTS}개의 작업 진행중...")


        self.thread = threading.Thread(target=lambda: [send_command(cmd) for cmd in cmds])
        self.thread.start()
        

    def get_minipad_data(self):
        if self.MINIPAD is None or not self.MINIPAD.is_open:
            self.MINIPAD = self.connect_minipad()

        self.send_command("get")
        data_str = ""

        while True:
            res = self.MINIPAD.readline().decode().strip()
            if not res or res == "GET END":
                break
            data_str += f"{res}\n"

        self.MINIPAD_DATA["firmware"] = data_str.split("\n")[0].replace("GET version=", "")
        matches = re.findall(self.DATA_PATTERN, data_str)
        for match in matches:
            hkey = match[0]
            parameter = match[1]
            value = match[2]

            if hkey not in self.MINIPAD_DATA:
                self.MINIPAD_DATA[hkey] = {}

            self.MINIPAD_DATA[hkey][parameter] = value

        self.MINIPAD.close()

    def get_latest_firmware(self):
        repo_url = "https://api.github.com/repos/zeee2/minitility/tags"

        response = requests.get(repo_url)
        if response.status_code == 200:
            tags = response.json()
            if len(tags) > 0:
                return tags[0]['name']

    def get_minipad_repo_data(self):
        # FOR TEST
        if self.DEVMODE:
            self.REPO_DATA = {
                    "name": "2023.516.1",
                    "zipball_url": "https://api.github.com/repos/minipadKB/minipad-firmware/zipball/refs/tags/2023.516.1",
                    "tarball_url": "https://api.github.com/repos/minipadKB/minipad-firmware/tarball/refs/tags/2023.516.1",
                    "commit": {
                    "sha": "31ef8d4a860a15f10ee8c804893b91e60f906ea1",
                    "url": "https://api.github.com/repos/minipadKB/minipad-firmware/commits/31ef8d4a860a15f10ee8c804893b91e60f906ea1"
                    },
                    "node_id": "REF_kwDOIsm5Z7RyZWZzL3RhZ3MvMjAyMy41MTYuMQ"
                }
        else:
            repo_url = "https://api.github.com/repos/minipadKB/minipad-firmware/tags"

            response = requests.get(repo_url)
            if response.status_code == 200:
                tags = response.json()
                if len(tags) > 0:
                    self.REPO_DATA = tags[0]
                    print("Latest release tag:", self.REPO_DATA["name"])