import os
import sys
import subprocess
from io import BytesIO
from zipfile import ZipFile
import requests

# Function to attempt installing a missing package
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

# List of required packages
required_packages = ['requests', 'zipfile', 'io']

# Attempt to install the missing packages
for package in required_packages:
    install_and_import(package)


class Updater:
    def __init__(self, repo_url, folder_name, version_file="version.txt"):
        self.repo_url = repo_url
        self.folder_name = folder_name
        self.version_file = version_file

    def get_exclusions(self, gitignore_path=".gitignore"):
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                exclusions = f.read().splitlines()
            exclusions = [e for e in exclusions if e and not e.startswith("#")] + [".gitignore", ".git"]
        else:
            exclusions = [".gitignore", ".git"]
        return exclusions

    def remove_old_files(self):
        exclusions = self.get_exclusions()
        print("Removing old files...")
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                path = os.path.join(root, name)
                relative_path = path[2:]
                if not relative_path.startswith(tuple(exclusions)):
                    os.remove(path)

    def download_repo(self):
        print("Downloading repository...")
        response = requests.get(self.repo_url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise Exception(f"Failed to download repo: {response.status_code}")

    def extract_files(self, data):
        print("Extracting files...")
        with ZipFile(data, "r") as zip_obj:
            files = [f for f in zip_obj.namelist() if f.startswith(self.folder_name) and not f.endswith("/")]
            for file in files:
                new_name = file.replace(f"{self.folder_name}/", "")
                dir_name = os.path.dirname(new_name)
                if "/" in new_name and not os.path.exists(dir_name):
                    print(f"Creating folder {dir_name}...")
                    os.makedirs(dir_name)
                with zip_obj.open(file) as src, open(new_name, "wb") as dst:
                    dst.write(src.read())

    def update_version(self, version):
        with open(self.version_file, "w") as f:
            f.write(version)
        print(f"Updated version to {version}")

    def get_current_version(self):
        if os.path.exists(self.version_file):
            with open(self.version_file, "r") as f:
                return f.read().strip()
        return None

    def get_latest_version(self, api_url):
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()["sha"]
        else:
            raise Exception(f"Failed to get latest version: {response.status_code}")

    def update(self, latest_version):
        self.remove_old_files()
        data = self.download_repo()
        self.extract_files(data)
        self.update_version(latest_version)


def main():
    user = input("Enter GitHub username: ")
    repo = input("Enter GitHub repository name: ")
    branch = input("Enter branch name (default: main): ") or "main"

    # Construct URLs based on user input
    repo_url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
    api_url = f"https://api.github.com/repos/{user}/{repo}/commits/{branch}"

    # Define the folder name to be extracted
    folder_name = f"{repo}-{branch}"

    updater = Updater(repo_url, folder_name)

    try:
        current_version = updater.get_current_version()
        latest_version = updater.get_latest_version(api_url)

        if current_version != latest_version:
            print("New version available!")
            updater.update(latest_version)
        else:
            print("Already up to date!")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
