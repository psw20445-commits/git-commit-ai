#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

def run_command(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr.strip()}")
        sys.exit(1)

def get_git_diff():
    # Check if inside a git repository
    run_command("git rev-parse --is-inside-work-tree")
    
    # Get staged changes
    diff = run_command("git diff --cached")
    if not diff:
        print("No staged changes found. Use 'git add <files>' to stage changes before generating a commit.")
        sys.exit(0)
    return diff

def generate_commit_message(api_key, diff):
    url = "https://api.openai.com/v1/chat/completions"
    
    system_instruction = (
        "You are an expert developer assistant. Your task is to analyze the provided git diff "
        "and write a professional, highly readable conventional commit message based on it.\n\n"
        "Follow these rules:\n"
        "1. The message must follow the Conventional Commits format: `<type>(<scope>): <description>`\n"
        "2. The description must be in imperative mood, lowercase, and concise (under 50 characters).\n"
        "3. Provide a bulleted body explaining 'what' and 'why' if the changes are complex.\n"
        "4. Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.\n"
        "5. Do NOT output anything else. Just the raw commit message text."
    )
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Here is the git diff:\n\n{diff}"}
        ],
        "temperature": 0.2
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            response_data = json.loads(res.read().decode("utf-8"))
            return response_data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        print(f"OpenAI API Error: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please run: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
        
    skip_confirm = "--yes" in sys.argv or "-y" in sys.argv
    diff = get_git_diff()
    
    print("Analyzing staged changes with AI...")
    commit_msg = generate_commit_message(api_key, diff)
    
    print("\n--- Generated Commit Message ---")
    print(commit_msg)
    print("--------------------------------\n")
    
    if skip_confirm:
        confirm = "y"
    else:
        confirm = input("Do you want to commit these changes with the message above? [y/N]: ").strip().lower()
    if confirm in ("y", "yes"):
        # Write to temporary file to avoid shell escaping issues with multi-line messages
        temp_file = ".git_commit_msg.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(commit_msg)
        try:
            subprocess.run(f"git commit -F {temp_file}", shell=True, check=True)
            print("\n🚀 Successfully committed! Done!")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    else:
        print("Commit aborted.")

if __name__ == "__main__":
    main()
