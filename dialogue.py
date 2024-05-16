import pygame, sys, random, math, time
from utils import *
from entities import PhysicsEntity, Player, Enemy, NPC
from tilemap import Tilemap
from clouds import Clouds
from particle import Particle
from spark import Spark
from cutscenes import *

""" 
Put dialogue logic here
state aka the current state of the npc
For example: 
    - Intro
    - TicTacToe
    - etc

For all of the dialogues, remeber to add it into the self.dialogues dictionary in game.py and cutscenes.py

Put elif statements for each state
Inside each state, you can customize how the dialogues work
The main code:
    - get_dialogues(self, "Name of the dialogue", self.dialogues, self.screen)
    - rundialogues(dialogue)
    - dialoguequestions(self.assets["dialoguebox"], "Question", ["Option1", "Option2", "Option3"], self.screen) // Max 3 options

If you want to make it more interactive, such as different dialogues based on the player's choice, you can add more elif statements
Example:
    - If the player chooses "Yes", then the dialogue will be different than if the player chooses "No"
    - You can also add more options, but make sure to add more options in the dialoguequestions function

    choice = dialoguequestions(self.assets["dialoguebox"], "Question", ["Option1", "Option2", "Option3"], self.screen)
    if choice == "Option1":
        dialogue = get_dialogues(self, "Dialogue1", self.dialogues, self.screen)
        rundialogues(dialogue)
    elif choice == "Option2":
        dialogue = get_dialogues(self, "Dialogue2", self.dialogues, self.screen)
        rundialogues(dialogue)
    elif choice == "Option3":
        dialogue = get_dialogues(self, "Dialogue3", self.dialogues, self.screen)
        rundialogues(dialogue)
    else:
        dialogue = get_dialogues(self, "Dialogue4", self.dialogues, self.screen)
        rundialogues(dialogue)

"""

# Include all dialogues here, please make sure the folder name is the same as the dialogue name, and all the dialogues and pictures are paired with numbers
dialogues = load_dialogue()

def init_dialogue(self):
    Dialogues = {
        npc: {str(num): Dialogue(self, self.screen, dialogues[npc][str(num)]) for num in range(len(dialogues[npc]))} for npc in dialogues
    }
    return Dialogues

def dialogue(self, state):
    self.movements = [False, False]
    if state == "Intro":
        rundialogues(self.dialogues["IntroP1(1)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Anyways, what brings you here traveller?",["I have no idea, where am I?", "I was tasked to replace the core"], self.screen)
        rundialogues(self.dialogues["IntroP2(1)"])

    elif state == "TicTacToe":
        rundialogues(self.dialogues["TicTacToeP1(1)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Do you want to play Tic Tac Toe?", ["Yes", "No"], self.screen)
        if choice == "Yes":
            if self.player.gold >= 300:
                self.player.gold -= 300
                rundialogues(self.dialogues["TicTacToeP1(1)"])
                # Add the Tic Tac Toe game here
            elif self.player.gold <300:
                rundialogues(self.dialogues["TicTacToeP2(1)"])
                pass
            else:
                pass
        elif choice == "No":
            rundialogues(self.dialogues["TicTacToeP2(1)"])
            # self.load_level("0")

    elif state == "Ending":
        rundialogues(self.dialogues["EndingP1(1)"])
        # self.player.safehouse()
        pass
