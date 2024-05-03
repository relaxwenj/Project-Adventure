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

def validate_map(data):
    room_names = {room['name'] for room in data['rooms']}
    if len(room_names) != len(data['rooms']):
        print("Error: Duplicate room names found.")
        sys.exit(1)
    
    if data['start'] not in room_names:
        print("Error: Start room does not exist.")
        sys.exit(1)
    
    for room in data['rooms']:
        for exit in room['exits'].values():
            if exit not in room_names:
                print(f"Error: Room '{room['name']}' has an exit to non-existing room '{exit}'.")
                sys.exit(1)

class AdventureGame:
    def __init__(self, map_file):
        self.map = load_map(map_file)
        validate_map(self.map)
        self.current_room = find_room_by_name(self.map['rooms'], self.map['start'])
        self.inventory = []
        self.win_items = {'daisy', 'rose', 'scorpion grasses'}
        self.lose_items = {'insecticide'}

    def describe_room(self):
        print(f"> {self.current_room['name']}\n{self.current_room['desc']}\nExits: {' '.join(self.current_room['exits'].keys())}")
        if 'items' in self.current_room and self.current_room['items']:
            print("Items: " + ", ".join(self.current_room['items']))

    def parse_command(self, command):
        command_parts = command.split(maxsplit=1)
        action = command_parts[0]
        argument = command_parts[1].strip() if len(command_parts) > 1 else ""

        if action == 'go' and argument:
            self.move(argument)
        elif action == 'get' and argument:
            self.get_item(argument)
        elif action == 'drop' and argument:
            self.drop_item(argument)
        elif action == 'look':
            self.describe_room()
        elif action == 'inventory':
            self.show_inventory()
        else:
            print("Sorry, I don't understand that.")

    def move(self, direction):
        if direction in self.current_room['exits']:
            self.current_room = find_room_by_name(self.map['rooms'], self.current_room['exits'][direction])
        else:
            print("There's no way to go that direction.")

    def get_item(self, item):
        if item in self.current_room.get('items', []):
            self.inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} here.")

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.setdefault('items', []).append(item)
            print(f"You drop the {item}.")
            self.check_game_status()
        else:
            print(f"You don't have {item} in your inventory.")

    def check_game_status(self):
        room_items = set(self.current_room.get('items', []))
        if self.win_items.intersection(room_items):
            print("Congratulations! You've successfully planted a flower in the greenhouse and won the game!")
            sys.exit(0)
        if self.lose_items.intersection(room_items):
            print("You have used insecticide in the greenhouse and killed all the plants. You lose the game.")
            sys.exit(0)

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
            try:
                command = input("> What would you like to do? ").strip().lower()
            except EOFError:
                print("\nUse 'quit' to exit.")
                continue
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
