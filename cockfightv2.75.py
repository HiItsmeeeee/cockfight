from cs50 import get_int, get_string
import math
import random

# Prompt for total gems
while True:
    user_input = input("Enter your total amount of gems: ")
    try:
        inputvar = int(user_input)
        confirm = get_string(f"You entered integer {inputvar}. Confirm? (y/n): ")
        if confirm.lower() == "y":
            break
    except ValueError:
        print("That’s not an integer. Please try again.")

# Prompt for risk tolerance
while True:
    risky = get_int("From 1 to 10, how much of a risktaker are you (INTEGERS ONLY) (): ")
    if 1 <= risky <= 10:
        if risky == 10:
            print("I won't advise you to be that risky.")
        break

# Initialize streaks and win chance
winstreak = 1
losestreak = 0
win_chance = 0.5  # start at 50%
allin = False
x = 1

while inputvar > 0:
    # 1) Normalize risk to 0.1-1.0 and cap streak-based factor
    risk_factor = risky / 5
    factor = min(winstreak * risk_factor * 1.15, 2.5)

    if winstreak >= 3:
        bonus = 0.05 * (winstreak - 2)
        factor = min(factor + bonus, 2.5)  # cap max factor to 3

    # 2) Build base/random bet component
    base = inputvar / 5 if allin else inputvar / 2.75
    allin = False
    rand = random.uniform(0.2, 0.4)
    raw_bet = base * rand * factor
    base_bet = max(1, math.floor(raw_bet))

    # 3) Apply losing-streak bump
    if losestreak >= 2:
        mult = 1.10 * math.log(losestreak + 1.2) * (risky / 5)
        mult = min(mult, 2.75)
        boosted = math.floor(base_bet * mult)
        y = random.randint(1, 4)
        if losestreak >= 2 and risky == 10:
            if y == 1:
                allin = True
        elif losestreak >= 3 and 7 <= risky <= 9:
            if y == 1:
                allin = True
        elif losestreak >= 4 and 3 <= risky <= 6:
            if y == 1:
                allin = True
        elif losestreak >= 5 and risky in (1, 2):
            if y == 1:
                allin = True

        if not allin:
            x = math.floor(min(boosted, inputvar))
            print(f"(Losing streak of {losestreak}, increasing bet by {mult:.2f}×!)")
    else:
        x = math.floor(base_bet * (risky / 6))

    # 4) Determine base chance decaying with win_chance
    base_chance = max(0.0, 0.40 - (win_chance - 0.50) * 1.5)
    # 5) Adjust chances by previous streaks and riskiness
    if losestreak > 1:
        adj = min((losestreak - 1) * 0.025 * (risky / 10), base_chance)
        boost_chance = min(1.0, base_chance + adj)
        reduce_chance = max(0.0, base_chance - adj)
    elif winstreak > 1:
        adj = min((winstreak - 1) * 0.025 * (risky / 10), base_chance)
        reduce_chance = min(1.0, base_chance + adj)
        boost_chance = max(0.0, base_chance - adj)
    else:
        boost_chance = base_chance
        reduce_chance = base_chance

    # 6) Apply conservative or recovery play
    if random.random() < reduce_chance:
        x = max(1, math.floor(x / 2))
        print(f"(Conservative mode: next bet divided by 2 – {reduce_chance*100:.1f}% chance)")  # Will be altered in v3
    if random.random() < boost_chance:
        x = math.floor(x * 1.25)
        print(f"(Recovery mode: next bet multiplied by 1.25 – {boost_chance*100:.1f}% chance)")  # Will be altered in v3

    # Display status
    x = min(x, inputvar)
    print(f"\nYour current gems: {inputvar}")
    print(f"Current win chance (for info): {win_chance*100:.1f}%")
    if allin or x >= inputvar:
        print("All IN FOR THIS ROUND!")
    else:
        print(f"Bet {x} gems for this round.")

    # Ask user outcome
    winorlose = get_int("Type 0 if lose and 1 if win: ")
    while winorlose not in (0, 1):
        print("Invalid input, please enter 0 or 1.")
        winorlose = get_int("Type 0 if lose and 1 if win: ")

    # 7) Update on win or loss
    if winorlose == 1:
        inputvar = inputvar * 2 if allin else inputvar + x
        winstreak += 1
        losestreak = 0
        win_chance = min(win_chance + 0.01, 1.0)
        print("Nice!")
    else:
        if allin:
            break
        inputvar -= x
        winstreak = 1
        losestreak += 1
        win_chance = 0.5
        print("Oh well.")

    # 8) Check game-over and continue prompt
    if inputvar <= 0:
        print("Never gamble again.")
        break
    if get_string("Press Enter to continue or type 'q' to quit: ").lower() == 'q':
        print("Made by: Pesdi_Oofyi\nGoodbye")
        break

print("You went bankrupt, sorry D:")
