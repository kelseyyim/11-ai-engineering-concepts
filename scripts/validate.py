#!/usr/bin/env python3
"""Run the entire offline check suite with the current Python interpreter."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
    ['scripts/check_content.py'],
    ['scripts/check_links.py'],
    ['scripts/render_readme.py', '--check'],
    ['examples/ollama_chat.py'],
    ['examples/bedrock_chat.py'],
    ['examples/bounded_agent.py'],
    ['examples/bounded_agent.py', '--eval'],
    ['-m', 'compileall', '-q', 'examples', 'scripts', 'tests'],
]

if __name__ == '__main__':
    for command in COMMANDS:
        print('+', sys.executable, *command, flush=True)
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True, timeout=120)
    print('All offline checks passed. No live model or AWS integration was tested.')
