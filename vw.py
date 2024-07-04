import sys
import time

from agents import Agent
from map import Map

# POINTS
SUCCESS = -10  # Vacuumed successfully
FAILURE = 10  # Vacuumed unsuccessfully, made a mess
POINTLESS = 2  # Vacuumed a clean room
MOVE = 1  # Moved to a new room
NO_ACTION = 0  # No action taken
DIRT_START = 10  # Points for each dirt pile at the start
DIRT_LEFT = 100  # Points for each dirt pile left at the end

MAX_STEPS = 10000
TOTAL_SIMS = 1000


def main():
    print("Welcome to the Vacuum World Simulator 9000!")
    menu()
    return


def get_yes_no_input(prompt):
    while True:
        response = input(prompt).lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Invalid input. Please enter yes or no.")


def menu():
    while True:
        print("1. Visual Reflex Agent Simulation")
        print("2. Visual Random Agent Simulation")
        print("3. Visual Murphy's Law Reflex Agent Simulation")
        print("4. Visual Murphy's Law Random Agent Simulation")
        print("5. Run a full gambit with reports")
        print("0. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case "0":
                print("Goodbye!")
                exit()
            case "1":
                vis_reflex_sim()
            case "2":
                vis_random_sim()
            case "3":
                vis_reflex_murphy_sim()
            case "4":
                vis_random_murphy_sim()
            case "5":
                full_gambit()
            case _:
                print("Invalid choice. Please enter a number between 0 and 5.")


def clear_screen():
    print("\033[H\033[J")


def visual_sim(max_steps=100, random=False, murphy=False):
    dirt_piles = int(input("Enter the number of dirt piles: (1, 3, 5): "))

    if dirt_piles > 9 or dirt_piles < 1:
        print("Invalid number of dirt piles. Defaulting to 5.")
        dirt_piles = 5

    map = Map(3, 3, dirt_piles)
    agent = Agent(position=map.random_position(), random=random, murphy=murphy)
    map.spread_dirt()

    while not map.all_clean():
        clear_screen()
        map.print(agent)
        agent.action(map.get_room(agent.position))
        print("Battery Remaining: ", max_steps)
        time.sleep(0.25)
        max_steps -= 1
        if max_steps == 0:
            print("Max steps reached")
            break

    if map.all_clean():
        clear_screen()
        map.print(agent)
        print("All clean!")


def sim(max_steps=MAX_STEPS, random=False, murphy=False, dirt_piles=0):
    steps = max_steps
    map = Map(3, 3, dirt_piles)
    agent = Agent(position=map.random_position(), random=random, murphy=murphy)
    map.spread_dirt()
    points = dirt_piles * DIRT_START
    spinner = spinning_cursor()

    for i in range(max_steps):
        last_action = agent.action(map.get_room(agent.position))
        points += add_points(last_action)
        steps -= 1
        if map.all_clean():
            return points

        if i % 1000 == 0:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write("\b")

    remaining_dirt = map.dirt_piles
    points += remaining_dirt * DIRT_LEFT
    return points


def add_points(action):
    match action:
        case "SUCK_SUCCESS":
            return SUCCESS
        case "SUCK_FAILURE":
            return FAILURE
        case "SUCK_POINTLESS":
            return POINTLESS
        case "MOVE":
            return MOVE
        case _:
            return NO_ACTION


def vis_reflex_sim():
    visual_sim(random=False, murphy=False)


def vis_random_sim():
    visual_sim(random=True, murphy=False)


def vis_reflex_murphy_sim():
    visual_sim(random=False, murphy=True)


def vis_random_murphy_sim():
    visual_sim(random=True, murphy=True)


def reflex_sim(piles):
    return sim(random=False, murphy=False, dirt_piles=piles)


def random_sim(piles):
    return sim(random=True, murphy=False, dirt_piles=piles)


def reflex_murphy_sim(piles):
    return sim(random=False, murphy=True, dirt_piles=piles)


def random_murphy_sim(piles):
    return sim(random=True, murphy=True, dirt_piles=piles)


def single_gambit(sim_type, agent_type, file, total_sims):
    points = []
    for piles in [1, 3, 5]:
        file.write(f"{agent_type},{piles},{total_sims}, ,")
        for i in range(total_sims):
            points.append(sim_type(piles))

        failures = 0
        for point in points:
            if point > MAX_STEPS:
                failures += 1
        file.write(f"{failures},")

        for point in points:
            file.write(f"{point},")
        file.write("\n")
        points.clear()
    return


def full_gambit():
    total_sims = TOTAL_SIMS
    # Create a CSV file
    output_file = "data.csv"

    print("Running Full Gambit of Tests...")
    with open(output_file, "w") as file:
        file.write("Agent, Dirt Piles, Sims, WIN ODDS, FAILURES, Points\n")
        print("Reflex Agent Simulation")
        single_gambit(reflex_sim, "Reflex", file, total_sims)
        print("Random Agent Simulation")
        single_gambit(random_sim, "Random", file, total_sims)
        print("Reflex Murphy's Law Agent Simulation")
        single_gambit(reflex_murphy_sim, "Reflex Murphy", file, total_sims)
        print("Random Murphy's Law Agent Simulation")
        single_gambit(random_murphy_sim, "Random Murphy", file, total_sims)
        file.close()
    print(f"All tests complete. Data written to {output_file}")
    return


def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


if __name__ == "__main__":
    main()
