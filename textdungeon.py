# Plenty of resources on Google but here's one, explore around in it a bit!
# Contains plenty of information on Python, link is specifically to dictionaries that we are using.
# https://www.w3schools.com/python/python_dictionaries.asp
# A dictionary {key : value} representing the player's attributes
player = {
    'health': 100,
    'attack': 10,
    'defense': 5
}
# A dictionary representing the player's attributes
enemy = {
    'name': 'Goblin',
    'health': 20,
    'attack': 8,
    'defense': 2,
    'alive': True
}

# Define a dictionary of rooms in the game, each with descriptions and exits
rooms = {
    'start': {
        'description': 'You are in the starting room. There\'s a door to the north.',
        'exits': {'north': 'hallway'}
    },
    'hallway': {
        'description': 'You are in a long hallway. There are doors to the north and south.',
        'exits': {'south': 'start', 'north': 'treasure'},
        'enemy': enemy # Reference to the enemy in this room
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
          damage = max(0, player['attack'] - enemy['defense'])
          enemy['health'] -= damage
          print(f"You dealt {damage} damage to the {enemy['name']}!")

          # Check if the enemy has been defeated
          if enemy['health'] <= 0:
              enemy['alive'] = False
              print(f"You defeated the {enemy['name']}!")
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
          break # Exit the combat loop if player is defeated

      # Show current health statuses after the round of combat
      health_status = f"Your health: {player['health']},"
      enemy_status = f"{enemy['name']} health: {enemy['health']}"
      print(health_status, enemy_status)

# Initialize the current_room variable to the starting room
current_room = 'start'

# Start the main game loop
while True:
    # Print the description of the current room
    print(rooms[current_room]['description'])

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
