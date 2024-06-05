from utils import *

def safehouse(self):
        if self.state == "safehouse":
            self.lives = self.player.HP
            if not self.start:
                # print(self.prevlevel, self.player.level)
                if self.prevlevel == self.player.level:
                    self.player.level = str(int(self.player.level) + 1)
            self.profile.data = self.player.data
            self.profile.saveprogress()
            
            if self.savetimer < 100 and not self.start:
                self.transitioning = True
                self.savetimer += 1
                self.display.fill((0, 0, 0))
                self.display.blit(self.assets["save"], (0, 0))
    
            else:
                self.transitioning = False
                if self.level == "safehouse":
                    self.level_transition(150, "Welcome to the safehouse")
                if self.store:
                    img = pygame.Surface((1200, 675))
                    img.fill((0,0,0))
                    img.set_alpha(200)
                    self.display.blit(img, (0,0))
                    self.display.blit(self.assets[self.store_state], (0, 0))
                    if self.store_state == "store_menu":
                        if self.upgrade_choice == 1:
                            render_img(self.assets["speed_potion"], 445, 370, self.display, True)
                            render_img(self.assets["big-heart"], 600, 370, self.display, True, transparency=150)
                            render_img(self.assets["big-shield"], 750, 370, self.display, True, transparency=150)
                        
                        elif self.upgrade_choice == 0:
                            render_img(self.assets["speed_potion"], 445, 370, self.display, True, transparency=150)
                            render_img(self.assets["big-heart"], 600, 370, self.display, True)
                            render_img(self.assets["big-shield"], 750, 370, self.display, True, transparency=150)

                        elif self.upgrade_choice == 2:
                            render_img(self.assets["speed_potion"], 445, 370, self.display, True, transparency=150)
                            render_img(self.assets["big-heart"], 600, 370, self.display, True, transparency=150)
                            render_img(self.assets["big-shield"], 750, 370, self.display, True)
                    
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
                            self.store_addsub_speed = round(self.store_addsub_speed + 0.1, 1)
                            self.store_clickcooldown = 20
                        if render_img(self.assets["-"], 700, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_speed > 0:
                            self.store_addsub_speed = round(self.store_addsub_speed - 0.1, 1)
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

                    # Store menu (Shield)
                    if self.store_state == "store_shield":
                        self.store_clickcooldown = max(0, self.store_clickcooldown - 1)
                        if render_img(self.assets["+"], 500, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_shield < self.max_shield - self.player.shield/100:
                            self.store_addsub_shield += 1
                            self.store_clickcooldown = 20
                        if render_img(self.assets["-"], 700, 390, self.display, True, True) and self.store_clickcooldown == 0 and self.store_addsub_shield > 0:
                            self.store_addsub_shield -= 1
                            self.store_clickcooldown = 20
                        render_text("x" + str(round(self.player.shield/100 + self.store_addsub_shield)), self.font, "black", 600, 380, self.display, True)
                        
                        # Warn player about min and max shield
                        if self.store_addsub_shield >= self.max_shield - self.player.shield/100:
                            self.store_addsub_shield = self.max_shield - self.player.shield/100
                            render_text("Max shield", self.font, "red", 600, 330, self.display, True)
                        elif self.store_addsub_shield <= 0:
                            self.store_addsub_shield = 0
                            render_text("Min shield", self.font, "red", 600, 330, self.display, True)

                        if self.player.gold < self.store_addsub_shield * 600:
                            render_text("Not enough gold", self.font, "red", 600, 440, self.display, True)

                        render_text(str(round(self.store_addsub_shield * 600)), self.font, "black", 600, 490, self.display, True)
                
                elif self.level_select:
                    # Check for level_select change
                    if self.level == "safehouse":
                        self.level = "level_1"
                    else:
                        self.display.blit(self.assets[self.level], (0, 0))

                    # Render the level selection screen
                    self.level_transition(50)
                    img = pygame.Surface((1200, 675))
                    img.fill((0,0,0))
                    img.set_alpha(150)
                    self.display.blit(img, (0,0))
                    self.display.blit(self.assets["level_selection"], (0, 0))
                    render_text("Level " + self.level.split("_")[1], self.font2, "white", 600, 300, self.display, centered=True)

                    # Check if the player can play the level
                    if int(self.level.split("_")[1]) <= int(self.player.level):
                        self.can_load_level = True
                    else:
                        self.can_load_level = False
                        render_text("Locked", self.font2, "red", 600, 400, self.display, centered=True)
                        render_text("Complete the previous level to unlock", self.font, "white", 600, 450, self.display, centered=True)
      