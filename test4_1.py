# main.py
import tkinter as tk
from tkinter import scrolledtext, Entry, END


class ShellEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS")
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

    def log_output(self, message):
        self.output.config(state='normal')
        self.output.insert(tk.END, message)
        self.output.config(state='disabled')
        self.output.see(tk.END)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()