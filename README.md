# decodelabs-Code-x_reviewer
<div align="center">

# 🤖 Intelligent Code Reviewer & Explainer
### Automated Code Architecture & Analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com)
[![Rich](https://img.shields.io/badge/UI-Rich-purple)](https://github.com/Textualize/rich)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<img src="https://raw.githubusercontent.com/Textualize/rich/master/imgs/features.png" width="600" alt="Terminal Preview">

An autonomous, AI-powered gatekeeper that ingests raw code files, applies strict system instructions for structured outputs, and renders optimized, syntax-highlighted code through pure orchestration logic.

🚀 [Quick Start](#-quick-start) • 📁 [Architecture](#-architecture) • ⚙️ [Configuration](#-configuration) • 🔒 [Security](#-security) • 🛠️ [Troubleshooting](#-troubleshooting)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Intelligent Analysis | Leverages Groq's `llama-3.3-70b-versatile` for deep code inspection |
| 📋 Structured Outputs | Enforces deterministic `## BUG_REPORT` and `## REFACTORED_CODE` sections |
| 🎨 Syntax Highlighting | Rich terminal rendering with color-mapped code blocks |
| 🛡️ Input Validation | Robust file ingestion triage with encoding fallback |
| 🌐 Multi-Language | Supports Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, SQL |
| ⚡ Zero Bloat | No conversational filler — pure analytical output |

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. Ingest  │────▶│  2. Build   │────▶│  3. Validate│────▶│  4. Render  │
│   Payload   │     │   Prompts   │     │   Output    │     │  Terminal   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                   │                    │
      ▼                    ▼                   ▼                    ▼
  .py .js .java      System + User       ## BUG_REPORT       Rich Markdown
  .ts .c .cpp        Prompt Fusion       ## REFACTORED_CODE   Syntax Highlight
```

**The Complete IPO Pipeline**

1. 📥 **Local System** — `open().read()` safely streams raw files into a string buffer
2. 🔗 **API Client** — Payload merges with persona constraints → Groq GenAI
3. ✅ **Validation** — Script verifies exact presence of `## BUG_REPORT` and `## REFACTORED_CODE`
4. 🖥️ **Terminal** — Rich engine compiles markdown and prints color-coded syntax

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A Groq Cloud API key (free tier available)

### 1. Clone & Enter
```bash
git clone https://github.com/yourusername/decodelabs-code-reviewer.git
cd decodelabs-code-reviewer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**
```
groq>=0.4.0
rich>=13.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### 3. Configure Your API Key

Never commit real credentials to source control. Copy the example file and fill in your own key locally:

```bash
cp .env.example .env
```

**.env.example**
```
GROQ_API_KEY=<your-groq-api-key-here>
```

Then edit `.env` and paste your actual key from [console.groq.com](https://console.groq.com).

> ⚠️ **Windows PowerShell users:** avoid `echo "..." > .env` — it writes UTF-16 by default and breaks `python-dotenv`. Use a text editor, or:
> ```powershell
> [System.IO.File]::WriteAllText("$PWD\.env", "GROQ_API_KEY=your-key-here", [System.Text.UTF8Encoding]::new($false))
> ```

### 4. Run It
```bash
# Review a Python file
python src/main.py samples/sample_bad.py

# Review JavaScript
python src/main.py samples/sample.js

# Review inline code
python src/main.py --code "print('hello world')" --lang python

# Save results to JSON
python src/main.py samples/sample_bad.py --output results.json
```

---

## 📁 Project Structure

```
decodelabs-code-reviewer/
│
├── 📂 src/
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # 🎛️ CLI entry point
│   ├── reviewer.py              # 🤖 Core AI orchestrator
│   ├── prompt_builder.py        # 📝 System & user prompt engineering
│   ├── models.py                # 📐 Pydantic data models
│   ├── validator.py             # ✅ Output format validation
│   └── renderer.py              # 🎨 Rich terminal rendering
│
├── 📂 samples/
│   ├── sample_bad.py            # 🐛 Intentionally buggy Python
│   ├── sample_good.py           # ✅ Clean Python reference
│   └── sample.js                # 🐛 Intentionally buggy JS
│
├── 📂 tests/
│   └── (your test files)
│
├── .env                         # 🔑 Local secrets — NEVER committed
├── .env.example                 # 📋 Template for env vars
├── .gitignore                   # 🚫 Excludes .env and other local files
├── requirements.txt             # 📦 Python dependencies
└── README.md                    # 📖 You are here
```

---

## 🔒 Security

This project follows a few basic hardening practices — please keep them intact if you fork or extend it:

- **Never commit `.env`.** Ensure your `.gitignore` includes:
  ```
  .env
  *.env
  __pycache__/
  *.pyc
  results.json
  ```
- **Rotate any key that is ever exposed.** If a real API key is accidentally committed or pasted into an issue/PR, revoke it immediately at console.groq.com and issue a new one — git history retains old commits even after deletion.
- **Treat reviewed source files as untrusted input.** The tool reads arbitrary local files and sends their contents to a third-party API; don't point it at files containing secrets, credentials, or sensitive data you don't want leaving your machine.
- **Pin dependency versions** in `requirements.txt` (as done above) and periodically run `pip list --outdated` / a vulnerability scanner (e.g. `pip-audit`) to catch known CVEs in dependencies.
- **No personal contact details or credentials belong in this README** or in commit history — use your organization's designated support channel instead.

If you discover a security issue in this project, please report it privately (e.g. via a GitHub Security Advisory) rather than opening a public issue.

---

## ⚙️ Configuration

### Supported Languages

| Language | Extension | Enum Value |
|---|---|---|
| Python | `.py` | `python` |
| JavaScript | `.js` | `javascript` |
| TypeScript | `.ts` | `typescript` |
| Java | `.java` | `java` |
| C | `.c` | `c` |
| C++ | `.cpp` | `cpp` |
| Go | `.go` | `go` |
| Rust | `.rs` | `rust` |
| SQL | `.sql` | `sql` |

### CLI Arguments
```bash
python src/main.py [FILE] [OPTIONS]

Options:
  -c, --code TEXT      Code string to review (alternative to file)
  -l, --lang TEXT      Programming language override
  -o, --output PATH    Save results to JSON file
  -v, --verbose        Show metadata (model, timestamp, etc.)
  --help               Show this message and exit
```

---

## 🖥️ Sample Output

```
================================================================================
                        🤖 INTELLIGENT CODE REVIEWER
================================================================================

🐛 BUG REPORT
----------------------------------------
• Critical — Line 7: Potential ZeroDivisionError when `numbers` is empty
• High     — Line 5: Inefficient `range(len(numbers))` loop; use `for num in numbers`
• Medium   — Line 10: Unused variable `data` declared but never referenced
• Low      — Line 12: Type mismatch — cannot concatenate str + float

💡 REFACTORED CODE
----------------------------------------
   1 │ from typing import List, Optional
   2 │
   3 │ def calculate_average(numbers: List[float]) -> Optional[float]:
   4 │     if not numbers:
   5 │         return None
   6 │     return sum(numbers) / len(numbers)
   7 │
   8 │ data = [1, 2, 3, 4, 5]
   9 │ avg = calculate_average(data)
  10 │ print(f"Average is: {avg}")

================================================================================
```

---

## 🛠️ Troubleshooting

**`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`**
Cause: `.env` file saved as UTF-16 (PowerShell default).
Fix:
```powershell
Remove-Item .env
[System.IO.File]::WriteAllText("$PWD\.env", "GROQ_API_KEY=your-key-here", [System.Text.UTF8Encoding]::new($false))
```

**`ModuleNotFoundError: No module named 'models'`**
Cause: Running from the wrong directory or `sys.path` not set.
Fix: Always run from the project root:
```bash
python src/main.py samples/sample_bad.py
```

**`Invalid API Key (401)`**
Cause: Placeholder key still in `.env`, or key revoked.
Fix: Grab a fresh key from console.groq.com and update `.env` — never share the key in chat, issues, or commits.

**`'PromptBuilder' object has no attribute 'build_system_prompt'`**
Cause: Old `prompt_builder.py` cached in memory.
Fix: Save the updated file and restart your terminal.

---

## 🧠 The LLM Taming Matrix

Unlike conversational AI that introduces non-deterministic variations, this tool locks behavior using strict system instructions:

| Conversational AI ❌ | Analytical Gatekeeper ✅ |
|---|---|
| "Sure, here is your code!" filler | Direct bullet points only |
| Structural noise breaks parsers | Valid markdown code blocks |
| Subjective feedback per run | Identical standards every commit |

---

## 👤 About the Developer

| | |
|---|---|
| **Name** | Muhammad Ekremah |
| **Institute** | Newports Institute of Communication & Economics |
| **Program** | BS Computer Science (BSCS) — 5th Semester |
| **Internship** | DecodeLabs — Generative AI Track |

For support, please open a GitHub Issue on this repository rather than using personal contact details.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

<div align="center">
Built with ❤️ for the DecodeLabs Generative AI Internship
</div>
