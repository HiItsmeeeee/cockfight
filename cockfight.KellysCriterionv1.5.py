from cs50 import get_int, get_string
import math
import random

def prompt_bankroll():
    """Ask user for starting gems (integer), preserving your prints."""
    while True:
        user_input = input("Enter your total amount of gems: ")
        try:
            inputvar = int(user_input)
            confirm = get_string(f"You entered integer {inputvar}. Confirm? (y/n): ")
            if confirm.lower() == "y":
                return inputvar
        except ValueError:
            print("That’s not an integer. Please try again.")

def prompt_risk():
    """Ask user for risk tolerance 1–10, preserving prints."""
    while True:
        risky = get_int("From 1 to 10, how much of a risktaker are you (INTEGERS ONLY) (): ")
        if 1 <= risky <= 10:
            if risky == 10:
                print("I won't advise you to be that risky.")
            return risky

def kelly_bet(bankroll, p, risky, min_frac=0.01, max_frac=0.25):
    """
    Compute bet size via Kelly for an even-money game,
    then scale it by (risky/5).

    bankroll: current gems.
    p: current win_chance [0..1].
    risky: 1–10.
    min_frac: minimum fraction of bankroll to bet.
    max_frac: hard cap on fraction of bankroll to bet.
    """
    edge = 2 * p - 1                   # Kelly edge for even‑money
    base_f = max(0.0, edge)            # no negative
    scaled_f = base_f * (risky / 5)    # now using risky/5
    # enforce floor & cap
    f = min(max(scaled_f, min_frac), max_frac)
    return max(1, math.floor(bankroll * f))

def main():
    inputvar   = prompt_bankroll()
    risky      = prompt_risk()
    win_chance = 0.50       # start at 50%

    while inputvar > 0:
        # 1) Size bet using scaled Kelly
        x = kelly_bet(inputvar, win_chance, risky)

        # 2) Preserve your prints
        print(f"\nYour current gems: {inputvar}")
        print(f"Current win chance (for info): {win_chance*100:.1f}%")
        if x >= inputvar:
            print("All IN FOR THIS ROUND!")
        else:
            print(f"Bet {x} gems for this round.")

        # 3) Ask for outcome
        winorlose = get_int("Type 0 if lose and 1 if win: ")
        while winorlose not in (0, 1):
            print("Invalid input, please enter 0 or 1.")
            winorlose = get_int("Type 0 if lose and 1 if win: ")

        # 4) Update bankroll & win_chance exactly as before
        if winorlose == 1:
            if x >= inputvar:
                inputvar *= 2
            else:
                inputvar += x
            win_chance = min(win_chance + 0.01, 1.0)
            print("Nice!")
        else:
            if x >= inputvar:
                break
            inputvar -= x
            win_chance = 0.50
            print("Oh well.")

        # 5) Continue or quit
        if inputvar <= 0:
            print("Never gamble again.")
            break
        if get_string("Press Enter to continue or type 'q' to quit: ").lower() == 'q':
            print("Made by: Pesdi_Oofyi\nGoodbye")
            break

    print("You went bankrupt, sorry D:")

if __name__ == "__main__":
    main()
