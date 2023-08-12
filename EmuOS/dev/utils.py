import os

def execute_script(script_name):
    script_path = os.path.join(os.path.dirname(
        __file__), '..', 'bin', script_name)
    if os.path.exists(script_path):
        try:
            with open(script_path, 'r') as script_file:
                script_code = script_file.read()
                exec(script_code)
        except Exception as e:
            print("Error while executing script:", e)
            import traceback
            traceback.print_exc()
    else:
        print("Script not found:", script_name)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
