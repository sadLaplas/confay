import tkinter as tk
from tkinter import scrolledtext, Entry, END

class SHemu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.output_area.pack(expand=True, fill='both')
        self.input_field = Entry(self.root)
        self.input_field.pack(fill='x')
        self.input_field.bind('<Return>', self.on_enter)
        self.current_path = "/"
        self.history = []
        self.p_pr()

    def p_pr(self):
        self.output_area.insert(tk.END, f"{self.current_path} ")

    def on_enter(self, event):
        command = self.input_field.get()
        self.input_field.delete(0, END)
        self.output_area.insert(tk.END, command + '\n')
        self.pa_ex(command)

    def pa_ex(self, command):
        pf = command.split()
        if not pf:
            self.p_pr()
            return
        cmd = pf[0]
        args = pf[1:]

        self.history.append({
            'command': cmd, 'args': args})

        if cmd == "exit":
            self.output_area.insert(tk.END, "Exit\n")
            self.root.quit()
        elif cmd == "ls":
            self.output_area.insert(tk.END, f"Command: {cmd}, Args: {args}\n")
        elif cmd == "cd":
            self.output_area.insert(tk.END, f"Command: {cmd}, Args: {args}\n")
        elif cmd == "history":
            for entry in self.history:
                self.output_area.insert(tk.END, f"{entry['command']} {' '.join(entry['args'])}\n")
        else:
            self.output_area.insert(tk.END, f"Unknown command: {cmd}\n")
        self.p_pr()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SHemu()
    app.run()