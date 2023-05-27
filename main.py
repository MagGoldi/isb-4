import multiprocessing as mp
import logging
import argparse
import json


logger = logging.getLogger()
logger.setLevel('INFO')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_path', default='files\\base.json',
                        help='Путь к json файлу с данными', action='store')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-f', '--find', help='Поиск номеров карт с заданным хэшем', action='store_true')
    group.add_argument(
        '-c', '--check', help='Проверяет карту на достоверность', action='store_true')
    group.add_argument(
        '-s', '--statistic', help='Вывод зависимости времени выполненя от кол-ва потоков', action='store_true')
    group.add_argument()
    args = parser.parse_args()
    data_path = args.data_path
    try:
        with open(data_path) as jf:
            data = json.load(jf)
    except FileNotFoundError:
        logging.error(f"{data_path} not found")

    if args.find:
        pass
    elif args.cheak:
        pass
    elif args.statistic:
        pass
