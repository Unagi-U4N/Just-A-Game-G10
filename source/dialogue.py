from source.utils import *
from source.cutscenes import *
from source.ttt import *
from source.startscreen import *

# Include all dialogues here, please make sure the folder name is the same as the dialogue name, and all the dialogues and pictures are paired with numbers
dialogues = load_dialogue()

def init_dialogue(self):
    Dialogues = {
        npc: {str(num): Dialogue(self, self.shakescreen, dialogues[npc][str(num)]) for num in range(len(dialogues[npc]))} for npc in dialogues
    }
    return Dialogues

def dialogue(self, state):
    choice = None
    self.movements = [False, False]
    if state == "Intro":
        rundialogues(self, self.dialogues["IntroP1(1)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Anyways, what brings you here traveller?",["I have no idea, where am I?", "I was tasked to replace the core"], self.shakescreen)
        rundialogues(self, self.dialogues["IntroP2(1)"])

    elif state == "TicTacToe":
        if self.canplay:
            rundialogues(self, self.dialogues["TicTacToeP1(1)"])
            choice = dialoguequestions(self.assets["dialoguebox"], "Do you want to play Tic Tac Toe?", ["Yes", "No"], self.shakescreen)
            if choice == "Yes":
                if self.player.gold >= 500:
                    rundialogues(self, self.dialogues["TicTacToeP1(1)Extra"])
                    self.play = True
                elif self.player.gold <500:
                    rundialogues(self, self.dialogues["TicTacToeP2(1)Extra"])
                    pass
            elif choice == "No":
                rundialogues(self, self.dialogues["TicTacToeP2(1)"])
        else:
            rundialogues(self, self.dialogues["NoTicTacToe"])

    elif state == "TicTacToeWin":
        rundialogues(self, self.dialogues["TicTacToeWin"])
        self.player.HP += 2
        self.HP = self.player.HP
        self.maxHP = self.player.HP
    
    elif state == "TicTacToeLose":
        rundialogues(self, self.dialogues["TicTacToeLose"])
        self.player.gold -= 500

    elif state == "TicTacToeDraw":
        rundialogues(self, self.dialogues["TicTacToeDraw"])
        self.player.gold += 100

    elif state == "Ending":
        rundialogues(self, self.dialogues["EndingP1(1)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Enter safehouse?", ["Yes", "No"], self.shakescreen)
        if choice == "Yes":
            self.player.gold += 1000*int(self.level)
            self.prevlevel = self.level
            self.level = "safehouse"
            self.load_level(self.level)
            self.state = "safehouse"
        elif choice == "No":
            rundialogues(self, self.dialogues["EndingP2(1)"])

    elif state == "Intro2":
        rundialogues(self, self.dialogues["IntroP1(2)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Are you ready to continue this level?", ["Yes", "No"], self.shakescreen)
        if choice == "Yes":
            rundialogues(self, self.dialogues["IntroP2(2)"])
        elif choice == "No":
            rundialogues(self, self.dialogues["IntroP3(2)"])
            self.level = "safehouse"
            self.load_level(self.level)
            self.state = "safehouse"

    elif state == "Ending2":
        rundialogues(self, self.dialogues["EndingP1(2)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Are you ready for the next level, soldier?", ["Yes", "No"], self.shakescreen)
        if choice == "Yes":
            rundialogues(self, self.dialogues["EndingP2(2)"])
            self.player.gold += 1000*int(self.level)
            self.prevlevel = self.level
            self.level = "safehouse"
            self.load_level(self.level)
            self.state = "safehouse"
        elif choice == "No":
            rundialogues(self, self.dialogues["EndingP3(2)"])

    elif state == "Intro3":
        rundialogues(self, self.dialogues["IntroP1(3)"])
        choice = dialoguequestions(self.assets["dialoguebox"], "ARE YOU READY, SOLDIER?", ["YES, I AM SO READY", "I'm not suree......I'm scared now....."], self.shakescreen)
        if choice == "I'm not suree......I'm scared now.....":
            rundialogues(self, self.dialogues["IntroP2(3)"])
            self.level = "safehouse"
            self.load_level(self.level)
            self.state = "safehouse"
    elif state == "Ending3":
        rundialogues(self, self.dialogues["EndingP1(3)"])
        self.game.startscreen = StartScreen(self.game)
        self.game.loaded = False
        self.game.state = "start"
        # self.load_level(self.level)
        # self.state = "safehouse"

    elif state == "Proceed":
        rundialogues(self, self.dialogues["Proceed"])
        choice = dialoguequestions(self.assets["dialoguebox"], "Are you ready to proceed?", ["Yes", "No"], self.shakescreen)
        if choice == "Yes":
            rundialogues(self, self.dialogues["Proceed2"])
            self.level = "safehouse"
            self.load_level(self.level)
            self.state = "safehouse"
            choice = dialoguequestions(self.assets["dialoguebox"], "Please choose a level", ["Level 1", "Level 2", "Level 3"], self.shakescreen)
            rundialogues(self, self.dialogues["Proceed1"])
            if choice == "Level 1":
                self.level = "1"
                self.load_level(self.level)
                self.state = "game"
            elif choice == "2":
                self.level = "2"
                self.load_level(self.level)
                self.state = "level2"
            elif choice == "3":
                self.level = "3"
                self.load_level(self.level)
                self.state = "game"
        elif choice == "No":
            rundialogues(self, self.dialogues["Proceed3"])