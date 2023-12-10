# INSTRUCTIONS:
# Just add to maps more rooms and monsters to interact with.
# Feel free to add more types of monsters or abilities to use.
# Make sure to modify the proper parameters when calling the monsters.

# Import necessary modules
import random

# Example type effectiveness
TYPE_EFFECTIVENESS = {
    'Fire': {
        'strong_against': 'Grass',
        'weak_against': 'Water'
    },
    'Water': {
        'strong_against': 'Fire',
        'weak_against': 'Grass'
    },
    'Grass': {
        'strong_against': 'Water',
        'weak_against': 'Fire'
    },
    'Electric': {
        'strong_against': 'Electric',
        'weak_against': 'Grass'
    },
    'Ice': {
        'strong_against': 'Ice',
        'weak_against': 'Fire'
    },
    'Earth': {
        'strong_against': 'Electric',
        'weak_against': 'Water'
    }
}


def calculate_type_effectiveness(attacker, target):
  multiplier = 1
  if target.type in TYPE_EFFECTIVENESS[attacker.type]['strong_against']:
    multiplier = 2
  elif target.type in TYPE_EFFECTIVENESS[attacker.type]['weak_against']:
    multiplier = 0.5
  return multiplier


def fireball(attacker, target):
  base_damage = attacker.strength * 2  # Example: Fireball does double strength damage
  multiplier = calculate_type_effectiveness(attacker, target)
  damage = int(base_damage * multiplier)
  target.health -= damage
  return (damage, 'damage')  # Return a tuple (amount, action type)


def thunderbolt(attacker, target):
  base_damage = attacker.strength * 2
  multiplier = calculate_type_effectiveness(attacker, target)
  damage = int(base_damage * multiplier)
  target.health -= damage
  return (damage, 'damage')


def frost_shock(attacker, target):
  base_damage = attacker.strength * 1.5
  multiplier = calculate_type_effectiveness(attacker, target)
  damage = int(base_damage * multiplier)
  target.health -= damage
  return (damage, 'damage')


def leaf_blade(attacker, target):
  base_damage = attacker.strength * 2
  multiplier = calculate_type_effectiveness(attacker, target)
  damage = int(base_damage * multiplier)
  target.health -= damage
  return (damage, 'damage')


def heal(attacker, _):
  heal_amount = int(attacker.max_health * 0.25)  # Heals 25% of max health
  attacker.health = min(attacker.health + heal_amount, attacker.max_health)
  return (heal_amount, 'heal')  # Return a tuple (amount, action type)


# Define your monsters and characters using classes
class Monster:

  def __init__(self, name, type, strength, health, speed, abilities):
    self.name = name
    self.type = type  # e.g., 'Fire', 'Water', 'Grass', etc.
    self.strength = strength
    self.health = health
    self.max_health = health
    self.speed = speed  # Determines turn order
    self.abilities = abilities  # A list of special moves or abilities
    self.level = 1
    self.experience = 0

  def use_ability(self, target, ability_name):
    ability = self.abilities.get(ability_name)
    if ability:
      return ability(self, target)
    else:
      print(f"{self.name} doesn't know {ability_name}!")
      return 0, ''

  def attack(self, target):
    base_damage = random.randint(0, self.strength)
    multiplier = 1

    # Check type effectiveness
    multiplier = calculate_type_effectiveness(self, target)

    damage = int(base_damage * multiplier)
    target.health -= damage
    return damage

  def is_weak_enough_to_catch(self):
    return self.health <= self.max_health / 3

  def heal(self):
    self.health = self.max_health

  def gain_experience(self, amount):
    self.experience += amount
    if self.experience >= 100:  # Assuming 100 XP needed per level
      self.level_up()

  def level_up(self):
    self.level += 1
    self.strength += 2  # Example increment
    self.max_health += 10
    self.health = self.max_health
    self.experience -= 100
    print(
        f"{self.name} leveled up! Level: {self.level}, Strength: {self.strength}, Max Health: {self.max_health}"
    )


class Player:

  def __init__(self, name):
    self.name = name
    # Starting with one monster
    self.inventory = [
        Monster("Starter Monster", "Fire", 8, 50, 15, {
            'Fireball': fireball,
            'Heal': heal
        })
    ]
    self.health = 100

  def catch_monster(self, monster):
    if monster.is_weak_enough_to_catch():
      monster.heal()
      self.inventory.append(monster)
      return True
    return False

  def battle(self, wild_monster):
    if self.inventory:
      player_monster = self.inventory[0]
      while player_monster.health > 0 and wild_monster.health > 0:
        print()
        # Player's turn
        player_choice = input(
            "Do you want to 'attack' or use an 'ability'? ").lower()
        if player_choice == 'ability':
          ability_name = input("Which ability do you want to use? ")
          effect, action_type = player_monster.use_ability(
              wild_monster, ability_name)

          if action_type == 'damage':
            print(
                f"{player_monster.name} used {ability_name}, dealing {effect} damage."
            )
          elif action_type == 'heal':
            print(
                f"{player_monster.name} used {ability_name}, healing {effect} health."
            )
        else:
          damage = player_monster.attack(wild_monster)
          print(
              f"{player_monster.name} attacks {wild_monster.name}, causing {damage} damage."
          )

        if wild_monster.health <= 0:
          print(f"{wild_monster.name} has been defeated!")
          break

        # Wild monster's turn
        # Here you could also implement a logic for the wild monster to use abilities
        damage = wild_monster.attack(player_monster)
        print(
            f"{wild_monster.name} attacks {player_monster.name}, causing {damage} damage."
        )

        if player_monster.health <= 0:
          print(f"{player_monster.name} has been defeated!")
          # After a monster is defeated
          exp_gained = random.randint(20, 50)
          player_monster.gain_experience(exp_gained)  # Example amount
          print(f"Gained {exp_gained} experience points.")
          break
    else:
      print("You have no monsters to battle with!")


# Define the map with rooms and monsters
map = {
    'start': {
        'description':
        'You are in the starting room. There is a path to the north.',
        'exits': {
            'north': 'forest',
        },
        'monster': None
    },
    'forest': {
        'description':
        'You are in a dark forest. There is a path to the south and east.',
        'exits': {
            'south': 'start',
            'east': 'darker forest',
        },
        'monster':
        Monster("Wild Forest Monster", "Grass", 10, 30, 10,
                {'Leaf Blade': leaf_blade})
    },
    'darker forest': {
        'description':
        'You are in a darker forest. There is a path to the south and east.',
        'exits': {
            'south': 'forest',
            'east': 'cave',
            'start': 'start',
        },
        'monster':
        Monster("Wild Forest Monster", "Grass", 10, 30, 10,
                {'Leaf Blade': leaf_blade})
    },
    'cave': {
        'description':
        'You are in a cold, dark cave. There is a path to the west.',
        'exits': {
            'west': 'forest',
        },
        'monster':
        Monster("Cave Dwelling Monster", "Earth", 15, 40, 5,
                {'Fireball': fireball})
    }
}

# Initialize the player
player = Player(input("Welcome Trainer! What is your name? "))

current_room = 'start'

# Game loop
while player.health > 0:
  print(map[current_room]['description'])

  # Print exits of the current room
  print("Exits:")
  for exit_direction in map[current_room]['exits']:
    print(f"- {exit_direction}")

  print()

  # Encounter and battle with a monster if present
  if map[current_room]['monster']:
    print(f"A wild {map[current_room]['monster'].name} appears!")
    action = input("Do you want to 'fight', 'catch', or 'leave'? ").lower()
    if action == 'fight':
      # Player battles the monster
      player.battle(map[current_room]['monster'])

      if map[current_room]['monster'].health <= 0:
        map[current_room]['monster'] = None
    elif action == 'catch':
      # If the player can catch the monster, it will be added to their inventory.
      if player.catch_monster(map[current_room]['monster']):
        print(f"You have caught {map[current_room]['monster'].name}!")
        map[current_room]['monster'] = None
      else:
        print(f"{map[current_room]['monster'].name} is too strong to catch!")
    elif action == 'leave':
      print("You choose to leave the monster be.")
    else:
      print("Invalid action.")

  # Move to another room
  direction = input("Which direction do you want to go? ").lower()
  if direction in map[current_room]['exits']:
    current_room = map[current_room]['exits'][direction]
  else:
    print("You can't go that way.")

  # Check the player's health
  if player.health <= 0:
    print("You have been defeated. Game Over.")
    break

print("Thanks for playing!")
