import pygame, sys, random, math, time
from utils import *
from entities import PhysicsEntity, Player, Enemy, NPC
from tilemap import Tilemap
from clouds import Clouds
from particle import Particle
from spark import Spark
from cutscenes import *
from ttt import *

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
            if self.player.gold >= 500:
                rundialogues(self.dialogues["TicTacToeP1(1)Extra"])
                self.play = True
            elif self.player.gold <500:
                rundialogues(self.dialogues["TicTacToeP2(1)Extra"])
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
