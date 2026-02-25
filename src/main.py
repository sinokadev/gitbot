import yaml
from git import Repo, Actor, GitCommandError
import types
import os
import subprocess

class RepoObject:
    def __init__(self, repo: Repo = None, commit_message: str = None, script: str = None, remote_name: str = None, name: str = None):
        self.repo: Repo | None = repo
        self.commit_message: str | None = commit_message
        self.script: str | None = script
        self.remote_name = remote_name
        self.name = name

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

    repo_obj = RepoObject(repo=git_repo, commit_message=repo_cfg.commit_message, script=repo_cfg.script, remote_name=repo_cfg.remote_name, name=repo_cfg.name)
    repos.append(repo_obj)


print("Bot is running!")
while True:
    try:
        for repo in repos:
            print("Pull")
            try:
                repo.repo.git.pull()
            except Exception as e:
                print(f"No remote branch to pull, skipping: {e}")
            print(f"Running script: {repo.script}")
            repo_path = f"repos/{repo.name}" # repo 폴더
            script_path = repo.script

            if os.path.exists(repo_path):
                print(f"Running script in {repo_path}: {script_path}")
                subprocess.run(script_path, shell=True, check=True, cwd=repo_path)
            else:
                print(f"Repo path {repo_path} does not exist.")
            
            print("Commit")
            repo.repo.git.add(all=True)
            repo.repo.index.commit(repo.commit_message, author=author)

            origin = repo.repo.remote(name=repo.remote_name)
            branch_name = repo.repo.active_branch.name
            origin.push(refspec=f"{branch_name}:{branch_name}")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        break