import pygame
class Fighter():
    def __init__(self,player, x, y, data, sprite_sheet, animation_steps, flip):
        self.player = player #identify player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]

        #rect variable for attack & player
        self.rect = pygame.Rect((x,y,80,180))
        self.cookrect = pygame.Rect((x, y, 150, 200))
        self.wizardattacking1rect = pygame.Rect((x, y, 150, 280))
        self.wizardattacking2rect = pygame.Rect((x,y,170,270))
        self.knightattack1rect = pygame.Rect((x,y,100,280))
        self.knightattack2rect = pygame.Rect((x,y,120,180))
        self.counterrect = pygame.Rect((x,y,150,180))

        #animation variable
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0=idle / 1=run / 2=jump / 3=attack1 / 4=attack2 / 5=hit / 6=miss / 7=coocking /8= cookattack/ 9=test attack
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

        self.update_time = pygame.time.get_ticks() #time variable
        self.flip = flip
        self.vel_y = 0
        self.running = False
        self.x = x
        self.y = y
        self.jump = False

        self.attacking1 = False
        self.attack1drawallow = False
        self.attack1_count = 0

        self.attacking2 = False
        self.attack2drawallow = False
        self.attack2_count = 0

        #global cooldown to all attack
        self.attack_cooldown = 0
        self.attack_check1 = 0

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
        self.hit_cooldown = 0
        self.hitbox = None
        self.knockback_count = 0
        self.counterattack = False #player in countering mode
        self.countercontact = False #wether the attack of the player have made the contact
        self.counter_duration = 0 #amount of time the counter can last
        self.counter_cooldown = 0 #how long before user can counter again
        self.counterallow = True
        self.startcounter = False
        self.attacking_rect = None
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
            if self.alive is True and self.attacking1 == False and self.attacking2 == False and self.chargedattacking == False:
                if self.cooking is False:
                    # flipping
                    if key[pygame.K_q] and not self.flipped_this_frame:
                        if self.blocking is not True:
                            self.flip = not self.flip
                            self.flipped_this_frame = True
                    if not key[pygame.K_q]:
                        self.flipped_this_frame = False

                    #Counterattack / Parry
                    if self.counter_cooldown == 0:
                        if self.counterallow is True:
                            if key[pygame.K_f] and not self.hit and self.hit_cooldown == 0:
                                self.counterallow = False
                                if self.counter_duration == 0 and self.counter_cooldown == 0:
                                    self.startcounter = True


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
                            self.block(surface, target)
                            self.dx = 0
                            #print(self.block_timer)
                    if not key[pygame.K_SPACE]:
                        self.blocking = False
                        self.attack_allow = True


                    # attack
                    if self.attack_allow is True:
                        if self.attack2_count == 0:
                            if key[pygame.K_r] and self.blocking is False and self.attack_cooldown == 0:
                                self.attack_type = 1
                                self.attack1drawallow = True
                                self.attacking1 = True
                        if self.attack1_count == 0:
                            if key[pygame.K_t] and self.blocking is False and self.attack_cooldown == 0:
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
                        self.shootallow = False
                        self.shooting = True
                        self.attack_cooldown = 35
                        self.shootoriginaly = self.rect.y
                        self.shootoriginalx = self.rect.x

        if self.player == 2:
            if self.alive is True and self.attacking1 == False and self.attacking2 == False and self.chargedattacking == False:
                if self.cooking is False:
                    # flipping
                    if key[pygame.K_KP_ENTER] and not self.flipped_this_frame:
                        if self.blocking is not True:
                            self.flip = not self.flip
                            self.flipped_this_frame = True
                    if not key[pygame.K_KP_ENTER]:
                        self.flipped_this_frame = False

                    #Counterattack / Parry
                    if self.counter_cooldown == 0:
                        if self.counterallow is True:
                            if key[pygame.K_KP3] and not self.hit and self.hit_cooldown == 0:
                                self.counterallow = False
                                if self.counter_duration == 0 and self.counter_cooldown == 0:
                                    self.startcounter = True


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
                                self.originalx = self.rect.x
                                self.vel_y = -30

                    #blocking
                    if self.blockallow is True:
                        if key[pygame.K_KP0] and self.jump is False and self.hit_cooldown == 0:
                            self.blocking = True
                            self.attack_allow = False
                            self.block(surface, target)
                            self.dx = 0
                            # print(self.block_timer)
                    if not key[pygame.K_KP0]:
                        self.blocking = False
                        self.attack_allow = True


                    # attack
                    if self.attack_allow is True:
                        if self.attack_allow is True:
                            if key[pygame.K_KP1] and self.blocking is False and self.attack_cooldown == 0:
                                self.attack_type = 1
                                self.attacking1 = True
                                self.attack1drawallow = True
                            if key[pygame.K_KP2] and self.blocking is False and self.attack_cooldown == 0:
                                self.attack2drawallow = True
                                self.attacking2 = True
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

        #vunrebility after blocking too long
        if self.block_cooldown > 0 and self.blocking is False:
            self.block_cooldown -= 1

        #counter cooldown
        if self.counter_cooldown > 0:
            self.counter_cooldown -= 1



        #ensure player stay on screen
        if self.rect.y < self.y:
            self.vel_y += Gravity
        self.dy += self.vel_y


        #update player position
        self.rect.x += self.dx
        self.rect.y += self.dy


        #complex argument during the gameplay

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
            if self.originalx < self.rect.x: #compare the initial position on ground to the current position in midair to determine player moving forward or backward
                if self.hit is False and self.rect.x > -1:
                    self.rect.x += 8
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


        #Block arguement
        if self.blocking is True:
            self.block_timer += 1
            print(self.block_timer)
            if self.block_timer > 5:
                self.block_cooldown += 10
            if self.block_timer > 30:
                self.attack_cooldown += 2 #punishing for heavily relying on block
            if self.block_timer >= 60:
                self.block_timer = 0
                self.blocking = False
                self.blockallow = False
                self.block_cooldown = 70  # amount of time wait before blocking again
        elif self.blocking is False and self.block_timer > 0:
            self.block_timer -= 0.2 #recharging block
            print(self.block_timer)
        if self.block_cooldown == 0:
            self.blockallow = True # allow to block again


        #counter attack arguement
        if self.startcounter is True:
            self.counter_duration = 50
            self.attack_cooldown = 50
            self.block_cooldown = 80
            self.startcounter = False
        if target.countercontact is True: #confirm that the opponent attack the players while in counter state
            self.counteratk(surface, target)
            target.countercontact = False
        if self.counter_duration > 0:
            self.counterallow = False
            self.counterattack = True
            self.counter_duration -= 1
            if self.counter_duration == 0:
                self.counterattack = False
                # print(self.counter_duration)
        if self.counterattack is True:
            self.counterallow = False
            if self.counter_duration == 0:
                self.counter_cooldown = 90
        if self.counter_cooldown == 0:
             self.counterallow = True
        #seperate cooldown prevent player from holding the button

        #slow down the speed of player when the screen move
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

        #attack 1 arguement
        if self.attack1_count >= 15:
            self.attack1drawallow = False
            self.attack1_count = 0
            if self.attack1knight(surface, target) is True and target.blocking is False:
                self.attack_cooldown += 10
            else:
                self.attack_cooldown += 55  # cooldown for trying to spam at opponent block
        elif self.attack1drawallow is True:
            self.attack1_count += 1
            print(self.attack1_count)


        # attack 2 arguement
        if self.attack2_count >= 2:
            self.attack2knight(surface, target)
            self.attack_cooldown += 70
            self.attack2drawallow = False
            self.attack2_count = 0
        elif self.attack2drawallow is True:
            self.attack2_count += 1

        #cooking up an attack
        if self.cooking is True and self.cook_count < 120:
            self.cook_count += 1
            print(self.cook_count)
        if self.cook_count == 120:
            self.cookattackallow = True
            self.cookallow = False
        else:
            self.cookattackallow = False

        if self.cookattackdrawallow is True:
            self.attackiscooking += 1
        if self.attackiscooking == 15:
            self.cookattack(surface, target)
        if self.attackiscooking >= 25:
            self.cookattackdrawallow = False
            self.cookattack(surface, target)
            self.attackiscooking = 0
            self.chargedattacking = False


        #shooting
        if self.shooting is True:
            self.shooting_attack(surface, target, self.shootoriginaly,self.shootoriginalx)
            self.shoot += 0.5
            if self.shoot >= 40:
                self.shooting = False
                self.shootallow = True
                self.shoot = 0








    def update(self, surface, target): #animation
        #check what action the player is performing
        max_knock = 30
        if self.health <= 0:
            self.alive = False
            self.health = 0
            self.update_action(6)
        elif self.hit == True: #get hit
            self.update_action(5) #hit animation
            self.cookallow = False
            self.originalx = self.rect.x
            if self.rect.x == 0 and self.border != -100:
                target.rect.x += 6
            elif self.rect.x >= 1220 and self.border != 100:
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
        elif self.blocking == True: #block
            self.update_action(9)
            print("block ani")
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
                #after animation get hit
                if self.action == 5:
                    self.hit = False
                    self.attacking1 = False
                    self.attacking2 = False
                    self.airstun = False
                    self.cookallow = True
                    self.attack_check1 += 1
                    print(self.attack_check1)




    def attack1wizard(self, surface, target):#flipping attack mechanism |
        if self.attack_cooldown == 0:                                  #|
            self.attacking1 = True                                     #V
            if self.hit is False:
                #self.attack1_getready = 70
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.wizardattacking1rect.width * self.flip), self.rect.y-60, 2 * self.wizardattacking1rect.width, self.wizardattacking1rect.height)
                pygame.draw.rect(surface,(0,0,255), attacking_rect)
                if attacking_rect.colliderect(target.rect):
                    if (target.blocking is False or target.flip is False and self.flip is False or target.flip is True and self.flip is True): #allow person to attack behind & no damage if the person blocked in front
                        if target.counterattack is False:
                            print("hit")
                            target.airstun = True
                            target.health -= 7
                            target.hit = True
                            target.hit_cooldown = 30
                            target.attack_cooldown = 45
                            if target.rect.x == 0:
                                target.dx = -1
                            elif target.rect.x == 1220:
                                target.dx = 2
                            return True
                        elif target.counterattack is True:
                            self.countercontact = True
                        else:
                            return False
            return self.attacking_rect == None




    def attack2wizard(self, surface, target):                         #| flipping attack mechanism
        if self.attack_cooldown == 0:                                 #|
            self.attacking2 = True                                    #V
            if self.hit is False:
                #self.attack2_getready = 50
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.wizardattacking2rect.width * self.flip), self.rect.y-35, 2 * self.wizardattacking2rect.width, self.wizardattacking2rect.height)
                pygame.draw.rect(surface,(0,255,255), attacking_rect)
                if attacking_rect.colliderect(target.rect):
                    if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):#allow person to attack behind & no damage if the person blocked in front
                        print("hit")
                        if target.counterattack is False:
                            target.health -= 12
                            target.hit = True
                            target.hit_cooldown = 40
                            target.attack_cooldown = 45
                        elif target.counterattack is True:
                            self.countercontact = True
                        else:
                            return False
        return self.attacking_rect == None

    def attack1knight(self, surface, target):
        if self.hit is False:
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.knightattack1rect.width * self.flip), self.rect.y, 2 * self.knightattack1rect.width, self.knightattack1rect.height)
            pygame.draw.rect(surface,(0,0,255), attacking_rect)
            if attacking_rect.colliderect(target.rect):
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):#allow person to attack behind & no damage if the person blocked in front
                    print("hit")
                    if target.counterattack is False:
                        target.airstun = True
                        target.health -= 10
                        target.hit = True
                        target.hit_cooldown = 40
                        target.attack_cooldown += 45
                        return True
                    elif target.counterattack is True:
                        self.countercontact = True
                    else:
                        return False
        return self.attacking_rect == None

    def attack2knight(self, surface, target):
        if self.hit is False:
            attacking_rect = pygame.Rect((self.rect.centerx-100) - (2*self.knightattack2rect.width * self.flip), self.rect.y, 2 * self.knightattack2rect.width, self.rect.height)
            pygame.draw.rect(surface,(0,255,255), attacking_rect)
            if attacking_rect.colliderect(target.rect):
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False): #allow person to attack behind & no damage if the person blocked in front                        if target.counterattack is False:
                    print("hit")
                    target.health -= 25
                    target.hit = True
                    target.hit_cooldown = 40
                    target.attack_cooldown += 45
                elif target.counterattack is True:
                    self.countercontact = True
                else:
                    return False
        return self.attacking_rect == None

    def counteratk(self, surface, target):
        counter_rect = pygame.Rect(self.rect.centerx - (2 * self.counterrect.width * self.flip), self.rect.y, 2 * self.counterrect.width, self.counterrect.height)
        pygame.draw.rect(surface, (59, 155, 150), counter_rect)  # Draw counterattack hitbox
        if counter_rect.colliderect(target.rect):
            print("Counterattack Hit!")
            target.health -= 10
            target.hit = True
            target.hit_cooldown = 40
            target.attack_cooldown = 45

    def cookattack(self, surface, target):
        if self.hit is False:
            cook_rect = pygame.Rect(self.rect.centerx - (2 * self.cookrect.width * self.flip), self.rect.y, 2 * self.cookrect.width, self.cookrect.height)
            pygame.draw.rect(surface, (59, 155, 150), cook_rect)  # Draw counterattack hitbox
            if cook_rect.colliderect(target.rect):
                print("Big attack")
                target.airstun = True
                target.health -= 15
                target.hit = True
                target.hit_cooldown = 40
                target.attack_cooldown = 45
                if target.blocking is True:
                    print("block break!!")
                    target.block_timer = 75
                    target.health -= 10

    def shooting_attack(self, surface, target, y, x):
            shooting_rect = pygame.Rect(x - (1 * self.rect.width * self.flip) +  50 * self.shoot - (100 * self.shoot * self.flip), y + 50, 0.5 * self.rect.width, self.rect.height /2.5)
            if shooting_rect.colliderect(target.rect):
                self.shooting = False
                self.shootallow = True
                self.shoot = 0
                if (target.blocking == False or self.flip is True and target.flip is True or self.flip is False and target.flip is False):
                    target.health -= 10
                    target.hit = True
            pygame.draw.rect(surface, (255, 0, 255), shooting_rect)


    def block(self, surface, target): #draw the blocking
        self.blocking = True
        self.defend_rect = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip), self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (255, 255, 0), self.defend_rect)

    def getborder(self,border):
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
        img = pygame.transform.flip(self.image,self.flip,False)
        self.hitbox = pygame.draw.rect(surface, (255,0,0), self.rect) #the hitbox/player box
        surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1]*self.image_scale)))