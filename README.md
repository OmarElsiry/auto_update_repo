# Auto Update Repo

A Python script designed to automate the process of updating your repository to the latest version from GitHub. This tool streamlines the update process by handling file removals, downloading the latest code, and extracting necessary files while respecting your `.gitignore` settings.

## Features

- **Automatic Updates**: Seamlessly update your repository with the latest changes from GitHub.
- **Exclusion Handling**: Automatically honors the exclusions defined in your `.gitignore` file.
- **Version Management**: Tracks your current version and updates it upon successful retrieval of the latest version.
- **Robust Error Handling**: Provides feedback on any issues encountered during the update process.

## Requirements

Ensure you have the following Python packages installed:

- `requests`

The script will attempt to install any missing packages automatically, provided you have Python installed on your system.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OmarElsiry/auto_update_repo.git
   cd auto_update_repo
   ```

2. **Create a .gitignore File**:
   Ensure you have a `.gitignore` file in your project directory specifying files and folders to be excluded during the update process.

3. **Add Your Version File**:
   Create a `version.txt` file in the project folder. This file will keep track of the current version of your repository.

4. **Run the Updater**:
   Execute the updater script by running:
   ```bash
   python updater.py
   ```

5. **Input Details**:
   When prompted, enter your GitHub username, repository name, and the branch you want to update (default is `main`).

## Usage Example

```bash
Enter GitHub username: OmarElsiry
Enter GitHub repository name: auto_update_repo
Enter branch name (default: main): main
```

The script will check for updates, remove any outdated files (respecting the `.gitignore`), download the latest version, and extract the files to your project directory.

## Troubleshooting

If you encounter any issues, check the following:

- Ensure you have an active internet connection.
- Verify that the GitHub repository URL is correct.
- Make sure Python is installed and properly configured on your system.
