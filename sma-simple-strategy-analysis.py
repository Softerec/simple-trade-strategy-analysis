# -*- coding: utf-8 -*-
''' Application checks simple trading strategy on historical prices of specific assets.

Prices of specific assets are taken from .csv files (downloaded from yahoo finance).
Each csv file contains historical prices of specific equity or fund.

A simple trading strategy is based on moving averages (SMA 50 and SMA 250) is tested.

Simple trading strategy execution:
Purchase is made at the moment when SMA50 cross from the bottom SMA250.
Sell take place when price rises or falls certain percent from the purchase price.

Each transaction is being displayed and the final outcome of the strategy (in %).

Written in 2017 in Windows 7 and checked later in Widnows 10.
'''

import os
import csv
import fnmatch

# True execute tests only for first 3 found csv files
in_development = False


def find_file_names(pattern, path):
    '''In given location, search for all file names per given file name pattern.

    Parameters
    pattern: string type, an example '*.csv'
    path: (row) string type, an example r'.'

    Returns
    list_of_file_names: list of file names fullfiling the criteria of path and pattern
    '''
    
    list_of_file_names = []
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                list_of_file_names.append(os.path.join(root, name))

            # Below condition is used in development to skip inputs and reduce running time.
            if in_development:
                if len(list_of_file_names) > 3:
                    return list_of_file_names
                    break

    return list_of_file_names


def load_data_from_csv(file):
    '''Loads required data from given csv file to structure for simulation of trading strategy.
    
    Parameters
    file: a name of csv file located in the same diretory as the script

    Returns
    list_of_numbers : list of specific data extracted used later for simulation of traiding strategy
    '''
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        list = []
        for row in readCSV: #puts values from the csv file into the list
            list.append(row)

        row_of_numbers = []
        list_of_numbers = []
        counter2=1
        for counter1 in range(1, len(list)):
            for x in range(1, 7): 
                row_of_text=list[counter2] # insert the row from list into row_of_text
                row_of_numbers.insert(x, float(row_of_text[x])) # insert numbers from row_of_text to row_of_numbers
            list_of_numbers.insert(counter2, row_of_numbers) # put row_of_numbers into the list of numbers
            counter2=counter2+1
            row_of_text=[]
            row_of_numbers=[]

    return list_of_numbers


def trading_strategy_sim(list_of_numbers, sell_percent_profit, sell_percent_loss):
    '''Executes the training stratedy on historical price data.
    
    Parameters:
    list_of_numbers: dedicated data structure, (rdata structure returned by load_data_from_csv()).
    sell_percent_profit: positive value (from: 0.01 to 1.00, where 1 corresponds to 100%),
        defines limit when sell is executed with profit, example: given 0.05 , means sell when profit more than 5%.
    sell_percent_loss: negative value (from: -0.99 to -0.01, where -0.5 corresponds to -50%),
        defines limit when sell is executed with loss, example: given -0.02, means sell when loss is more than -2%.

    Returns:
    final_result: final result of executed strategy from whole period (timeperiod as per input csv file).
    
    During execution:
    Displays purchase & sell moments during execution of traiding simulation, does it according to defined rules and boundaries.
    - buy when sma50 cross from the bottom sma250; sell: when price increase of given % or price decrease of given %
        (see parameters: sell_percent_profit and sell_percent_loss).
    '''
    
    transaction_on = 0 # flag used to detect that purchase was the last transaction
    transactions = []
    transaction = ['Transaction day, action, price/profit/loss, result in percentage']
    transactions.append(transaction)
    previous_sma250 = 0.01
    previous_sma50 = 0.1
    purchase_price = 1
    final_result = 0
    for counter2 in range(0,len(list_of_numbers)-250):
        sum250=0
        sum50=0
        row_of_numbers=[]
        row_of_numbers2=list_of_numbers[counter2+250] # the day when sma250 is being counted is after 250 day

        for counter1 in range(0,250):
            row_of_numbers=list_of_numbers[counter1+counter2]
            sum250=sum250+row_of_numbers[1] # one day price is included in sum of 250
            if counter1 > 199: # sma50 is counted of last 50 days of counting sma250
                sum50=sum50+row_of_numbers[1]
        sma250=sum250/250 #sma250 - the simple moving average of 250 trainding days
        sma50=sum50/50

        if (sma50 > sma250) & (not transaction_on) & (previous_sma50 < previous_sma250): # condition to purchase
            transaction_on = 1 # flag informs that the last transaction was purchase
            purchase_price = row_of_numbers2[1]
            transaction_day = counter2+250
            transaction=[transaction_day, purchase_price]
            print('Day: {0}. Purchase price: {1}'.format(transaction[0],transaction[1]))
            transactions.append(transaction)

        previous_sma50 = sma50
        previous_sma250 = sma250

        if (transaction_on == 1): # included only when previous transaction was purchase
            result_in_the_day = round(((row_of_numbers2[1] - purchase_price ) / purchase_price),4)

            if ((result_in_the_day > sell_percent_profit) & transaction_on): # condition if assumed profit reached
                profit_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=[transaction_day, profit_sell_price, result_in_the_day]
                print('Day: {0}. Profit sell price: {1}. The result: {2} , GAIN.'.format(transaction[0], transaction[1], transaction[2]))
                transactions.append(transaction)
                transaction_on = 0
                final_result = final_result + result_in_the_day

            if ((result_in_the_day < sell_percent_loss) & transaction_on & (result_in_the_day != 0)): # if trade loss
                loss_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=[transaction_day, loss_sell_price, result_in_the_day]
                print('Day: {0}. Loss sell price: {1}. The result: {2} , LOSS.'.format(transaction[0], transaction[1], transaction[2]))
                transactions.append(transaction)
                transaction_on = 0
                final_result = final_result + result_in_the_day

    return final_result


def clean_file_names(list_of_files):
    '''Needed when running in Raspian, not needed and not used in Windows.
    Removes ./ from the begining of the file names in the list of the file names.

    Parameters
    list_of_files: list of names of files with extension, example file name in the list: './yahoo.csv'.

    Returns
    cleaned_list: cleaned list of names of files with extension, example file name in the list: 'yahoo.csv'.
    '''
    
    cleaned_list=[]
    
    for file_name in list_of_files:
        if file_name[0] == '.':
            file_name = file_name[1:]
            if file_name[0] == '/':
                file_name = file_name[1:]
        cleaned_list.append(file_name)

    return cleaned_list


def main():
    # File names filter for search.
    file_name_pattern = "*.csv"

    # Defines initial path for files as local. r(raw) is to handle spaces in folder and file names.
    search_path = r"." 

    #  Find files as per specified file mask and under specified folder
    files_list =  find_file_names(file_name_pattern, search_path)

    if len(files_list) > 0:
        print("\nFound below csv files for analysis:")
    else:
        print("\n\nNot found any csv files for analysis. \nApplication ends.")
        exit()

    for csv_file_name in files_list:
        print('\t' + csv_file_name[2:])

    #In Raspian, uncomment below line
    #files_list = clean_file_names(files_list)

    
    file_counter = 0
    instruments_results=dict()

    # executes traiding simulation for all csv files included in the files list.
    for file_counter in range(0,len(files_list)):

        file = files_list[file_counter]

        # At the begining of file analysis the file name is displayed.
        print ('\nFile for analysis:', file)
        
        # loads necessary data from the csv file to dedicated data structure containing required numbers
        list_of_numbers = load_data_from_csv(file)
        
        final_result = trading_strategy_sim(list_of_numbers, 0.05, -0.05)
        
        print('\n--> STRATEGY TESTING OF',file[2:],'BRINGS RESULT OF', round(final_result*100, 4),'%')
        instruments_results[file] = round(final_result*100, 4)

    print('\nBELOW, OVERVIEW OF THE TRAINDING STRATEGY RESULTS FOR EACH INSTRUMENT:')

    max_lenght_file_name = 0
    for i in instruments_results:
        if max_lenght_file_name < len(i):
            max_lenght_file_name = len(i)

    result_sum = 0
    for instrument in instruments_results.keys():
        result_display_shift = max_lenght_file_name - len(instrument)
        display_result = instruments_results[instrument]
        space = ' '
        print(f'Instrument {instrument[2:(len(instrument)-4)]} {space*result_display_shift} {display_result:>8.2f} %')
        result_sum = instruments_results[instrument]
    average_result = result_sum / len(instruments_results)
    print(f'\nAverage result for all periods is: {average_result:>8.2f} %')
    print('\nAppication end.')
    

if __name__ == "__main__":
    main()
