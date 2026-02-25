import yaml
from git import Repo, Actor, GitCommandError
import types
import os
import subprocess
import time

class RepoObject:
    def __init__(self, repo=None, commit_message=None, script=None,
                 remote_name=None, name=None, condition=None):
        self.repo = repo
        self.commit_message = commit_message
        self.script = script
        self.remote_name = remote_name
        self.name = name
        self.condition = condition
        self.last_run = 0  # timestamp of last run

def should_run(repo_obj: RepoObject, conditions_list):
    if not repo_obj.condition:
        return False

    cond = next((c for c in conditions_list if c["name"] == repo_obj.condition), None)
    if cond and cond["type"] == "run" and cond["value"] is True:
        return True
    return False

def commit_condition_passed(repo_obj, conditions_list, latest_commit_message):
    cond = next(
        (c for c in conditions_list if c["name"] == repo_obj.condition),
        None
    )

    if cond is None:
        return False

    if cond["type"] == "commit_message_contains":
        # 최신 커밋 메시지에 value 문자열 포함 여부
        return cond["value"] == latest_commit_message

    return False

def interval_condition_passed(repo_obj, conditions_list):
    cond = next((c for c in conditions_list if c["name"] == repo_obj.condition), None)
    if cond is None or cond["type"] != "interval":
        return False

    now = time.time()
    if now - repo_obj.last_run >= cond["value"]:  # value는 초
        repo_obj.last_run = now
        return True
    return False

def dict_to_namespace(d):
    if isinstance(d, dict):
        return types.SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(x) for x in d]
    else:
        return d

def load_config(path="config.yml"):
    with open(path, "r") as config_file:
        config_yaml = config_file.read()
        config_dict = yaml.safe_load(config_yaml)
        config_namespace = dict_to_namespace(config_dict)
        return config_namespace

def commit_process(repo: RepoObject, latest_commit_message):
    print("Pull")
    try:
        repo.repo.git.pull()
    except Exception as e:
        print(f"No remote branch to pull, skipping: {e}")

    print(f"Running script: {repo.script}")
    repo_path = f"repos/{repo.name}"  # repo 폴더
    script_path = repo.script

    if os.path.exists(repo_path):
        print(f"Running script in {repo_path}: {script_path}")
        result = subprocess.run(
            f"{script_path} \"{latest_commit_message}\"",
            shell=True,
            check=True,
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        commit_msg = repo.commit_message  # 기본 메시지
        for line in result.stdout.splitlines():
            if "GitBotCM:" in line:
                commit_msg = line.split("GitBotCM:", 1)[1].strip()
                break  # 첫 번째만 사용
    else:
        print(f"Repo path {repo_path} does not exist.")
        return  # repo가 없으면 종료

    # 변경 사항이 있는지 확인
    if repo.repo.is_dirty(untracked_files=True):
        print("Changes detected, committing...")
        repo.repo.git.add(all=True)
        repo.repo.index.commit(commit_msg, author=author)

        origin = repo.repo.remote(name=repo.remote_name)
        branch_name = repo.repo.active_branch.name
        origin.push(refspec=f"{branch_name}:{branch_name}")
        print(f"Committed and pushed: {commit_msg}")
    else:
        print("No changes detected. Skipping commit.")

print("Load Config")
config = load_config()

author = Actor(config.author.name, config.author.email)

print("Cloning a Repo")
repos: list[RepoObject] = []

for repo_cfg in config.repos:
    repo_path = f"repos/{repo_cfg.name}"
    git_repo: Repo = None

    if os.path.exists(repo_path):
        print(f"{repo_cfg.name} repo already exists. Opening existing repository.")
        git_repo = Repo(repo_path)
    else:
        print(f"Cloning repository: {repo_cfg.url}...")
        git_repo = Repo.clone_from(repo_cfg.url, repo_path)

    try:
        git_repo.git.checkout(repo_cfg.branch)
    except GitCommandError:
        print(f"Branch {repo_cfg.branch} does not exist. Creating new branch.")
        git_repo.git.checkout("-b", repo_cfg.branch)

    repo_obj = RepoObject(repo=git_repo, commit_message=repo_cfg.commit_message, script=repo_cfg.script, remote_name=repo_cfg.remote_name, name=repo_cfg.name, condition=repo_cfg.run)
    repos.append(repo_obj)


print("Bot is running!")
conditions_list = [vars(c) for c in config.condition]
while True:
    try:
        for repo in repos:
            origin = repo.repo.remote(name=repo.remote_name) # 원격 가져오기
            branch_name = repo.repo.active_branch.name # 현재 브랜치 이름

            # 원격 최신 정보 가져오기 (fetch)
            origin.fetch()
            # 원격 브랜치 최신 커밋 가져오기
            latest_remote_commit = list(repo.repo.iter_commits(f"origin/{branch_name}", max_count=1))[0]

            latest_commit_message = latest_remote_commit.message

            if should_run(repo, conditions_list=conditions_list):
                commit_process(repo, latest_commit_message)
            elif commit_condition_passed(repo, conditions_list, latest_commit_message):
                commit_process(repo, latest_commit_message)
            elif interval_condition_passed(repo, conditions_list):
                commit_process(repo, latest_commit_message)
            else:
                print("Passed")
            
            print("End")
            
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        break