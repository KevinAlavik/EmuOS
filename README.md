# EmuOS
Emulated operating system

## Set Up
To use this you need to go to a release and download the: `EmuOS-vX.X.X.zip`. Once you downloaded that extract that and then open it in your favorite text editor once you done that go to **EmuOS/boot/config.py** and change `filesystem` to the path where the extracted folder is (Example: `'filesystem': '~/Desktop/EmuOS/EmuOS/'`). This is where the OS's filesystem will be based.

**Make sure you have python installed**

For MacOS and Linux simply run: `sudo python3 -m EmuOS.boot.entry`
For Windows open command prompt in administrator and simply run: `python3 -m EmuOS.boot.entry`
^ Make sure your in the folder you extracted