# Let's go for TTYD Hello World Mod

## 1. Requirements

 - Recent Dolphin Emulator
 - The TTYD ROM in ISO or CISO fornat (USA version, may work for others but not tested)

## 2. Hello World

1. Put your ROM in the Dolphin ROM folder, then on Dolphin -> Right Click on your ROM -> Properties -> Filesystem -> Right Click on Disk -> Extract Entire Disk -> Put in your repo under `raw_rom` folder (you may have `files` & `sys` subfolders)
2. Edit first line of `raw_rom/files/msg/US/aaa_00.txt`, change "Mail call!" to "Hello World!"
3. On Dolphin -> Click Config -> Paths -> Check Search Subfolder
4. On Makefile, set DEVELOPMENT_TARGET to your actual Dolphin path (including the name of you mod at the end)
5. Build the project with `make build`
6. You should see a new rom in the list, launch it, and check the postman say "Hello World!"

