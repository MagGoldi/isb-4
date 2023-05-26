import logging
import argparse
import json


logger = logging.getLogger()
logger.setLevel('INFO')


SETTINGS_FILE = 'files/settings.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_path', default='files\\base.json',
                        help='Путь к json файлу с данными', action='store')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument()
    args = parser.parse_args()
    base_path = args.base_path
    try:
        with open(base_path) as jf:
            init = json.load(jf)
    except FileNotFoundError:
        logging.error(f"{base_path} not found")

    match mode:
        case ():
            pass
        case ():
            pass
        case ():
            pass
        case:
            pass
