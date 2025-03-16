import time
import pynput
from modules.ducky_parser import parseDuckyScript

Keyboard = pynput.keyboard.Controller()
Key = pynput.keyboard.Key

def press_key_combination(*keys):
    for key in keys:
        Keyboard.press(key)
    for key in reversed(keys):
        Keyboard.release(key)

def executeScript(file_path, log_callback):
    commands = parseDuckyScript(file_path)

    seen_commands = set()
    for cmd, val in commands:
        if (cmd, val) in seen_commands:
            pass
        else:
            seen_commands.add((cmd, val))
        
        if cmd == "STRING":
            log_callback(f"Typing: {val}")
            Keyboard.type(val)
        elif cmd == "ENTER":
            log_callback("Pressing Enter")
            Keyboard.press(Key.enter)
            Keyboard.release(Key.enter)
        elif cmd == "DELAY":
            log_callback(f"Delay: {val}ms")
            time.sleep(val / 1000)
        elif cmd == "GUI":
            if val:
                log_callback(f"Pressing GUI + {val}")
                press_key_combination(Key.cmd, val.lower())
            else:
                log_callback("Pressing GUI Key")
                Keyboard.press(Key.cmd)
                Keyboard.release(Key.cmd)
        elif cmd == "ALT":
            if val:
                log_callback(f"Pressing ALT + {val.upper()}")
                Keyboard.press(Key.alt)
                Keyboard.press(val.lower())  
                Keyboard.release(val.lower())
                Keyboard.release(Key.alt)
            else:
                log_callback("Pressing ALT key")
                Keyboard.press(Key.alt)
                Keyboard.release(Key.alt)
        elif cmd == "TAB":
            log_callback("Pressing TAB")
            Keyboard.press(Key.tab)
            Keyboard.release(Key.tab)
        elif cmd == "CTRL":
            if val:
                log_callback(f"Pressing CTRL + {val.upper()}")
                press_key_combination(Key.ctrl, val.lower())
            else:
                log_callback("Pressing CTRL Key")
                Keyboard.press(Key.ctrl)
                Keyboard.release(Key.ctrl)
        elif cmd == "SHIFT":
            if val:
                log_callback(f"Pressing SHIFT + {val.upper()}")
                press_key_combination(Key.shift, val.lower())
            else:
                log_callback("Pressing SHIFT Key")
                Keyboard.press(Key.shift)
                Keyboard.release(Key.shift)
        elif cmd == "REPEAT":
            repeat_count = int(val) if val.isdigit() else 1
            log_callback(f"Repeating last command {repeat_count} times")
            for _ in range(repeat_count):
                last_cmd, last_val = commands[-2] if len(commands) > 1 else ("", "")
                if last_cmd == "STRING":
                    Keyboard.type(last_val)
                elif last_cmd == "ENTER":
                    Keyboard.press(Key.enter)
                    Keyboard.release(Key.enter)
                elif last_cmd == "DELAY":
                    time.sleep(last_val / 1000)
                elif last_cmd == "GUI":
                    press_key_combination(Key.cmd, last_val.lower())
                elif last_cmd == "ALT":
                    Keyboard.press(Key.alt)
                    Keyboard.press(last_val.lower())  
                    Keyboard.release(last_val.lower())
                    Keyboard.release(Key.alt)

    log_callback("Execution complete.")
