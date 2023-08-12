import os


class FileSystem:
    def __init__(self, root_path):
        self.root_path = root_path
        self.current_path = root_path
        self.bin_scripts = self._get_bin_scripts()

    def _get_bin_scripts(self):
        bin_path = os.path.join(self.root_path, 'bin')
        if os.path.exists(bin_path):
            return [script[:-3] for script in os.listdir(bin_path) if script.endswith('.py')]
        return []

    def change_directory(self, new_path):
        if new_path == "/":
            self.current_path = self.root_path
        elif not new_path.startswith("/"):
            new_path = os.path.join(self.current_path, new_path)

        emuos_root = os.path.abspath(self.root_path)
        if not os.path.abspath(new_path).startswith(emuos_root):
            print("Access denied, Reason: Cant escape fs")
            return

        if os.path.exists(new_path):
            self.current_path = new_path
        else:
            print("Directory not found:", new_path.replace(self.root_path, "/"))

    def list_directory(self, directory=None):
        if directory:
            path = os.path.join(self.current_path, directory)
        else:
            path = self.current_path

        contents = os.listdir(path)
        formatted_contents = [
            item + '/' if os.path.isdir(os.path.join(path, item)) else item for item in contents]
        print("\n".join(formatted_contents))

    def make_file(self, filename):
        path = os.path.join(self.current_path, filename)
        if os.path.exists(path):
            print("File already exists:", filename)
        else:
            open(path, 'a').close()

    def make_dir(self, dirname):
        path = os.path.join(self.current_path, dirname)
        if os.path.exists(path):
            print("Directory already exists:", dirname)
        else:
            os.mkdir(path)

    def show_file(self, filename):
        path = os.path.join(self.current_path, filename)
        if os.path.exists(path):
            with open(path, 'r') as file:
                print(file.read())
        else:
            print("File not found:", filename)

    def execute_script(self, script_name, *args):
        script_path = os.path.join(self.root_path, 'bin', f"{script_name}.py")
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r') as script_file:
                    script_code = script_file.read()
                    script_globals = {
                        '__name__': '__main__',
                        '__file__': script_path,
                        '__builtins__': __builtins__,
                        'args': args,  # Pass the arguments to the script
                    }
                    exec(script_code, script_globals)
            except Exception as e:
                print("Error while executing script:", e)
                import traceback
                traceback.print_exc()
        else:
            # Try with .py extension
            alt_script_path = os.path.join(
                self.root_path, 'bin', f"{script_name}.py")
            if os.path.exists(alt_script_path):
                try:
                    with open(alt_script_path, 'r') as script_file:
                        script_code = script_file.read()
                        script_globals = {
                            '__name__': '__main__',
                            '__file__': alt_script_path,
                            '__builtins__': __builtins__,
                            'args': args,  # Pass the arguments to the script
                        }
                        exec(script_code, script_globals)
                except Exception as e:
                    print("Error while executing script:", e)
                    import traceback
                    traceback.print_exc()
            else:
                print("Script not found:", script_name)
