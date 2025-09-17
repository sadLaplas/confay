import sys
import os
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
        self.log_output(f"VFS Path: {vfs_path}\n")
        self.log_output(f"Script Path: {script_path}\n")

        if script_path and os.path.exists(script_path):
            self.run_script(script_path)

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
                    # Здесь можно добавить парсинг и выполнение команд

    def execute_command(self, event):
        command_line = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.log_output(f"user@vfs:~$ {command_line}\n")

        parts = command_line.strip().split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            self.root.quit()
        elif cmd == "ls":
            self.log_output(f"ls {' '.join(args)}\n")
        elif cmd == "cd":
            self.log_output(f"cd {' '.join(args)}\n")
        else:
            self.log_output(f"Command not found: {cmd}\n")


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