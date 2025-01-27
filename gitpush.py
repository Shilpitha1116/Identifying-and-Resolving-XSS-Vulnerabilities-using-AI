import subprocess
from flask import Flask, request

app = Flask(__name__)

# Directly assign your GitHub token here (not recommended for production)
GITHUB_TOKEN = "github-key"

@app.route('/push', methods=['POST'])
def push():
    commit_message = request.form.get('commit_message', 'Auto commit')
    repo_path = r"C:\Users\Shilpitha\EZFlow\UPS-POC\PocUI\xss"  # Local path to your cloned repository
    branch_name = 'main'  # Update to the branch you want to push to

    try:
        # Check for changes to commit
        print("Checking status of repository...")
        status_result = subprocess.run(
            ["git", "-C", repo_path, "status"],
            capture_output=True, text=True
        )
        print("Repository status:", status_result.stdout)

        # Add changes
        print("Attempting to add changes...")
        add_result = subprocess.run(
            ["git", "-C", repo_path, "add", "."],
            capture_output=True, text=True
        )
        if add_result.returncode != 0:
            print(f"Add Error: {add_result.stderr}")
            return f"Failed to add changes:\n{add_result.stderr}", 500

        # Commit changes
        print("Attempting to commit changes...")
        commit_result = subprocess.run(
            ["git", "-C", repo_path, "commit", "-m", commit_message],
            capture_output=True, text=True
        )
        if commit_result.returncode != 0:
            if "nothing to commit" in commit_result.stderr:
                print("No changes to commit.")
                return "No changes to commit.", 200
            else:
                print(f"Commit Error: {commit_result.stderr}")
                return f"Failed to commit changes:\n{commit_result.stderr}", 500

        # Push changes using token for authentication
        print("Attempting to push changes...")
        push_result = subprocess.run(
            ["git", "-C", repo_path, "push", f"https://{GITHUB_TOKEN}@github.com/EPS2024/xss.git", branch_name],
            capture_output=True, text=True
        )
        if push_result.returncode != 0:
            print(f"Push Error: {push_result.stderr}")
            return f"Failed to push changes:\n{push_result.stderr}", 500

        return "Changes pushed successfully!", 200

    except subprocess.CalledProcessError as e:
        print(f"General Error: {e.stderr}")
        return f"An error occurred:\n{e.stderr}", 500
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return f"Unexpected error:\n{str(e)}", 500




if __name__ == '__main__':
    app.run(port=8000)


