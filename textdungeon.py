player = {
    'health': 100,
    'attack': 10,
    'defense': 5
}

enemy = {
    'name': 'Goblin',
    'health': 20,
    'attack': 8,
    'defense': 2,
    'alive': True
}

rooms = {
    'start': {
        'description': 'You are in the starting room. There\'s a door to the north.',
        'exits': {'north': 'hallway'}
    },
    'hallway': {
        'description': 'You are in a long hallway. There are doors to the north and south.',
        'exits': {'south': 'start', 'north': 'treasure'},
        'enemy': enemy
    },
    'treasure': {
        'description': 'Congratulations! You found the treasure room!',
        'exits': {'south': 'hallway'}
    },
}

def combat(player, enemy):
  while player['health'] > 0 and enemy['health'] > 0:
      action = input('Do you want to "attack" or "defend"? ')

      if action == 'attack':
          damage = max(0, player['attack'] - enemy['defense'])
          enemy['health'] -= damage
          print(f"You dealt {damage} damage to the {enemy['name']}!")

          if enemy['health'] <= 0:
              enemy['alive'] = False
              print(f"You defeated the {enemy['name']}!")
              break

      if action != 'defend':
          player_damage = max(0, enemy['attack'] - player['defense'])
      else:
          player_damage = max(0, enemy['attack'] // 2)

      player['health'] -= player_damage
      print(f"The {enemy['name']} dealt {player_damage} damage to you!")

      if player['health'] <= 0:
          print("You have been defeated!")
          break

      health_status = f"Your health: {player['health']},"
      enemy_status = f"{enemy['name']} health: {enemy['health']}"
      print(health_status, enemy_status)


current_room = 'start'

while True:
    print(rooms[current_room]['description'])

    # Check for enemy encounter
    if 'enemy' in rooms[current_room] and rooms[current_room]['enemy']['alive']:
        print(f"You see a {rooms[current_room]['enemy']['name']}!")
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
