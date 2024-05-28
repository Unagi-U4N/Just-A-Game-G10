# Some of the python files are not complete yet, to test them please comment out the parts that are undone
# Undone part used in this file: Tilemap, Clouds


from tkinter import font
import pygame, sys, random, math
from utils import *
from entities import Player, Enemy, NPC
from tilemap import Tilemap
from clouds import Clouds
from particle import Particle
from spark import Spark
import dialogue
from music import Music
from ttt import *
from playerprofile import *

class Play():
    def __init__(self, game):

        # data = [playername, level, gold, speed, HP]
        pygame.init()
        self.mousepos = (0, 0)
        self.pausetimer = 50
        self.e = False
        self.clickpause = False
        self.enemykill = True
        self.leafkill = True
        self.choice = ""
        self.pause = False
        self.sfx = game.sfx
        self.game = game
        self.winner = None
        self.screen = game.screen
        self.display = game.display
        self.assets = game.assets
        self.dialogues = dialogue.init_dialogue(self)
        self.cutscenes = game.cutscenes
        self.clouds = Clouds(self.assets["clouds"], 16)
        self.player = Player(game, (0, 0))
        self.ttt = TicTacToe(self)
        self.playerrespawn = (0, 0)
        self.render_scroll = (0, 0)
        self.tilemap = Tilemap(game, tile_Size=32)
        self.font = game.font
        self.bg = self.assets["day"]
        self.sfx = game.sfx
        self.level = 0
        self.current_level = 0
        self.upgrade_choice = 0
        self.store = False
        self.store_state = "store"
        self.max_heart = 15
        self.max_speed = 4
        self.store_addsub_heart = 0
        self.store_addsub_speed = 0
        self.store_clickcooldown = 20
        self.state = "game"
        self.profile = PlayerProfile(game)
        self.savetimer = 0
        self.reasonofdeath = None
        self.transitioning = True
        self.transition = 0
        self.transition_timer = 0
        self.transition_ed = True
        self.results = ""
        self.felltransition = 0
        self.play = False
        self.canplay = True
        self.deductlife = True
        self.playedwaste = False
        self.restart = False
        self.shut = False
        self.respawn = False
        self.font = pygame.font.Font(self.game.font, 36)
        self.font2 = pygame.font.Font(self.game.font, 50)
        self.deadmsg = ""
        self.death_msg = {
            "fall" : ["You ignored physics class", "You thought you were superman", "So this is the FALLEN angel?", "Just a reminder you're not a bird"],
            "enemy" : ["You were killed by an enemy", "Unfortunately you are not bulletproof", "You were too weak", "You were too fragile", "You thought bullet was friendly", "Stop playing, touch grass"],
        }

        # self.load_level(self.level)

    def interact(self):
        for npc in self.npc:
            if self.player.rect().colliderect(npc.interact):           
                render_text("Press E", pygame.font.Font(self.game.font, 40), (0, 0, 0), 600, 550, self.display)
                if self.e:
                    if not npc.not_dialogue:
                        return npc.name
                    else:
                        return "Store"
    
    def load(self, data):
        self.player.updateprofile(data)
        self.level = data[1]
        self.maxHP = self.player.HP
        self.lives = self.player.HP
        self.speed = self.player.speed
        self.load_level(self.level)

    def check_button(self):
        # Check if the pause or info button is clicked
        pause = render_img(self.assets["pausebuttonround"], 70, 70, self.display, True, True)
        info = render_img(self.assets["info"], 140, 70, self.display, True, True)

        self.clickpause = True
        if pause:
            if self.pausetimer > 50:
                self.pause = not self.pause

                self.choice = "pause"
                self.pausetimer = 0
        elif info:
            if self.pausetimer > 50:
                self.pause = not self.pause
                self.choice = "info"
                self.pausetimer = 0

        # Limit the button to be clicked once every 50 frames
        if self.clickpause:
            self.pausetimer += 1

    def load_level(self, map_id):       

        if map_id == "1":
            self.bg = self.assets["day"]

        elif map_id == "2":
            self.bg = self.assets["night"]

        elif map_id == "safehouse":
            self.bg = self.assets["safehousebg"]

        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 20 + tree["pos"][1], 23, 13))
        
        self.enemies = []
        
        self.npc = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1), ("spawners", 2), ("spawners", 3), ("spawners", 4)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                self.player.air_time = 0
            elif spawner["variant"] == 1:
                self.enemies.append(Enemy(self, spawner["pos"], (16, 30), difficulty=1)) # Scaled
            elif spawner["variant"] == 2:
                self.enemies.append(Enemy(self, spawner["pos"], (16, 30), difficulty=2))
            elif spawner["variant"] == 3:
                self.enemies.append(Enemy(self, spawner["pos"], (16, 30), difficulty=3))
            elif spawner["variant"] == 4:
                self.npc.append(NPC(self, spawner["pos"], (16, 30), ""))

        # Assign names to the npcs
        self.npc.sort(key=lambda x: x.pos[0])
        for i, npc in enumerate(self.npc):
            if i == 0 and map_id == "test":
                npc.name = "Intro"
            elif i == 1 and map_id == "test":
                npc.name = "TicTacToe"
            elif i == 2 and map_id == "test":
                npc.name = "Ending"
            elif i == 0 and map_id == "safehouse":
                npc.not_dialogue = True
                npc.name = "Store"

        # Deals with offset, when the player moves, everything moves in the opposite direction to make the illusion that the player is moving
        self.scroll = [0, 0]
        self.dead = 0 
        self.firsthit = False
        self.deadscreen = False
        self.deadscreentrans = 0

        self.movements = [False, False]

        if self.game.particles is not None:
            self.game.particles.clear()
        self.particles = self.game.particles

        if self.game.sparks is not None:
            self.game.sparks.clear()
        self.sparks = self.game.sparks

        if self.game.projectiles is not None:
            self.game.projectiles.clear()
        self.projectiles = self.game.projectiles

        if self.game.exclamation is not None:
            self.game.exclamation.clear()
        self.exclamation = self.game.exclamation

    def update(self):

        # Update the game, the particles, enemies, npc, player

        # Make sure that the player is always in the middle of the screen
        self.scroll[0] += (self.player.pos[0] - self.scroll[0] - 600) / 20
        self.scroll[1] += (self.player.pos[1] - self.scroll[1] - 337.5) / 20
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.clouds.update()
        self.player.update(self.tilemap ,((self.movements[1] - self.movements[0]) * self.speed, 0)) # update(self, tilemap, movement=(0,0))

        for npc in self.npc:
            npc.update(self.tilemap, (0, 0))

        for enemy in self.enemies.copy():
            self.enemykill = enemy.update(self.tilemap, (0, 0))
            if self.enemykill:
                self.enemies.remove(enemy)
                self.lives = min(self.maxHP, self.lives + 1)
                self.player.gold += 100

        # Get the latest solid tiles the player is stepping on as the latest respawn point
        if self.player.latest_block is not None:
            self.playerrespawn = (self.player.latest_block.x + 8, self.player.latest_block.y)

        # [[x, y], direction, timer]
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
              
            # Check if the projectile hits a solid tile
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random(), (255,0,0)))
            
            # Check if the projectile is out of bounds
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)

            # Check if the projectile hits the player, when the player is not dashing
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    self.sfx['shoot'].play()
                    if self.lives > 1 and not self.dead:
                        self.lives -= 1

                    elif not self.firsthit and self.lives == 1:
                        self.dead += 1
                        if self.reasonofdeath is None:
                            self.reasonofdeath = "enemy"
                            self.deadmsg = random.choice(self.death_msg[self.reasonofdeath])
                        self.firsthit = True
                    self.projectiles.remove(projectile)
                    for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random(), (255,0,0)))
                        self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

        for particle in self.particles.copy():
            kill = particle.update()
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

        for spark in self.sparks.copy():
            kill = spark.update()
            if kill:
                self.sparks.remove(spark)
        
    def death(self):

        # Death logic
        if self.transition < 0:
            self.transition += 1

        if self.felltransition < 0:
            self.felltransition += 1
        
        # Respawn transition
        if self.lives > 1 and self.deductlife and self.player.airtime() and not self.dead:
            self.player.air_time = 0
            self.deductlife = False
            self.respawn = True
            self.lives -= 1

        # Dead screen transition
        if self.dead or self.player.airtime() and self.lives == 1:
            self.deadscreen = True
            self.dead += 1
            if self.reasonofdeath is None:
                self.reasonofdeath = "fall"
                self.deadmsg = random.choice(self.death_msg[self.reasonofdeath])
            self.deadscreentrans = min(200, self.deadscreentrans + 3)

        # Load dead screen
        if self.deadscreen:
            self.movements = [False, False]
            if not self.playedwaste and not self.respawn:
                self.playedwaste = True   
                self.sfx['wasted'].play()
            img = pygame.Surface((1200, 675))
            img.fill((0,0,0))
            img.set_alpha(self.deadscreentrans)
            self.display.blit(img, (0,0))

            if self.dead > 135 and not self.respawn:
                render_text("Wasted", pygame.font.Font(self.game.font, 110), (255, 0, 0), 600, 250, self.display)
                render_text(self.deadmsg, pygame.font.Font(self.game.font, 50), (255, 255, 255), 600, 300, self.display)
                render_text("Press SPACE to restart", pygame.font.Font(self.game.font, 50), (255, 255, 255), 600, 600, self.display)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.dead > 135:
                                self.restart = True

            else:
                pygame.event.clear()
            
            # Restart the game
            if self.restart:
                self.transition += 1
                if self.transition > 75:
                    self.lives = self.maxHP
                    self.player.gold = max(0, self.player.gold - 100)
                    self.dead = 0
                    self.firsthit = False
                    self.deadscreen = False
                    self.deadmsg = ""
                    self.reasonofdeath = None
                    self.load_level(self.level)
                    self.playedwaste = False
                    self.restart = False
                    self.sfx['wasted'].stop()
                    self.transition = -75
                    self.shut = False
                    # self.game.sfx['ambience'].play(-1)

            # Load respawn screen
        if self.respawn:
            self.felltransition += 1
            if self.felltransition > 60:
                self.player.pos = self.playerrespawn
                self.deductlife = True
                self.respawn = False
                self.felltransition = -60

    def paused(self):

        # Pause screen
            
        img=pygame.Surface((1200, 675))
        img.fill((0,0,0))
        img.set_alpha(150)
        self.display.blit(img, (0,0))
        if self.choice == "pause":
            render_img(self.assets["pause"], 0, 0, self.display, centered=False)
            quit = render_img(self.assets["quit"], 600, 400, self.display, True, True, self.assets["quit2"])
            resume = render_img(self.assets["resume"], 600, 300, self.display, True, True, self.assets["resume2"])

            if resume:
                self.pause = not self.pause
            if quit:
                pygame.quit()
                sys.exit()

        elif self.choice == "info":
            render_img(self.assets["controls"], 0, 0, self.display, centered=False)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                 
    def userinput(self):
        # This part will check the controls of the player

        self.mousepos = pygame.mouse.get_pos()

        if not self.dead and not self.pause and not self.play and not self.store and not self.transitioning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.choice = "pause"
                        self.pause = not self.pause
                    if event.key == pygame.K_a:
                        self.movements[0] = True
                    if event.key == pygame.K_d:
                        self.movements[1] = True
                    if event.key == pygame.K_w:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_SPACE:
                        self.player.dash()
                    if event.key == pygame.K_e:
                        self.e = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movements[0] = False
                    if event.key == pygame.K_d:
                        self.movements[1] = False
                    if event.key == pygame.K_e:
                        self.e = False

        elif self.store:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.store_state == "store":
                            self.store = False
                        elif self.store_state == "store_menu":
                            self.store_state = "store"
                        elif self.store_state == "store_heart" or self.store_state == "store_speed":
                            self.store_addsub_speed = 0
                            self.store_addsub_heart = 0
                            self.store_state = "store_menu"
                                            
                    if event.key == pygame.K_SPACE:
                        if self.store_state == "store":
                            self.store_state = "store_menu"

                        elif self.store_state == "store_menu":
                            if self.upgrade_choice == 0:
                                self.store_state = "store_heart"
                            elif self.upgrade_choice == 1:
                                self.store_state = "store_speed"

                        elif self.store_state == "store_heart":
                            if self.store_addsub_heart > 0 and self.store_addsub_heart <= self.max_heart - self.maxHP and self.player.gold >= self.store_addsub_heart * 750:
                                self.player.gold -= self.store_addsub_heart * 750
                                self.maxHP += self.store_addsub_heart
                                self.lives += self.store_addsub_heart
                                self.store_state = "store_menu"
                                self.store_addsub_heart = 0

                        elif self.store_state == "store_speed":
                            if self.store_addsub_speed > 0 and self.store_addsub_speed <= self.max_speed - self.player.speed and self.player.gold >= self.store_addsub_speed * 500:
                                self.player.gold -= int(self.store_addsub_speed * 500)
                                self.player.speed += self.store_addsub_speed
                                self.speed = self.player.speed
                                self.store_state = "store_menu"
                                self.store_addsub_speed = 0

                    if event.key == pygame.K_LEFT and self.store_state == "store_menu":
                        self.upgrade_choice = (self.upgrade_choice - 1) % 2
                            
                    if event.key == pygame.K_RIGHT and self.store_state == "store_menu":
                        self.upgrade_choice = (self.upgrade_choice + 1) % 2
        else:
            pygame.event.clear()
            self.movements = [False, False]
        
    def render(self):

        # Render all the assets
        self.clouds.render(self.display, offset=self.render_scroll)
        self.tilemap.render(self.display, offset=self.render_scroll) 

        # Render the enemies
        for enemy in self.enemies:
            if int(enemy.pos[0]) in range(int(self.player.pos[0] - self.display.get_width() / 2 - 100), int(self.player.pos[0] + self.display.get_width() / 2 + 100)):
                enemy.render(self.display, offset=self.render_scroll)
        
        # Render the npcs
        for npc in self.npc:
            npc.render(self.display, offset=self.render_scroll)

        # Render the player
        self.player.render(self.display, offset=self.render_scroll)

         # exclamation mark above enemy heads
        for exclamation in self.exclamation.copy():
            img = self.assets['!']
            if int(exclamation[0]) in range(int(self.player.pos[0] - self.display.get_width() / 2 - 100), int(self.player.pos[0] + self.display.get_width() / 2 + 100)):
                self.display.blit(img, (exclamation[0] - img.get_width() / 2 - self.render_scroll[0], exclamation[1] - img.get_height() - self.render_scroll[1] - 20))
                self.exclamation.remove(exclamation)
        
        # Render the projectiles
        for projectile in self.projectiles.copy():
            img = self.assets['projectile']
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - self.render_scroll[0], projectile[0][1] - img.get_height() / 2 - self.render_scroll[1]))

        # Render the particles
        for particle in self.particles.copy():
            particle.render(self.display, offset=self.render_scroll)

        # Render the sparks
        for spark in self.sparks.copy():
            spark.render(self.display, offset=self.render_scroll)

        # Render the UI
        for x in range(self.lives):
            render_img(self.game.assets["heart"], 1140 - x * 50,70, self.display, centered=True)
        render_text(str(self.maxHP), self.font, "white", 1141, 70, self.display, True)
        render_img(self.game.assets["speed"], 1141, 115, self.display, centered=True)
        render_text(str(self.speed), self.font, "black", 1030, 100, self.display, False)
        num= self.player.gold
        count= 0

        while num !=0:
            num//= 10
            count += 1
        render_img(self.game.assets["gold"], 1143, 160, self.display, centered=True)
        render_text(str(self.player.gold), self.font, "black", 1030 - count * 2, 145, self.display, False)

    def minigame(self):
        # Play minigame
        if self.play and self.canplay:
            self.results = self.ttt.run()
            if self.results == "Win":
                self.canplay = False
                self.play = False
                dialogue.dialogue(self, "TicTacToeWin")
            elif self.results == "Lose":
                self.play = False
                dialogue.dialogue(self, "TicTacToeLose")
            elif self.results == "Draw":
                self.play = False
                dialogue.dialogue(self, "TicTacToeDraw")
                    
    def transitions(self):
        # Dim the screen and slowly light up evertime the map refreshes
        if self.transition != 0:
            img = pygame.Surface((1200, 675))
            img.fill((0,0,0))
            img.set_alpha(min(200, abs(self.transition) * 2))
            self.display.blit(img, (0,0))

        if self.felltransition != 0:
            img = pygame.Surface((1200, 675))
            img.fill((0,0,0))
            img.set_alpha(min(200, abs(self.felltransition) * 4))
            self.display.blit(img, (0,0))
  
        # Secondary screen, used for transition when dead
        if self.transition:
            transition_surf = pygame.Surface((1200, 675))
            self.shut = True if self.transition in range(70, 135) else False
            if self.transition < 0:
                transition_surf.blit(self.assets["loadscreen1"], (0, min(337, -675 - self.transition * 9)))
                transition_surf.blit(self.assets["loadscreen2"], (0, min(675, 1012 + self.transition * 9)))

            elif self.transition > 0:
                transition_surf.blit(self.assets["loadscreen1"], (0, min(0, -337 + self.transition * 9)))
                transition_surf.blit(self.assets["loadscreen2"], (0, max(337, 675 - self.transition * 9)))
            transition_surf.set_colorkey((0, 0, 0))
            self.display.blit(transition_surf, (0, 0))

        # secondary screen, used for transition when falling
        if self.felltransition:
            transition_surf = pygame.Surface((1200, 675))
            pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (60 - abs(self.felltransition)) * 30)
            transition_surf.set_colorkey((255, 255, 255))
            self.display.blit(transition_surf, (0, 0))

    def level_transition(self, timer, text):

        if self.current_level != self.level:
            self.current_level = self.level
            self.transition_ed = False 

        if not self.transition_ed:
            if self.transition_timer < timer:
                self.transitioning = True
                self.transition_timer += 1
                img = pygame.Surface((1200, 675))
                img.fill((0,0,0))
                img.set_alpha(255-self.transition_timer/timer*255)
                self.display.blit(img, (0,0))
                render_text(text, self.font2, "white", 600, 300, self.display, centered=True, transparency=255)

            elif self.transition_timer == timer:
                self.transition_timer = 0
                self.transition_ed = True
                self.transitioning = False
                
    def safehouse(self):
        if self.state == "safehouse":
            self.profile.data = self.player.data
            self.profile.saveprogress()
            
            if self.savetimer < 100:
                self.transitioning = True
                self.savetimer += 1
                self.display.fill((0, 0, 0))
                self.display.blit(self.assets["save"], (0, 0))
    
            else:
                self.transitioning = False
                self.level_transition(200, "Welcome to the safehouse")
                if self.store:
                    img = pygame.Surface((1200, 675))
                    img.fill((0,0,0))
                    img.set_alpha(150)
                    self.display.blit(img, (0,0))
                    self.display.blit(self.assets[self.store_state], (0, 0))
                    if self.store_state == "store_menu":
                        if self.upgrade_choice == 1:
                            render_img(self.assets["speed_potion"], 490, 350, self.display, True)
                            render_img(self.assets["big-heart"], 710, 350, self.display, True, transparency=150)
                        
                        elif self.upgrade_choice == 0:
                            render_img(self.assets["speed_potion"], 490, 350, self.display, True, transparency=150)
                            render_img(self.assets["big-heart"], 710, 350, self.display, True)
                    
                    # Store menu (Heart)
                    if self.store_state == "store_heart":
                        self.store_clickcooldown = max(0, self.store_clickcooldown - 1)
                        if render_img(self.assets["+"], 500, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_heart < self.max_heart - self.maxHP:
                            self.store_addsub_heart += 1
                            self.store_clickcooldown = 20
                        if render_img(self.assets["-"], 700, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_heart > 0:
                            self.store_addsub_heart -= 1
                            self.store_clickcooldown = 20
                        render_text(str(self.store_addsub_heart), self.font, "white", 600, 390, self.display, True)
                        
                        # Warn player about min and max hearts
                        if self.store_addsub_heart >= self.max_heart - self.maxHP:
                            self.store_addsub_heart = self.max_heart - self.maxHP
                            render_text("Max hearts", self.font, "red", 600, 330, self.display, True)
                        elif self.store_addsub_heart <= 0:
                            self.store_addsub_heart = 0
                            render_text("Min hearts", self.font, "red", 600, 330, self.display, True)

                        if self.player.gold < self.store_addsub_heart * 750:
                            render_text("Not enough gold", self.font, "red", 600, 440, self.display, True)

                        render_text(str(self.store_addsub_heart * 750), self.font, "black", 600, 490, self.display, True)

                    # Store menu (Speed)
                    if self.store_state == "store_speed":

                        # make the speed be 1 decimal point
                        self.store_addsub_speed = round(self.store_addsub_speed, 1)
                        self.store_clickcooldown = max(0, self.store_clickcooldown - 1)
                        if render_img(self.assets["+"], 500, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_speed < self.max_speed - self.player.speed:
                            self.store_addsub_speed += 0.1
                            self.store_clickcooldown = 20
                        if render_img(self.assets["-"], 700, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_speed > 0:
                            self.store_addsub_speed -= 0.1
                            self.store_clickcooldown = 20
                        render_text(str(self.store_addsub_speed), self.font, "white", 600, 400, self.display, True)
                        
                        # Warn player about min and max speed
                        if self.store_addsub_speed >= self.max_speed - self.player.speed:
                            self.store_addsub_speed = self.max_speed - self.player.speed
                            render_text("Max speed", self.font, "red", 600, 330, self.display, True)
                        elif self.store_addsub_speed <= 0:
                            self.store_addsub_speed = 0
                            render_text("Min speed", self.font, "red", 600, 330, self.display, True)

                        if self.player.gold < self.store_addsub_speed * 5000:
                            render_text("Not enough gold", self.font, "red", 600, 440, self.display, True)

                        render_text(str(int(self.store_addsub_speed * 5000)), self.font, "black", 600, 490, self.display, True)

    def run(self):
                
        self.display.blit(self.bg, (0, 0))
        self.render()

        # Example of implementation of code for dialogue
        self.npc_name = self.interact()
        if self.npc_name == "Store":
            self.store = True
            self.e = False
        
        elif self.npc_name is not None:
            dialogue.dialogue(self, self.npc_name)
            self.e = False


        # Pause button, if paused don't update the game
        self.check_button()
        if not self.pause and not self.play and not self.store:
            self.update()
        
        if self.pause:
            self.paused()
        
        self.death()
        self.minigame()
        self.userinput()
        self.transitions()
        self.safehouse()
        if self.level != "safehouse":
            self.level_transition(200, "Level " + self.level)
        