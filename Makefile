all: ideabank

ideabank: src/ideabank.py
			$ pyinstaller src/ideabank.py --onefile

