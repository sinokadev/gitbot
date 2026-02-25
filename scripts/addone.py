import os
import sys

filename = "test"

def increment_file(filename):
    if not os.path.exists(filename):
        number = 1
        with open(filename, "w") as f:
            f.write(str(number))
        print("Since the file does not exist, I created it and wrote 1.")
    else:
        with open(filename, "r+") as f:
            content = f.read().strip()
            try:
                number = int(content)
            except ValueError:
                number = 0
            number += 1
            f.seek(0)
            f.write(str(number))
            f.truncate()
        print(f"The file exists, so add the existing number +1: {number}")

    return number

if __name__ == "__main__":
    last_commit_msg = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if last_commit_msg == "auto generated commit":
        num = increment_file(filename)
        print(f"GitBotCM:{num}")
    else:
        print("The last commit message is not 'auto generated commit', so no action is taken.")