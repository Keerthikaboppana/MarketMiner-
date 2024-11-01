import argparse
from marketminer.apriori import apriori, generate_rules
from marketminer.utils import load_transactions, save_output

def main():
    parser = argparse.ArgumentParser(description="MarketMiner - Association Rule Mining with Apriori Algorithm")
    parser.add_argument("--file_path", type=str, help="Path to the CSV file containing transactions", required=True)
    parser.add_argument("--min_support", type=int, help="Minimum support count", required=True)
    parser.add_argument("--min_confidence", type=float, help="Minimum confidence", required=True)
    parser.add_argument("--output_format", type=str, choices=["json", "tsv"], help="Output format (json or tsv)", required=True)
    args = parser.parse_args()
    
    transactions = load_transactions(args.file_path)
    frequent_itemsets = apriori(transactions, args.min_support)
    rules = generate_rules(frequent_itemsets, args.min_confidence)
    save_output(frequent_itemsets, rules, args.output_format)

if __name__ == "__main__":
    main()
