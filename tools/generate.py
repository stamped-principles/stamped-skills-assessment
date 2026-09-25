"""Export record JSON Schemas from the canonical LinkML model."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src/stamped_assessment/data'
CLASSES = {'use_case': 'UseCase', 'object': 'ObjectRecord', 'rubric': 'Rubric',
           'assessment': 'Assessment', 'review': 'Review'}

def main():
    output = DATA / 'generated'
    output.mkdir(exist_ok=True)
    for kind, name in CLASSES.items():
        result = subprocess.run([
            str(Path(sys.executable).with_name('gen-json-schema')),
            '--closed', '--top-class', name, str(DATA / 'schemas/assessment.yaml'),
        ], check=True, text=True, capture_output=True)
        (output / f'{kind}.schema.json').write_text(result.stdout.rstrip() + '\n')

if __name__ == '__main__':
    main()
