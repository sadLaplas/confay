import sys
import os
import json
import base64
import tkinter as tk
from tkinter import scrolledtext, Entry
import argparse


class ShellEmulator:
    def __init__(self, root, vfs_path, script_path):
        self.root = root
        self.root.title("VFS")
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.current_dir = "/"
        self.vfs = self.load_vfs(vfs_path)
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        self.prompt_label = tk.Label(self.input_frame, text="user@vfs:~$ ")
        self.prompt_label.pack(side=tk.LEFT)

        self.command_entry = Entry(self.input_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.execute_command)

        self.log_output("Welcome to VFS Shell Emulator\n")
        self.show_motd()

        if script_path and os.path.exists(script_path):
            self.run_script(script_path)

    def load_vfs(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.log_output(f"Error loading VFS: {e}\n")
            return {}

    def show_motd(self):
        motd = self.get_file_content("motd")
        if motd:
            self.log_output(motd + "\n")

    def get_file_content(self, path):
        keys = path.strip("/").split("/")
        current = self.vfs
        for key in keys:
            if key in current:
                current = current[key]
            else:
                return None
        if isinstance(current, str):
            try:
                return base64.b64decode(current).decode()
            except:
                return current
        return None

    def list_dir(self, path):
        keys = path.strip("/").split("/")
        current = self.vfs
        for key in keys:
            if key in current:
                current = current[key]
            else:
                return []
        if isinstance(current, dict):
            return list(current.keys())
        return []

    def log_output(self, message):
        self.output.config(state='normal')
        self.output.insert(tk.END, message)
        self.output.config(state='disabled')
        self.output.see(tk.END)

    def run_script(self, path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.log_output(f"user@vfs:~$ {line}\n")
                    self.parse_and_execute(line)

    def parse_and_execute(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            self.root.quit()
        elif cmd == "ls":
            path = args[0] if args else self.current_dir
            items = self.list_dir(path)
            self.log_output(" ".join(items) + "\n")
        elif cmd == "cd":
            if args:
                new_path = args[0]
                if new_path.startswith("/"):
                    self.current_dir = new_path
                else:
                    self.current_dir = os.path.join(self.current_dir, new_path).replace("\\", "/")
            self.log_output(f"Changed directory to {self.current_dir}\n")
        else:
            self.log_output(f"Command not found: {cmd}\n")

    def execute_command(self, event):
        command_line = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.log_output(f"user@vfs:~$ {command_line}\n")
        self.parse_and_execute(command_line)


def main():
    parser = argparse.ArgumentParser(description="VFS Shell Emulator")
    parser.add_argument("vfs_path", help="Path to VFS JSON file")
    parser.add_argument("script_path", nargs='?', default=None, help="Path to startup script")
    args = parser.parse_args()

    root = tk.Tk()
    app = ShellEmulator(root, args.vfs_path, args.script_path)
    root.mainloop()


if __name__ == "__main__":
    main()