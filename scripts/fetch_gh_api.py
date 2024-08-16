
import os
import requests

# Constants
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = "Alegarciy"
README_PATH = "README.md"
SECTION_TITLE = "### Latest Repositories"

# GitHub URL API
api_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=5"

# Headers with authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def fetch_latest_repos():
    """Fetch the 5 latest updated repositories of a user."""
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return [(repo['name'], repo['html_url']) for repo in repos]
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []

def update_readme(repos):
    """Update the README.md file with the latest repositories."""
    if not repos:
        return

    with open(README_PATH, "r") as file:
        readme_content = file.readlines()

    # Find where the latest repos section starts
    try:
        section_start_index = readme_content.index(f"{SECTION_TITLE}\n")
    except ValueError:
        # If the section doesn't exist, add it to the end
        section_start_index = len(readme_content)
        readme_content.append(f"\n{SECTION_TITLE}\n")

    # Replace the content after the section title
    updated_content = readme_content[:section_start_index + 1]
    for repo_name, repo_url in repos:
        updated_content.append(f"- [{repo_name}]({repo_url})\n")

    # Write the updated content back to the README.md
    with open(README_PATH, "w") as file:
        file.writelines(updated_content)

def main():
    latest_repos = fetch_latest_repos()
    update_readme(latest_repos)

if __name__ == "__main__":
    main()
