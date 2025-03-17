import pygame
class Fighter():
    def __init__(self,player, x, y, data, sprite_sheet, animation_steps, flip, attack_sound, light_attack_sound, long_attack_sound, charge_attack_sound, charge_attackindicator, walking_sound, damage_sound, sword_clash ,sword_projectile, cooking):
        self.player = player #identify player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]

        #rect variable for attack & player
        self.rect = pygame.Rect((x,y,80,180))
        self.cookrect = pygame.Rect((x, y, 150, 200))
        self.wizardattacking1rect = pygame.Rect((x, y, 150, 280))
        self.wizardattacking2rect = pygame.Rect((x,y,170,270))
        self.counterrect = pygame.Rect((x,y,150,180))

        #animation variable
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0=idle / 1=run / 2=jump / 3=attack1 / 4=attack2 / 5=hit / 6=miss / 7=cooking /8= cookattack/ 9=lightattack /10=block /11=shooting / 12=counterstand /13= counterattacking
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

        self.update_time = pygame.time.get_ticks() #time variable
        self.flip = flip
        self.vel_y = 0
        self.running = False
        self.x = x
        self.y = y
        self.jump = False

        #sound
        self.attack_sound = attack_sound
        self.light_attack_sound = light_attack_sound
        self.charged_attack_sound = charge_attack_sound
        self.walking_sound = walking_sound
        self.damage_sound = damage_sound
        self.long_attack_sound = long_attack_sound
        self.charge_attackindicator = charge_attackindicator
        self.sword_clash = sword_clash
        self.hasagi = sword_projectile
        self.cooking_sound = cooking

        #check if sword clashed
        self.sword_clash_check = False

        self.attacking1 = False
        self.knightattack1rect = pygame.Rect((x, y, 100, 280))
        self.attack1drawallow = False
        self.attack1_count = 0

        self.attacking2 = False
        self.knightattack2rect = pygame.Rect((x, y, 120, 200))
        self.attack2drawallow = False
        self.attack2_count = 0

        self.attacking3 = False
        self.knightattack3rect = pygame.Rect((x, y, 108, 280))
        self.attack3drawallow = False
        self.attack3_count = 0

        #global cooldown to all attack
        self.attack_cooldown = 0
        #attack cooldown at corner
        self.attack_check1 = 0
        #light attack cooldown
        self.attack3_check = 0
        self.attack3_cooldown = 0
        #global cooldown for everything (movement etc)
        self.hit_cooldown = 0

        self.distance_on_left = 0
        self.distance_on_right = 0

        self.blockallow = True
        self.block_timer = 0
        self.block_cooldown = 0
        self.blocking = False

        self.attack_type = 0
        self.health = 200
        self.alive = True
        self.flipped_this_frame = False #not flipped
        self.hit = False
        self.airhit = False
        self.attack_allow = True
        self.hitbox = None

        self.counterattack = False #player in countering mode
        self.counterattacking = False
        self.countercontact = False #wether the attack of the player have made the contact
        self.counter_duration = 0 #amount of time the counter can last
        self.counter_cooldown = 0 #how long before user can counter again
        self.counterallow = True
        self.countercooldownstart = False
        self.startcounter = False

        self.stop = False
        self.airstun = False
        self.midair = False
        self.originalx = 0
        self.border = 0

        self.cooking = False
        self.cookallow = True
        self.cook_count = 0
        self.cookattackallow = False
        self.attackiscooking = 0
        self.cookattackdrawallow = False
        self.chargedattacking = False

        self.shoot = 0
        self.shooting = False
        self.shootallow = True
        self.shootoriginaly = 0
        self.shootoriginalx = 0


    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for i in range(animation):
                temp_img = sprite_sheet.subsurface(i * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, Screen_width, Screen_height, surface, target):
        self.Sp = 8 #speed player move (8 pixels per frame)
        self.dx = 0
        Gravity = 2
        self.dy = 0
        self.running = False
        self.attack_type = 0
        self.rect.x = max(0, min(Screen_width - self.rect.width, self.rect.x))


        #keypress
        key = pygame.key.get_pressed()


        #player 1 control
        if self.player == 1:
            if self.alive is True and self.attacking1 == False and self.attacking2 == False and self.chargedattacking == False and self.attacking3 == False and self.counterattack is False:
                if self.cooking is False:
                    # flipping
                    if key[pygame.K_TAB] and not self.flipped_this_frame:
                        if self.blocking is not True:
                            self.flip = not self.flip
                            self.flipped_this_frame = True
                    if not key[pygame.K_TAB]:
                        self.flipped_this_frame = False

                    #Counterattack / Parry
                    if self.counterallow is True:
                        if key[pygame.K_f] and not self.hit and self.hit_cooldown == 0:
                            self.counterattack = True
                            self.counterallow = False


                    if key[pygame.K_d] and key[pygame.K_a]:
                        self.dx = 0
                        self.stop = True
                    else:
                        self.stop = False

                #movement function
                    if self.counterattack is False:
                        if self.midair is False:
                            if self.stop is False:
                                if key[pygame.K_a] and self.hit is False and self.hit_cooldown == 0 and self.cooking is False:
                                    self.dx = -self.Sp
                                    self.running = True
                                if key[pygame.K_d] and self.hit is False and self.hit_cooldown == 0 and self.cooking is False:
                                    self.dx = self.Sp
                                    self.running = True



                        #jump function
                        if key[pygame.K_w] and self.jump is False and self.blocking is False and self.hit_cooldown == 0:
                            if self.counterattack is False:
                                self.jump = True
                                self.originalx = self.rect.x
                                self.vel_y = -30

                    #blocking
                    if self.blockallow is True:
                        if key[pygame.K_SPACE] and self.jump is False and self.hit_cooldown == 0:
                            self.blocking = True
                            self.attack_allow = False
                            self.block(target)
                            self.dx = 0
                            #print(self.block_timer)
                    if not key[pygame.K_SPACE]:
                        self.blocking = False
                        self.attack_allow = True


                    # attack
                    if self.attack_allow is True:
                        if self.attack2_count == 0:
                            if self.blocking is False and self.attack_cooldown == 0:
                                if key[pygame.K_t] and not key[pygame.K_a] and not key[pygame.K_d] and not key[pygame.K_y] and self.attack3_cooldown == 0:
                                    self.attacking3 = True
                                    self.attack3drawallow = True
                                    self.attack_type = 4
                                    self.attack3_check += 1
                                if self.flip is True:
                                    if key[pygame.K_a] and key[pygame.K_t]:
                                        self.attack_type = 1
                                        self.attack1drawallow = True
                                        self.attacking1 = True
                                elif self.flip is False:
                                    if key[pygame.K_d] and key[pygame.K_t]:
                                        self.attack_type = 1
                                        self.attack1drawallow = True
                                        self.attacking1 = True

                        if self.attack1_count == 0:
                            if key[pygame.K_y] and not key[pygame.K_t] and self.blocking is False and self.attack_cooldown == 0:
                                self.attacking2 = True
                                self.attack2drawallow = True
                                self.attack_type = 2


                if key[pygame.K_v] and self.cookallow is True and self.midair is False:
                    self.cooking = True
                    if self.cook_count < 120:
                        self.dx = 0
                if not key[pygame.K_v]:
                    self.cooking = False

                if self.cookattackallow is True:
                    if key[pygame.K_g]:
                        self.chargedattacking = True
                        self.attack_type = 3
                        self.cook_count = 0
                        self.cookallow = True
                        self.cookattackdrawallow = True

                if self.shootallow is True:
                    if key[pygame.K_c] and self.attack_cooldown == 0:
                        self.hasagi.play()
                        self.shootallow = False
                        self.shooting = True
                        self.attack_cooldown = 35
                        self.shootoriginaly = self.rect.y
                        self.shootoriginalx = self.rect.x

        if self.player == 2:
            if self.alive is True and self.attacking1 == False and self.attacking2 == False and self.chargedattacking == False and self.attacking3 == False and self.counterattack is False:
                if self.cooking is False:
                    # flipping
                    if key[pygame.K_KP_ENTER] and not self.flipped_this_frame:
                        if self.blocking is not True:
                            self.flip = not self.flip
                            self.flipped_this_frame = True
                    if not key[pygame.K_KP_ENTER]:
                        self.flipped_this_frame = False

                    #Counterattack / Parry
                    if self.counterallow is True:
                        if key[pygame.K_KP4] and not self.hit and self.hit_cooldown == 0:
                            self.counterattack = True
                            self.counterallow = False


                    if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
                        self.dx = 0
                        self.stop = True
                    else:
                        self.stop = False

                #movement function
                    if self.counterattack is False:
                        if self.midair is False:
                            if self.stop is False:
                                if key[pygame.K_LEFT] and self.hit is False and self.hit_cooldown == 0 and self.cooking is False:
                                    self.dx = -self.Sp
                                    self.running = True
                                if key[pygame.K_RIGHT] and self.hit is False and self.hit_cooldown == 0 and self.cooking is False:
                                    self.dx = self.Sp
                                    self.running = True


                        #jump function
                        if key[pygame.K_UP] and self.jump is False and self.blocking is False and self.hit_cooldown == 0:
                            if self.counterattack is False:
                                self.jump = True
                                self.originalx = self.rect.x #saving the initial position
                                self.vel_y = -30

                    #blocking
                    if self.blockallow is True:
                        if key[pygame.K_KP0] and self.jump is False and self.hit_cooldown == 0:
                            self.blocking = True
                            self.attack_allow = False
                            self.block(target)
                            self.dx = 0
                            #print(self.block_timer)
                    if not key[pygame.K_KP0]:
                        self.blocking = False
                        self.attack_allow = True


                    # attack
                    if self.attack_allow is True:
                        if self.attack2_count == 0:
                            if self.blocking is False and self.attack_cooldown == 0:
                                if key[pygame.K_KP1] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_KP2] and self.attack3_cooldown == 0:
                                    self.attacking3 = True
                                    self.attack3drawallow = True
                                    self.attack_type = 4
                                    self.attack3_check += 1
                                if self.flip is True:
                                    if key[pygame.K_LEFT] and key[pygame.K_KP1]:
                                        self.attack_type = 1
                                        self.attack1drawallow = True
                                        self.attacking1 = True
                                elif self.flip is False:
                                    if key[pygame.K_RIGHT] and key[pygame.K_KP1]:
                                        self.attack_type = 1
                                        self.attack1drawallow = True
                                        self.attacking1 = True

                        if self.attack1_count == 0:
                            if key[pygame.K_KP2] and not key[pygame.K_KP1] and self.blocking is False and self.attack_cooldown == 0:
                                self.attacking2 = True
                                self.attack2drawallow = True
                                self.attack_type = 2

                if key[pygame.K_KP_PLUS] and self.cookallow is True and self.midair is False:
                    self.cooking = True
                    if self.cook_count < 120:
                        self.dx = 0
                if not key[pygame.K_KP_PLUS]:
                    self.cooking = False

                if self.cookattackallow is True:
                    if key[pygame.K_KP6]:
                        self.chargedattacking = True
                        self.attack_type = 3
                        self.cook_count = 0
                        self.cookallow = True
                        self.cookattackdrawallow = True

                if self.shootallow is True:
                    if key[pygame.K_KP5] and self.attack_cooldown == 0:
                        self.hasagi.play()
                        self.shootallow = False
                        self.shooting = True
                        self.attack_cooldown = 35
                        self.shootoriginaly = self.rect.y
                        self.shootoriginalx = self.rect.x



        #apply the attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #hit cooldown
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        #block cooldown arguement
        if self.block_cooldown > 0:
            self.block_cooldown -= 1

        if self.attack3_cooldown > 0:
            self.attack3_cooldown -= 1

        #ensure player stay on screen
        if self.rect.y < self.y:
            self.vel_y += Gravity
        self.dy += self.vel_y


        #update player position
        self.rect.x += self.dx
        self.rect.y += self.dy


        #physics/movement argument during the gameplay

        if self.rect.left + self.dx < 0:
            self.dx = -self.rect.left
        if self.rect.right + self.dx > Screen_width:
            self.dx = Screen_width - self.rect.right
        if self.rect.bottom + self.dy > Screen_height - 60:
            self.vel_y = 0
            self.jump = False
            self.dy = Screen_height - 60 - self.rect.bottom #dropping
        if self.rect.y < 400:
            self.midair = True
            #falling forward & backward
            if self.originalx < self.rect.x: #compare the initial position on ground to the current position in midair to determine where the player is jumping/falling to
                if self.hit is False and self.rect.x > -1:
                    self.rect.x += 8 #apply the constant rate of
                else:
                    self.rect.x += 3 #knockback after getting hit
            elif self.originalx > self.rect.x:
                if self.hit is False and self.rect.x < 1305:
                    self.rect.x -= 8
                else:
                    self.rect.x -= 3
            #print("in air")
        else:
            self.midair = False
            #print("on land")

        #to prevent spam corner attack
        if target.attack_check1 == 3:
            target.attack_check1 = 0
            self.attack_cooldown += 70

        if self.attack3_check == 2: #limiting number of time light attack can use (make player more resourceful with the attack)
            self.attack3_cooldown = 50
            self.attack3_check = 0

        if self.cooking is True and self.cook_count < 110:
            self.cooking_sound.play()

        # if self.sword_clash_check is True:
        #     print(self.sword_clash_check)
        #     self.sword_clash.play()
        #     self.sword_clash_check = False


    def update(self, surface, target): #animation
        #check what action the player is performing

        #Block arguement
        if self.blocking is True:
            self.block_timer += 1
            if self.block_timer > 30:
                self.attack_cooldown += 2 #punishing for heavily relying on block
            if self.block_timer >= 60: #when block timer reach it max
                self.block_timer = 0 #reset the timer
                self.blocking = False
                self.blockallow = False #disallow blocking
                self.block_cooldown = 70  # amount of time wait before blocking again
        elif self.blocking is False and self.block_timer > 0:
            self.block_timer -= 0.3 #recharging block
            print(self.block_timer)
        if self.block_cooldown == 0:
            self.blockallow = True # allow to block again



        #counter attack arguement
        if self.counter_duration == 60: #counter timer end
            self.counterattack = False
            self.countercooldownstart = True #begin the cooldown
            self.counterattacking = False
            target.countercontact = False #preventing a bug
        elif self.counterattack is True:
            self.counterallow = False
            self.counter_duration += 1
            if target.countercontact is True: #attack when the contact from the enemy is true
                self.attack_type = 5
                self.counteratk(surface, target)
        if self.counter_cooldown == 1: #when the cooldown begin
            self.blockallow = False #disallow player to block
            self.block_cooldown =+ 70 #add the CD to blocking
        if self.counter_cooldown == 150: #when the cooldown is finish
            self.countercooldownstart = False
            self.counter_cooldown = 0 #reset everything
            self.counter_duration = 0
            self.counterallow = True #allow player to press it again
        elif self.countercooldownstart is True:
            self.counter_cooldown += 1



        #move the player back with the background when target moving to the edge of the screen
        if target.rect.x < 0:
            if self.border > -95:
                self.rect.x += 7
        elif target.rect.x > 1225:
            if self.border < 95:
                self.rect.x -= 7

        #tp player after they get tp
        if self.rect.x == 0:
            self.rect.x = 3
        elif self.rect.x == 1220:
            self.rect.x = 1217

            # quick attack arguement
        if self.attack3_count == 4: #take only 1 frames (this is to counter stun attack)
             self.lightattackknight(surface, target)
        if self.attack3_count == 15: #run until the end of the animation(end lag)
            self.attack3drawallow = False
            self.attack3_count = 0
        elif self.attack3drawallow is True:
            self.attack3_count += 1 #counter


        #attack 1 arguement
        if self.attack1_count >= 13: #the animation have already started, this is to wait for the 5th frames (attack frames)
            self.attack1drawallow = False
            self.attack1_count = 0
            if self.attack1knight(surface, target) is True and target.blocking is False: #check if it hit(yes = low CD, no = long CD)
                self.attack_cooldown += 10                                               #allow player to incoporate the next move
            else:
                self.attack_cooldown += 55  # punish player for using recklessly
        elif self.attack1drawallow is True:
            self.attack1_count += 1
            print(self.attack1_count)


        # attack 2 arguement
        if self.attack2_count >= 7: #similar to stun attack, but a faster hitbox with no air stun and a longer end lag
            self.attack2knight(surface, target)
            self.attack_cooldown += 70 #the end-lag
            self.attack2drawallow = False
            self.attack2_count = 0
        elif self.attack2drawallow is True:
            self.attack2_count += 1

        #cooking up an attack
        if self.cooking is True and self.cook_count < 120: #while pressing the 'charging' button
            self.cook_count += 1
            print(self.cook_count)
        if self.cook_count == 119: #a notification to the player that their attack is charged
            self.charge_attackindicator.play()
        if self.cook_count == 120:
            self.cookattackallow = True #now allow the 'charge attack' button to be press
            self.cookallow = False
        else:
            self.cookattackallow = False

        if self.cookattackdrawallow is True:
            self.attackiscooking += 1             #final attack - the last attack in a combo or a last attack after the first attack
        if self.attackiscooking == 15: #it slower than stun attack to force the player to use it as a final attack)
            self.cookattack(surface, target) #first damage(to break block)
        if self.attackiscooking >= 25: #second damage(to knock the enemy far away so the player cant follow-up with an attack)
            self.cookattackdrawallow = False #disallow the 'charge attack' button to be press
            self.cookattack(surface, target)
            self.attackiscooking = 0  #reset the charging
            self.chargedattacking = False

        #shooting arguement
        if self.shooting is True:
            self.shooting_attack(surface, target, self.shootoriginaly,self.shootoriginalx)
            self.shoot += 0.35
            if self.shoot >= 40:
                self.shooting = False
                self.shootallow = True
                self.shoot = 0

        #where animation is added
        if self.health <= 0:
            self.alive = False
            self.health = 0
            self.update_action(6)
        elif self.hit == True: #get hit
            self.cook_count = 0
            self.update_action(5) #hit animation
            self.cookallow = False
            self.originalx = self.rect.x
            #move the opponent back when player is hit at the corner (so it the knockback seem real)
            if self.rect.x <= 3 and self.border != -100:
                target.rect.x += 6
            elif self.rect.x >= 1215 and self.border != 100:
                target.rect.x -= 6
            # knockback
            if target.flip is False:
                self.rect.x += 3
            else:
                self.rect.x -= 3
            if self.alive is True:
                if self.airstun is True:
                    if self.midair is True: #preventing player from getting send to stratosphere to meet jesus
                        self.vel_y -= 1
                    else:
                         self.vel_y -= 5
            #self.attack_cooldown =+ 60      <----Can also add cooldown here
        elif self.attacking1 == True:
            if self.attack_type == 1:
                self.update_action(3) #attack 1
        elif self.chargedattacking == True:
            if self.attack_type == 3:
                self.update_action(8)
        elif self.attacking2 == True:
            if self.attack_type == 2:
                self.update_action(4) #attack 2
        elif self.attacking3 == True:
            if self.attack_type == 4:
                self.update_action(9)
        elif self.blocking == True: #block
            self.update_action(10)
            print("block ani")
        elif self.shoot > 1 and self.shoot < 6:
            self.update_action(11)
        elif self.counterattack == True:
            if target.countercontact == True:
                if self.attack_type == 5:
                    self.update_action(13)
            else:
                self.update_action(12)
        elif self.jump == True:
            self.update_action(2) #jump
        elif self.running == True and self.blocking == False:
            self.update_action(1) #moving
        elif self.cooking is True and self.cook_count < 120:
            self.update_action(7)  # HE'S COOKING!!!
        else:
            self.update_action(0)
        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #animation is finished?
        if self.frame_index >= len(self.animation_list[self.action]):
            #if player is dead
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #is the attack executed? (after attack animation)
                if self.action == 8:
                    self.chargedattacking = False #the charged/cooking attack
                    #target.hit = False
                if self.action == 3:
                    self.attacking1 = False
                if self.action == 4:
                    self.attacking2 = False
                if self.action == 9:
                    self.attacking3 = False
                if self.action == 13:
                    self.counterattacking = False
                    target.countercontact = False
                #after animation get hit
                if self.action == 5:
                    self.damage_sound.play()
                    self.hit = False
                    self.attacking1 = False
                    self.attacking2 = False
                    self.attacking3 = False
                    self.airstun = False
                    self.cookallow = True
                    if self.rect.x <= 0 or self.rect.x >= 1220:
                        self.attack_check1 += 1
                        print(self.attack_check1)
                if self.action == 11:
                    self.shoot += 0.5


    def attack1knight(self, surface, target):                                       #position of the drawing rect |
        if self.hit is False:                                                                                   # V
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.knightattack1rect.width * self.flip), self.rect.y, 2 * self.knightattack1rect.width, self.knightattack1rect.height)
            self.attack_sound.play() #play the sfx
            if attacking_rect.colliderect(target.rect):
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):#allow person to attack behind & no damage if the person blocked in front
                    print("hit")
                    if target.counterattack is False: #extra condition on opponent counter attack
                        target.airstun = True #stronger knockback
                        target.hit = True #allow every condition of the opponent self.hit condition to play out
                        target.health -= 10 #damage dealt by the attack
                        target.hit_cooldown = 40 #preventing the enemy from attacking during the hit animation
                        target.attack_cooldown += 40
                        return True
                    elif target.counterattack is True:
                        self.countercontact = True
                    else:
                        return False


    def attack2knight(self, surface, target):
        if self.hit is False:
            self.long_attack_sound.play()                                   #position & drawing of the hitbox |
            self.attack_sound.play()                                                                        # V
            attacking_rect = pygame.Rect(self.rect.centerx- 55 - (2 * self.knightattack2rect.width * self.flip), self.rect.y, 2 * self.knightattack2rect.width, self.knightattack2rect.height)
            if attacking_rect.colliderect(target.rect):
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):#allow person to attack behind & no damage if the person blocked in front
                    print("hit")
                    if target.counterattack is False: #extra condition on opponent counter attack
                        target.health -= 25 #damage dealt by the attack
                        target.hit = True #allow every condition of the opponent self.hit condition to play out
                        target.hit_cooldown = 40 #preventing the enemy from attacking during the hit animation
                        target.attack_cooldown += 45
                        return True
                    elif target.counterattack is True:
                        self.countercontact = True
                    else:
                        return False

    def lightattackknight(self, surface, target):                                   #position & drawing of the hitbox |
        if self.hit is False:                                                                                       # V
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.knightattack3rect.width * self.flip), self.rect.y, 2 * self.knightattack3rect.width, self.knightattack3rect.height)
            self.light_attack_sound.play()
            if attacking_rect.colliderect(target.rect):
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):#allow person to attack behind & no damage if the person blocked in front
                    print("hit")
                    if target.counterattack is False: #extra condition on opponent counter attack
                        target.health -= 5 #damage dealt by the attack
                        target.hit = True #allow every condition of the opponent self.hit condition to play out
                        target.hit_cooldown = 40 #preventing the enemy from attacking during the hit animation
                        target.attack_cooldown += 25
                        return True
                    elif target.counterattack is True:
                        self.countercontact = True #send back the info to the arguement
                    else:
                        return False

    def counteratk(self, surface, target):
        if self.hit is False:
            counter_rect = pygame.Rect(self.rect.centerx - (2 * self.counterrect.width * self.flip), self.rect.y, 2 * self.counterrect.width, self.counterrect.height)
            self.light_attack_sound.play()
            if counter_rect.colliderect(target.rect):
                print("Counterattack Hit!")
                target.health -= 1 #damage dealt by the attack(this is because the rect is draw multiple times)
                target.hit = True #allow every condition of the opponent self.hit condition to play out
                target.hit_cooldown = 40 #preventing the enemy from attacking during the hit animation
                target.attack_cooldown = 45

    def cookattack(self, surface, target):
        if self.hit is False:
            self.charged_attack_sound.play()
            cook_rect = pygame.Rect(self.rect.centerx - (2 * self.cookrect.width * self.flip), self.rect.y, 2 * self.cookrect.width, self.cookrect.height)
            if cook_rect.colliderect(target.rect):
                print("Big attack")
                target.airstun = True #big knockback
                target.health -= 15  #damage dealt by the attack(this is because the rect is draw multiple times)
                target.hit = True  #allow every condition of the opponent self.hit condition to play out
                target.hit_cooldown = 40 #preventing the enemy from attacking during the hit animation
                target.attack_cooldown = 45
                if target.blocking is True:
                    print("block break!!")
                    target.block_timer = 75 #nulify enemy blocking (the attack special ability)
                    target.health -= 25 #increase the damage

    def shooting_attack(self, surface, target, y, x):
            shooting_rect1 = pygame.Rect(x - (1 * self.rect.width * self.flip) + 50 * self.shoot - (100 * self.shoot * self.flip), y + 50, 0.5 * self.rect.width / 3, self.rect.height / 2.5)
            shooting_rect = pygame.Rect(x - (1 * self.rect.width * self.flip) + 50 * self.shoot - (100 * self.shoot * self.flip), y + 40, 0.5 * self.rect.width/3.2, self.rect.height /2)
            if shooting_rect.colliderect(target.rect) or shooting_rect1.colliderect(target.rect):
                self.shooting = False  #if any of these hit then the other will disappear with it (damage dealt only once instead of 2)
                self.shootallow = True
                self.shoot = 0
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):
                    if target.counterattack is True:
                        self.countercontact = True #allow the counterattack to still play out
                        target.health -= 10 #damage dealt by the attack
                    else:
                        target.health -= 10 #damage dealt by the attack
                        target.hit = True #allow every condition of the opponent self.hit condition to play out
            pygame.draw.rect(surface, (0, 255, 250), shooting_rect)
            pygame.draw.rect(surface, (0, 255, 250), shooting_rect1)


    def block(self, target): #send back information that player is in blocking state
        self.blocking = True

    def getborder(self,border): #get the scrolling from the main.py
        self.border = border
        #print(self.border)
        return self.border

    def update_action(self, new_action):
        #check if the new action is different to the previous
        if new_action != self.action:
            self.action = new_action
            #update the animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image,self.flip,False) #the hitbox/player box
        surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1]*self.image_scale)))