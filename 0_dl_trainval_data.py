"""This script is responsible for processing data using the BinanceProcessor class and saving the results to disk. It
first prints the configuration variables, then processes the data and saves the resulting dataframe, price array,
tech array and time array.

Attributes:
    TICKER_LIST (list): List of tickers to process.
    TECHNICAL_INDICATORS_LIST (list): List of technical indicators to calculate.
    TIMEFRAME (str): Timeframe of the data.
    trade_start_date (str): Start date for trading data.
    trade_end_date (str): End date for trading data.
    no_candles_for_train (int): Number of candles for training.

Functions: main(): main function which runs the script. print_config_variables(): Print the current configuration
variables process_data(): process data using the BinanceProcessor class and return the dataframe, price array,
tech array and time array. save_data_to_disk(data_from_processor, price_array, tech_array, time_array): save the
dataframe, price array, tech array and time array to the specified data folder. _save_to_disk(data, file_path): save
the data to the specified file path

"""

import os
import sys
import pickle

from logbook import Logger, StreamHandler
from config_main import (
    TICKER_LIST,
    TIMEFRAME,
    no_candles_for_train,
    no_candles_for_val,
    TECHNICAL_INDICATORS_LIST,
    TRAIN_START_DATE,
    TRAIN_END_DATE,
    VAL_START_DATE,
    VAL_END_DATE,
    FOLDER_DIR
)
from processor_Binance import BinanceProcessor

StreamHandler(sys.stdout).push_application()
log = Logger('0_dl_trainval_data')

log.info('start logging')
def print_config_variables():
    
    log.info(f'TIMEFRAME : {TIMEFRAME}')
    log.info(f'no_candles_for_train : {no_candles_for_train}')
    log.info(f'no_candles_for_val : {no_candles_for_val}')
    log.info(f'TRAIN_START_DATE : {TRAIN_START_DATE}')
    log.info(f'TRAIN_END_DATE : {TRAIN_END_DATE}')
    log.info(f'VAL_START_DATE : {VAL_START_DATE}' )
    log.info(f'VAL_END_DATE : {VAL_END_DATE}')
    log.info(f'TICKER LIST : {TICKER_LIST}')


def process_data():
    DataProcessor = BinanceProcessor()
    data_from_processor, price_array, tech_array, time_array = DataProcessor.run(
        TICKER_LIST,
        TRAIN_START_DATE,
        VAL_END_DATE,
        TIMEFRAME,
        TECHNICAL_INDICATORS_LIST,
        if_vix=False
    )
    return data_from_processor, price_array, tech_array, time_array


# def save_data(data_folder, data_from_processor, price_array, tech_array, time_array):
#     if not os.path.exists(data_folder):
#         os.makedirs(data_folder, exist_ok=True)

#     with open(data_folder + '/data_from_processor', 'wb') as handle:
#         pickle.dump(data_from_processor, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     with open(data_folder + '/price_array', 'wb') as handle:
#         pickle.dump(price_array, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     with open(data_folder + '/tech_array', 'wb') as handle:
#         pickle.dump(tech_array, handle, protocol=pickle.HIGHEST_PROTOCOL)

#     with open(data_folder + '/time_array', 'wb') as handle:
#         pickle.dump(time_array, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_data_to_disk(data_from_processor, price_array, tech_array, time_array):
    data_folder = f'{FOLDER_DIR}/data/{TIMEFRAME}_{no_candles_for_train + no_candles_for_val}'
    if not os.path.exists(data_folder):
        log.info (f'mkdir: {data_folder}')
        os.makedirs(data_folder, exist_ok=True)
    _save_to_disk(data_from_processor, f"{data_folder}/data_from_processor")
    _save_to_disk(price_array, f"{data_folder}/price_array")
    _save_to_disk(tech_array, f"{data_folder}/tech_array")
    _save_to_disk(time_array, f"{data_folder}/time_array")


def _save_to_disk(data, file_path):
    with open(file_path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    print_config_variables()
    data_from_processor, price_array, tech_array, time_array = process_data()
    save_data_to_disk(data_from_processor, price_array, tech_array, time_array)


if __name__ == "__main__":
    main()
