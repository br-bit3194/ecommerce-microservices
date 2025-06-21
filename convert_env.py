# convert_env.py
import os
from pathlib import Path

def convert_env_files(root_dir='.'):
    for path in Path(root_dir).rglob('.env*'):
        try:
            with open(path, 'r', encoding='utf-16') as f:
                content = f.read()

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Converted: {path}")
        except Exception as e:
            print(f"⚠️  Skipped: {path} ({e})")

if __name__ == '__main__':
    convert_env_files()
