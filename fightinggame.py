import pygame
from fighter import Fighter
pygame.init()


#game window
Scr_width = 1300
Scr_height = 700

#set framerate
clock = pygame.time.Clock()
FPS = 60

#color for health bar
red = (255,0,0)
yellow = (255,255,0)
darkyellow = (255,215,0)
green = (0,255,0)
orange = (255,165,0)
dark_orange = (255,140,0)
black = (0,0,0)

#define fighter variables
warrior_size = 162 #pixel per frame
warrior_scale = 4
warrior_offscreen = [72, 56]
warrior_data = [warrior_size, warrior_scale, warrior_offscreen]
warrior2_data = [warrior_size, warrior_scale, warrior_offscreen]

#define game variables
intro_count = 3
ROUND_OVER_COOLDOWN = 2000
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player score p1 & p2
round_over_time = 0
round_over = False

#loading spritesheets
screen = pygame.display.set_mode([Scr_width,Scr_height])
warrior_sheet = pygame.image.load("Fantasy Warrior/Fantasy Warrior/Sprites/warrior1.png").convert_alpha()
warrior2_sheet = pygame.image.load("Fantasy Warrior/Fantasy Warrior/Sprites/warrior2.png").convert_alpha()
pygame.display.set_caption("Brawler")
victory_img = pygame.image.load("victory.png").convert_alpha()
Warrior_Animation_Steps = [10,8,1,7,7,3,7,4,7,4,6,3,1,4]
Warrior2_Animation_Steps = [10,8,1,7,7,3,7,4,7,4,6,3,1,4]

#load music/sound
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0, 5000)

sword_fx = pygame.mixer.Sound("sword.wav")
sword_fx.set_volume(0.4)

light_sword_fx = pygame.mixer.Sound("light attack.mp3")
sword_fx.set_volume(0.6)

walking = pygame.mixer.Sound("walk.mp3")
walking.set_volume(0.5)

charged_attack_fx = pygame.mixer.Sound("charged attack.mp3")

long_swing_fx = pygame.mixer.Sound("long attack.mp3")
long_swing_fx.set_volume(0.3)
indicator_charge_attack = pygame.mixer.Sound("charge attack is charged.mp3")

damage = pygame.mixer.Sound("damagesoundeffect.mp3")
damage.set_volume(0.5)

beep = pygame.mixer.Sound("beep.mp3")

ko = pygame.mixer.Sound("ko.mp3")

sword_clash = pygame.mixer.Sound("sword clash.mp3")

sword_projectile = pygame.mixer.Sound("shooting attack.mp3")

cooking = pygame.mixer.Sound("cooking.mp3")
#define background
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"plx-{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (2304, Scr_height))
    bg_images.append(bg_image)
bg_image = bg_images[0].get_width()


#the ground
ground_image = pygame.image.load("ground.png")
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
#scroll speed
scroll = 0
#coundown during the game
countdown = 4500
beepcountdown = 1500



#define font
count_font = pygame.font.Font("turok/Turok.ttf", 80)
countdown_font = pygame.font.Font("turok/Turok.ttf", 80)
score_font = pygame.font.Font("turok/Turok.ttf", 30)
player_font = pygame.font.Font("turok/Turok.ttf", 80)


def draw_text(text, font, text_col,x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#create background
def draw_bg():
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_image-1000) - scroll * speed, 0)) #changed the code
            speed += 0.2

def draw_ground():
    for x in range(8):
        screen.blit(ground_image,((x * ground_width - 1000) - scroll *2.2, Scr_height - ground_height))


#health bar
def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, black, (x, y, 580, 35))
    pygame.draw.rect(screen, red, (x, y, 580, 30))
    ratio = health / 150
    pygame.draw.rect(screen, darkyellow, (x, y, 435 * ratio, 30))

def draw_thirdattack_bar(attackallow, attackcount,x, y):
    pygame.draw.rect(screen, black, (x - 2, y - 2, 24, 24))
    pygame.draw.rect(screen, red, (x, y, 20, 20))
    if attackcount >= 60:
        pygame.draw.rect(screen, yellow, (x, y, 20, 20))
    if attackallow is True:
        pygame.draw.rect(screen, green, (x, y, 20, 20))

def draw_block_bar(blockallow,block_timer,block_cooldown,x, y):
    pygame.draw.rect(screen, black, (x-2, y-2, 204, 24))
    pygame.draw.rect(screen, red, (x, y, 200, 20))
    ratio_cooldown = block_cooldown / 70
    ratio = block_timer / 60
    if block_timer > 45:
        pygame.draw.rect(screen, yellow, (x, y, 200 * ratio, 20))
    elif blockallow is True:
        pygame.draw.rect(screen, green, (x, y, 200 * ratio, 20))
    elif block_cooldown > 0:
        pygame.draw.rect(screen, dark_orange, (x, y, 200 * ratio_cooldown, 20))

def draw_attackcooldown_bar(attackcooldown,blocking,x, y):
    pygame.draw.rect(screen, black, (x - 2, y - 2, 44, 24))
    pygame.draw.rect(screen, green, (x, y, 40, 20))
    if attackcooldown > 0 or blocking is True:
        pygame.draw.rect(screen, red, (x, y, 40, 20))

def draw_counter_bar(counterallow,countertimer,blocking,x, y):
    pygame.draw.rect(screen, black, (x - 2, y - 2, 84, 24))
    pygame.draw.rect(screen, green, (x, y, 80, 20))
    ratio = countertimer / 60
    if counterallow is False or blocking is True:
        pygame.draw.rect(screen, red, (x, y, 80, 20))
    if countertimer < 60:
     pygame.draw.rect(screen, yellow, (x, y, 80 * ratio, 20))


def draw_lightattack_bar(attackcount,attackallow, attackcooldown,x, y):
    pygame.draw.rect(screen, black, (x - 2, y - 2, 34, 24))
    pygame.draw.rect(screen, green, (x, y, 30, 20))
    if attackcount == 1:
        pygame.draw.rect(screen, yellow, (x, y, 30, 20))
    elif attackcooldown > 0 or attackallow is False:
        pygame.draw.rect(screen, red, (x, y, 30, 20))




#create 2 instances of fighters class (where they will spawn)
fighter_1 = Fighter(1,200,460, warrior_data, warrior_sheet, Warrior_Animation_Steps, False, sword_fx, light_sword_fx,long_swing_fx, charged_attack_fx,indicator_charge_attack, walking, damage, sword_clash, sword_projectile, cooking)
fighter_2 = Fighter(2,1000,460, warrior2_data, warrior2_sheet, Warrior2_Animation_Steps, True, sword_fx, light_sword_fx,long_swing_fx, charged_attack_fx,indicator_charge_attack, walking, damage, sword_clash,sword_projectile, cooking)

run = True
while run:
    #create the background
    draw_bg()
    draw_ground()
    if fighter_1.rect.x < 0 and fighter_2.rect.x < 1220 or fighter_2.rect.x < 0 and fighter_1.rect.x < 1220:
        if scroll > -100:
            scroll -= 5
    elif fighter_1.rect.x == 0 and fighter_1.hit is True or fighter_2.rect.x < 0 and fighter_2.hit is True:
        if scroll > -100:
            scroll -= 5

    if fighter_1.rect.x > 1221 and fighter_2.rect.x > 0 or fighter_2.rect.x > 1221 and fighter_1.rect.x > 0:
        if scroll < 100:
            scroll += 5
    elif fighter_1.rect.x >= 1200 and fighter_1.hit is True or fighter_2.rect.x >= 1200 and fighter_2.hit is True:
        if scroll < 100:
            scroll += 5
    fighter_1.getborder(scroll)
    fighter_2.getborder(scroll)
    #draw the notification on the charge attack
    draw_thirdattack_bar(fighter_1.cookattackallow,fighter_1.cook_count,20,70)
    draw_thirdattack_bar(fighter_2.cookattackallow,fighter_2.cook_count,1260,70)
    #draw notification for allow to block or not
    draw_block_bar(fighter_1.blockallow,fighter_1.block_timer,fighter_1.block_cooldown, 400, 70)
    draw_block_bar(fighter_2.blockallow,fighter_2.block_timer,fighter_2.block_cooldown, 700, 70)
    #draw attackallow indicator
    draw_attackcooldown_bar(fighter_1.attack_cooldown,fighter_1.blocking, 200, 70)
    draw_attackcooldown_bar(fighter_2.attack_cooldown,fighter_2.blocking,1060,70)
    #draw light attack indicator
    draw_lightattack_bar(fighter_1.attack3_check,fighter_1.attack_allow, fighter_1.attack3_cooldown, 250, 70)
    draw_lightattack_bar(fighter_2.attack3_check,fighter_2.attack_allow,fighter_2.attack3_cooldown, 1020, 70)
    #draw counterbar
    draw_counter_bar(fighter_1.counterallow,fighter_1.counter_duration,fighter_1.blocking, 290, 70)
    draw_counter_bar(fighter_2.counterallow,fighter_2.counter_duration,fighter_2.blocking, 930, 70)
    #draw player health
    draw_health_bar(fighter_1.health, 20,20)
    draw_health_bar(fighter_2.health, 700,20)
    #draw
    draw_text("P1: " + str(score[0]), score_font, red, 50, 60)
    draw_text("P2: " + str(score[1]), score_font, red, 1195, 60)
    #lock framerated
    clock.tick(FPS)

    #update player animation
    fighter_1.update(screen, fighter_2)
    fighter_2.update(screen, fighter_1)
    #character move function
    if intro_count != 0:
        draw_text("00", countdown_font, red, 615, 10)
    if intro_count <= 0:
        if countdown > 0:
            countdown -= 1
            display_countdown = countdown // 100
            if countdown > 1599:
                draw_text(str(display_countdown), countdown_font, black, 615, 10)
            else:
                draw_text(str(display_countdown), countdown_font, red, 615, 10)
            if countdown < 1600 and countdown == beepcountdown:
                beepcountdown -= 100
            if countdown < 1600 and countdown == beepcountdown:
                beepcountdown -= 100
        fighter_1.move(Scr_width, Scr_height, screen, fighter_2)
        fighter_2.move(Scr_width, Scr_height, screen, fighter_1)
    else:
        #display counter
        draw_text(str(intro_count), count_font, red, 630, Scr_height / 3)
        if (pygame.time.get_ticks() - last_count_update >= 1000):
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()




    #create the fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check if player is defeated
    if round_over == False:
        if fighter_1.alive == False or fighter_1.health < fighter_2.health and countdown == 0:
            score[1]+= 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False or fighter_1.health > fighter_2.health and countdown == 0:
            score[0]+= 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_1.health == fighter_2.health and countdown == 0:
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        if fighter_1.health == fighter_2.health:
            draw_text("draw", countdown_font, red, 575, 200)
        else:
            ko.play()
            if fighter_1.health > fighter_2.health:
                draw_text("Player 1 win", player_font,red,455, 200)
            elif fighter_2.health > fighter_1.health:
                draw_text("Player 2 win", player_font, red, 455, 200)
        countdown = 4600
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 460, warrior_data, warrior_sheet, Warrior_Animation_Steps, False, sword_fx, light_sword_fx,long_swing_fx, charged_attack_fx,indicator_charge_attack, walking, damage, sword_clash, sword_projectile, cooking)
            fighter_2 = Fighter(2, 1000, 460, warrior2_data, warrior2_sheet, Warrior2_Animation_Steps, True, sword_fx, light_sword_fx,long_swing_fx, charged_attack_fx,indicator_charge_attack, walking, damage, sword_clash, sword_projectile, cooking)


    #update what display
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
