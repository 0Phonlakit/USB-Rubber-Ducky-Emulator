def parseDuckyScript(file_path):
    commands = []
    last_command = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(maxsplit=1)
            command = parts[0]
            argument = parts[1] if len(parts) > 1 else None

            if command == "STRING":
                commands.append(("STRING", argument))
            elif command == "ENTER":
                commands.append(("ENTER", None))
            elif command == "DELAY":
                commands.append(("DELAY", int(argument)))
            elif command == "GUI":
                commands.append(("GUI", argument))
            elif command == "ALT":
                commands.append(("ALT", argument))
            elif command == "CTRL":
                commands.append(("CTRL", argument))
            elif command == "SHIFT":
                commands.append(("SHIFT", argument))
            elif command == "TAB":
                commands.append(("TAB", None))
            elif command == "REPEAT":
                repeat_count = int(argument) if argument else 1
                if last_command:
                    commands.extend([last_command] * repeat_count)

            last_command = (command, argument)

    return commands