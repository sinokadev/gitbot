# addone.py

import os

filename = "test"

def increment_file():
    # 파일이 없으면 1로 시작
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
        print("파일이 없어서 생성하고 1을 썼습니다.")
    else:
        # 파일이 있으면 기존 숫자를 읽고 +1
        with open(filename, "r+") as f:
            content = f.read().strip()
            try:
                number = int(content)
            except ValueError:
                # 내용이 숫자가 아니면 0으로 초기화
                number = 0
            number += 1
            # 파일 처음부터 덮어쓰기
            f.seek(0)
            f.write(str(number))
            f.truncate()
        print(f"파일이 존재해서 기존 숫자 +1: {number}")

if __name__ == "__main__":
    increment_file()