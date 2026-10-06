import random

TICKET_COST = 5
MAIN_COUNT = 5
MAIN_POOL = 70   # 5 numbers from 1-70
BONUS_POOL = 24  # 1 Mega Ball from 1-24

# Real Mega Millions base prize table (before any multiplier), keyed by
# (main matches, mega ball matched).
JACKPOT = 50_000_000  # starting jackpot, rolls higher if unclaimed
PAYOUTS = {
    (5, True): JACKPOT,
    (5, False): 1_000_000,
    (4, True): 10_000,
    (4, False): 500,
    (3, True): 200,
    (3, False): 10,
    (2, True): 10,
    (1, True): 4,
    (0, True): 2,
}

MY_MAIN = {12, 21, 35, 38, 47}  # your preset main numbers
MY_BONUS = 10                   # your preset Mega Ball number


def draw():
    """One random draw: 5 unique numbers from 1-70 plus 1 Mega Ball from 1-24."""
    main = set(random.sample(range(1, MAIN_POOL + 1), MAIN_COUNT))
    bonus = random.randint(1, BONUS_POOL)
    return main, bonus


def run_simulation(budget, my_main=MY_MAIN, my_bonus=MY_BONUS,
                   detailed_limit=1000, timeline_points=200):
    """Spend `budget` dollars, one ticket per draw.

    Returns totals, a sampled timeline for the live chart, number frequencies,
    and (for small runs only) every individual draw.
    """
    num_draws = budget // TICKET_COST
    step = max(1, num_draws // timeline_points)
    spent = won = best_win = 0
    results = {}                      # (main matches, bonus matched) -> count
    main_freq = [0] * (MAIN_POOL + 1)  # index = number drawn
    bonus_freq = [0] * (BONUS_POOL + 1)
    timeline = []                     # [draw #, spent, won] samples
    detail = []

    for i in range(1, num_draws + 1):
        main, bonus = draw()
        key = (len(main & my_main), bonus == my_bonus)
        prize = PAYOUTS.get(key, 0)
        spent += TICKET_COST
        won += prize
        best_win = max(best_win, prize)
        results[key] = results.get(key, 0) + 1
        for n in main:
            main_freq[n] += 1
        bonus_freq[bonus] += 1
        if i % step == 0 or i == num_draws:
            timeline.append([i, spent, won])
        if num_draws <= detailed_limit:
            detail.append({"main": sorted(main), "bonus": bonus,
                           "matches": key[0], "bonus_hit": key[1], "prize": prize})

    return {
        "draws": num_draws,
        "spent": spent,
        "won": won,
        "net": won - spent,
        "best_win": best_win,
        "results": {f"{m}+{'B' if b else '0'}": c for (m, b), c in sorted(results.items())},
        "main_freq": main_freq[1:],
        "bonus_freq": bonus_freq[1:],
        "timeline": timeline,
        "my_main": sorted(my_main),
        "my_bonus": my_bonus,
        "detail": detail,  # empty for big runs
    }


if __name__ == "__main__":
    r = run_simulation(budget=1_000_000)
    print(f"Draws: {r['draws']}  Spent: ${r['spent']}  Won: ${r['won']}  Net: ${r['net']}")
    print("Results:", r["results"])
