# 📝 Git Commit AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

An lightweight, open-source terminal utility that uses the OpenAI API (GPT/Codex) to automatically generate clean, standardized Conventional Commit messages based on your staged changes (`git diff --cached`).

---

## 🚀 Features

- **Instant Diff Analysis**: Inspects your staging area automatically.
- **Conventional Commits**: Formats output strictly using standard categories (`feat`, `fix`, `docs`, `refactor`, etc.).
- **Bulletproof Standard Library Execution**: Runs completely on Python's built-in standard library with **zero external dependencies** for lightning-fast startups.
- **Optional Auto-Commit**: Prompts to execute `git commit` directly with the generated message.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/psw20445-commits/git-commit-ai.git
   cd git-commit-ai
   ```

2. **Make Executable (Optional)**:
   ```bash
   chmod +x git_commit_ai.py
   ```

3. **Set your OpenAI API Key**:
   Ensure your OpenAI API key is exported in your environment:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

---

## 💻 How to Use

1. **Stage your files**:
   ```bash
   git add file1.py file2.js
   ```

2. **Run the tool**:
   ```bash
   python git_commit_ai.py
   ```

3. **Review and Confirm**:
   The script will print out the suggested conventional commit message and ask:
   ```txt
   Do you want to commit these changes with the message above? [y/N]:
   ```
   Press `y` to commit immediately!

---

## 🤝 Contributing

Contributions are highly welcome! Check out [CONTRIBUTING.md](file:///c:/Users/psw20/Downloads/git-commit-ai/CONTRIBUTING.md) to get started.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
