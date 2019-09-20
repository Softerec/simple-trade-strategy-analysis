# -*- coding: utf-8 -*-

''' Application checks simple trading strategy on historical prices of specific assets.

Prices of specific assets are stored in .csv files (downloaded from yahoo finance).
Each of the csv files contain historical prices of specific equity or fund.

Only one simple trading strategy is tested.
The simple trading strategy test is based on moving averages (SMA 50 and SMA 250).

Simple trading strategy execution:
Purchase is made at the moment when SMA50 cross from the bottom SMA250.
Sell take place when price rise or falls certain percent from the purchase price.

Each transaction is being displayed and the final result of the simple strategy also.  
'''

import os
import csv
import fnmatch


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
    return list_of_file_names


def clean_file_names(list_of_files):
    '''Removes ./ from the begining of the file names in the list of the file names.

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

class bcolors:
    '''To include colors in display of profit or loss transactions.
    Brings effect in windows, does not bring effect in Raspbian.'''

    
    Blue = '\033[94m'
    Green = '\033[92m'
    Red = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.Blue = ''
        self.Green = ''
        self.Red = ''
        self.ENDC = ''


def load_data_from_csv(file):
    '''Loads required data from given csv file to data structure for later usage in simulation of trading strategy.
    
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
            transaction=['Day:',transaction_day, ' Purchase price ', purchase_price]
            print(transaction)
            transactions.append(transaction)

        previous_sma50 = sma50
        previous_sma250 = sma250

        if (transaction_on == 1): # included only when previous transaction was purchase
            result_in_the_day = round(((row_of_numbers2[1] - purchase_price ) / purchase_price),4)

            if ((result_in_the_day > sell_percent_profit) & transaction_on): # condition if assumed profit reached
                profit_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=['Day:', transaction_day, ' Profit sell price', profit_sell_price, 'result: ', result_in_the_day]
                print(transaction)
                print(bcolors.Green + ' Gain' + bcolors.ENDC)
                transactions.append(transaction)
                transaction_on = 0
                final_result = final_result + result_in_the_day

            if ((result_in_the_day < sell_percent_loss) & transaction_on & (result_in_the_day != 0)): # if trade loss
                loss_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=['Day:', transaction_day, ' Loss sell price', loss_sell_price, 'result: ', result_in_the_day]
                print(transaction)
                print(bcolors.Red + ' Loss' + bcolors.ENDC)
                transactions.append(transaction)
                transaction_on = 0
                final_result = final_result + result_in_the_day

    return final_result


def main():

    # File names filter for search.
    file_name_pattern = "*.csv"

    # Defines initial path for files as local. r(raw) is to handle spaces in folder and file names.
    search_path = r"." 

    #  Find files as per specified file mask and under specified folder
    files_list =  find_file_names(file_name_pattern, search_path)
    print(files_list)

    #files_list = clean_file_names(files_list)
    print(files_list)

    files=[]
    files=files_list
    
    file_counter = 0

    # Repeats same simulation for all csv files included in the file list.
    for file_counter in range(0,len(files)):

        file = files[file_counter]

        # At the begining of file analysis the file name is displayed.
        print ('\nFile for analysis:', file)
        
        # loads necessary data from the csv file to dedicated data structure containing required numbers
        list_of_numbers = load_data_from_csv(file)
        
        final_result = trading_strategy_sim(list_of_numbers, 0.05, -0.05)
        
        print('-----> Final result of',file,'analysis is:', round(final_result*100, 4),'%')

    print('\n\n>End of the execution.<')
    


if __name__ == "__main__":
    main()

