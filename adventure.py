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
        # if command.startswith('go '):
        #     self.move(command[3:])
        if command.startswith('go'):
            direction = command[3:].strip()  # Trim whitespace from the direction
            if direction:  # Check if there's an actual direction provided
                self.move(direction)
            else:
                print("Sorry, you need to 'go' somewhere.")
        elif command == 'look':
            self.describe_room()
        # elif command.startswith('get '):
        #     self.get_item(command[4:])
        elif command.startswith('get'):
            item = command[4:].strip()  
            if item:  # Check if there's an actual item name provided
                self.get_item(item)
            else:
                print("Sorry, you need to 'get' something.")
        elif command == 'inventory':
            self.show_inventory()
        else:
            print("Sorry, I don't understand that.")

    def move(self, direction):
        current_exits = self.current_room['exits']
        if direction in current_exits:
            self.current_room = find_room_by_name(self.map['rooms'], current_exits[direction])
            if not self.current_room:
                print("Error: The room you are trying to move to does not exist.")
        else:
            print("There's no way to go that direction.")

    def get_item(self, item):
        if not item.strip():  # Check if the item is empty or just whitespace
            print("Sorry, you need to 'get' something.")
            return
        room_items = self.current_room.get('items', [])
        if item in room_items:
            self.inventory.append(item)
            room_items.remove(item)
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

    # def run(self):
    #     while True:
    #         self.describe_room()
    #         command = input("> What would you like to do? ").strip().lower()
    #         if command == 'quit':
    #             print("Goodbye!")
    #             break
    #         self.parse_command(command)

    def run(self):
        while True:
            self.describe_room()
            try:
                command = input("> What would you like to do? ").strip().lower()
            except EOFError:
                print("\nUse 'quit' to exit.")  # Prompt the user to use 'quit' to exit
                continue  # Continue the game loop
            if command == 'quit':
                print("Goodbye!")
                break  # Break out of the loop to end the game
            self.parse_command(command)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    game = AdventureGame(sys.argv[1])
    game.run()
