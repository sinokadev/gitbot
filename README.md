# Git Automation Bot

이 프로젝트는 Git 저장소를 자동으로 관리하고, 조건에 따라 스크립트를 실행하고 커밋 및 푸시를 수행하는 Python 기반 자동화 봇입니다.



## 주요 기능

- Git 저장소 자동 클론 및 브랜치 체크아웃
- 지정된 조건(true/false, commit 메시지 포함, 간격)에 따라 스크립트 실행
- 스크립트 결과에 따라 커밋 메시지 동적 설정
- 변경 사항 자동 커밋 및 푸시
- 여러 저장소 동시 관리 가능



## 설치

### 1. 의존성 설치

```bash
pip install gitpython pyyaml
```

### 2. 프로젝트 구조

.
├── config.yml       # 설정 파일
├── gitbot.py        # GitBot 실행 스크립트
└── repos/           # 클론된 저장소 폴더



## 설정 (`config.yml`)

예시:

```yaml
author:
  name: "Your Name"
  email: "your.email@example.com"

condition:
  - name: "run_every_minute"
    type: "interval"
    value: 60  # 초 단위

  - name: "commit_message_trigger"
    type: "commit_message_contains"
    value: "Update"
  - name: "bool_trigger"
    type: "run"
    value: false

repos:
  - name: "example-repo"
    url: "https://github.com/user/example-repo.git"
    branch: "main"
    commit_message: "Auto commit by GitBot"
    script: "run_script.sh"
    remote_name: "origin"
    run: "run_every_minute"
```



## 사용법

1. `config.yml`에 저장소, 브랜치, 스크립트, 조건 등을 설정합니다.
2. Python 스크립트 실행:

```bash
python gitbot.py
```

3. 봇이 지정된 조건에 따라 자동으로 스크립트를 실행하고 커밋 및 푸시를 수행합니다.



## 조건 유형

- `run`: 단순 실행 여부 (`true`/`false`)
- `commit_message_contains`: 최신 커밋 메시지에 특정 문자열 포함 여부
- `interval`: 지정 시간 간격(초 단위)마다 실행



## 스크립트 실행

- `script` 필드에 지정된 스크립트가 실행됩니다.
- 스크립트 출력에서 `GitBotCM:`이 포함된 첫 번째 줄을 커밋 메시지로 사용합니다.



## 참고 사항

- `repos/` 폴더에 저장소를 클론하며, 이미 존재하면 기존 저장소를 열고 업데이트합니다.
- 커밋 및 푸시는 `config.yml`에서 설정한 원격 브랜치를 기준으로 수행됩니다.
- 오류 발생 시 콘솔에 메시지가 출력됩니다.



## 라이선스

MIT License