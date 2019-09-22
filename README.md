# simple-trade-strategy-analysis
Written for Windows, Python 3.7, 2017.

Script to analyse very simple trading strategy against historical data of particular equity.

Script reads .csv files (downloaded from yahoo finance).
Each file contains historical prices of specific equity or fund.
Data read from file is used to analyze simple trading strategy (simulation on historical prices).

Simulation of simple trading strategy is based on moving averages (50 and 250).
Purchase is made at the moment when shorter moving average cross from the bottom the longer moving average.
Selling take place when price rise or falls certain percent from the purchase price.
( in this software initial limits are: profit when +5% reached, loss when -5% )

Transactions are displayed and result of the executed strategy is displayed.
(When run in Windows then message "Gain" is shown in green, message "Loss" is shown in red.)
