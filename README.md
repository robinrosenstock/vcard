# Install

```bash
python3 -m venv vcard
source vcard/bin/activate
# optional: upgrade pip
python -m pip install --upgrade pip
# Install requirements:
pip install -r requirements.txt
```

# Usage

## Category diff

```bash
# stdout will contain the matching vCards unless `--out` is provided.
python vcard.py categorydiff CategoryA CategoryB file1.vcf [file2.vcf ...] [--out out.vcf]
```

## Category counts

```bash
# Print category occurrence counts (to stdout by default).
python vcard.py categorycounts file1.vcf [file2.vcf ...]

# Or write counts to a file:
python vcard.py categorycounts file1.vcf [file2.vcf ...] --out counts.txt
```

Note: If no files are provided, the command will print a brief usage hint describing how to supply vCard files.

# Run tests

```bash
pytest -q
```

# run as cli command vcard

Run the CLI command `vcard` from within a Python virtual environment.

1. Install package (editable during development):
   pip install -e .
2. Run:
   vcard --help

Notes
- `pip install -e .` registers the console script defined in pyproject.toml (`vcard = "vcard.vcard:main"`).
- To remove the script, run: `pip uninstall vcard` while the same venv is active.
- If you change entry points or setup, reinstall (`pip install -e .`) to update the script.
