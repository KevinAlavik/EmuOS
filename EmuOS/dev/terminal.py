import os
import keyboard
import curses
from EmuOS.var.mem import Memory
from EmuOS.dev.fs import FileSystem
from EmuOS.dev.utils import clear_screen, execute_script


def list_directory(fs, args):
    if args:
        if args[0] == "*":
            fs.list_directory()
        else:
            fs.list_directory(args[0])
    else:
        fs.list_directory()


def make_file(fs, args):
    if args:
        fs.make_file(args[0])
    else:
        print("Usage: mf <filename>")


def make_directory(fs, args):
    if args:
        fs.make_dir(args[0])
    else:
        print("Usage: md <dirname>")


def show_file(fs, args):
    if args:
        fs.show_file(args[0])
    else:
        print("Usage: sf <filename>")


def remove(fs, args):
    if not args:
        print("Usage: rm <filename or dirname>")
        return

    target_path = os.path.join(fs.current_path, args[0])
    if args[0] == "*":
        confirm = input(
            f"Are you sure you want to remove everything in this directory '{fs.current_path.replace(fs.root_path, '/')}'? (y/n): ")
        if confirm.lower() == "y":
            for item in os.listdir(fs.current_path):
                item_path = os.path.join(fs.current_path, item)
                if os.path.isdir(item_path):
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
        else:
            print("Operation canceled.")
    elif os.path.exists(target_path):
        if os.path.isdir(target_path):
            confirm = input(
                f"Are you sure you want to remove the directory '{args[0]}' and its contents? (y/n): ")
            if confirm.lower() == "y":
                try:
                    os.rmdir(target_path)
                except OSError:
                    print(f"Error: Directory '{args[0]}' is not empty.")
            else:
                print("Operation canceled.")
        else:
            os.remove(target_path)
    else:
        print(f"File or directory '{args[0]}' not found.")


def write_to_mem(fs, args):
    if len(args) < 2:
        print("Usage: wm <name> <value>")
        return
    name = args[0]
    value = ' '.join(args[1:])
    Memory.set(name, value)
    print(f"Memory variable '{name}' set to '{value}'")


def run_script(fs, args):
    if args:
        script_path = os.path.join(fs.current_path, args[0])
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r') as script_file:
                    script_code = script_file.read()
                    script_globals = {
                        '__name__': '__main__',
                        '__file__': script_path,
                        '__builtins__': __builtins__,
                    }
                    exec(script_code, script_globals)
            except Exception as e:
                print("Error while executing script:", e)
                import traceback
                traceback.print_exc()
        else:
            print("Script not found:", args[0])
    else:
        print("Usage: run <script_name>")


def move(fs, args):
    if len(args) < 2:
        print("Usage: mv <source> <destination>")
        return

    source_path = os.path.join(fs.current_path, args[0])
    destination_path = os.path.join(fs.current_path, args[1])

    if os.path.exists(source_path):
        try:
            os.rename(source_path, destination_path)
            print(f"Moved '{args[0]}' to '{args[1]}'")
        except Exception as e:
            print("Error while moving:", e)
    else:
        print(f"Source '{args[0]}' not found.")


# Define your built-in commands
builtinCmds = {
    "ls": list_directory,
    "mf": make_file,
    "sf": show_file,
    "md": make_directory,
    "rm": remove,
    "wm": write_to_mem,
    "run": run_script,
    "mv": move,
}


def initializeTerminal(fs):
    while True:
        relative_path = os.path.relpath(fs.current_path, fs.root_path)
        command = input(f"({relative_path}) $ ")

        if command == "exit":
            break
        elif command == "mem":
            print(Memory._shared_variables)
        elif command == "clear":
            clear_screen()
        elif command.startswith("cd"):
            new_dir = command[3:].strip()
            fs.change_directory(new_dir)
        else:
            parts = command.split()
            cmd_name = parts[0]
            args = parts[1:]

            if cmd_name in fs.bin_scripts:
                fs.execute_script(cmd_name, *args)
            elif cmd_name in builtinCmds:
                builtinCmds[cmd_name](fs, args)
            else:
                print("Invalid command:", command)


# Run the terminal
if __name__ == "__main__":
    fs = FileSystem('~/Desktop/EmuOS/EmuOS/')
    print("Welcome to EmuOS")
    print("Initializing Filesystem...")
    print("Done")
    print("Launching terminal")
    initializeTerminal(fs)
