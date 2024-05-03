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
    if len(room_names) != len(data['rooms']):
        sys.stderr.write("Error: Duplicate room names detected.\n")
        return False
    for room in data['rooms']:
        for exit in room['exits'].values():
            if exit not in room_names:
                sys.stderr.write(f"Error: Invalid exit '{exit}' in room '{room['name']}'.\n")
                return False
    return True

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
        self.running = True
        self.room_description_displayed = False 

    def describe_room(self):
        if not self.room_description_displayed:  
            items = ", ".join(self.current_room.get('items', [])) if self.current_room.get('items', []) else "No items"
            print(f"> {self.current_room['name']}\n\n{self.current_room['desc']}\n\nExits: {' '.join(self.current_room['exits'].keys())}\n")
            if items != "No items":
                print(f"Items: {items}\n")
            self.room_description_displayed = True 
    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        print("What would you like to do?\n")

    def parse_command(self, command):
        command = command.strip().lower()
        if command.startswith('go '):
            direction = command[3:].strip()
            self.move(direction)
            print()
        elif command.startswith('get '):
            item = command[4:].strip()
            self.get_item(item)
        elif command == 'inventory':
            self.show_inventory()
        elif command == 'look':
            pass
        elif command == 'quit':
            self.quit_game()
        else:
            print("Sorry, I don't understand that.")

    def move(self, direction):
        if direction in self.current_room['exits']:
            next_room_name = self.current_room['exits'][direction]
            self.current_room = find_room_by_name(self.map['rooms'], next_room_name)
            print(f"You go {direction}.")
            self.room_description_displayed = False  
        else:
            while True:
                print(f"There's no way to go {direction}.")
                new_direction = input("What would you like to do? ").strip().lower()
                if new_direction.startswith('go ') and new_direction[3:].strip() in self.current_room['exits']:
                    self.move(new_direction[3:].strip())
                    break
                else:
                    print("Sorry, you need to 'go' somewhere.")


    def get_item(self, item):
        if item in self.current_room.get('items', []):
            self.inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"Picked up {item}. Inventory now: {self.inventory}")
        else:
            print(f"There's no {item}anywhere.")
            

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        print("What would you like to do?\n")




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
