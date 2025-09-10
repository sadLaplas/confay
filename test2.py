import tkinter as tk
from tkinter import scrolledtext, END
import sys
import os

class VFSgui:
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path or os.getcwd()
        self.script_path = script_path
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
        self.print_output("Команды:ls, cd, exit, conf-dump\n")
        self.print_output("Введите 'exit' для выхода\n\n")
        self.print_conf()

        if self.script_path and os.path.exists(self.script_path):
            self.root.after(100, self.exec_script)

    def print_conf(self):
        self.print_output("Конфигурация эмулятора:\n")
        self.print_output(f"  vfs_path: {self.vfs_path}\n")
        self.print_output(f"  script_path: {self.script_path}\n\n")

    def print_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.insert(END, text)
        self.output_text.config(state='disabled')
        self.output_text.see(END)

    def parco(self, command_line):
        if not command_line.strip():
            return None, []

        parts = command_line.strip().split()
        command = parts[0]
        arguments = parts[1:] if len(parts) > 1 else []
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

    def ex_conf_dump(self, arguments):
        self.print_output("Конфигурация эмулятора:\n")
        self.print_output(f"  vfs_path: {self.vfs_path}\n")
        self.print_output(f"  script_path: {self.script_path}\n")
        self.print_output(f"  current_directory: {self.current_directory}\n\n")

    def exec_script(self):
        try:
            with open(self.script_path, 'r', encoding='utf-8') as file:
                commands = file.readlines()

            for command_line in commands:
                command_line = command_line.strip()
                if not command_line or command_line.startswith('#'):
                    continue

                self.print_output(f"user@vfs:{self.current_directory}$ {command_line}\n")

                command, arguments = self.parco(command_line)

                if command is None:
                    continue

                try:
                    if command == "ls":
                        self.ex_ls(arguments)
                    elif command == "cd":
                        self.ex_cd(arguments)
                    elif command == "exit":
                        self.ex_exit(arguments)
                        break
                    elif command == "conf-dump":
                        self.ex_conf_dump(arguments)
                    else:
                        self.print_output(f"Команда '{command}' не найдена\n")
                        break
                except Exception as e:
                    self.print_output(f"Ошибка выполнения команды '{command_line}': {str(e)}\n")
                    break

        except Exception as e:
            self.print_output(f"Ошибка чтения скрипта: {str(e)}\n")

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
            elif command == "conf-dump":
                self.ex_conf_dump(arguments)
            else:
                self.print_output(f"Команда '{command}' не найдена\n")
        except Exception as e:
            self.print_output(f"Ошибка выполнения: {str(e)}\n")

    def run(self):
        self.root.mainloop()


def main():
    vfs_path = None
    script_path = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--vfs-path" and i + 1 < len(args):
            vfs_path = args[i + 1]
            i += 2
        elif args[i] == "--script-path" and i + 1 < len(args):
            script_path = args[i + 1]
            i += 2
        else:
            i += 1

    emulator = VFSgui(vfs_path, script_path)
    emulator.run()


if __name__ == "__main__":
    main()