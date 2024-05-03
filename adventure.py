import sys
import json

def load_map(filename):
    try:
        with open(filename, 'r') as file:
            map_data = json.load(file)
    except FileNotFoundError:
        sys.stderr.write("Error: Map file not found.\n")
        sys.exit(1)
    except json.JSONDecodeError:
        sys.stderr.write("Error: Map file is not valid JSON.\n")
        sys.exit(1)
    
    # Validate map data
    if not validate_map(map_data):
        sys.stderr.write("Error: Invalid map configuration.\n")
        sys.exit(1)
    
    return map_data

def validate_map(data):
    if 'rooms' not in data or 'start' not in data:
        return False
    room_names = {room['name'] for room in data['rooms']}
    if data['start'] not in room_names:
        return False
    for room in data['rooms']:
        for exit in room['exits'].values():
            if exit not in room_names:
                return False
    return True


class AdventureGame:
    def __init__(self, map_file):
        self.map = load_map(map_file)
        if not self.map:
            print("Failed to load the map.")
            self.running = False
        else:
            self.current_room = find_room_by_name(self.map['rooms'], self.map['start'])
            self.inventory = []
            self.running = True

    def describe_room(self):
        if 'items' in self.current_room and self.current_room['items']:
            items = ", ".join(self.current_room['items'])
        else:
            items = "No items"
        print(f"> {self.current_room['name']}\n{self.current_room['desc']}\nExits: {' '.join(self.current_room['exits'].keys())}\nItems: {items}")

    def parse_command(self, command):
        command = command.strip().lower()
        if command.startswith('go '):
            self.move(command[3:].strip())
        elif command.startswith('get '):
            self.get_item(command[4:].strip())
        elif command == 'inventory':
            self.show_inventory()
        elif command == 'look':
            self.describe_room()
        elif command == 'quit':
            self.quit_game()
        else:
            print("Sorry, I don't understand that.")

    def move(self, direction):
        if direction in self.current_room['exits']:
            self.current_room = find_room_by_name(self.map['rooms'], self.current_room['exits'][direction])
            if not self.current_room:
                print("Error: The room you are trying to move to does not exist.")
        else:
            print("There's no way to go that direction.")

    def get_item(self, item):
        if item in self.current_room.get('items', []):
            self.inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} here.")

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def quit_game(self):
        print("Goodbye!")
        self.running = False

    def run(self):
        while self.running:
            self.describe_room()
            command = input("> What would you like to do? ").strip().lower()
            self.parse_command(command)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
    else:
        game = AdventureGame(sys.argv[1])
        game.run()
