import tkinter as tk
from tkinter import scrolledtext, END
import os

class VFSgui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VFS")
        self.root.geometry("800x600")
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        self.prompt_label = tk.Label(input_frame, text="user@vfs:~$ ", font=("Courier", 10))
        self.prompt_label.pack(side=tk.LEFT)
        self.command_entry = tk.Entry(input_frame, font=("Courier", 10))
        self.command_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.command_entry.bind('<Return>', self.proc)
        self.command_entry.focus()
        self.current_directory = "~"
        self.print_output("Это эмулятор VFS\n")
        self.print_output("Команды:ls, cd, exit\n")
        self.print_output("Введите 'exit' для выхода\n\n")

    def print_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.insert(END, text)
        self.output_text.config(state='disabled')
        self.output_text.see(END)

    def parco(self, input_text):
        if not input_text.strip():
            return None, []

        rts = [rt for rt in input_text.strip().split() if rt]
        if not rts:
            return None, []

        command = rts[0]
        arguments = rts[1:] if len(rts) > 1 else []
        return command, arguments

    def ex_ls(self, arguments):
        output = f"ls: "
        if arguments:
            output += " ".join(arguments)
        else:
            output += "[вывод содержимого]"
        output += "\n"
        self.print_output(output)

    def ex_cd(self, arguments):
        output = f"cd: "
        if arguments:
            self.current_directory = arguments[0]
            output += f"переход в директорию {arguments[0]}"
        else:
            output += "не указана директория"
        output += "\n"
        self.print_output(output)
        self.prompt_label.config(text=f"user@vfs:{self.current_directory}$ ")

    def ex_exit(self, arguments):
        self.print_output("Выход из программы\n")
        self.root.quit()
        return True

    def proc(self, event=None):
        command_line = self.command_entry.get()

        self.print_output(f"user@vfs:{self.current_directory}$ {command_line}\n")

        self.command_entry.delete(0, END)

        command, arguments = self.parco(command_line)

        if command is None:
            return

        try:
            if command == "ls":
                self.ex_ls(arguments)
            elif command == "cd":
                self.ex_cd(arguments)
            elif command == "exit":
                self.ex_exit(arguments)
            else:
                self.print_output(f"Команда '{command}' не найдена\n")
        except Exception as e:
            self.print_output(f"Ошибка выполнения: {str(e)}\n")

    def run(self):
        self.root.mainloop()


def main():
    emulator = VFSgui()
    emulator.run()


if __name__ == "__main__":
    main()