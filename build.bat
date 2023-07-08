pip install -r requirements.txt
pyinstaller -F main.py --collect-all customtkinter -w
echo "Done."