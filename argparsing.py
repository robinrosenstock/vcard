#!/usr/bin/env python3
import argparse

__all__ = ["build_parser", "parse_args"]

def parse_args(argv):
    """Parse command line arguments (legacy helper).

    This mirrors the previous simple parse_args helper used elsewhere.
    """
    if len(argv) < 3:
        print("Usage: vcard.py CategoryA CategoryB file1.vcf [file2.vcf ...] [--out out.vcf]")
        raise SystemExit(2)

    args = list(argv)
    out_path = None
    if "--out" in args:
        i = args.index("--out")
        if i == len(args) - 1:
            print("Provide output filename after --out")
            raise SystemExit(2)
        out_path = args[i+1]
        args = args[:i] + args[i+2:]

    cat_a = args[0].lower()
    cat_b = args[1].lower()
    files = args[2:]
    return cat_a, cat_b, files, out_path

def build_parser():
    """Construct and return the top-level argparse.ArgumentParser for this CLI."""
    parser = argparse.ArgumentParser(prog="vcard.py", description="vCard utilities")
    parser.add_argument("--version", action="version", version="0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # categorydiff subcommand
    p_diff = subparsers.add_parser("categorydiff", help="Output vCards that have CategoryA but not CategoryB")
    p_diff.add_argument("category_a")
    p_diff.add_argument("category_b")
    p_diff.add_argument("files", nargs="+", help="One or more .vcf files")
    p_diff.add_argument("--out", "-o", dest="out", help="Write matches to file (default stdout)")

    # categorycontacts subcommand
    p_contacts = subparsers.add_parser("categorycontacts", help="Output vCards that have the specified category(ies)")
    p_contacts.add_argument("category", nargs="+", help="One or more category names (comma/semicolon allowed in a single argument)")
    p_contacts.add_argument("files", nargs="+", help="One or more .vcf files")
    p_contacts.add_argument("--name", action="store_true", dest="name", help="Output only the contact name(s) instead of full vCard")
    p_contacts.add_argument("--number", action="store_true", dest="number", help="Output only telephone number(s) instead of full vCard")
    p_contacts.add_argument("--out", "-o", dest="out", help="Write matches to file (default stdout)")

    # categorycontacts_all subcommand (logical AND)
    p_contacts_all = subparsers.add_parser("categorycontacts_all", help="Output vCards that have all specified categories")
    p_contacts_all.add_argument("category", nargs="+", help="One or more category names (comma/semicolon allowed in a single argument)")
    p_contacts_all.add_argument("files", nargs="+", help="One or more .vcf files")
    p_contacts_all.add_argument("--name", action="store_true", dest="name", help="Output only the contact name(s) instead of full vCard")
    p_contacts_all.add_argument("--number", action="store_true", dest="number", help="Output only telephone number(s) instead of full vCard")
    p_contacts_all.add_argument("--out", "-o", dest="out", help="Write matches to file (default stdout)")

    # categorycounts subcommand
    p_counts = subparsers.add_parser("categorycounts", help="Compute/print category occurrence counts")
    p_counts.add_argument("files", nargs="*", help="Optional .vcf files to compute counts from")
    p_counts.add_argument("--out", "-o", dest="out", help="Write counts to file (default stdout)")

    return parser
