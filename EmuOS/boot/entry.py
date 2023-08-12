import os
from EmuOS.dev.terminal import initializeTerminal
from EmuOS.dev.fs import FileSystem
from EmuOS.etc.motd import motd
from EmuOS.dev.utils import clear_screen
from EmuOS.boot.config import config

clear_screen()
fs_path = os.path.expanduser(config['filesystem'])
fs = FileSystem(fs_path)
motd()
initializeTerminal(fs)
