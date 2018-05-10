"""
Utility to print cryptocurrency exchange rates on the command line.
"""
import argparse
import requests


def get_quotes_from_api(symbol):
    """
    Makes a request to coinmarketcap.com for latest crypto rates.
    """
    return requests.get(
        "https://api.coinmarketcap.com/v1"
        "/ticker/?convert={0}&limit=1500".format(symbol)
    ).json()


def read_currencies(filename):
    """
    Reads the currencies we are interested in from a file.
    """
    with open(filename) as f:
        return {c.split(",")[0]: float(c.split(",")[1]) 
                for c in f.read().splitlines()
                if c.strip()}


def print_header(currency_symbol):
    """
    Prints the table headers in colour.
    """
    print("\033[1;32;40m")
    print("{0:10}{1:15}{2:10}{3:>10}{4:>15}{5:>15}{6:>15}{7:>15}".format(
        "Rank",
        "Currency", 
        "Symbol", 
        "Holdings",
        currency_symbol, 
        "Holdings {0}".format(currency_symbol),
        "USD", 
        "Holdings USD"))
    print("\033[0;37;40m")

def print_quotes(fx, currencies, symbol):
    """
    Prints FX rates for currencies of interest.
    """
    local_total = 0
    usd_total = 0

    for currency in fx:
        if currency["id"] in currencies.keys():
            holdings = currencies[currency["id"]]
            local_rate = float(currency["price_{0}".format(symbol.lower())])
            usd_rate = float(currency["price_usd"])

            local_holdings = holdings * local_rate
            usd_holdings = holdings * usd_rate

            local_total += local_holdings
            usd_total += usd_holdings

            print("{0:10}{1:15}{2:<10}{3:>10,.4f}{4:>15,.2f}{5:>15,.2f}{6:>15,.2f}{7:>15,.2f}".format(
                currency["rank"], 
                currency["name"], 
                currency["symbol"],
                holdings, 
                local_rate,
                local_holdings,
                usd_rate,
                usd_holdings))

    print()
    print("{0} Total: {1:,.2f}".format(symbol, local_total))
    print("USD Total: {0:,.2f}".format(usd_total))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("currencies", help="file containing currencies of interest")
    parser.add_argument("--symbol", help="symbol for fiat currency to show alongside USD")
    args = parser.parse_args()

    symbol = args.symbol if args.symbol else "GBP"
    fx = get_quotes_from_api(symbol)
    currencies = read_currencies(args.currencies)
    print_header(symbol)
    print_quotes(fx, currencies, symbol)


if __name__ == '__main__':
    main()
