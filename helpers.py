import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# GitHub token should be set as an environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Function to get GitHub data (only README files)
def get_github_data():
    context = ""
    api_url = "https://api.github.com/user/repos"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            # Fetch the README file from each repository
            readme_url = f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/contents/README.md"
            readme_response = requests.get(readme_url, headers=headers)

            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                readme_content = readme_data['content']
                decoded_content = base64.b64decode(readme_content).decode('utf-8')
                context += f"README for {repo['name']}:\n{decoded_content}\n" + "-"*80 + "\n"
            else:
                context += f"No README found for {repo['name']}\n" + "-"*80 + "\n"
    else:
        print(f"Authentication failed. Status code: {response.status_code}")
        print("Response:", response.json())  # Show detailed response
        context += f"Failed to fetch repositories: {response.status_code}\n"

    return context
