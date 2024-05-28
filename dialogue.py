from utils import *
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
    choice = None
    self.movements = [False, False]
    if state == "Intro":
        rundialogues(self.dialogues["IntroP1(1)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Anyways, what brings you here traveller?",["I have no idea, where am I?", "I was tasked to replace the core"], self.screen)
        rundialogues(self.dialogues["IntroP2(1)"])

    elif state == "TicTacToe":
        if self.canplay:
            rundialogues(self.dialogues["TicTacToeP1(1)"])
            choice = dialoguequestions(self.assets["dialoguebox"], "Do you want to play Tic Tac Toe?", ["Yes", "No"], self.screen)
            if choice == "Yes":
                if self.player.gold >= 500:
                    rundialogues(self.dialogues["TicTacToeP1(1)Extra"])
                    self.play = True
                elif self.player.gold <500:
                    rundialogues(self.dialogues["TicTacToeP2(1)Extra"])
                    pass
            elif choice == "No":
                rundialogues(self.dialogues["TicTacToeP2(1)"])
        else:
            rundialogues(self.dialogues["NoTicTacToe"])

    elif state == "TicTacToeWin":
        rundialogues(self.dialogues["TicTacToeWin"])
        self.maxHP += 3
        self.lives += 3
    
    elif state == "TicTacToeLose":
        rundialogues(self.dialogues["TicTacToeLose"])
        self.player.gold -= 500

    elif state == "TicTacToeDraw":
        rundialogues(self.dialogues["TicTacToeDraw"])
        self.player.gold += 100

    elif state == "Ending":
        rundialogues(self.dialogues["EndingP1(1)"])
        self.player.gold += 1000
        self.load_level("safehouse")
        self.state = "safehouse"

    if state == "Intro2":
        rundialogues(self.dialogues["IntroP1(2)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Are you ready to continue this level?", ["Yes", "No"], self.screen)
        if choice == "Yes":
            rundialogues(self.dialogues["IntroP2(2)"])
        elif choice == "No":
            rundialogues(self.dialogues["IntroP3(2)"])
            self.load_level("safehouse")
            self.state = "safehouse"

    elif state == "Ending2":
        rundialogues(self.dialogues["EndingP1(2)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Are you ready for the next level, soldier?", ["Yes", "No"], self.screen)
        if choice == "Yes":
            rundialogues(self.dialogues["EndingP2(2)"])
            self.load_level("safehouse")
            self.state = "safehouse"
        elif choice == "No":
            rundialogues(self.dialogues["EndingP3(2)"])
            self.load_level("safehouse")
            self.state = "safehouse"

    if state == "Intro3":
        rundialogues(self.dialogues["IntroP1(3)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "ARE YOU READY, SOLDIER?", ["YES, I AM SO READY", "I'm not suree......I'm scared now....."], self.screen)
        if choice == "I'm not suree......I'm scared now.....":
            rundialogues(self.dialogues["IntroP2(3)"])
            self.load_level("safehouse")
            self.state = "safehouse"
    elif state == "Ending3":
        rundialogues(self.dialogues["EndingP1(3)"])