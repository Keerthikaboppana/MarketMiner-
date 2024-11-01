import csv
import json
import os

def load_transactions(file_path):
    transactions = []
    with open(file_path, mode='r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            transactions.append(set(row))
    return transactions

def save_output(frequent_itemsets, rules, output_format):
    os.makedirs("output", exist_ok=True)
    output_data = {
        "frequent_itemsets": [{ "itemset": list(item), "support": support} for item, support in frequent_itemsets.items()],
        "rules": rules
    }
    
    if output_format == "json":
        with open("output/output.json", "w") as f:
            json.dump(output_data, f, indent=4)
    elif output_format == "tsv":
        with open("output/output.tsv", "w") as f:
            for item in output_data["frequent_itemsets"]:
                f.write("\t".join(item["itemset"]) + "\t" + str(item["support"]) + "\n")
            f.write("\n")
            for rule in output_data["rules"]:
                f.write("\t".join(rule["antecedent"]) + "\t" + "\t".join(rule["consequent"]) + "\t" + str(rule["support"]) + "\t" + str(rule["confidence"]) + "\n")
