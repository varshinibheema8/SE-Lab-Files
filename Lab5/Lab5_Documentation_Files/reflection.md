# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and how is it different from testing?

Static code analysis examines source code without executing the program. It identifies possible programming mistakes, security weaknesses, and style violations. Testing runs the program with inputs to check its behaviour. Both are useful because static analysis can find suspicious code patterns, while tests can reveal runtime and functional problems.

## 2. What are the roles of Pylint, Bandit, and Flake8?

- **Pylint** checks code quality, naming, documentation, maintainability, and possible programming mistakes.
- **Bandit** scans Python code for common security issues, such as unsafe `eval()` and shell-command execution.
- **Flake8** checks Python style and common errors, including unused imports, line length, and exception syntax.

## 3. Which issues were most important, and why?

The highest-priority findings were the shell command built with `os.system()` and the weak MD5 hash reported by Bandit as high severity. The unsafe `eval()` finding was medium severity. These issues matter because they can introduce security risks. The bare exception and mutable default argument were also important because they can hide failures or cause confusing behaviour.

## 4. How did static analysis improve the program, and what are its limitations?

The tools helped identify security, reliability, and style issues. The code was updated to validate discount input, avoid dynamic evaluation, remove shell execution, use SHA-256, generate PINs with `secrets`, handle files with a context manager, and improve naming and documentation. After the fixes, Pylint scored the file 10/10, Bandit reported no issues, and Flake8 reported no violations. Static analysis cannot prove that a program is fully correct; functional tests and manual review are still necessary.
