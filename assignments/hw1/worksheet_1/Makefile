# Path to commercial Adobe fonts if you are using them
FONT_PATH := "${HOME}/Library/Application Support/Adobe/CoreSync/plugins/livetype/.r"

worksheet_1:
	typst compile worksheet_1.typ --root ../../../ --font-path $(FONT_PATH)

# For live previewing
watch:
	typst watch worksheet_1.typ --root ../../../ --font-path $(FONT_PATH)
