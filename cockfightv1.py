from cs50 import get_int, get_string
import math
from random import uniform

# Prompt for total gems
while True:
    user_input = input("Enter your total amount of gems: ")
    try:
        inputvar = int(user_input)
        confirm = get_string(f"You entered integer {inputvar}. Confirm? (y/n): ")

        if confirm.lower() == "y":
            break
        else:
            continue
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
    # 1) Normalize risk to 0.1-1.0
    risk_factor = risky / 7.5

    # 2) Compute and cap streak-based factor (max 3×)
    factor = min(winstreak * risk_factor, 3)

    # 3) Build base/random bet component
    if allin:
        base = inputvar / 5
        allin = False
    else:
        base = inputvar / 2.75

    # Narrow random range for smoother progression
    rand = uniform(0.2, 0.4)
    raw_bet = base * rand * factor
    base_bet = max(1, math.floor(raw_bet))

    # 4) Bump up on losing streak (logarithmic, capped to 3×)
    if losestreak >= 2:
        multiplier = 1.5 * math.log(losestreak + 1) * (risky / 5)
        multiplier = min(multiplier, 3)
        boosted = math.floor(base_bet * multiplier)

        if boosted >= x:
            allin = True
        else:
            x = boosted
            print(f"(Losing streak of {losestreak}, increasing bet by {multiplier:.2f}×!)")
    else:
        x = round(base_bet * (risky / 5))

    # Display status
    print(f"\nYour current gems: {inputvar}")
    print(f"Current win chance (for info): {win_chance*100:.1f}%")
    if allin:
        print("All IN FOR THIS ROUND!")
    else:
        print(f"Bet {x} gems for this round.")

    # Ask user outcome
    winorlose = get_int("Type 0 if lose and 1 if win: ")
    while winorlose not in (0, 1):
        print("Invalid input, please enter 0 or 1.")
        winorlose = get_int("Type 0 if lose and 1 if win: ")

    # Update on win
    if winorlose == 1:
        if allin:
            inputvar *= 2
        else:
            inputvar += x

        winstreak += 1
        losestreak = 0
        win_chance = min(win_chance + 0.01, 1.0)
        print("Nice!")
    else:
        # Update on loss
        if allin:
            break
        else:
            inputvar -= x
        winstreak = 1
        losestreak += 1
        win_chance = 0.5
        print("Oh well.")

    # Check game-over
    if inputvar <= 0:
        print("Never gamble again.")
        break

    # Continue or quit
    cont = get_string("Press Enter to continue or type 'q' to quit: ")
    if cont.lower() == 'q':
        print("Made by: Pesdi_Oofyi")
        print("Goodbye")
        break

print("You went bankrupt, sorry D:")
