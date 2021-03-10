import argparse
import json
import sys
from pathlib import Path

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('source', help='The source yaml configuration file')
parser.add_argument('target', help='The directory path to create beta1.cfg in, or a file path can be specified to create/overwrite the cfg file at the location.')
args = parser.parse_args()

try:
    source_file = open(args.source, 'r')
except IOError:
    print(f"Error: Failed to access source yaml file: {args.source}")
    sys.exit(1)

try:
    target_file_path = Path(args.target)
    if target_file_path.is_dir():
        target_file = open(f'{args.target}/beta1.cfg', 'w')
    else:
        target_file = open(args.target, 'w')
except IOError:
    print(f"Error: Failed to open/create target cfg file with write access: {args.target}")
    sys.exit(1)

blocks = yaml.load(source_file, Loader=yaml.FullLoader)
for x in blocks:
    # assumption is we only care about things that are dictionary for env variables
    if x.get('op') == 'add' and type(x['value']) is dict:
        name = x['value']['name']
        value = x['value']['value']

        try:
            value = json.loads(value)
        except:
            pass

        if isinstance(value, str):
            value = '"' + value + '"'

        print(f'{name}={value}', file=target_file)

source_file.close()
target_file.close()
