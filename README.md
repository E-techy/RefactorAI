# 🚀 RefactorAI

> **AI-Powered GitHub Repository Enhancement from Your Terminal**

RefactorAI is a powerful command-line interface (CLI) tool designed to **automate code enhancement, documentation generation, and repository cleanup** using state-of-the-art AI models.

It acts as a bridge between your local development environment and major AI providers like **Google Gemini, OpenAI, and Anthropic**, allowing you to refactor, analyze, and improve repositories directly from your terminal — securely and efficiently.

---

## 🌟 Why RefactorAI?

Maintaining high-quality repositories takes time:

* Writing documentation
* Adding meaningful comments
* Refactoring messy code
* Removing dead or redundant logic
* Improving structure and readability

RefactorAI automates this process using AI — helping you maintain **clean, production-ready, and professional repositories** with minimal effort.

---

# ✨ Features

## 🧠 AI-Powered Code Intelligence

* Automatically refactor and improve code quality
* Generate inline comments and documentation
* Create README files for projects and individual modules
* Summarize files and repository structure
* Detect and suggest removal of bad or unused code

---

## 🔐 Secure Credential Management

Security is a top priority.

RefactorAI uses your operating system’s encrypted credential storage via **`keyring`**:

* 🍎 macOS → Keychain
* 🪟 Windows → Credential Manager
* 🐧 Linux → Secret Service / system vault

✅ No API keys are stored in plain text
✅ No sensitive data committed to version control

---

## 🔌 Multi-Provider AI Support

Choose your preferred AI provider:

### 🔹 Google Gemini

* Gemini 1.5 Pro
* Gemini Flash

### 🔹 OpenAI

* GPT-4o
* GPT-3.5

### 🔹 Anthropic

* Claude 3 Opus
* Claude 3 Sonnet
* Claude 3 Haiku

Switch providers anytime through the interactive configuration menu.

---

## 🖥️ Interactive Terminal UI

RefactorAI provides a clean and intuitive CLI experience powered by:

* `rich` for styled terminal output
* `questionary` for interactive prompts

Features include:

* Arrow-key navigation
* Hidden password inputs
* Clean menu-driven configuration

---

## 🛠️ GitHub Integration (In Development)

Upcoming features include:

* Direct repository management
* Automatic pull request generation
* AI-powered commit suggestions
* Repository-wide analysis and cleanup
* Intelligent branch creation for improvements

---

# 🚀 Installation

## 📌 Prerequisites

* Python **3.9+**
* Git
* pip

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/E-techy/RefactorAI.git
cd RefactorAI
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---

### 3️⃣ Install the Application

```bash
pip install -e .
```

> The `-e` flag installs RefactorAI in **editable mode**, so any changes you make to the source code are immediately reflected in the CLI.

---

# 📖 Usage

## 🔧 Initial Configuration

Before using AI features, configure your API keys securely:

```bash
refactor configure
```

### What This Does:

* Opens an interactive configuration menu
* Lets you choose your AI provider
* Securely stores API keys in your OS vault
* Allows safe updating or deletion of keys
* Stores only non-sensitive preferences locally

---

## 🧪 Upcoming Commands

```bash
refactor analyze <repo-url>
```

Analyze a repository for:

* Code quality improvements
* Documentation gaps
* Structural optimization
* Dead code detection

```bash
refactor fix <file-path>
```

Apply AI-powered enhancements to a specific file.

More commands coming soon:

* `refactor doc <path>`
* `refactor summarize <repo>`
* `refactor clean <repo>`

---

# 🛡️ Security & Privacy

We take security seriously.

* API keys are never stored in plain text.
* No credentials are committed to Git.
* Sensitive information is stored using the system's secure vault.
* Only non-sensitive configuration data is stored locally.

RefactorAI is built with **secure-by-design principles**.

---

# 🏗️ Project Vision

RefactorAI aims to become:

> The ultimate AI-powered repository maintenance engine.

Future roadmap includes:

* Full GitHub automation
* Pull request generation
* CI/CD integration
* Multi-language support
* Plugin architecture
* Web dashboard companion
* Self-hosted AI model support

---

# 🤝 Contributing

We welcome contributions of all kinds:

* 🐛 Bug fixes
* 📚 Documentation improvements
* ✨ Feature suggestions
* 🔧 Performance optimizations

Please read `CONTRIBUTING.md` for guidelines and the pull request process.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 💡 Final Note

RefactorAI is built for developers who value:

* Clean code
* Automation
* Security
* Productivity

If you believe repositories should maintain themselves —
**RefactorAI is for you.** 🚀
