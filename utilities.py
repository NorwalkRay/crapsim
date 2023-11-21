import random

def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2

def generate_dice_rolls(num_rolls, file_name):
    """Generate a specified number of dice rolls and save to a file."""
    with open(file_name, 'w') as file:
        for _ in range(num_rolls):
            roll = roll_dice()
            file.write(f"{roll[0]},{roll[1]}\n")

if __name__ == "__main__":
    NUM_ROLLS = 100000  # Specify the number of rolls
    FILE_NAME = "dice_rolls1.txt"  # Specify the output file name

    generate_dice_rolls(NUM_ROLLS, FILE_NAME)