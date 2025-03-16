import tkinter as tk
from tkinter import filedialog
import threading
from modules import key_injector, c2_client, ducky_parser

script_path = None
parsed_commands = []

def load_script():
    global script_path, parsed_commands
    script_path = filedialog.askopenfilename(filetypes=[("Ducky Script", "*.txt")])
    
    if script_path:
        parsed_commands = ducky_parser.parseDuckyScript(script_path)
        root.after(0, update_status, f"Loaded script: {script_path}")
        btn_run.config(state=tk.NORMAL)
        c2_client.sendData(f"[INFO] Loaded script: {script_path}")

def run_payload():
    global script_path
    if script_path:
        threading.Thread(target=execute_payload, args=(script_path,)).start()

def execute_payload(script_path):
    root.after(0, update_status, "Payload is running...")
    c2_client.sendData("[INFO] Payload is running...")

    key_injector.executeScript(script_path, log_message) 

    root.after(0, update_status, "Payload execution complete.")
    c2_client.sendData("[INFO] Payload execution complete.") 

def update_status(message):
    status_label.config(text=message)

def log_message(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.yview(tk.END) 
    c2_client.sendData(message)

# GUI
root = tk.Tk()
root.geometry("500x300")
root.title("USB Rubber Ducky Emulator")

btn_load = tk.Button(root, text="Load Ducky Script", command=load_script)
btn_load.pack(pady=10)

btn_run = tk.Button(root, text="Run Payload", command=run_payload, state=tk.DISABLED)
btn_run.pack(pady=10)

status_label = tk.Label(root, text="No script loaded", wraplength=350)
status_label.pack(pady=10)

log_box = tk.Text(root, height=8, width=50, wrap=tk.WORD)
log_box.pack(pady=10)

root.mainloop()