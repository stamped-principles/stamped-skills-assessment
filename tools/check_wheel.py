"""Exercise the built wheel outside the source checkout."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
wheel = sorted((root / 'dist').glob('*.whl'))[-1]
with tempfile.TemporaryDirectory(prefix='stamped-wheel-') as temp:
    base = Path(temp)
    subprocess.run([sys.executable, '-m', 'venv', str(base / 'env')], check=True)
    python = base / 'env/bin/python'
    subprocess.run([str(python), '-m', 'pip', 'install', str(wheel)], check=True, cwd=base)
    shutil.copytree(root / 'records', base / 'records')
    cli = base / 'env/bin/stamped-assess'
    for command in ('validate', 'summarize', 'review-report'):
        subprocess.run([str(cli), command, 'records'], check=True, cwd=base)
