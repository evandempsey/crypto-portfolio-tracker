# crypto-portfolio-tracker
A command line crypto portfolio tracker

## Usage

```
python cash.py holdings.csv --symbol=EUR
``` 

## Holdings format

The holdings file is a CSV with no header where the first column is the name
of the coin in the format returned by the Coinmarketcap.com API and the second
column is the quantity held.

Here is an example:

```
bitcoin,3.556
bitcoin-cash,0.80515495
litecoin,1.555
ethereum,78.322
```
