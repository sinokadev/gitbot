# addone.py

import os
import sys

filename = "test"

def increment_file(filename):
    # 파일이 없으면 1로 시작
    if not os.path.exists(filename):
        number = 1
        with open(filename, "w") as f:
            f.write(str(number))
        print("파일이 없어서 생성하고 1을 썼습니다.")
    else:
        # 파일이 있으면 기존 숫자를 읽고 +1
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
        print(f"파일이 존재해서 기존 숫자 +1: {number}")

    return number

if __name__ == "__main__":
    # 스크립트 인자로 마지막 커밋 메시지 받기
    last_commit_msg = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # "자동 생성된 커밋" 일 때만 수행
    if last_commit_msg == "자동 생성된 커밋":
        num = increment_file(filename)
        # GitBotCM 메시지 출력
        print(f"GitBotCM:{num}")
    else:
        print("마지막 커밋 메시지가 '자동 생성된 커밋'이 아니므로 작업을 수행하지 않습니다.")