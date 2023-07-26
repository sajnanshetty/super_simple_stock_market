# Simple Stock Market
Example Assignment – Super Simple Stock Market

## Requirements
Provide working source code that will :-

- For a given stock, 
    - Given any price as input, calculate the dividend yield
    - Given any price as input, calculate the P/E Ratio
    - Record a trade, with timestamp, quantity of shares, buy or sell indicator and
traded price
    - Calculate Volume Weighted Stock Price based on trades in past 15 minutes
- Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

## Constraints & Notes

1.	Written in one of these languages:
        - Java, C#, C++, Python

2.	No database or GUI is required, all data need only be held in memory

3. No prior knowledge of stock markets or trading is required – all formulas are provided.

## Table1. Sample data from the Global Beverage Corporation Exchange

Stock Symbol  | Type | Last Dividend | Fixed Dividend | Par Value
------------- | ---- | ------------: | :------------: | --------: 
TEA           | Common    | 0  |    | 100
POP           | Common    | 8  |    | 100
ALE           | Common    | 23 |    | 60
GIN           | Preferred | 8  | 2% | 100
JOE           | Common    | 13 |    | 250

All number values in pennies


## Requirements

- Python 3

## Run

The code for super simple Stock exercises under package plugins module stock_service.py class SuperSimpleStock. 
```
python stock_service.py
```

### Console window

Input required on console window:

```
Select a number for corresponding operation for a given a Stock:
    ==============================================================================================
    1 Given any price as input, calculates the dividend yield
    2 Given any price as input, calculates the P/E Ratio
    3 Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
    4 Calculates Volume Weighted Stock Price based on trades in past 15 minutes
    5 Calculatesthe GBCE All Share Index using the geometric mean of prices for all stocks
    0 To exit, if you are done with all the operations.
    ==============================================================================================
```

Choose the option according to the need.


## Tests

tests suits are in tests/test_stock_service.py to run it

```
python -m unittest tests.test_stock_service
```
or
```
python run_tests.py
```

Note: Unit tests are executed in the GitHub workflow for any pull request or push to the repository.

## Author

Sajna N Shetty


