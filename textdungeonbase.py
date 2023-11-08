# Plenty of resources on Google but here's one, explore around in it a bit!
# Contains plenty of information on Python, link is specifically to dictionaries that we are using.
# https://www.w3schools.com/python/python_dictionaries.asp
# A dictionary {key : value} representing the player's attributes
player = {
    'health': 100,
    'attack': 10,
    'defense': 5,
    # Try adding in XP and levels! Will also need a key with the value being the amount of XP needed to level up.
    'gold': 100,
    'inventory': [] #Contains a list of items
}
# A dictionary representing the player's attributes
enemy = {
    'name': 'Goblin',
    'health': 20,
    'attack': 8,
    'defense': 2,
    'alive': True
}

# Define an NPC with a quest
npc = {
    'name': 'Old Wizard',
    'dialogue': 'Greetings, traveler! The cursed goblins have stolen my magic scroll. Can you retrieve it for me?',
    'quest': {
        'description': 'Retrieve the magic scroll from the goblins.',
        'completed': False
    },
    'reward': {
        'xp': 100,
        'items': [{'name': 'Magic Wand', 'type': 'attack', 'value': 5, 'cost': 100}],
        'gold': 50
    }
}

# Example items, try adding more items!
health_potion = {'name': 'Health Potion', 'type': 'heal', 'value': 20, 'cost': 30}

# Shop inventory, try creating a shop room! (Hint: still a 'key' : value pair)
shop_inventory = [health_potion]

# Define a dictionary of rooms in the game, each with descriptions and exits
# Use a flow chart site like https://www.lucidchart.com/ to have a clear idea of your rooms layout
rooms = {
    'start': {
        'description': 'You are in the starting room. There\'s a door to the north.',
        'exits': {'north': 'hallway'}
    },
    'hallway': {
        'description':
        'You are in a long hallway. There are doors to the north and south.',
        'exits': {
            'south': 'start',
            'north': 'hallwaytwo'
        },
        'enemy': enemy
    },
    # Define a room with an NPC
    'wizard_hut' : {
        'description': 'An old wizard appears to be in deep thought here.',
        'npc': npc
        # Add in exits
    },
    'hallwaytwo': {
        'description':
        'You are in a long hallway. There are doors to the north and south.',
        'exits': {
            'south': 'hallway',
            'north': 'treasure',
        },
        # Another way to implement enemies into the game without declaring a variable earlier
        'enemy': {
          'name': 'Orc',
          'health': 30,
          'attack': 10,
          'defense': 2,
          'alive': True
      }
    },
    'treasure': {
        'description': 'Congratulations! You found the treasure room!',
        'exits': {'south': 'hallway'}
    },
}

# Combat function that takes player and enemy dictionaries as parameters
def combat(player, enemy):
# The fight continues as long as both have more than 0 health
  while player['health'] > 0 and enemy['health'] > 0:
      # Ask the player for their action
      action = input('Do you want to "attack" or "defend"? ')

      # If the player chooses to attack, calculate damage and update the enemy's health
      if action == 'attack':
          # We use the max() function in case the player's attack is somehow less than the enemy's defense.
          damage = max(0, player['attack'] - enemy['defense'])
          # Deal damage to the enemy's health
          enemy['health'] -= damage
          print(f"You dealt {damage} damage to the {enemy['name']}!")

          # Check if the enemy has been defeated
          if enemy['health'] <= 0:
              enemy['alive'] = False
              print(f"You defeated the {enemy['name']}!")
              #Add to XP however much XP this enemy is worth
              check_level_up(player)
              break # Exit the combat loop if the enemy is defeated

      # If the player didn't choose to defend, calculate the full damage from the enemy's attack
      if action != 'defend':
          player_damage = max(0, enemy['attack'] - player['defense'])
      # If the player chooses to defend, reduce the damage taken by half
      else:
          player_damage = max(0, enemy['attack'] // 2)

      # Update the player's health after taking damage
      player['health'] -= player_damage
      print(f"The {enemy['name']} dealt {player_damage} damage to you!")

      # Check if the player has been defeated
      if player['health'] <= 0:
          print("You have been defeated!")
          break # Exit the combat loop if the player is defeated

      # Show current health statuses after the round of combat
      health_status = f"Your health: {player['health']},"
      enemy_status = f"{enemy['name']} health: {enemy['health']}"
      print(health_status, enemy_status)
      
# Levels the player up and increases their stats
def check_level_up(player):
  if player['xp'] >= player['xp_to_level']:
    player['level'] += 1
    player['xp'] = 0  # Reset XP
    player['xp_to_level'] *= 2  # Increase XP needed for next level
    player['health'] += 20 # Increase player stats
    player['attack'] += 5
    player['defense'] += 5
    print(f"You've leveled up to level {player['level']}!")

# Initialize the current_room variable to the starting room
current_room = 'start'

# Start the main game loop
while True:
    # Print the description of the current room
    print(rooms[current_room]['description'])

    # Todo: Add shop logic

    # Check if there is an NPC in the room
    if 'npc' in rooms[current_room]:
        print(f"You see {rooms[current_room]['npc']['name']}.")
        action = input('Do you want to "talk" to the NPC or "leave"? ')

        # After enemy defeat
        if 'quest' in player and not player['quest']['completed']:
            # Check if the conditions are met (e.g., a specific enemy was defeated)
            player['quest']['completed'] = True
            print("You have completed the quest!")
            
            # Grant quest rewards
            player['xp'] += npc['reward']['xp']
            player['gold'] += npc['reward']['gold']
            player['inventory'].extend(npc['reward']['items'])
        
        if action == 'talk':
            print(rooms[current_room]['npc']['dialogue'])
            quest_action = input('Will you "accept" the quest? (yes/no) ')
            if quest_action == 'yes':
                player['quest'] = rooms[current_room]['npc']['quest']
                print(f"Quest accepted: {player['quest']['description']}")

    #Check if there's an enemy in the current room and if it's alive
    if 'enemy' in rooms[current_room] and rooms[current_room]['enemy']['alive']:
        print(f"You see a {rooms[current_room]['enemy']['name']}!")
        combat(player, rooms[current_room]['enemy']) # Start combat function
        if player['health'] <= 0:
            print("Game Over!")  #End the game if the player has been defeated
            break
            
    # Ask the player what they want to do next      
    action = input('Which direction will you go? (or type "quit" to exit) ')

    # Move to the next room if the direction is valid
    if action in rooms[current_room]['exits']:
        current_room = rooms[current_room]['exits'][action]
    elif action == 'quit':
        print('Goodbye!') # End the game if the player decides to quit
        break
    # Handle the case where the player inputs an invalid direction
    else:
        print('Invalid direction.')
