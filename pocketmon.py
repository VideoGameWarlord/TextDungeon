# Import necessary modules
import random

# Define your monsters and characters using classes
class Monster:
    def __init__(self, name, strength, health):
        self.name = name
        self.strength = strength
        self.health = health

    def attack(self, target):
        damage = random.randint(0, self.strength)
        target.health -= damage
        return damage

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = 'start'
        self.health = 100

    def catch_monster(self, monster):
        self.inventory.append(monster)

    def battle(self, monster):
        # Simple battle logic: player's first monster in inventory battles
        if self.inventory:
            player_monster = self.inventory[0]
            damage = player_monster.attack(monster)
            print(f"{player_monster.name} attacks {monster.name} causing {damage} damage.")
            if monster.health <= 0:
                print(f"{monster.name} has been defeated!")
        else:
            print("You have no monsters to battle with!")

# Define the map with rooms and monsters
map = {
    'start': {
        'description': 'You are in the starting room. There is a path to the north.',
        'north': 'forest',
        'monster': None
    },
    'forest': {
        'description': 'You are in a dark forest. There is a path to the south and east.',
        'south': 'start',
        'east': 'cave',
        'monster': Monster("Wild Forest Monster", 10, 30)
    },
    'cave': {
        'description': 'You are in a cold, dark cave. There is a path to the west.',
        'west': 'forest',
        'monster': Monster("Cave Dwelling Monster", 15, 40)
    }
}

# Initialize the player
player = Player(input("Welcome Trainer! What is your name? "))

# Game loop
while player.health > 0:
    current_room = map[player.current_room]
    print(current_room['description'])

    # Encounter and battle with a monster if present
    if current_room['monster']:
        print(f"A wild {current_room['monster'].name} appears!")
        action = input("Do you want to 'fight' or 'catch'? ").lower()
        if action == 'fight':
            player.battle(current_room['monster'])
            if current_room['monster'].health <= 0:
                # Monster is defeated and removed from the room
                current_room['monster'] = None
        elif action == 'catch':
            player.catch_monster(current_room['monster'])
            print(f"You have caught a {current_room['monster'].name}!")
            current_room['monster'] = None
        else:
            print("You choose to do nothing and the monster goes away.")
    else:
        print("There are no monsters here.")

    # Move to another room
    direction = input("Which direction do you want to go? ").lower()
    if direction in current_room and direction in ['north', 'south', 'east', 'west']:
        player.current_room = current_room[direction]
    else:
        print("You can't go that way.")

    # Check the player's health
    if player.health <= 0:
        print("You have been defeated. Game Over.")
        break

print("Thanks for playing!")
