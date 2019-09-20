# simple-trade-strategy-analysis
Written in Python 3.7
Simple software to analyse very simple trading strategy against historical data of particular equity.

This piece of software reads .csv files (downloaded from yahoo finance).
Each of files contain historical prices of specific equity or fund.
Data read from file is used to analyze simple trading strategy (tested on historical prices).
First test of simple trading strategy(so far the only one test) is based on moving averages (50 and 250).
Purchase is made at the moment when shorter moving average cross from the bottom the longer moving average.
Selling take place when price rise or falls certain percent from the purchase price.
( in this software initial limits are: profit when +5% reached, loss when -5% )
Transactions are displayed and result of the simple strategy tested is displayed.

(When run in Windows then message "Gain" is shown in green, message "Loss" is shown in red.)
