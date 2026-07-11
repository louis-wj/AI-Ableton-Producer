import socket
import json
import pyautogui
import time

class AbletonController:
    def __init__(self, ip="127.0.0.1", port=11000):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def execute(self, command_obj):
        """
        Executes a complex LOM command object. 
        Can be a simple command or a LOM Gateway command.
        """
        if not command_obj: return
        
        # Handle UI Automation first
        cmd = command_obj.get("command")
        if cmd == "search_library":
            self.search_library(command_obj.get("query", ""))
            return

        # Wrap everything else for the Remote Script
        message = json.dumps(command_obj).encode('utf-8')
        try:
            self.socket.sendto(message, (self.ip, self.port))
            print(f"Sent command to DAW: {cmd}")
        except Exception as e:
            print(f"Controller Error: {e}")

    def send_command(self, command, args=None):
        """
        Legacy support for simple commands.
        """
        self.execute({"command": command, "args": args or {}})

    def play(self):
        self.send_command("play")

    def stop(self):
        self.send_command("stop")

    def set_tempo(self, tempo):
        self.send_command("set_tempo", {"value": tempo})

    def create_track(self, type="midi"):
        cmd = "create_midi_track" if type == "midi" else "create_audio_track"
        self.send_command(cmd)

    def log_message(self, message):
        self.send_command("log", {"message": message})

    # --- UI Automation Methods ---
    
    def search_library(self, query):
        """
        Automates clicking the search bar and typing.
        """
        # Focus Ableton (Assume it's the active window or use pwnauto)
        # Standard shortcut for search in Live is Ctrl + F
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.1)
        pyautogui.write(query, interval=0.05)
        pyautogui.press('enter')
        self.log_message(f"Searching library for: {query}")

    def save_project_as(self, name):
        """
        Automates 'Save Live Set As'
        """
        pyautogui.hotkey('ctrl', 'shift', 's')
        time.sleep(0.5)
        pyautogui.write(name)
        pyautogui.press('enter')
        self.log_message(f"Saved project as: {name}")

    def new_project(self):
        """
        Creates a new blank project.
        """
        pyautogui.hotkey('ctrl', 'n')
        self.log_message("Created new project.")
