# Git Automation Bot

This project is a Python-based automation bot that manages Git repositories, executes scripts based on specified conditions, and performs commits and pushes automatically.  

## Key Features

- Automatic cloning of Git repositories and branch checkout  
- Script execution based on specified conditions (true/false, commit message content, interval)  
- Dynamic commit messages based on script results  
- Automatic commit and push of changes  
- Management of multiple repositories simultaneously  

## Install

1. `pip install -r requirements.txt`
2. End!

## Config (`config.yml`)

Example:  

```yaml
author:
  name: "GitBot"
  email: "gitbot@sinoka.dev"

condition:
  - name: testone
    type: run
    value: true
  - name: every_minute
    type: interval
    value: 60
  - name: commit_check
    type: commit_message_contains
    value: "auto generated commit"

repos:
  - url: "https://github.com/sinokadev/gitbot-test.git"
    name: "test"
    branch: "main"
    remote_name: "origin"
    script: "python /home/sinokadev/gitbot/scripts/addone.py"
    commit_message: "auto generated commit"
    run: testone
```

## Usage

1. Set up your repositories, branches, scripts, and conditions in `config.yml`.  
2. Run the Python script:  

```
python src/main.py
```

3. The bot will automatically execute scripts and perform commits and pushes according to the specified conditions.  

## Condition Types

- `run`: Simple execution toggle (`true` / `false`)  
- `commit_message_contains`: Checks if the latest commit message contains a specific string  
- `interval`: Executes at a specified time interval (in seconds)  

## Script Execution

- The script specified in the `script` field will be executed.  
- The first line in the script output that contains `GitBotCM:` will be used as the commit message.  

## Notes

- Repositories are cloned into the `repos/` folder. If they already exist, the existing repository will be opened and updated.  
- Commits and pushes are performed based on the remote branch specified in `config.yml`.  
- Any errors will be printed to the console.  

## License

MIT License