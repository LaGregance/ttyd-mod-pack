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

## 3. Pack the ISO for distribution

1. Use melvin to create the patch (https://git.gauf.re/antoine/melvin/releases)
    1. Run “melvin_diff_tool” on terminal
    2. Select the original iso, raw_rom folder, output folder
    3. Create the patch
4. Finally go to the output folder, run the executable for your OS, select original iso, run the patch
5. You got your packed ISO !

Note: to avoid legal issue, you souldn't distribute the iso, instead you should distribute the patch executable build with melvin and
let your users build the iso on their own by providing their legal copy of the original ROM.

# Using tools

You can use tools to help you during modding under the `tools` folder.
Most of them are written in Python, make sure you have python3 & pip installed, warning GUI tools use TKInter, that is not packed in
every python version (on MacOS you can use `brew install python-tk`, or Windows check `tcl/tk and IDLE during Python installation).
More info here: https://stackoverflow.com/questions/69603788/how-to-pip-install-tkinter

I also recommand you to create a venv using `python -m venv .venv` and activate it depending on your platform:
```bash
source .venv/bin/activate # Linux / Mac
.\.venv\Scripts\Activate.ps1 # Windows powershell
.\.venv\Scripts\activate.bat # Windows bash

# Tips: if you use direnv, you can automatically activate venv when you are in this folder in your terminal by adding this in your .envrc
export VIRTUAL_ENV=.venv
layout python
```

Once it done, install requirements: `pip3 install -r requirements.txt`

This is the list of tools, check the README in each of them for more details:
 - dialog_editor: A GUI that help you finding & editing dialog