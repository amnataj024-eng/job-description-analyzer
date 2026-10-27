"""Command-line test (no UI):  python main.py sample_jd.txt"""
import json
import sys

from graph import run_analysis

if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else ""
    result = run_analysis(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
