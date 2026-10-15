# Lab 5: Static Code Analysis — Issue Documentation

**Target file:** `restaurant_order_system.py`  
**Tools used:** Pylint, Bandit, and Flake8

## Original findings and fixes

| Issue | Type | Original location | Description | Fix applied |
|---|---|---:|---|---|
| Unsafe `eval()` | Security — Medium (Bandit B307) | Line 42 | Evaluating a string as Python code can execute unintended expressions. | Replaced the expression parameter with a numeric discount rate and validated its type and range. |
| Shell command using `os.system()` | Security — High (Bandit B605) | Line 58 | Building a shell command from a filename can expose command-injection risk. | Removed shell execution; the program writes orders using `pathlib` and logs the export. |
| MD5 hash | Security — High (Bandit B324) | Line 47 | MD5 is a weak hash and is unsuitable for security-sensitive use. | Replaced MD5 with SHA-256 for the ticket digest. |
| Non-cryptographic random PIN | Security — Low (Bandit B311) | Line 51 | `random.randint()` is not designed for security-sensitive random values. | Replaced it with `secrets.randbelow()`. |
| Bare `except` and silent failure | Reliability / maintainability (Pylint W0702, Bandit B110, Flake8 E722) | Lines 25–27 | All exceptions were silently ignored, hiding unexpected errors. | Used `orders.pop(table_id, None)` and returned whether an order existed. |
| Mutable default list | Bug / maintainability (Pylint W0102) | Line 15 | A default list is shared between calls. | Changed `order_log=[]` to `order_log=None`; append only when a list is supplied. |
| Unused import and variables | Code quality (Pylint / Flake8) | Multiple | `math`, `service_tax`, `base_bill` (in the original function), and loop variable `t` were unused. | Removed unused imports/variables and simplified pending-order counting. |
| Incorrect comparison to `None` and complex conditional | Style / maintainability | Line 32–36 | `== None` and an if/else return pattern are less clear. | Used `is not None` logic and a direct boolean return. |
| File opened without context manager or encoding | Reliability / style (Pylint W1514, R1732) | Lines 55–56 | The file might not be closed reliably and encoding was unspecified. | Used `Path.open()` in a `with` statement with UTF-8 encoding. |
| Naming, missing docstrings, line length, missing final newline | Style / maintainability (Pylint / Flake8) | Multiple | Several functions used camelCase and lacked documentation; some lines were too long. | Used snake_case names, added docstrings, formatted long lines, and retained a final newline. |
| Hard-coded POS secret printed | Security / secret management | In `main()` | A secret-like value was embedded in the source and printed. | Removed the hard-coded secret and its output. |

## Verification results

- **Program execution:** completed successfully. The sample discounted bill for T1 was `40.50`.
- **Pylint after fixes:** `10.00/10`.
- **Bandit after fixes:** no issues identified.
- **Flake8 after fixes:** empty report, meaning no violations were reported.

The original tool output showed a Pylint score of `4.81/10` and five Bandit findings (two high, one medium, two low). Flake8 reported nine findings. The final reports were generated again after the changes.

**Note:** Line numbers refer to the original version and can differ from the corrected file.
