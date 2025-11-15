# Installation and virtual environment (venv)

Purpose:
- Quick steps to create a virtual environment named `vcard`, install packages, run tests, and run the vcard tool.

Prerequisites:
- Python 3.8+ installed and on PATH.
- pip available.

1) Create and activate a virtual environment named `vcard`
    python3 -m venv vcard
    source vcard/bin/activate

2) Upgrade pip (recommended)
    python -m pip install --upgrade pip

3) Install requirements
- If the repository contains requirements.txt:
    pip install -r requirements.txt
- If there is no requirements file, install the testing tool:
    pip install pytest

4) Run tests
    pytest -q

5) Run the vcard script
- Example:
    python vcard.py CategoryA CategoryB file1.vcf [file2.vcf ...] [--out out.vcf]
- stdout will contain the matching vCards unless `--out` is provided.

6) Create/refresh requirements.txt (optional)
    pip freeze > requirements.txt

Troubleshooting
- If `python -m venv` is missing, install the venv support or use virtualenv:
    python -m pip install virtualenv
- If activation fails on PowerShell, you may need to adjust execution policy:
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Notes
- Tests and file I/O assume UTF-8; ensure files are encoded accordingly.
- The repository's tests load vcard.py by path to ensure the provided implementation is used.
