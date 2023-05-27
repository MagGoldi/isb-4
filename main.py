import multiprocessing as mp
import logging
import argparse
import json

from functions import searching, luhn, get_stats


logger = logging.getLogger()
logger.setLevel('INFO')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_path', default='files\\data.json',
                        help='Путь к json файлу с данными', action='store')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-f', '--find', help='Поиск номеров карт с заданным хэшем', action='store_true')
    group.add_argument(
        '-c', '--check', help='Проверяет карту на достоверность', action='store_true')
    group.add_argument(
        '-s', '--statistic', help='Вывод зависимости времени выполненя от кол-ва потоков', action='store_true')
    args = parser.parse_args()
    data_path = args.data_path
    try:
        with open(data_path) as jf:
            data = json.load(jf)
    except FileNotFoundError:
        logging.error(f"{data_path} not found")

    if args.find:
        logging.info('Search for the card number...\n')
        searching(data, int(data["processes_amount"]))
        logging.info('Card number search completed')
    elif args.check:
        logging.info('Checking the correctness of the card...')
        luhn(data)
        logging.info('Verification of the cards correctness is completed')
    elif args.statistic:
        logging.info('Data collection...\n')
        get_stats(data)
        logging.info('Вata collection completed\n')
    else:
        logging.error("is something wrong")
