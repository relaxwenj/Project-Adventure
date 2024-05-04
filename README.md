# Project-Adventure

# your name and Stevens login:

Jing Wen jwen11@stevens.edu

2. the URL of your public GitHub repo:

https://github.com/relaxwenj/Project-Adventure

3. an estimate of how many hours you spent on the project:

Around 18 hours. I used around 10 hours to understand the promp, set up the map, and twirte the code. Around 5 hours to test run and debug. Around 2 hours to write the README.md

4. a description of how you tested your code:

Combine autograder and manually test. I set up different maps while testing my code. Also, I compared every verb's output
with the canvas' example.

5. any bugs or issues you could not resolve:

NO.

6. an example of a difficult issue or bug and how you resolved:

One tough problem I encountered was handling command parsing. Initially, I used startswith to simplify command parsing, but this method didn't work well for commands like "go" when entered without additional text, which should result in an error message. To solve this, I had to split the command into different situations. For commands like "get" and "drop", I continued using startswith but added a check if len(command.split()) == 1: to determine if any text followed the command. For "go", "lock", and "unlock", I used a strict equality condition to judge whether a command was entered without necessary additional information. These methods were used in the same function to help effectively parse and respond to user inputs. It also reminded me that I need to carefully handle verb commands and consider all possible scenarios to ensure they are properly addressed.

7. a list of the three extensions you’ve chosen to implement, with appropriate detail on them for the CAs to evaluate them (i.e., what are the new verbs/features, how do you exercise them, where are they in the map.
   
# A "drop" verb. 
This extension enables users to remove an item from their inventory and place it in the current room. Users can only drop items that they currently have. 

To test it, first, I obtain some items from the room, and then I use the "drop" command which calling the drop_item function in my code to append the items into map's rooms list, under items object. I utilize the inventory to verify successfully dropping items, and use "look" to check if that they can be successfully dropped in any room.

# Locked door. 
I have added two functions, "lock" and "unlock," to my code. These functions allow users to lock or unlock any door in the room without using any items. Additionally, I have configured the maps to include "locked" objects that indicate some doors in some direction are locked upon entering the room. If users want to access a door that is originally locked, they must first unlock it.

To test it, I randomly choose a door in the room, then I type "lock + direction" to lock the door. If I then attempt to "go + direction," it will display the message, "The door is locked, you must unlock it" to proceed in that direction. After I type "unlock + direction," I can successfully pass through the door. The maps will also shows which doors in loocked by default. In my maps, if the door is locked, the description of that room will show "This room is XXX. The west door is locked.". Users have to unlock it to access the door.

# Winning and losing conditions.
I have added winning and losing conditions to my code. The winning condition is achieved when users drop any type of plant in a specific room—"A greenhouse." The losing condition is triggered when users drop "insecticide." If players win or lose, the game will immediately terminate, displaying either "Congratulations! You've successfully planted a flower in the greenhouse and won the game!" or "You have used insecticide in the greenhouse and killed all the plants. You lose the game." I have added a "A greenhouse" room into the map to ensure the presence of the winning or losing room. In my code, I have also defined the winning items as {'daisy', 'rose', 'scorpion grasses'} and the losing item as {'insecticide'}.

To test it, I will pick up some winning items and attempt to reach "A greenhouse." If the item is one of the winning items I have defined in my code, and I drop it in that room, I will win the game. If I pick up the 'insecticide' and drop it into "A Greenhouse," I will lose the game. Dropping items in any room other than "A greenhouse" will not affect the outcome of the game.
