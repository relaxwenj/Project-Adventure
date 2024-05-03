import sys
import json

def load_map(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: Map file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Map file is not valid JSON.")
        sys.exit(1)

def find_room_by_name(rooms, name):
    for room in rooms:
        if room['name'] == name:
            return room
    return None

class AdventureGame:
    def __init__(self, map_file):
        self.map = load_map(map_file)
        self.current_room = find_room_by_name(self.map['rooms'], self.map['start'])
        self.inventory = []

    def describe_room(self):
        print(f"> {self.current_room['name']}\n{self.current_room['desc']}\nExits: {' '.join(self.current_room['exits'].keys())}")
        if 'items' in self.current_room and self.current_room['items']:
            print("Items: " + ", ".join(self.current_room['items']))

    def parse_command(self, command):
        command = command.strip().lower()
        if command.startswith('go '):
            direction = command[3:].strip()
            self.move(direction)
        elif command.startswith('get '):
            item = command[4:].strip()
            self.get_item(item)
        elif command == 'inventory':
            self.show_inventory()
        elif command == 'look':
            self.describe_room()
        else:
            print("Sorry, I don't understand that.")

    def move(self, direction):
        if direction in self.current_room['exits']:
            next_room = self.current_room['exits'][direction]
            self.current_room = find_room_by_name(self.map['rooms'], next_room)
            print(f"Moved to {self.current_room['name']}.")  # Debugging output
        else:
            print(f"There's no way to go {direction}.")

    def get_item(self, item):
        if item in self.current_room.get('items', []):
            self.inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"You pick up the {item}.")  # Debugging output
        else:
            print(f"There's no {item} here.")

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def run(self):
        while True:
            self.describe_room()
            command = input("> What would you like to do? ").strip().lower()
            if command == 'quit':
                print("Goodbye!")
                break
            self.parse_command(command)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    game = AdventureGame(sys.argv[1])
    game.run()
