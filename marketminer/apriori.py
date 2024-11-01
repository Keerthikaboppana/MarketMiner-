from itertools import combinations
from collections import defaultdict
import concurrent.futures

def generate_candidates(frequent_itemsets, k):
    candidates = set()
    for itemset1 in frequent_itemsets:
        for itemset2 in frequent_itemsets:
            union_itemset = itemset1 | itemset2
            if len(union_itemset) == k:
                candidates.add(union_itemset)
    return candidates

def calculate_support(transactions, candidates, min_support):
    support_counts = defaultdict(int)
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                support_counts[candidate] += 1
    return {itemset: count for itemset, count in support_counts.items() if count >= min_support}

def apriori(transactions, min_support):
    frequent_itemsets = {}
    k = 1
    candidates = {frozenset([item]) for transaction in transactions for item in transaction}
    
    while candidates:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.submit(calculate_support, transactions, candidates, min_support)
            frequent_itemsets_k = result.result()
        
        if not frequent_itemsets_k:
            break
        frequent_itemsets.update(frequent_itemsets_k)
        
        k += 1
        candidates = generate_candidates(frequent_itemsets_k.keys(), k)
    
    return frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset, support in frequent_itemsets.items():
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                if antecedent and consequent:
                    antecedent_support = frequent_itemsets[antecedent]
                    confidence = support / antecedent_support
                    if confidence >= min_confidence:
                        rules.append({
                            "antecedent": list(antecedent),
                            "consequent": list(consequent),
                            "support": support,
                            "confidence": confidence
                        })
    return rules
