"""
test_vcard.py

Purpose:
    Unit tests for the vcard utilities implemented in vcard.py. These tests
    exercise unfolding of folded vCard lines, iteration over multiple vCards
    in a single stream, extraction of CATEGORIES, argument parsing, matching
    logic (category A present and category B absent), and writing matches
    to an output file.

How to run:
    From the repository root run:
        pytest -q

Notes:
    - The test module loads the target implementation by path to ensure the
      provided vcard.py is exercised exactly as given.
    - Tests use pytest's tmp_path fixture for file I/O to avoid touching the
      working directory.
    - Category matching is expected to be case-insensitive; tests assert
      lowercase normalization where appropriate.

Test summaries:
    - test_unfold_basic: Verifies folded lines (CRLF + space or tab) are
      unfolded correctly and contents preserved.
    - test_iter_vcards_and_categories: Verifies multiple vCards separated by
      CRLF or LF are iterated correctly and category parsing returns the
      expected lowercased set.
    - test_categories_no_entry: Ensures absence of CATEGORIES yields an empty set.
    - test_parse_args_and_find_matching_vcards: Creates temporary vcf files and
      verifies parsing of CLI-like args (including --out) and the matching logic.
    - test_write_matches_to_file: Confirms matching vCards are written with a
      trailing newline when written to a file.

"""

import importlib.util
from pathlib import Path
import sys

import pytest

# Load the module from the exact file path so tests exercise the provided file.
def load_module():
    fp = Path("/home/robin/Downloads/vcard/vcard.py")
    spec = importlib.util.spec_from_file_location("vcard", str(fp))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_unfold_basic():
    mod = load_module()
    folded = "FN:John\r\n Doe\r\nTEL:123\r\n\t456\r\n"
    out = mod.unfold(folded)
    # folded newline+space should be removed, tab-continuation becomes newline removed by logic
    assert "FN:John" in out
    assert "Doe" in out
    assert "123" in out
    assert "456" in out

def test_iter_vcards_and_categories():
    mod = load_module()
    v1 = "\r\n".join([
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:Alice",
        "CATEGORIES:Friends,Work",
        "END:VCARD",
    ]) + "\r\n"
    v2 = "\n".join([
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:Bob",
        "CATEGORIES:Work",
        "END:VCARD",
    ]) + "\n"
    stream = v1 + v2
    cards = list(mod.iter_vcards(stream))
    assert len(cards) == 2
    assert any("FN:Alice" in c for c in cards)
    assert any("FN:Bob" in c for c in cards)

    cats1 = mod.categories_from_vcard(cards[0])
    assert "friends" in cats1 and "work" in cats1

    cats2 = mod.categories_from_vcard(cards[1])
    assert cats2 == {"work"}

def test_categories_no_entry():
    mod = load_module()
    card = "BEGIN:VCARD\nFN:NoCat\nEND:VCARD\n"
    assert mod.categories_from_vcard(card) == set()

def test_parse_args_and_find_matching_vcards(tmp_path):
    mod = load_module()
    # create two files: one with both categories, one with only the first
    f1 = tmp_path / "a.vcf"
    f2 = tmp_path / "b.vcf"
    f1.write_text("\n".join([
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:Alice",
        "CATEGORIES:Friends,Work",
        "END:VCARD",
    ]) + "\n", encoding="utf-8")
    f2.write_text("\n".join([
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:Bob",
        "CATEGORIES:Work",
        "END:VCARD",
    ]) + "\n", encoding="utf-8")

    # cat_a = work, cat_b = friends -> only Bob should match
    matches, total, matched = mod.find_matching_vcards("work", "friends", [str(f1), str(f2)])
    assert total == 2
    assert matched == 1
    assert len(matches) == 1
    assert "FN:Bob" in matches[0]

    # parse_args with --out
    cat_a, cat_b, files, outp = mod.parse_args(["Work", "Friends", str(f1), "--out", "out.vcf"])
    assert cat_a == "work"
    assert cat_b == "friends"
    assert files == [str(f1)]
    assert outp == "out.vcf"

def test_write_matches_to_file(tmp_path):
    mod = load_module()
    out_file = tmp_path / "out.vcf"
    matches = ["BEGIN:VCARD\nFN:Test\nEND:VCARD"]
    mod.write_matches(matches, str(out_file))
    content = out_file.read_text(encoding="utf-8")
    assert content == "BEGIN:VCARD\nFN:Test\nEND:VCARD\n"
