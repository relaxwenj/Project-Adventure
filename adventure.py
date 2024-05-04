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
        # Define winning and losing items
        self.win_items = {'daisy', 'rose', 'scorpion grasses'}
        self.lose_items = {'insecticide'}

    def describe_room(self):
        if not self.room_description_displayed:  
            items = ", ".join(self.current_room.get('items', [])) if self.current_room.get('items', []) else "No items"
            print(f"> {self.current_room['name']}\n\n{self.current_room['desc']}\n")
            if items != "No items":
                print(f"Items: {items}\n")
            print(f"Exits: {' '.join(self.current_room['exits'].keys())}\n")
            self.room_description_displayed = True 

    # Extra feature for droping
    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.setdefault('items', []).append(item)
            print(f"You drop the {item}.")
            self.check_game_status()
        else:
            print(f"You don't have {item} in your inventory.")

    # Extra feature for winning or losing conditions
    def check_game_status(self):
        if self.current_room['name'] == "A greenhouse":
            room_items = set(self.current_room.get('items', []))
            if self.win_items.intersection(room_items):
                print("Congratulations! You've successfully planted a flower in the greenhouse and won the game!")
                self.quit_game()
            elif self.lose_items.intersection(room_items):
                print("You have used insecticide in the greenhouse and killed all the plants. You lose the game.")
                self.quit_game()


    def parse_command(self, command):
        command = command.strip().lower()
        if command == 'go':
            print("Sorry, you need to 'go' somewhere.")
        elif command.startswith('go '):
            direction = command[3:].strip()
            self.move(direction)
        elif command.startswith('get'):
            if len(command.split()) == 1:
                print("Sorry, you need to 'get' something.")
            else:
                item = command[4:].strip()
                self.get_item(item)
        elif command.startswith('drop'):
            if len(command.split()) == 1:
                print("Sorry, you need to 'drop' something.")
            else:
                item = command[5:].strip()
                self.drop_item(item)
        elif command == 'inventory':
            self.show_inventory()
        elif command == 'look':
            self.describe_room()
            self.room_description_displayed = False 
        elif command == 'quit':
            self.quit_game()
        elif command == 'unlock':
            print("You have to choose one door to unlock it.")
        elif command.startswith('unlock '):
            direction = command[7:].strip()
            self.unlock(direction)
        elif command == 'lock':
            print("You have to choose one door to lock it.")
        elif command.startswith('lock '):
            direction = command[5:].strip()
            self.lock(direction)
        else:
            print("Sorry, I don't understand that.")


    def move(self, direction):
        if direction in self.current_room['exits']:
            if "locked" in self.current_room and self.current_room['locked'].get(direction, False):
                print(f"The door to the {direction} is locked. Please unlock it first.")
            else:
                next_room_name = self.current_room['exits'][direction]
                self.current_room = find_room_by_name(self.map['rooms'], next_room_name)
                print(f"You go {direction}.")
                print()
                self.room_description_displayed = False
        else:
            print(f"There's no way to go {direction}.")
            self.room_description_displayed = True


    def get_item(self, item):
        if item in self.current_room.get('items', []):
            self.inventory.append(item)
            self.current_room['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} anywhere.")
            

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    # Extra feature for unlocking
    def unlock(self, direction):
        if direction in self.current_room['exits']:
            if "locked" in self.current_room and direction in self.current_room['locked']:
                self.current_room['locked'][direction] = False
                print(f"You have unlocked the door to the {direction}.")
            else:
                print(f"There is no lock on the door to the {direction}.")
        else:
            print(f"There is no door in the {direction} direction.")

    # Extra feature for locking
    def lock(self, direction):
        if direction in self.current_room['exits']:
            if "locked" in self.current_room:
                self.current_room['locked'][direction] = True
                print(f"You have locked the door to the {direction}.")
            else:
                self.current_room['locked'] = {direction: True}
                print(f"You have locked the door to the {direction}.")
        else:
            print(f"There is no door in the {direction} direction.")


    def quit_game(self):
        print("Goodbye!")
        self.running = False

    def run(self):
        while self.running:
            self.describe_room()
            command = input("What would you like to do? ").strip().lower()
            self.parse_command(command)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    else:
        game = AdventureGame(sys.argv[1])
        game.run()
