# 2017
# This piece of software reads .csv files (downloaded from yahoo finance).
# Each of the files contain historical prices of specific equity or fund.
# Data read from file is used to analyze simple trading strategy (tested on historical prices).
# First test of simple trading strategy(so far the only one test) is based on moving averages (50 and 250).
# Purchase is made at the moment when shorter moving average cross from the bottom the longer moving average.
# Selling take place when price rise or falls certain percent from the purchase price.
# ( in this software assumed limits are: profit when +5% reached, loss when -2% )
# Transactions are displayed and result of the simple strategy tested is displayed.

class bcolors: # only for colors of profit or loss later (not functional logic)
    Blue = '\033[94m'
    Green = '\033[92m'
    Red = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):  # only for colors of profit or loss later (not functional logic)
        self.Blue = ''
        self.Green = ''
        self.Red = ''
        self.ENDC = ''

# Beginning of the functional logic

# Below downloaded files from yahoo finance
file1 = 'ADI Analog Devices.csv'
file2 = 'Apple Inc.csv'
file3 = 'Bank of America Corporation.csv'
file4 = 'yahoo.csv'
file5 = 'CAT.csv'
file6 = 'chevron.csv'
file7 = 'DJI_Dow 30.csv'
file9 = 'GOLD Randgold Resources Limited.csv'
file10 = 'GSPC S&P 500.csv'
file11 = 'Halliburton Company.csv'
file12 = 'IXIC Nasdaq .csv'
file13 = 'Microsoft Corporation.csv'
file14 = 'NASDAQ Composite.csv'
file15 = 'NRCIB National Research Corporation.csv'
file16 = 'PRGO Perrigo Company.csv'
file17 = 'S&P 100 INDEX.csv'
file18 = 'S&P 500.csv'
file19 = 'S&P MID CAP 400 INDEX.csv'
file20 = 'SCON Superconductor Technologie.csv'
file21 = 'SYT Syngenta AG.csv'
file21 = 'VelocityShares 3x Long Crude Oil ETN.csv'
file22 = 'XOMA Corporation.csv'

files=[]
#list of files
files=[file1, file2, file3, file4, file5, file6, file7]#, file22 ]
file_counter=0

for file_counter in range(0,len(files)): #execute the same analysis for files included in the file list
    file=files[file_counter]
    print ('\nFile for analysis:', file) #on the begining of file analysis the file name is displayed

    import csv
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        list = []
        for row in readCSV: #puts values from the csv file into the list
            list.append(row)

        row_of_numbers = []
        list_of_numbers = []
        counter2=1
        for counter1 in range(1,len(list)):
            for x in range(1, 7): 
                row_of_text=list[counter2] # insert the row from list into row_of_text
                row_of_numbers.insert(x,float(row_of_text[x])) # insert numbers from row_of_text to row_of_numbers
            list_of_numbers.insert(counter2,row_of_numbers) # put row_of_numbers into the list of numbers
            counter2=counter2+1
            row_of_text=[]
            row_of_numbers=[]

    transaction_not_on = 1 # flag used to detect that purchase was not the last transaction
    transaction_on = 0 # flag used to detect that purchase was the last transaction
    transactions = []
    transaction = ['Transaction day, action, price/profit/loss, result in percentage']
    transactions.append(transaction)
    old_sma250 = 0.01
    old_sma50 = 0.1
    purchase_price = 1
    sell_percent_profit = 0.05 # value (in percentage 1 = 100%) when sell is done with profit
    sell_percent_loss = -0.02 # value (in percentage -1 = -100%) when sell is done with profit
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
        #print('sma250', sma250)
        #print('sma50', sma50)

        if (sma50 > sma250) & transaction_not_on & (old_sma50 < old_sma250): # condition to purchase
            transaction_not_on = 0
            transaction_on = 1 # flag informs that the last transaction was purchase
            purchase_price = row_of_numbers2[1]
            transaction_day = counter2+250
            transaction=['Day:',transaction_day, ' Purchase price ', purchase_price]
            print(transaction)
            transactions.append(transaction)

        old_sma50 = sma50
        old_sma250 = sma250

        if (transaction_on == 1): # included only when previous transaction was purchase
            result_in_the_day = round(((row_of_numbers2[1] - purchase_price ) / purchase_price),4)

            if ((result_in_the_day > sell_percent_profit) & transaction_on): # condition if assumed profit reached
                profit_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=['Day:', transaction_day, ' Profit sell price',profit_sell_price, 'result: ',result_in_the_day]
                print(transaction)
                print(bcolors.Green + ' Gain' + bcolors.ENDC)
                transactions.append(transaction)
                transaction_not_on = 1
                transaction_on = 0
                final_result = final_result + result_in_the_day

            if ((result_in_the_day < sell_percent_loss) & transaction_on & (result_in_the_day != 0)): # if trade loss
                loss_sell_price = row_of_numbers2[1]
                transaction_day = counter2+250
                transaction=['Day:', transaction_day, ' Loss sell price', loss_sell_price, 'result: ',result_in_the_day]
                print(transaction)
                print(bcolors.Red + ' Loss' + bcolors.ENDC)
                transactions.append(transaction)
                transaction_not_on = 1
                transaction_on = 0
                final_result = final_result + result_in_the_day

    #for print_index in range(0,len(transactions)):
    #    print(transactions[print_index])
    print('-----> Final result of',file,'analysis is:', round(final_result*100,4),'%')

print('>END<')