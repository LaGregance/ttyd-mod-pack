from tools.dialog_editor.ttyd_txt_parser import TTYDTxtParser

parser = TTYDTxtParser('raw_rom/files/msg/US/aji_00.txt')
parser.load()

matches = parser.search("let's get")
print(matches)
