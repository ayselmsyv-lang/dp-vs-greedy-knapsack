'''This is dp approach:
i represents each district and budget is budget of and 
cost is cost of and value is value of each district
we will use memoization to avoid recalculating the same subproblem.'''

# Each district: (name, cost, value)
districts = [("Nizami",4,10),("Nesimi",6,12),("Yasamal",3,7),
             ("Nerimanov",5,12),("Ehmedli",7,11),("Xetai",5,9)]

budget = int(input("Enter budget: "))

# Pairs that CANNOT both be chosen at the same time
conflicts = [("Nizami","Ehmedli"),("Yasamal","Nerimanov"),("Nesimi","Xetai")]

# Separate the data into simple lists
names = [d[0] for d in districts]
cost  = [d[1] for d in districts]
value = [d[2] for d in districts]
n = len(districts)

# --------------------------------------------------------------------------------------
# DP — knapsack table approach
# dp[i][b] = best value using first i districts with exactly b budget remaining
# -------------------------------------------------------------------------------
dp = [[0] * (budget + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for b in range(budget + 1):
        dp[i][b] = dp[i-1][b]              # option 1: skip this district
        if cost[i-1] <= b:
            take = dp[i-1][b-cost[i-1]] + value[i-1]
            if take > dp[i][b]:
                dp[i][b] = take            # option 2: take this district (if better)

# Backtrack through the table to find which districts were actually picked
chosen_dp, b = [], budget
for i in range(n, 0, -1):
    if dp[i][b] != dp[i-1][b]:            # value changed → district i was taken
        chosen_dp.append(names[i-1])
        b -= cost[i-1]                     # reduce budget by its cost

# Remove one district from any conflicting pair
for a, x in conflicts:
    if a in chosen_dp and x in chosen_dp:
        chosen_dp.remove(x)                # drop the second district in the pair

# ------------------------------------------------
# Greedy — value/cost ratio approach
# Sort districts by ratio (best bang per budget first)
# Pick each one if it fits and has no conflict
# ------------------------------------------------
order = sorted(range(n), key=lambda i: -value[i]/cost[i])
chosen_g, left = [], budget

for i in order:
    if cost[i] <= left:                    # fits in remaining budget?
        # check if adding this district breaks any conflict rule
        ok = all(not(names[i]==a and x in chosen_g) and
                 not(names[i]==x and a in chosen_g) for a,x in conflicts)
        if ok:
            chosen_g.append(names[i])
            left -= cost[i]                # spend the budget

# ------------------------------------------------
# Compare results
# gap% = how much value greedy missed vs DP
# 0% = greedy was perfect, 20% = greedy got 20% less
# ------------------------------------------------
dp_val = sum(value[names.index(d)] for d in chosen_dp)
g_val  = sum(value[names.index(d)] for d in chosen_g)
gap    = round((dp_val - g_val) / dp_val * 100) if dp_val else 0

print(f"\nDP     → value={dp_val}, districts={chosen_dp}")
print(f"Greedy → value={g_val}, districts={chosen_g}, gap={gap}%")
