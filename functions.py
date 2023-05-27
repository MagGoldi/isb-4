import hashlib
import json
import logging
import multiprocessing as mp
from functools import partial
from time import time
from tqdm import tqdm
from matplotlib import pyplot as plt


def luhn(data: dict) -> bool:
    """
    Checks the number for correctness by the luhn algorithm

    Args:
    data(dict): input data
    Return:
    (bool): True if everything came together, otherwise - False
    """
    try:
        with open(data["found_card"]) as f:
            found_card = json.load(f)
    except FileNotFoundError:
        logging.error(f"{data['found_card']} not found")
    number = str(found_card["card_number"])
    if not number.isdigit() or len(number) != 16:
        logging.info("The card is incorrect")
        return False

    checksum = 0
    for i, digit in enumerate(reversed(number)):
        if i % 2 == 0:
            checksum += int(digit)
        else:
            checksum += sum(divmod(int(digit) * 2, 10))

    if checksum % 10 == 0:
        logging.info("The card is correct")
        return True
    else:
        logging.info("The card is incorrect")
        return False


def checking_hash(bin: int, data: dict, number: int) -> int:
    """
    Compares the hash of the received card with an existing one

    args:
    bin(int): the first 6 digits card's
    data(dict): input data
    number(int): generated card digits
    return:
    (int): number, if the hash matches, otherwise False
    """
    if hashlib.sha3_256(f'{bin}{number:06d}{data["last_digits"]}'.encode()).hexdigest() == f'{data["hash"]}':
        return int(f'{bin}{number:06d}{data["last_digits"]}')
    else:
        return False


def searching(data: dict, processes: int):
    """
    Is looking for a card with the same hash

    args:
    data(dict): input data
    processes(int): number of processes
    """
    flag = False
    with mp.Pool(processes) as p:
        for bin in data['first_digits']:
            logging.info(
                f'Search for a hash for a card {bin[:4]}-{bin[-2:]}XX-XXXX-{data["last_digits"]}')
            for result in p.map(partial(checking_hash, int(bin), data), tqdm(range(1000000))):
                if result:
                    p.terminate()
                    flag = True
                    logging.info(
                        f'The found card is on the way{data["found_card"]}')
                    result_str = str(result)
                    logging.info(
                        f'The found card {result_str[:4]}-{result_str[4:8]}-{result_str[8:12]}-{result_str[12:]}')
                    data_tmp = {}
                    data_tmp["card_number"] = f"{result}"
                    data_tmp["luhn_check"] = None
                    try:
                        with open(data["found_card"], 'w') as f:
                            json.dump(data_tmp, f)
                    except FileNotFoundError:
                        logging.error(f"{data['found_card']} not found")
                    break
            if flag == True:
                break
    if flag == False:
        logging.info('Card not found')


def get_stats(data: dict):
    """
    Preserves the dependence of the hash collision search time on the number of processes
    args:
    data(dict): input data
    """
    times = []
    for i in range(int(data["processes_amount"])):
        start = time()
        logging.info(f'number of processes: {i+1}\n')
        searching(data, i+1)
        times.append(time()-start)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Time')
    plt.xlabel('Processes')
    plt.title('Time dependence on the number of processes')
    plt.plot(
        list(x+1 for x in range(int(data["processes_amount"]))), times, color="orange")
    plt.savefig(f'{data["statistic_path"]}')
    logging.info(
        f'Time dependence on processes is preserved along the way {data["statistic_path"]}\n')
