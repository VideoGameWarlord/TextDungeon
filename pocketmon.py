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
        'weak_against': 'Earth'
    },
    'Ice': {
        'strong_against': 'Water',
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


def earth_wall(attacker, _):
  attacker.defense_up = True  # Indicates that the defense is raised
  attacker.defense_turns = 2  # Number of turns the defense is up
  return (0, 'defense')  # No immediate effect, so return 0 and a new action type 'defense'


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


def lightning_stun(attacker, target):
  target.stunned = True  # Target is stunned and misses the next turn
  return (0, 'stun')  # No damage, so return 0 and a new action type 'stun'


def heal(attacker, _):
  heal_amount = int(attacker.max_health * 0.25)  # Heals 25% of max health
  attacker.health = min(attacker.health + heal_amount, attacker.max_health)
  return (heal_amount, 'heal')  # Return a tuple (amount, action type)

monster_templates = {
    'Flamey': {
        'type': 'Fire',
        'base_strength': 10,
        'base_health': 40,
        'speed': 7,
        'abilities': {'Fireball': fireball},
        'evolution_level': 3,
        'evolution': 'Flamester'
    },
    'Flamester': {
        'type': 'Fire',
        'base_strength': 15,
        'base_health': 60,
        'speed': 9,
        'abilities': {'Fireball': fireball},
        'evolution_level': None,
        'evolution': None
    },
  
    'Pinne Fawn': {
        'type': 'Grass',
        'base_strength': 15,
        'base_health': 70,
        'speed': 10,
        'abilities': {'Leaf Blade': leaf_blade},
        'evolution_level': 5,
        'evolution': 'Pinne Deer'
    },
    'Pinne Deer': {
        'type': 'Grass',
        'base_strength': 25,
        'base_health': 120,
        'speed': 15,
        'abilities': {'Leaf Blade': leaf_blade},
        'evolution_level': None,
        'evolution': None
    },
  
    'Lesser Freezeguin': {
        'type': 'Ice',
        'base_strength': 10,
        'base_health': 90,
        'speed': 5,
        'abilities': {'Frost Shock': frost_shock},
        'evolution_level': None,
        'evolution': None
    },
    'Fishy Fish': {
        'type': 'Water',
        'base_strength': 3,
        'base_health': 100,
        'speed': 12,
        'abilities': {'Flip Flop': lightning_stun},
        'evolution_level': None,
        'evolution': None
    },
    'Wild Forest Monster': {
        'type': 'Grass',
        'base_strength': 10,
        'base_health': 30,
        'speed': 10,
        'abilities': {'Leaf Blade': leaf_blade},
        'evolution_level': None,
        'evolution': None
    }
    # Define other monsters...
}

def spawn_monster(name):
  template = monster_templates[name]
  strength_variation = random.randint(-2, 2)
  health_variation = random.randint(-10, 10)
  monster = Monster(
      name=name,
      type=template['type'],
      strength=template['base_strength'] + strength_variation,
      health=template['base_health'] + health_variation,
      speed=template['speed'],
      abilities=template['abilities']
  )
  monster.evolution_level = template['evolution_level']
  monster.evolution = template['evolution']
  return monster

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
    self.evolution_level = None
    self.evolution = None

    # Battle Modifiers
    self.defense_up = False
    self.defense_turns = 0
    self.stunned = False

  def use_ability(self, target, ability_name):
    ability = self.abilities.get(ability_name)
    if ability:
      return ability(self, target)
    else:
      print(f"{self.name} doesn't know {ability_name}!")
      return 0, ''

  def attack(self, target):
    # Calculate dodge chance based on speed difference
    dodge_chance = max(0, min((target.speed - self.speed) / 10, 0.3))  # Example formula
    if random.random() < dodge_chance:
        print(f"{target.name} dodged the attack!")
        return 0
    
    base_damage = random.randint(0, self.strength)
    multiplier = 1

    # Check type effectiveness
    multiplier = calculate_type_effectiveness(self, target)
    damage = int(base_damage * multiplier)

    # Check if opposing monster's defense is up (true/false)
    if target.defense_up:
      damage = int(damage * 0.5)  # Reduce damage by half if defense is up

    target.health -= damage
    return damage

  def end_turn_update(self):
    # Update defense status
    if self.defense_up:
      self.defense_turns -= 1
      if self.defense_turns == 0:
        self.defense_up = False
    if self.stunned:
      self.stunned = False  # Reset stun status at the end of the turn

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
    print(f"{self.name} leveled up! Level: {self.level}, Strength: {self.strength}, Max Health: {self.max_health}")
    # Check for evolution
    evolution = self.check_evolution()
    if evolution:
        self.evolve(evolution)

  def check_evolution(self):
    if self.evolution and self.evolution_level is not None and self.level >= self.evolution_level:
        return self.evolution
    return None

  def evolve(self, new_form):
    evolution_template = monster_templates[new_form]
    self.name = new_form
    self.type = evolution_template['type']
    self.strength = evolution_template['base_strength']
    self.max_health = evolution_template['base_health']
    self.speed = evolution_template['speed']
    self.abilities = evolution_template['abilities']
    self.evolution_level = evolution_template['evolution_level']
    self.evolution = evolution_template['evolution']
    self.health = self.max_health  # Heal to full on evolution
    print(f"{self.name} has evolved into {new_form}!")

class Player:

  def __init__(self, name):
    self.name = name
    # Starting with one monster
    self.inventory = [
        Monster("Starter Monster", "Fire", 8, 50, 15, {
            'Fireball': fireball,
            'Heal': heal,
            'Stun': lightning_stun
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
        print(
            f"\n{player_monster.name}'s has {player_monster.health} health left."
        )
        print(
            f"{wild_monster.name}'s has {wild_monster.health} health left.\n")

        # Player's turn
        if not player_monster.stunned:  # Check if player's monster is stunned
            # Display abilities
            print("Choose an action or 'catch':")
            print("0: Normal attack")
            for i, ability_name in enumerate(player_monster.abilities, start=1):
                print(f"{i}: {ability_name}")

            # Player chooses action
            choice = input("Enter your choice: ")
            if choice.isdigit():
                choice = int(choice)
                if choice == 0:
                    damage = player_monster.attack(wild_monster)
                    print(f"{player_monster.name} attacks {wild_monster.name}, causing {damage} damage.")
                elif 1 <= choice <= len(player_monster.abilities):
                    ability_name = list(player_monster.abilities.keys())[choice - 1]
                    effect, action_type = player_monster.use_ability(wild_monster, ability_name)

                  # Print out effect of ability
                    if action_type == 'damage':
                      print(f"{player_monster.name} used {ability_name}, dealing {effect} damage.")
                    elif action_type == 'heal':
                      print(f"{player_monster.name} used {ability_name}, healing {effect} health.")
                    elif action_type == 'stun':
                      print(f"{player_monster.name} used {ability_name}, stunning {wild_monster.name}.")
                    elif action_type == 'defense':
                      print(f"{player_monster.name} used {ability_name}, defending against {wild_monster.name}'s next attack.")
                      
            elif choice == 'catch':
              # If the player can catch the monster, it will be added to their inventory.
              if player.catch_monster(map[current_room]['monster']):
                print(f"You have caught {map[current_room]['monster'].name}!")
                map[current_room]['monster'] = None
                break
              else:
                print(f"{map[current_room]['monster'].name} is too strong to catch!")
            else:
              damage = player_monster.attack(wild_monster)
              print(f"{player_monster.name} attacks {wild_monster.name}, causing {damage} damage.")
        else:
          print(f"{player_monster.name} is stunned and cannot move!")

        # At the end of each turn
        player_monster.end_turn_update()

        if not wild_monster.stunned:  # Check if wild monster is stunned
          if wild_monster.health <= 0:
            print(f"{wild_monster.name} has been defeated!")
            map[current_room]['monster'] = None
            break

          # Wild monster's turn
          if random.random() < 0.35:  # 35% chance to use an ability
            ability_name = random.choice(list(wild_monster.abilities.keys()))
            effect, action_type = wild_monster.use_ability(
                player_monster, ability_name)
            # Display appropriate message based on action_type
            if action_type == 'damage':
              print(
                  f"{wild_monster.name} used {ability_name}, dealing {effect} damage."
              )
            elif action_type == 'heal':
              print(
                  f"{wild_monster.name} used {ability_name}, healing {effect} health."
              )
            elif action_type == 'stun':
              print(
                  f"{wild_monster.name} used {ability_name}, stunning {player_monster.name}."
              )
            elif action_type == 'defense':
              print(
                  f"{wild_monster.name} used {ability_name}, defending against {player_monster.name}'s next attack."
              )
          else:
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
          print(f"{wild_monster.name} is stunned and cannot move!")

        # At the end of each turn
        wild_monster.end_turn_update()

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
        'monster': spawn_monster('Pinne Fawn')
    },
    'darker forest': {
        'description':
        'You are in a darker forest. There is a path to the south and east.',
        'exits': {
            'south': 'forest',
            'east': 'cave',
            'start': 'start',
        },
        'monster': spawn_monster('Wild Forest Monster')
    },
    'cave': {
        'description':
        'You are in a cold, dark cave. There is a path to the west.',
        'exits': {
            'west': 'forest',
        },
        'monster': spawn_monster('Lesser Freezeguin')
    }
}

# Initialize the player
player = Player(input("Welcome Trainer! What is your name? "))

current_room = 'start'

# Game loop
while player.health > 0:
  print(map[current_room]['description'])

  # Encounter and battle with a monster if present
  if map[current_room]['monster']:
    print(f"A wild {map[current_room]['monster'].name} appears!")
    action = input("Do you want to 'fight' or 'leave'? ").lower()
    if action == 'fight':
      # Player battles the monster
      player.battle(map[current_room]['monster'])
    elif action == 'leave':
      print("You choose to leave the monster be.")
    else:
      print("Invalid action.")

  # Print exits of the current room
  print("Exits:")
  for exit_direction in map[current_room]['exits']:
    print(f"- {exit_direction}")

  print()
  
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
