# Plenty of resources on Google but here's one, explore around in it a bit!
# Contains plenty of information on Python, link is specifically to dictionaries that we are using.
# https://www.w3schools.com/python/python_dictionaries.asp
# A dictionary is variable = {key : value}

import pickle
import random

# Define an NPC with a quest
npc = {
    'name': 'Old Wizard',
    'dialogue':
    'Greetings, traveler! The cursed goblins have stolen my magic scroll. Can you retrieve it for me?',
    'quest': {
        'description': 'Retrieve the magic scroll from the goblins.',
        'completed': False
    },
    'reward': {
        'xp':
        100,
        'items': [{'name': 'Magic Wand', 'type': 'attack', 'value': 5, 'cost': 100 }],
        'gold': 50
    }
}

# Example items
health_potion = {
    'name': 'Health Potion',
    'type': 'heal',
    'value': 20,
    'cost': 30
}
attack_boost = {
    'name': 'Attack Boost',
    'type': 'attack',
    'value': 5,
    'cost': 50
}

# Shop inventory
shop_inventory = [health_potion, attack_boost]
# To add to inventory
#player['inventory'].append(health_potion)

# This is the rooms which contrains a dictorinary of different rooms, with
# descriptions and enemies in each room. The exits are also stored in a list
# which is linked to the room dict.
rooms = {
    'start': {
        'description':
        'You are in the starting room. There\'s a door to the north.',
        'exits': {
            'north': 'hallway'
        }
    },
    'hallway': {
        'description':
        'You are in a long hallway. There are doors to the north and south.',
        'exits': {
            'south': 'start',
            'north': 'shop',
            'east': 'wizard_hut',
            'west': 'library'
        },
        'enemy': {
          'name': 'Goblin',
          'health': 5,
          'attack': 8,
          'defense': 2,
          'alive': True
      }
    },
    # Define a room with an NPC
    'wizard_hut': {
        'description': 'An old wizard appears to be in deep thought here.',
        'exits': {
            'west': 'hallway',
        },
        'npc': npc
        # Add in exits
    },
      'library': {
        'description': 'Rows upon rows of ancient books surround you.',
        'exits': {
            'east': 'hallway',
        },
        'enemy': {
            'name': 'Cursed Librarian',
            'health': 60,
            'attack': 12,
            'defense': 8,
            'alive': True
        }
    },
    'shop': {
        'description':
        'You are in a shop. There are doors to the north and south.',
        'exits': {
            'south': 'hallway',
            'north': 'hallwaytwo'
        },
        'inventory': shop_inventory
    },
    'hallwaytwo': {
        'description':
        'You are in a long hallway. There are doors to the north and south.',
        'exits': {
            'south': 'shop',
            'north': 'guarded_treasury',
            'east': 'crypt'
        },
        'enemy': {
            'name': 'Orc',
            'health': 30,
            'attack': 10,
            'defense': 2,
            'alive': True
        }
    },
    'crypt': {
        'description':
        'A chilling wind greets you in this dark crypt. Beware of the undead!',
        'exits': {
            'west': 'hallwaytwo'
        },
        'enemy': {
            'name': 'Phantom',
            'health': 80,
            'attack': 15,
            'defense': 5,
            'alive': True
        }
    },
    'closet': {
        'description':
        'You are in a long hallway. There is a door to the north.',
        'exits': {
            'north': 'hallwaytwo'
        },
    },
    'guarded_treasury': {
        'description':
        'Gold and jewels shine brightly, but a dragon guards this room!',
        'exits': {
            'north': 'treasure',
            'south': 'hallwaytwo'
        },
        'enemy': {
            'name': 'Dragon',
            'health': 150,
            'attack': 25,
            'defense': 10,
            'alive': True
        }
    },
    'treasure': {
        'description': 'Congratulations! You found the treasure room!',
        'exits': {
            'south': 'guarded_treasury'
        }
    },
}


def combat(player, enemy):
  while player['health'] > 0 and enemy['health'] > 0:
    action = input('Do you want to "attack", "defend", or "run"? ')

    if action == 'attack' or action == 'a':
      damage = max(0, player['attack'] - enemy['defense'])
      enemy['health'] -= damage
      print(f"You dealt {damage} damage to the {enemy['name']}!")

      if enemy['health'] <= 0:
        enemy['alive'] = False
        print(f"You defeated the {enemy['name']}!")
        # Loot logic
        loot_gold = 20  # or some logic to determine loot amount
        player['gold'] += loot_gold
        print(f"You found {loot_gold} gold on the enemy.")

        # Chance to drop an item
        if random.random() < 1.0:  # 30% chance to drop an item
          loot_item = {
              'name': 'Healing Herb',
              'type': 'heal',
              'value': 10,
              'cost': 10
          }
          player['inventory'].append(loot_item)
          print(f"The enemy dropped a {loot_item['name']}.")

        player['xp'] += 50  # or however much XP this enemy is worth
        print(f"You gained {player['xp']} XP.")
        check_level_up(player)
        break

    if action != 'defend':
      player_damage = max(0, enemy['attack'] - player['defense'])
    else:
      player_damage = max(0, enemy['attack'] // 2)

    player['health'] -= player_damage
    print(f"The {enemy['name']} dealt {player_damage} damage to you!")

    if action == 'run':
      print("You managed to escape!")
      break

    if player['health'] <= 0:
      print("You have been defeated!")
      break

    health_status = f"Your health: {player['health']},"
    enemy_status = f"{enemy['name']} health: {enemy['health']}"
    print(health_status, enemy_status)


def check_level_up(player):
  if player['xp'] >= player['xp_to_level']:
    player['level'] += 1
    player['xp'] = 0  # Reset XP
    player['xp_to_level'] *= 2  # Increase XP needed for next level
    player['health'] += 20
    player['attack'] += 5
    print(f"You've leveled up to level {player['level']}!")


player = {}

# The initialize_player function should create a new player dictionary with default values
def initialize_player():
  # Set up the default player data
  return {
      'health': 100,
      'attack': 10,
      'defense': 5,
      'level': 1,
      'xp': 0,
      'xp_to_level': 100,
      'gold': 100,
      'inventory': [],
      'attack_boost_duration': 0
  }

def initialize_game():
  action = input('Would you like to "load" a game or "start" a new one? ')
  if action == 'load':
    return load_game()  # This will either return a valid game state or (None, '')
  else:
    # If starting a new game or if loading failed, initialize player
    print('Starting a new game...')
    return initialize_player(
    ), 'start'  # Replace with actual player initialization

file_path = 'textrpg.pickle'

def save_game(player, current_room):
  try:
    with open(file_path, 'wb') as file:
      game_state = {'player': player, 'current_room': current_room, 'rooms' : rooms}
      pickle.dump(game_state, file)
      print('Game saved succesfully!')
  except Exception as e:
    print(f"An error occurred while saving the game: {e}")


def load_game():
  try:
    with open(file_path, 'rb') as file:
      game_state = pickle.load(file)
      player = game_state['player']
      current_room = game_state['current_room']
      rooms = game_state['rooms']
      return player, current_room
  except FileNotFoundError:
    print("No saved game found.")
    return None, ''


# Initialize the game (either load a saved game or start a new one)
player, current_room = initialize_game()

# Check if player is None, which indicates loading failed or a new game should be started
if player is None:
  player = initialize_player()  # Make sure this function returns a valid player dictionary
  current_room = 'start'
  #rooms = initialize_rooms()  # Function to create the initial rooms
#else:
    # Use the loaded rooms if available
    #rooms = loaded_rooms if loaded_rooms else initialize_rooms()

def display_player_stats():
  print(f"Level: {player['level']}")
  print(f"XP: {player['xp']}/{player['xp_to_level']}")
  print(f"Health: {player['health']}")
  print(f"Attack: {player['attack']}")
  print(f"Defense: {player['defense']}")
  print(f"Gold: {player['gold']}")
  print(f"Inventory: {player['inventory']}")

def display_inventory():
  if len(player['inventory']) == 0:
    print("Your inventory is empty.")
  else:
    print("Your inventory:")
    

# Main Game Loop
while True:
  print(rooms[current_room]['description'])

  # Print exits of the current room
  print("Exits:")

  # Check if there is an NPC in the room
  if 'npc' in rooms[current_room]:
    print(f"You see {rooms[current_room]['npc']['name']}.")
    # After enemy defeat
    if 'quest' in player and not player['quest']['completed']:
      # Check if the conditions are met (e.g., a specific enemy was defeated)
      player['quest']['completed'] = True
      print("You have completed the quest!")

      # Grant quest rewards
      player['xp'] += npc['reward']['xp']
      player['gold'] += npc['reward']['gold']
      player['inventory'].extend(npc['reward']['items'])

    action = input('Do you want to "talk" to the NPC or "leave"? ')

    if action == 'talk':
      print(rooms[current_room]['npc']['dialogue'])
      quest_action = input('Will you "accept" the quest? (yes/no) ')
      if quest_action == 'yes':
        player['quest'] = rooms[current_room]['npc']['quest']
        print(f"Quest accepted: {player['quest']['description']}")

  # If the player is in the shop
  if current_room == 'shop':
    print("Items available:")
    for idx, item in enumerate(rooms['shop']['inventory']):
      print(f"{idx+1}. {item['name']} - {item['cost']} gold")

    action = input('Do you want to "buy [item number]" or "leave"? ')

    if action.startswith('buy'):
      item_idx = int(action.split(' ')[1]) - 1  # Convert user input to item index
      item_to_buy = rooms['shop']['inventory'][item_idx]

      if player['gold'] >= item_to_buy['cost']:
        player['gold'] -= item_to_buy['cost']
        player['inventory'].append(item_to_buy)
        print(f"You bought {item_to_buy['name']}!")
      else:
        print("You don't have enough gold.")

  # Check for enemy encounter
  if 'enemy' in rooms[current_room] and rooms[current_room]['enemy']['alive']:
    print(f"You see a {rooms[current_room]['enemy']['name']}!")
    # Pass in player and enemy in the room we are currently in.
    combat(player, rooms[current_room]['enemy'])
    if player['health'] <= 0:
      print("Game Over!")
      break

  action = input('Which direction will you go? (or type "quit" to exit) ')

  if action in rooms[current_room]['exits']:
    current_room = rooms[current_room]['exits'][action]
  elif action == 'quit':
    print('Goodbye!')
    break
  else:
    print('Invalid direction.')

  if (action == 'save'):
    save_game(player, current_room)

  if(action == 'check stats'):
    display_player_stats()

  if(action == 'check inv'):
    display_inventory()
