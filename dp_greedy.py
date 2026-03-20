'''This is dp vs greedy approach:
Each district is represented as:
(name, cost, value)'''

def solve_dp(districts, budget, conflicts):
    """
    DP approach (0/1 knapsack style).
    This finds the best value under the budget constraint first,
    then removes one district from any conflicting pair afterwards.
    Returns:
        total_value, chosen_districts, total_cost
    """

    names = [d[0] for d in districts]
    costs = [d[1] for d in districts]
    values = [d[2] for d in districts]
    n = len(districts)

    # dp[i][b] = maximum value using first i districts with budget b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # skip current district

            if costs[i - 1] <= b:
                take = dp[i - 1][b - costs[i - 1]] + values[i - 1]
                if take > dp[i][b]:
                    dp[i][b] = take

    # Backtrack to find chosen districts
    chosen = []
    b = budget

    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]

    chosen.reverse()

    # Remove one district from conflicting pairs
    chosen_set = set(chosen)
    for a, x in conflicts:
        if a in chosen_set and x in chosen_set:
            # remove the second one in the pair
            chosen_set.remove(x)

    chosen = [name for name in chosen if name in chosen_set]

    total_value = sum(values[names.index(d)] for d in chosen)
    total_cost = sum(costs[names.index(d)] for d in chosen)

    return total_value, chosen, total_cost


def solve_greedy(districts, budget, conflicts, strategy="best_ratio"):
    """
    Greedy approach.
    strategy:
        'highest_value'
        'lowest_cost'
        'best_ratio'
    Returns:
        total_value, chosen_districts, total_cost
    """

    names = [d[0] for d in districts]
    costs = [d[1] for d in districts]
    values = [d[2] for d in districts]
    n = len(districts)

    if strategy == "highest_value":
        order = sorted(range(n), key=lambda i: values[i], reverse=True)
    elif strategy == "lowest_cost":
        order = sorted(range(n), key=lambda i: costs[i])
    elif strategy == "best_ratio":
        order = sorted(range(n), key=lambda i: values[i] / costs[i], reverse=True)
    else:
        raise ValueError("Invalid strategy. Use 'highest_value', 'lowest_cost', or 'best_ratio'.")

    chosen = []
    left = budget

    for i in order:
        if costs[i] <= left:
            # check conflict
            ok = True
            for a, x in conflicts:
                if (names[i] == a and x in chosen) or (names[i] == x and a in chosen):
                    ok = False
                    break

            if ok:
                chosen.append(names[i])
                left -= costs[i]

    total_value = sum(values[names.index(d)] for d in chosen)
    total_cost = sum(costs[names.index(d)] for d in chosen)

    return total_value, chosen, total_cost


def compare_case(case_name, districts, budget, conflicts):
    print(f"\n{'=' * 60}")
    print(f"{case_name}")
    print(f"{'=' * 60}")

    dp_value, dp_chosen, dp_cost = solve_dp(districts, budget, conflicts)

    greedy_value, greedy_chosen, greedy_cost = solve_greedy(
        districts, budget, conflicts, strategy="best_ratio"
    )

    gap = round((dp_value - greedy_value) / dp_value * 100, 2) if dp_value else 0

    print(f"Budget: {budget}")
    print(f"Conflicts: {conflicts}")
    print()
    print(f"DP     -> value={dp_value}, cost={dp_cost}, districts={dp_chosen}")
    print(f"Greedy -> value={greedy_value}, cost={greedy_cost}, districts={greedy_chosen}")
    print(f"Gap    -> {gap}%")

    # Optional: compare extra greedy strategies too
    gv1, gc1, gco1 = solve_greedy(districts, budget, conflicts, "highest_value")
    gv2, gc2, gco2 = solve_greedy(districts, budget, conflicts, "lowest_cost")

    print("\nOther Greedy Strategies:")
    print(f"highest_value -> value={gv1}, cost={gco1}, districts={gc1}")
    print(f"lowest_cost   -> value={gv2}, cost={gco2}, districts={gc2}")


# ---------------------------------------------------------
# MAIN INPUT CASE
# ---------------------------------------------------------

districts = [
    ("Nizami", 4, 10),
    ("Nesimi", 6, 12),
    ("Yasamal", 3, 7),
    ("Nerimanov", 5, 12),
    ("Ehmedli", 7, 11),
    ("Xetai", 5, 9)
]

budget = int(input("Enter budget: "))

conflicts = [
    ("Nizami", "Ehmedli"),
    ("Yasamal", "Nerimanov"),
    ("Nesimi", "Xetai")
]

compare_case("User Input Case", districts, budget, conflicts)


# ---------------------------------------------------------
# TEST CASES
# ---------------------------------------------------------

test_cases = [
    {
        "name": "Case 1",
        "districts": [
            ("Nizami", 4, 10),
            ("Nesimi", 6, 12),
            ("Yasamal", 3, 7),
            ("Nerimanov", 5, 12),
            ("Ehmedli", 7, 11),
            ("Xetai", 5, 9)
        ],
        "budget": 15,
        "conflicts": [
            ("Nizami", "Ehmedli"),
            ("Yasamal", "Nerimanov"),
            ("Nesimi", "Xetai")
        ]
    },
    {
        "name": "Case 2",
        "districts": [
            ("Shaki", 2, 4),
            ("Baki", 5, 10),
            ("Ganca", 4, 7),
            ("Daskesen", 3, 5)
        ],
        "budget": 5,
        "conflicts": [
            ("Shaki", "Daskesen")
        ]
    },
    {
        "name": "Case 3",
        "districts": [
            ("Agsu", 3, 8),
            ("Bilesuvar", 4, 9),
            ("Xacmaz", 2, 5),
            ("Bineqedi", 6, 12),
            ("Salyan", 5, 11)
        ],
        "budget": 10,
        "conflicts": []
    },
    {
        "name": "Case 4",
        "districts": [
            ("Agdam", 4, 9),
            ("Lacin", 5, 10),
            ("Xirdalan", 2, 4),
            ("Lenkeran", 6, 13),
            ("Sirvan", 3, 6)
        ],
        "budget": 11,
        "conflicts": [
            ("Agdam", "Lacin"),
            ("Xirdalan", "Lenkeran")
        ]
    },
    {
        "name": "Case 5",
        "districts": [
            ("Mingecevir", 10, 60),
            ("Quba", 20, 100),
            ("Qebele", 30, 120)
        ],
        "budget": 50,
        "conflicts": []
    }
]

# ---------------------------------------------------------
# RUN ALL TEST CASES
# ---------------------------------------------------------

for case in test_cases:
    compare_case(
        case["name"],
        case["districts"],
        case["budget"],
        case["conflicts"]
    )
