# To Do
#   poop
#   love/hate bonus
#   rewrite stats method :(
#   modularize this whole thing
#   society detection/shift mechanism

import os
import random
from datetime import datetime
import names
import pygame

log_details = True
draw_world = True
save_all_drawings = False
save_some_drawings = 17     # 0 for no, otherwise months for how frequent to snap a shot

genesis_count = 1000        # how many lifeforms to start with
world_size = 75             # how big is the flat earth
apocalypse_years = 999      # how many yaers until no more months can pass
months_in_a_year = 12       # how many months in a year
roll_max = 100              # the upper bound for rolls
lifeform_draw_size = 5      # how many pixels a lifeform will get when drawn on the world_board
font_size = round(world_size/3) if world_size <= 126 else 42
min_energy = 800
max_energy = 1000
lifetime_min_start = 20
lifetime_max_start = 50
maturity_min_start = 14
maturity_max_start = 19
luck_min_start = 1
luck_max_start = 8
diligent_min_start = 1
diligent_max_start = 5
wit_min_start = 0
wit_max_start = 8
speed_min_start = 2
speed_max_start = 7
restless_min_start = 0
restless_max_start = 4
gestation_min_start = 7
gestation_max_start = 10
hunger_start = 0
piggy_min_start = 2
piggy_max_start = 7
food_min_start = 20
food_max_start = 50
greed_min_start = 1
greed_max_start = 8
joy_min_start = 0
joy_max_start = 7
hostility_min_start = 0
hostility_max_start = 8
miserly_min_start = 1
miserly_max_start = 14
charm_min_start = 3
charm_max_start = 14
beauty_min_start = 20
beauty_max_start = 40
reach_min_start = 1
reach_max_start = 4
skill_min_start = 8
skill_max_start = 24
kinship_min_start = 7
kinship_max_start = 14

begs = 0
gifts = 0
thefts = 0
finds = 0
last_id = 0

apocalypse = apocalypse_years*months_in_a_year
world = [[None for i in range(world_size)] for j in range(world_size)]
alive_list = []
run_id = int(round(datetime.now().timestamp()))
detail_csv_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{run_id}.csv"), "a+")
pygame.init()
world_board=pygame.display.set_mode([world_size*lifeform_draw_size*6 + 5, world_size*lifeform_draw_size*2 + 1])
font = pygame.font.SysFont(None, font_size)
pygame.display.set_caption("LifeForms")
default_font_color = (255, 255, 255)

class LifeFormColors:
    class Food:
        low = (255, 0, 0)
        medium = (255, 255, 0)
        high = (0, 255, 0)

    class Hunger:
        low = (0, 255, 0)
        medium = (255, 255, 0)
        high = (255, 0, 0)

    class Hates:
        hostility = (165, 42, 42)
        piggy = (255, 127, 80)
        greed = (255, 215, 0)
        miserly = (218, 165, 32)
        lifetime = (128, 128, 0)

    class Loves:
        wit = (65, 105, 225)
        luck = (127, 255, 0)
        skill = (138, 43, 226)
        diligent = (0, 255, 255)
        charm = (244, 164, 96)
        beauty = (240, 255, 255)
        food = (245, 222, 179)
        energy = (255, 0, 255)
        joy = (255, 20, 147)
        hostility = (255, 69, 0)
        kinship = (139, 69, 19)
    
    class Energy:
        excess = (246, 189, 192)
        high = (241, 149, 155)
        medium = (240, 116, 112)
        low = (234, 76, 70)
        dying = (220, 28, 19)

    class Joy:
        tops = (0, 0, 0)
        excess = (208, 239, 255)
        high = (42, 157, 244)
        medium = (24, 123, 205)
        low = (17, 103, 177)
        dying = (3, 37, 76)

    class Lifetime:
        baby = (132, 255, 159)
        child = (237,255,143)
        adult = (130,182,255)
        old = (255,150,104)
        ancient = (255,89,148)

    class Gender:
        male = (137,207,240)
        female = (242,172,185)
        mated_recently = (238, 38, 37)
        pregnant_round_1 = (241, 229, 191)
        pregnant_round_2 = (236, 221, 171)
        pregnant_round_3 = (232, 213, 150)
        pregnant_round_4 = (228, 205, 130)
        pregnant_round_5 = (223, 197, 110)
        pregnant_round_6 = (219, 189, 90)
        pregnant_round_7 = (215, 181, 70)
        pregnant_round_8 = (210, 173, 50)
        pregnant_round_9 = (194, 158, 41)
        pregnant_round_10 = (174, 142, 37)
        pregnant_round_11 = (154, 125, 33)
        pregnant_round_12 = (134, 109, 28)
        pregnant = (237, 255, 0)

    class Beauty:
        excess = (37, 44, 88)
        high = (215, 114, 124)
        medium = (219, 202, 183)
        low = (63, 41, 5)
        dying = (189, 160, 106)

    class Luck:
        excess = (237, 140, 140)
        high = (235, 34, 37)
        medium = (237, 140, 140)
        low = (187, 196, 200)
        dying = (116, 132, 148)

    class Heart:
        # fought = (255, 255, 0)
        love = (255, 192, 203)
        hate = (255, 0, 0)

class LifeForm:
    loves = ["wit", "luck", "skill", "diligent", "charm", "beauty", "food", "energy", "joy", "hostility", "kinship"]
    hates = ["hostility", "piggy", "greed", "miserly", "lifetime"]

    def __init__(self):
        # broad properties
        self.luck = 0           # catch all positive/negative value
        self.diligent = 0      # how many failures a lifeform can tollerate in a turn
        self.skill = 0          # value of individual performance capability
        self.wit = 0   # how many turns ahead a lifeform can try to optimize strategies for dependent props

        # death properties
        self.energy = 0         # how far from death the lifeform is
        self.lifetime = 0       # how many turns a lifeform has been alive

        # movement properties
        self.speed = 0          # movements per round
        self.restless = 0       # likihood of trying to move per round

        # reproduction properties
        self.mature = False     # whether or not entity can reproduce
        self.mature_age = 0     # age when mature
        self.male = False       # whether the lifeform is male or female
        self.pregnant = False   # whether or not for the current turn the lifeform is pregnant
        self.gestation = 0      # how many turns it takes for a new lifeform to birth
        self.birth_month = 0    # what month the lifeform was born

        # energy properties
        self.hunger = 0         # numerical value representing current hunger, affects energy
        self.piggy = 0        # how much food a lifeform tries to eat a turn
        self.food = 0           # how much food a lifeform owns
        self.greed = 0          # factor of actual need greater that lifeform requires

        # social properties
        self.joy = 0            # how happy the lifeform is
        self.hostility = 0      # how many fights a turn a lifeform can have
        self.miserly = 0        # how willing a lifeform is to assist others against joy
        self.charm = 0          # how much this lifeform affects other lifeforms nearby
        self.beauty = 0         # how preferable a lifeform is for mating
        self.reach = 0          # how far from the lifeform does it care about other lifeform's charm & attractiveness
        self.kinship = 0        # how much a lifeform cares about its kin
        self.family = ""
        self.name = ""
        self.love = ""          # which lifeform property a lifeform wants to be around [wit, luck, skill, diligent, charm, beauty, food, energy]
        self.hate = ""          # which lifeform property a lifeform wants to avoid [fights, piggy, greed, miserly, lifetime]
        self.hate_first = False # whether or not the love or its hate is more driving

        # purely derivied meta properties
        self.actions = []
        self.parents = []
        self.children = []
        self.prediction_success_rate = 0
        self.x = 0                          # current x position in the world
        self.y = 0                          # current y position in the world
        self.id = 0
        self.fights = 0
        self.rounds_pregnant = 0
        self.extra_pregnancy_food = 0
        self.paternal_genes = {}
        self.baby_daddy = None
        self.mated_recently = False
        self.scars = 0

    # primary repeated method
    def take_turn(self, month):
        for action in self.actions:
            action(month)
    
    # lifecycle methods
    def _spawn(self, x, y, id, male, birth_month, luck=0, diligent=0, wit=0, skill=0, energy=0, lifetime=0,
              speed=0,restless=0, mature=False, gestation=0, hunger=0, piggy=0, food=0, greed=0, joy=0,
              miserly=0, charm=0, beauty=0, reach=0, kinship=0, name="", family="", mature_age=0, hostility=0):
        self.luck=luck
        self.diligent=diligent
        self.wit=wit
        self.skill=skill
        self.energy=energy
        self.lifetime=lifetime
        self.speed=speed
        self.restless=restless
        self.diligent=diligent
        self.mature=mature
        self.mature_age=mature_age
        self.male=male
        self.pregnant=False
        self.gestation=gestation
        self.hunger=hunger
        self.piggy=piggy
        self.food=food
        self.greed=greed
        self.joy=joy
        self.hostility=hostility
        self.miserly=miserly
        self.charm=charm
        self.beauty=beauty
        self.reach=reach
        self.kinship=kinship
        self.name=name
        self.family=family
        self.birth_month=birth_month
        self.x=x
        self.y=y
        self.id=id
        self.actions = [self.move, self.forage, self.mingle, self.pregnancy, self.eat, self.push]
        self.love = random.choice(self.loves)
        self.hate = random.choice(self.hates)
        self.hate_first = random.choice([True, False])
        random.shuffle(self.actions)
        self.actions.append(self.age)

    def _birth(self, x, y, id, male, food, mother_genes, father_genes, name, family, love, hate, hate_first, birth_month):
        self.male = male
        self.food = food
        self.lifetime = 0
        self.mature = False
        self.pregnant = False
        self.x = x
        self.y = y
        self.id = id
        self.name = name
        self.family = family
        self.love = love
        self.hate = hate
        self.hate_first = hate_first
        self.birth_month = birth_month
        self.actions = [self.move, self.forage, self.mingle, self.pregnancy, self.eat, self.push]
        random.shuffle(self.actions)
        self.actions.append(self.age)

        for key in mother_genes.keys():
            mod = [mother_genes[key], father_genes[key]]
            mod.sort()
            if key == "skill":
                mod[0] = round(mod[0]/2)
            setattr(self, key, random.randrange(mod[0], mod[1] + 1))

        luck_improve_roll = random.randrange(0, roll_max) # maybe [0, luck^2), some social component should be in here when switching to {{society style}}
        if luck_improve_roll <= self.luck:
            self.luck = self.luck + 1

        beauty_improve_roll = random.randrange(0, roll_max) # maybe [0, beauty*beauty - luck)
        if beauty_improve_roll <= self.luck + self.beauty:
            self.beauty = self.beauty + 1

        wit_improve_roll = random.randrange(0, roll_max)
        if wit_improve_roll <= self.luck + self.wit:
            self.wit = self.wit + 1

        diligent_improve_roll = random.randrange(0, roll_max)
        if diligent_improve_roll <= self.luck + self.diligent:
            self.diligent = self.diligent + 1
        
        charm_improve_roll = random.randrange(0, roll_max)
        if charm_improve_roll <= self.luck + self.charm:
            self.charm = self.charm + 1

        reach_improve_roll = random.randrange(0, self.luck*self.luck)
        if reach_improve_roll <= self.luck + self.reach:
            self.reach = self.reach + 1

        kinship_improve_roll = random.randrange(0, roll_max)
        if kinship_improve_roll <= self.luck + self.kinship:
            self.kinship = self.kinship + 1
        
        greed_improve_roll = random.randrange(0, roll_max)
        if greed_improve_roll <= self.luck + self.greed:
            self.greed = self.greed - 1

        miserly_improve_roll = random.randrange(0, roll_max)
        if miserly_improve_roll <= self.luck + self.miserly:
            self.miserly = self.miserly - 1
        
        love_hate_flip_roll = random.randrange(0, roll_max)
        if love_hate_flip_roll <= self.luck:
            self.hate_first = not self.hate_first
        
        love_change_roll = random.randrange(0, roll_max)
        if love_change_roll <= self.luck:
            self.love = random.choice(self.loves)

        hate_change_roll = random.randrange(0, roll_max)
        if hate_change_roll <= self.luck:
            self.hate = random.choice(self.hates)

    def _die(self):
        alive_list.remove(self)
        world[self.x][self.y] = None

        child_luck_sum = 0
        for child in self.children:
            child_luck_sum = child_luck_sum + child.luck
        inheritance_roll = random.randrange(0, roll_max)
        if inheritance_roll < child_luck_sum:
            inheritance_split = len(self.children) + 1
            for child in self.children:
                child.food = child.food + round(self.food/inheritance_split)
        self.food = 0

    # core actions
    def move(self, _):
        steps_taken = 0
        original_x = self.x
        original_y = self.y
        target_x = original_x
        target_y = original_y
        delta_x = random.randrange(-1*self.speed, self.speed + 1)
        delta_y = random.randrange(-1*self.speed, self.speed + 1)
        while steps_taken < self.restless:
            target_x = self.x + delta_x
            target_y = self.y + delta_y
            delta_x = random.randrange(-1*self.speed, self.speed + 1)
            delta_y = random.randrange(-1*self.speed, self.speed + 1)
            if self.wit > 0 and not self.pregnant:
                property_consideration = self.love
                if self.hate_first:
                    property_consideration = self.hate
                target_neighbor = None
                neighbors = [world[i][j]
                    for i in range(self.x - self.wit, self.x + self.wit + 1)
                    for j in range(self.y - self.wit, self.y + self.wit + 1)
                    if i > -1 and j > -1 and j < len(world[0]) and i < len(world) and
                    world[i][j] is not None and world[i][j] is not self]
                random.shuffle(neighbors)
                for neighbor in neighbors:
                    if target_neighbor is None:
                        target_neighbor = neighbor
                    elif getattr(target_neighbor, property_consideration) < getattr(neighbor, property_consideration):
                        target_neighbor = neighbor
                    target_x = target_neighbor.x
                    target_y = target_neighbor.y
                if target_neighbor is not None and self.hate_first:
                    if target_neighbor.x > self.x:
                        delta_x = -self.speed if target_neighbor.x - self.x > self.speed else -random.randrange(0, target_neighbor.x - self.x)
                    elif target_neighbor.x < self.x:
                        delta_x = self.speed if self.x - target_neighbor.x > self.speed else random.randrange(0, self.x - target_neighbor.x)
                    else:
                        delta_x = random.choice([1,-1])
                    if target_neighbor.y > self.y:
                        delta_y = -self.speed if target_neighbor.y - self.y > self.speed else -random.randrange(0, target_neighbor.y - self.y)
                    elif target_neighbor.y < self.y:
                        delta_y = self.speed if self.y - target_neighbor.y > self.speed else random.randrange(0, self.y - target_neighbor.y)
                    else:
                        delta_y = random.choice([1,-1])
                elif target_neighbor is not None:
                    if target_neighbor.x > self.x:
                        delta_x = self.speed if target_neighbor.x - self.x > self.speed else random.randrange(0, target_neighbor.x - self.x)
                    elif target_neighbor.x < self.x:
                        delta_x = -self.speed if self.x - target_neighbor.x > self.speed else -random.randrange(0, self.x - target_neighbor.x)
                    else:
                        delta_x = 0
                    if target_neighbor.y > self.y:
                        delta_y = self.speed if target_neighbor.y - self.y > self.speed else random.randrange(0, target_neighbor.y - self.y)
                    elif target_neighbor.y < self.y:
                        delta_y = -self.speed if self.y - target_neighbor.y > self.speed else -random.randrange(0, self.y - target_neighbor.y)
                    else:
                        delta_y = 0
            x = (self.x + delta_x + world_size) % world_size
            y = (self.y + delta_y + world_size) % world_size
            if world[x][y] == None:
                world[x][y] = self
                world[self.x][self.y] = None
                self.x = x
                self.y = y
            steps_taken = steps_taken + 1
        # If the lifeform didn't move, perform a super jump... if you can stick the landing
        if self.x == original_x and self.y == original_y and target_x != original_x and target_y != original_y:
            if self.hate_first:
                target_x = (target_x - delta_x + world_size) % world_size
                target_y = (target_y - delta_y + world_size) % world_size
            else:
                target_x = (target_x + delta_x + world_size) % world_size
                target_y = (target_y + delta_y + world_size) % world_size
            
            if world[target_x][target_y] == None:
                world[target_x][target_y] = self
                world[self.x][self.y] = None
                self.x = target_x
                self.y = target_y

    def push(self, _):
        irritable_roll = random.randrange(0, roll_max)
        if self.hate_first or irritable_roll < self.hostility:
            neighbors = [world[i][j]
                        for i in range(self.x - self.reach, self.x + self.reach + 1)
                        for j in range(self.y - self.reach, self.y + self.reach + 1)
                        if i > -1 and j > -1 and j < len(world[0]) and i < len(world) and
                        world[i][j] is not None and world[i][j] is not self and 
                        getattr(world[i][j], self.hate) > getattr(self, self.hate)]
            random.shuffle(neighbors)
            pushed = 0
            for neighbor in neighbors:
                if pushed < self.hostility:
                    x = (neighbor.x + random.choice([1,-1])*self.reach + world_size) % world_size
                    y = (neighbor.y + random.choice([1,-1])*self.reach + world_size) % world_size
                    if world[x][y] is None:
                        world[x][y] = neighbor
                        world[neighbor.x][neighbor.y] = None
                        neighbor.x = x
                        neighbor.y = y
                        pushed = pushed + 1

    def forage(self, _):
        if self.mature and self.food < self.greed*self.piggy:
            food_found = False
            attempts = 0
            while attempts < self.diligent and not food_found:
                food_roll = random.randrange(0, roll_max)
                if food_roll < (self.luck + self.skill + self.wit):
                    food_found = True
                attempts = attempts + 1
            if food_found:
                luck_imapct = random.randrange(0, self.luck)
                found_ammount_found = luck_imapct*(self.skill*self.wit - attempts - 1)
                self.food = self.food + found_ammount_found
                global finds; finds = finds + 1
            elif self.joy > self.hunger and self.hunger < 0:
                self.joy = self.joy + self.hunger
            elif self.joy > self.hunger and self.hunger >= 0:
                self.joy = self.joy - self.hunger
            else:
                self.joy = 0
    
    def eat(self, _):
        if self.food > self.piggy + self.extra_pregnancy_food:
            self.food = self.food - self.piggy - self.extra_pregnancy_food
            if self.energy + self.piggy + self.luck <= max_energy:
                self.energy = self.energy + self.piggy + self.luck
            else:
                self.energy = max_energy + self.luck
        else:
            self.hunger = self.hunger + self.food - self.piggy - self.extra_pregnancy_food
            self.food = 0        

        if self.hunger < 0:
            if self.food > 0:
                if self.food <= -1*self.hunger:
                    self.hunger = self.hunger + self.food
                    self.food = 0
                else:
                    self.food = self.food + self.hunger
                    self.hunger = 0
            self.energy = self.energy + self.hunger
            joy_mods = [self.hunger, self.luck]
            joy_mods.sort()
            self.joy = self.joy + random.randrange(joy_mods[0], joy_mods[1] + 1)
        elif self.luck > 0:
            satisfaction_roll = random.randrange(0, roll_max)
            if satisfaction_roll < self.luck:
                self.joy = self.joy + random.randrange(0, self.luck)

    def mingle(self, _):
        neighbors = [world[i][j]
                    for i in range(self.x - self.reach, self.x + self.reach + 1)
                    for j in range(self.y - self.reach, self.y + self.reach + 1)
                    if i > -1 and j > -1 and j < len(world[0]) and i < len(world) and 
                    world[i][j] is not None and world[i][j] is not self]
        random.shuffle(neighbors)
        trade_requests = 0
        recent_fights = 0
        for neighbor in neighbors:
            # charity
            if self.hunger < 0:
                neighbor._give(self, -1*self.hunger)
                trade_requests = trade_requests + 1
            if self.food < self.greed*self.piggy:
                neighbor._give(self, self.greed*self.piggy - self.food)
                trade_requests = trade_requests + 1
            
            # trade
            if self.joy > neighbor.joy and \
                self.charm + self.luck > neighbor.charm and \
                neighbor.food > 0 and \
                self.food < self.greed*self.piggy:
                self._trade(neighbor, self.greed*self.piggy - self.food)
                trade_requests = trade_requests + 1

            # steal
            if trade_requests < self.diligent and \
                (self.hunger < 0 or self.food < round(self.greed*self.piggy/2) and \
                self.energy > 0 and neighbor.energy > 0):
                self._take(neighbor, self.greed*self.piggy - self.food)
                trade_requests = trade_requests + 1
                recent_fights = recent_fights + 1

            # attack/jealousy
            if self.joy < neighbor.joy and \
                self.energy > neighbor.energy and \
                self.energy > 0 and \
                neighbor.energy > 0 and \
                not self.pregnant and \
                not neighbor.pregnant and \
                self.hostility > recent_fights and \
                (self.luck < neighbor.luck or \
                    self.beauty < neighbor.beauty or \
                    self.wit < neighbor.wit or \
                    self.food < neighbor.food or \
                    self.hunger < neighbor.hunger):
                grievances = []
                if self.food + neighbor.luck < neighbor.food:
                    grievances.append("food")
                if self.hunger + neighbor.luck < neighbor.hunger:
                    grievances.append("hunger")
                if self.beauty + neighbor.luck + self.scars < neighbor.beauty + neighbor.scars:
                    grievances.append("beauty")
                if self.wit + neighbor.luck < neighbor.wit:
                    grievances.append("wit")
                if self.luck + neighbor.luck < neighbor.luck:
                    grievances.append("luck")

                random.shuffle(grievances)
                if len(grievances) > 0:
                    if grievances[0] == "food":
                        self._take(neighbor, neighbor.food - self.food + neighbor.joy - self.joy)
                    elif grievances[0] == "hunger":
                        self._take(neighbor, (-1*self.hunger) - (-1*neighbor.hunger) + neighbor.joy - self.joy)
                    elif grievances[0] == "beauty":
                        delta_beauty = neighbor.beauty - self.beauty
                        self.energy = self.energy - delta_beauty
                        self.joy = self.joy + round(delta_beauty/2)
                        if -1*neighbor.scars <= neighbor.beauty:
                            neighbor.scars = neighbor.scars - delta_beauty
                        else:
                            neighbor.scars = neighbor.beauty*-1
                        if neighbor.joy > delta_beauty:
                            neighbor.joy = neighbor.joy - delta_beauty
                        else:
                            neighbor.joy = 0
                    elif grievances[0] == "wit":
                        delta_wit = neighbor.wit - self.wit
                        self.energy = self.energy - delta_wit
                        self.joy = self.joy + round(delta_wit/2)
                        neighbor.wit = neighbor.wit - delta_wit
                        if neighbor.joy > delta_wit:
                            neighbor.joy = neighbor.joy - delta_wit
                        else:
                            neighbor.joy = 0
                    elif grievances[0] == "luck":
                        delta_luck = neighbor.wit - self.wit
                        self.energy = self.energy - delta_luck
                        self.joy = self.joy + round(delta_luck/2)
                        if neighbor.joy > delta_luck:
                            neighbor.joy = neighbor.joy - delta_luck
                        else:
                            neighbor.joy = 0

                    if self.luck < neighbor.beauty + neighbor.scars:
                        if -1*neighbor.scars >= self.luck:
                            neighbor.scars = neighbor.scars - self.luck
                        else:
                            neighbor.scars = -1*self.luck
                    if neighbor.luck < self.beauty + self.scars:
                        if -1*self.scars >= neighbor.luck:
                            self.scars = self.scars - neighbor.luck
                        else:
                            self.scars = -1*neighbor.luck
                    recent_fights = recent_fights + 1
                    self.fights = self.fights + 1
            # thanos clause
            if len(alive_list)/(world_size*world_size) > (roll_max - self.hostility)/roll_max or\
                len(alive_list)/(world_size*world_size) < (self.hostility)/roll_max:
                neighbor.energy = 0
                self.energy = 0

            # mate
            if ((self.male and not neighbor.male) or (neighbor.male and not self.male)) and \
                not self.mated_recently and \
                not neighbor.mated_recently and \
                not neighbor.pregnant and \
                not self.pregnant and \
                self.mature and \
                neighbor.mature and \
                neighbor.energy + (neighbor.beauty + neighbor.scars)*neighbor.luck*neighbor.charm > self.energy:
                self._mate(neighbor)

    def pregnancy(self, month):
        if not self.male and self.pregnant:
            if self.rounds_pregnant < self.gestation:
                self.rounds_pregnant = self.rounds_pregnant + 1
                self.extra_pregnancy_food = round(self.piggy*(self.rounds_pregnant/self.gestation))
            else:
                maternal_genes = {
                    "luck": self.luck,
                    "diligent": self.diligent,
                    "wit": self.wit,
                    "skill": self.skill,
                    "energy": self.energy,
                    "speed": self.speed,
                    "restless": self.restless,
                    "gestation": self.gestation,
                    "piggy": self.piggy,
                    "greed": self.greed,
                    "hostility": self.hostility,
                    "miserly": self.miserly,
                    "charm": self.charm,
                    "beauty": self.beauty,
                    "mature_age": self.mature_age,
                    "reach": self.reach,
                    "kinship": self.kinship
                }
                baby_place = None
                baby_open_space_found = False
                for reach in range(self.reach + self.luck):
                    if not baby_open_space_found:
                        baby_cord = [(i,j)
                            for i in range(self.x - reach, self.x + reach + 1)
                            for j in range(self.y - reach, self.y + reach + 1)
                            if i > -1 and j > -1 and j < len(world[0]) and i < len(world)]
                        for cord in baby_cord:
                            if not baby_open_space_found:
                                baby_open_space_found = world[cord[0]][cord[1]] is None
                                baby_place = cord
                if baby_open_space_found:
                    global last_id; last_id = last_id + 1
                    xy = random.choice([True, False])
                    gender_text = 'male' if xy else 'female'
                    family_name = self.baby_daddy.family if xy else self.family
                    if len(alive_list) < world_size*world_size:
                        child = LifeForm()
                        child._birth(
                            x=baby_place[0],
                            y=baby_place[1],
                            id=last_id,
                            male=xy,
                            food=round(self.food/2)+self.paternal_genes["food"],
                            mother_genes=maternal_genes,
                            father_genes=self.paternal_genes,
                            name=names.get_first_name(gender=gender_text),
                            family=family_name,
                            love=random.choice([self.love, self.baby_daddy.love]),
                            hate=random.choice([self.hate, self.baby_daddy.hate]),
                            hate_first=random.choice([self.hate_first, self.baby_daddy.hate_first]),
                            birth_month=month%months_in_a_year
                            )
                        child.parents.append(self)
                        child.parents.append(self.baby_daddy)
                        self.food = round(self.food/2)
                        self.children.append(child)
                        self.baby_daddy.children.append(child)
                        world[local_x][local_y] = child
                        alive_list.append(child)
                elif self.joy > 0:
                    self.joy = round(self.joy/2)    # baby was lost
                self.paternal_genes = {}
                self.rounds_pregnant = 0
                self.pregnant = False
                self.extra_pregnancy_food = 0

    def age(self, month):
        if month > 0 and month % months_in_a_year == self.birth_month:
            self.lifetime = self.lifetime + 1
        self.mated_recently = False
        age_roll = random.randrange(0, round(self.lifetime/months_in_a_year) + 1)
        if age_roll > self.luck:
            self.energy = self.energy - self.lifetime
        scar_heal_roll = random.randrange(0, roll_max)
        if self.scars < 0 and scar_heal_roll < self.luck:
            self.scars = self.scars + 1
        maturity_offset = random.randrange(0, self.luck)
        if not self.mature and self.mature_age <= self.lifetime + maturity_offset:
            self.mature = True
        if self.energy < 0 or (self.joy < 0 and -1*self.joy > self.luck):
            self._die()
    
    # interaction methods
    def _give(self, target, ammount):
        global begs
        
        def give_food(self, target, ammount, do_miserly, teach_skill):
            global gifts
            if self.food >= ammount:
                self.food = self.food - ammount
                target.food = target.food + ammount
                self.joy = self.joy + ammount
            else:
                target.food = target.food + self.food
                self.joy = self.joy + self.food
                self.food = 0
            if do_miserly:
                miserly_roll = random.randrange(0, roll_max)
                if miserly_roll < target.miserly:
                    target.miserly = target.miserly - 1
            if teach_skill and self.skill + self.luck > target.skill:
                target.skill = target.skill + 1
            else:
                skill_up_roll = random.randrange(0, target.luck + target.skill)
                if skill_up_roll > target.skill:
                    target.skill = target.skill + 1
            gifts = gifts + 1
        
        kinship_roll = random.randrange(0, roll_max)
        weak_kin_bond = kinship_roll < self.kinship + target.luck + self.luck
        strong_kin_bond = kinship_roll < self.kinship
        if (self.food > self.greed*self.piggy + ammount - target.luck - target.charm \
                and self.hunger >= 0 \
                and target.luck + target.charm > self.miserly):
            give_food(self, target, ammount, True, False)
        elif (target in self.children and \
                self.food >= ammount and \
                target.hunger < 0 and \
                weak_kin_bond) or \
              (len(self.parents) > 0 and \
              (self.parents[0] in target.parents or \
                self.parents[1] in target.parents) and \
              (self.food >= ammount or \
                target.hunger < 0 or \
                weak_kin_bond)) or \
              (target in self.children and \
              (self.food >= ammount or \
                target.hunger < 0 or \
                strong_kin_bond)) or \
              (len(self.parents) > 0 and \
              (self.parents[0] in target.parents or \
                self.parents[1] in target.parents) and \
              (self.food >= ammount or \
                target.hunger < 0 or \
                strong_kin_bond)):
            give_food(self, target, ammount, False, True)

        begs = begs + 1

    def _trade(self, target, ammount):
        joy_split = round(self.joy - target.joy)
        if target.food > ammount:
            target.food = target.food - ammount
            self.food = self.food + ammount
        else:
            self.food = self.food + target.food
            target.food = 0
        target.joy = target.joy + joy_split
        self.joy = self.joy - joy_split

    def _take(self, target, ammount):
        if self.energy + self.luck > target.energy + target.luck:
            energy_delta = self.energy + self.luck - target.energy - target.luck
            target.energy = target.energy - energy_delta
            self.energy = self.energy - round(energy_delta/2)

            if target.joy > ammount - target.luck:
                target.joy = target.joy - ammount + target.luck
            else:
                target.joy = 0

            if target.food > ammount:
                target.food = target.food - ammount
                self.food = self.food + ammount
            else:
                self.food = self.food + target.food
                target.food = 0
        else:
            energy_delta = target.energy + target.luck - self.energy - self.luck
            target.energy = target.energy - round(energy_delta/2)
            self.energy = self.energy - energy_delta

            if self.joy > ammount - self.luck:
                self.joy = self.joy - ammount + self.luck
            else:
                self.joy = 0

            if self.food > 0:
                target.food = target.food + round(self.food/2)
                self.food = round(self.food/2)
        self.fights = self.fights + 1
        global thefts; thefts = thefts + 1

    def _mate(self, target):
        if self.energy + self.beauty + self.scars > target.beauty + target.scars + target.energy:
            self.joy = self.joy + abs(self.beauty - target.beauty)
            target.joy = target.joy + abs(target.beauty - self.beauty)
            if self.male and not target.male and not target.pregnant:
                target.pregnant = True
                target.rounds_pregnant = 0
                target.paternal_genes = {
                    "luck": self.luck,
                    "diligent": self.diligent,
                    "wit": self.wit,
                    "skill": self.skill,
                    "energy": self.energy,
                    "speed": self.speed,
                    "restless": self.restless,
                    "gestation": self.gestation,
                    "piggy": self.piggy,
                    "greed": self.greed,
                    "hostility": self.hostility,
                    "miserly": self.miserly,
                    "charm": self.charm,
                    "beauty": self.beauty,
                    "mature_age": self.mature_age,
                    "reach": self.reach,
                    "kinship": self.kinship,
                    "food": round(self.food/2)      # This is not a property on the maternal list, daddy pays up front
                    }
                self.food = round(self.food/2)
                target.baby_daddy = self
            elif target.male and not self.male and not self.pregnant:
                self.pregnant = True
                self.rounds_pregnant = 0
                self.paternal_genes = {
                    "luck": target.luck,
                    "diligent": target.diligent,
                    "wit": target.wit,
                    "skill": target.skill,
                    "energy": target.energy,
                    "speed": target.speed,
                    "restless": target.restless,
                    "gestation": target.gestation,
                    "piggy": target.piggy,
                    "greed": target.greed,
                    "hostility": target.hostility,
                    "miserly": target.miserly,
                    "charm": target.charm,
                    "beauty": target.beauty,
                    "mature_age": target.mature_age,
                    "reach": target.reach,
                    "kinship": target.kinship,
                    "food": round(target.food/2)    # This is not a property on the maternal list, daddy pays up front
                }
                self.baby_daddy = target
                target.food = round(target.food/2)
            self.mated_recently = self.luck*self.greed > random.randrange(0, roll_max)
        else:
            self.joy = self.joy + self.beauty - target.beauty 
            target.joy = target.joy + target.beauty - self.beauty
# ["hostility", "piggy", "greed", "miserly", "lifetime"]
drawn_msgs = [
    [("Blocks in order from Top Left to Bottom Right:", default_font_color),
     ("Top Far Left (FL):  Food", default_font_color),
     ("Top Left Center (LC):  Energy", default_font_color),
     ("Top Center Left (CL):  Joy", default_font_color),
     ("Top Center Right (CR):  Love", default_font_color),
     ("Top Right Center (RC):  Hate", default_font_color),
     ("Top Far Right (FR):  Heart", default_font_color),
     ("Bot Far Left (FL):  Hunger", default_font_color),
     ("Bot Left Center (LC):  Gender", default_font_color),
     ("Bot Center Left (CL):  Age", default_font_color),
     ("Bot Center Right (CR):  Luck", default_font_color),
     ("Bot Right Center (RC):  Beauty", default_font_color),
     ("Bot Far Right (FR):  Key/Msg", default_font_color)],
    [("Food Block (Top FL) Key:", default_font_color),
     ("Low:  Food < Greed*Piggy/Luck", LifeFormColors.Food.low),
     ("Medium: Inbetween", LifeFormColors.Food.medium),
     ("High: Food < Greed*Piggy", LifeFormColors.Food.high)],
    [("Hunger Block (Bot FL) Key:", default_font_color),
     ("High:  Hunger < -Luck", LifeFormColors.Hunger.high),
     ("Medium:  -Luck <= Energy < 0", LifeFormColors.Hunger.medium),
     ("Low:  Hunger >= 0", LifeFormColors.Hunger.low)],
    [("Energy Block (Top LC) Key:", default_font_color),
     ("Excess:  Energy > 1000", LifeFormColors.Energy.excess),
     ("High:  800 < Energy <= 1000", LifeFormColors.Energy.high),
     ("Medium:  500 < Energy <= 800", LifeFormColors.Energy.medium),
     ("Low:  250 < Energy <= 500", LifeFormColors.Energy.low),
     ("Dying:  Energy <= 250", LifeFormColors.Energy.dying)],
    [("Joy Block (Top CL) Key:", default_font_color),
     ("Tops:  Joy > 1000", LifeFormColors.Joy.tops),
     ("Excess: 650 < Joy <= 1000", LifeFormColors.Joy.excess),
     ("High: 350 < Joy <= 650", LifeFormColors.Joy.high),
     ("Medium:  100 < Joy <= 350", LifeFormColors.Joy.medium),
     ("Low: 50 < Joy <= 100", LifeFormColors.Joy.low),
     ("Dying: Joy <= 50", LifeFormColors.Joy.dying)],
    [("Love Block (Top CR) Key:", default_font_color),
     ("Wit", LifeFormColors.Loves.wit),
     ("Luck", LifeFormColors.Loves.luck),
     ("Skill", LifeFormColors.Loves.skill),
     ("Diligent", LifeFormColors.Loves.diligent),
     ("Charm", LifeFormColors.Loves.charm),
     ("Beauty", LifeFormColors.Loves.beauty),
     ("Food", LifeFormColors.Loves.food),
     ("Energy", LifeFormColors.Loves.energy),
     ("Joy", LifeFormColors.Loves.joy),
     ("Hostility", LifeFormColors.Loves.hostility),
     ("Kinship", LifeFormColors.Loves.kinship)],
    [("Hate Block (Top RC) Key:", default_font_color),
     ("Hostility", LifeFormColors.Hates.hostility),
     ("Piggy", LifeFormColors.Hates.piggy),
     ("Greed", LifeFormColors.Hates.greed),
     ("Miserly", LifeFormColors.Hates.miserly),
     ("Lifetime", LifeFormColors.Hates.lifetime)],
    [("Heart Block (Top FR) Key:", default_font_color),
     ("Love", LifeFormColors.Heart.love),
     ("Hate", LifeFormColors.Heart.hate)],
    [("Gender Block (Bot LC) Key:", default_font_color),
     ("Female Pregnancy Pre-Start", LifeFormColors.Gender.pregnant),
     ("Female Pregnancy Start", LifeFormColors.Gender.pregnant_round_1),
     ("Female Pregnancy End", LifeFormColors.Gender.pregnant_round_12),
     ("Recently Mated", LifeFormColors.Gender.mated_recently),
     ("Male", LifeFormColors.Gender.male),
     ("Female", LifeFormColors.Gender.female)],
    [("Age Block (Bot CL) Key:", default_font_color),
     (f"Baby: Age < {maturity_min_start}", LifeFormColors.Lifetime.baby),
     (f"Child: {maturity_min_start} <= Age < lifeform's adult age", LifeFormColors.Lifetime.child),
     (f"Adult: lifeform's adult age <= Age < 50", LifeFormColors.Lifetime.adult),
     ("Old: 50 <= Age < 100", LifeFormColors.Lifetime.old),
     ("Ancient: 100 <= Age ", LifeFormColors.Lifetime.ancient)],
    [("Luck Block (Bot CR) Key:", default_font_color),
     (f"Excess: Luck > {luck_max_start}", LifeFormColors.Luck.excess),
     (f"High: {luck_max_start} >= Luck > {round(3*(luck_max_start - luck_min_start)/4 + luck_min_start)}", LifeFormColors.Luck.high),
     (f"Medium: {round(3*(luck_max_start - luck_min_start)/4 + luck_min_start)} >= Luck > {round((luck_max_start - luck_min_start)/2)}", LifeFormColors.Luck.medium),
     (f"Low: {round((luck_max_start - luck_min_start)/2)} >= Luck > {round((luck_min_start - luck_max_start)/4 + luck_min_start)}", LifeFormColors.Luck.low),
     (f"Dying: {round((luck_max_start - luck_min_start)/4 + luck_min_start)} >= Luck ", LifeFormColors.Luck.dying)],
    [("Beauty Block (Bot RC) Key:", default_font_color),
     (f"Excess: Beauty > {beauty_max_start}", LifeFormColors.Beauty.excess),
     (f"High: {beauty_max_start} >= Beauty > {round(3*(beauty_max_start - beauty_min_start)/4 + beauty_min_start)}", LifeFormColors.Beauty.high),
     (f"Medium: {round(3*(beauty_max_start - beauty_min_start)/4 + beauty_min_start)} >= Beauty > {round((beauty_max_start - beauty_min_start)/2)}", LifeFormColors.Beauty.medium),
     (f"Low: {round((beauty_max_start - beauty_min_start)/2)} >= Beauty > {round((beauty_min_start - beauty_max_start)/4 + beauty_min_start)}", LifeFormColors.Beauty.low),
     (f"Dying: {round((beauty_max_start - beauty_min_start)/4 + beauty_min_start)} >= Beauty ", LifeFormColors.Beauty.dying)]
    ]

def print_world(month):
    pygame.display.set_caption(f"LifeForms {int(month/months_in_a_year)}.{month % months_in_a_year + 1} {len(alive_list)}")
    world_board.fill((0, 0, 0))
    for x in range(world_size):
        for y in range(world_size):
            if world[x][y] is not None:                
                if world[x][y].food > world[x][y].greed*world[x][y].piggy:
                    lifeform_food = LifeFormColors.Food.high
                elif world[x][y].food < world[x][y].greed*world[x][y].piggy/world[x][y].luck:
                    lifeform_food = LifeFormColors.Food.low
                else:
                    lifeform_food = LifeFormColors.Food.medium

                if world[x][y].energy > 1000:
                    lifeform_energy = LifeFormColors.Energy.excess
                elif world[x][y].energy > 800:
                    lifeform_energy = LifeFormColors.Energy.high
                elif world[x][y].energy > 500:
                    lifeform_energy = LifeFormColors.Energy.medium
                elif world[x][y].energy > 250:
                    lifeform_energy = LifeFormColors.Energy.low
                else:
                    lifeform_energy = LifeFormColors.Energy.dying

                if world[x][y].joy > 1000:
                    lifeform_joy = LifeFormColors.Joy.tops
                elif world[x][y].joy > 650:
                    lifeform_joy = LifeFormColors.Joy.excess
                elif world[x][y].joy > 350:
                    lifeform_joy = LifeFormColors.Joy.high
                elif world[x][y].joy > 100:
                    lifeform_joy = LifeFormColors.Joy.medium
                elif world[x][y].joy > 50:
                    lifeform_joy = LifeFormColors.Joy.low
                else:
                    lifeform_joy = LifeFormColors.Joy.dying

                if world[x][y].hate_first:
                    lifeform_heart = LifeFormColors.Heart.hate
                else:
                    lifeform_heart = LifeFormColors.Heart.love

                if world[x][y].rounds_pregnant == 1:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_1
                elif world[x][y].rounds_pregnant == 2:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_2
                elif world[x][y].rounds_pregnant == 3:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_3
                elif world[x][y].rounds_pregnant == 4:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_4
                elif world[x][y].rounds_pregnant == 5:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_5
                elif world[x][y].rounds_pregnant == 6:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_6
                elif world[x][y].rounds_pregnant == 7:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_7
                elif world[x][y].rounds_pregnant == 8:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_8
                elif world[x][y].rounds_pregnant == 9:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_9
                elif world[x][y].rounds_pregnant == 10:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_10
                elif world[x][y].rounds_pregnant == 11:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_11
                elif world[x][y].rounds_pregnant == 12:
                    lifeform_gender = LifeFormColors.Gender.pregnant_round_12
                elif world[x][y].pregnant:
                    lifeform_gender = LifeFormColors.Gender.pregnant
                elif world[x][y].mated_recently:
                    lifeform_gender = LifeFormColors.Gender.mated_recently
                elif world[x][y].male:
                    lifeform_gender = LifeFormColors.Gender.male
                else:
                    lifeform_gender = LifeFormColors.Gender.female
                
                if world[x][y].lifetime < maturity_min_start:
                    lifeform_lifetime = LifeFormColors.Lifetime.baby
                elif world[x][y].lifetime < world[x][y].mature_age:
                    lifeform_lifetime = LifeFormColors.Lifetime.child
                elif world[x][y].lifetime < 50:
                    lifeform_lifetime = LifeFormColors.Lifetime.adult
                elif world[x][y].lifetime < 100:
                    lifeform_lifetime = LifeFormColors.Lifetime.old
                else:
                    lifeform_lifetime = LifeFormColors.Lifetime.ancient

                if world[x][y].luck > luck_max_start:
                    lifeform_luck = LifeFormColors.Luck.excess
                elif world[x][y].luck > 3*(luck_max_start - luck_min_start)/4 + luck_min_start:
                    lifeform_luck = LifeFormColors.Luck.high
                elif world[x][y].luck > (luck_min_start + luck_max_start)/2:
                    lifeform_luck = LifeFormColors.Luck.medium
                elif world[x][y].luck > (luck_max_start - luck_min_start)/4 + luck_min_start:
                    lifeform_luck = LifeFormColors.Luck.low
                else:
                    lifeform_luck = LifeFormColors.Luck.dying

                if world[x][y].beauty > beauty_max_start:
                    lifeform_beauty = LifeFormColors.Beauty.excess
                elif world[x][y].beauty > 3*(beauty_max_start - beauty_min_start)/4 + beauty_min_start:
                    lifeform_beauty = LifeFormColors.Beauty.high
                elif world[x][y].beauty > (beauty_min_start + beauty_max_start)/2:
                    lifeform_beauty = LifeFormColors.Beauty.medium
                elif world[x][y].beauty > (beauty_max_start - beauty_min_start)/4 + beauty_min_start:
                    lifeform_beauty = LifeFormColors.Beauty.low
                else:
                    lifeform_beauty = LifeFormColors.Beauty.dying

                if world[x][y].hunger < -1*world[x][y].luck:
                    lifeform_hunger = LifeFormColors.Food.high
                elif world[x][y].food >= 0:
                    lifeform_hunger = LifeFormColors.Hunger.low
                else:
                    lifeform_hunger = LifeFormColors.Food.medium

                lifeform_love = getattr(LifeFormColors.Loves, world[x][y].love)
                lifeform_hate = getattr(LifeFormColors.Hates, world[x][y].hate)
                pygame.draw.rect(world_board, lifeform_food, (x*lifeform_draw_size + 0*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (1*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_energy, (x*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (2*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_joy, (x*lifeform_draw_size + 2*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (3*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_love, (x*lifeform_draw_size + 3*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (4*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_hate, (x*lifeform_draw_size + 4*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (5*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_heart, (x*lifeform_draw_size + 5*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))

                pygame.draw.rect(world_board, (255,255,255), (0, 1*(world_size*lifeform_draw_size + 1), world_size*lifeform_draw_size*6 + 5, 1))

                pygame.draw.rect(world_board, lifeform_hunger, (x*lifeform_draw_size + 0*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (1*(world_size*lifeform_draw_size + 1) - 1, 1*(world_size*lifeform_draw_size + 1), 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_gender, (x*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (2*(world_size*lifeform_draw_size + 1) - 1, 1*(world_size*lifeform_draw_size + 1), 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_lifetime, (x*lifeform_draw_size + 2*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (3*(world_size*lifeform_draw_size + 1) - 1, 1*(world_size*lifeform_draw_size + 1), 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_luck, (x*lifeform_draw_size + 3*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (4*(world_size*lifeform_draw_size + 1) - 1, 1*(world_size*lifeform_draw_size + 1), 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_beauty, (x*lifeform_draw_size + 4*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (5*(world_size*lifeform_draw_size + 1) - 1, 1*(world_size*lifeform_draw_size + 1), 1, world_size*lifeform_draw_size))

    line_counter = 0
    for msg in drawn_msgs[month % len(drawn_msgs)]:
        text = font.render(msg[0], True, msg[1])
        world_board.blit(text, (5*(world_size*lifeform_draw_size + 1) + font_size/2, 1*(world_size*lifeform_draw_size + 1) + line_counter*font_size + font_size/2))
        line_counter = line_counter + 1
    pygame.display.update()
    if save_all_drawings or (save_some_drawings > 0 and month % save_some_drawings == 0):
        pygame.image.save(world_board, os.path.join(os.path.dirname(os.path.realpath(__file__)), f"sim_{run_id}_{int(month/months_in_a_year)}.{month % months_in_a_year + 1}.jpg"))

for creation in range(genesis_count):
    local_x = random.randrange(0, world_size)
    local_y = random.randrange(0, world_size)
    while world[local_x][local_y] is not None:
        local_x = random.randrange(0, world_size)
        local_y = random.randrange(0, world_size)
    new_creature = LifeForm()
    xy = random.choice([True, False])
    gender_text = 'male' if xy else 'female'
    new_creature._spawn(
        x=local_x, 
        y=local_y, 
        id=creation, 
        male=xy,
        luck=random.randrange(luck_min_start, luck_max_start),
        diligent=random.randrange(diligent_min_start, diligent_max_start),
        wit=random.randrange(wit_min_start, wit_max_start),
        energy=random.randrange(min_energy, max_energy),
        lifetime=random.randrange(lifetime_min_start, lifetime_max_start),
        speed=random.randrange(speed_min_start, speed_max_start),
        restless=random.randrange(restless_min_start, restless_max_start),
        mature=True,
        mature_age=random.randrange(maturity_min_start, maturity_max_start),
        gestation=random.randrange(gestation_min_start, gestation_max_start),
        hunger=hunger_start,
        piggy=random.randrange(piggy_min_start, piggy_max_start),
        food=random.randrange(food_min_start, food_max_start),
        greed=random.randrange(greed_min_start, greed_max_start),
        joy=random.randrange(joy_min_start, joy_max_start),
        hostility=random.randrange(hostility_min_start, hostility_max_start),
        miserly=random.randrange(miserly_min_start, miserly_max_start),
        charm=random.randrange(charm_min_start, charm_max_start),
        beauty=random.randrange(beauty_min_start, beauty_max_start),
        reach=random.randrange(reach_min_start, reach_max_start),
        skill=random.randrange(skill_min_start, skill_max_start),
        name=names.get_first_name(gender=gender_text),
        family=names.get_last_name(),
        kinship=random.randrange(kinship_min_start, kinship_max_start),
        birth_month=random.randrange(1, months_in_a_year + 1)
        )
    world[local_x][local_y] = new_creature
    alive_list.append(new_creature)
    last_id = creation

month = 0
detail_csv_file.write("date,name,family,x,y,lifetime,energy,luck,diligent,skill,wit,speed,restless,mature,"
                      "mature_age,male,pregnant,gestation,birth_month,hunger,piggy,food,greed,joy,hostility,"
                      "miserly,charm,beauty,reach,kinship,love,hate,hate_first,parent_0_name,parent_0_family,"
                      "parent_1_name,parent_1_family,children_count,id,fights,scars,alive,begs,gifts,thefts,finds")
while month < apocalypse and len(alive_list) < world_size*world_size:
    random.shuffle(alive_list)
    for lifeform in alive_list:
        lifeform.take_turn(month)
        if draw_world:
            print_world(month)
        if log_details:
            output = f"\n{int(month/months_in_a_year)}.{month % months_in_a_year + 1},"
            output = f"{output}{lifeform.name},"
            output = f"{output}{lifeform.family},"
            output = f"{output}{lifeform.x},"
            output = f"{output}{lifeform.y},"
            output = f"{output}{lifeform.lifetime},"
            output = f"{output}{lifeform.energy},"
            output = f"{output}{lifeform.luck},"
            output = f"{output}{lifeform.diligent},"
            output = f"{output}{lifeform.skill},"
            output = f"{output}{lifeform.wit},"
            output = f"{output}{lifeform.speed},"
            output = f"{output}{lifeform.restless},"
            output = f"{output}{lifeform.mature},"
            output = f"{output}{lifeform.mature_age},"
            output = f"{output}{lifeform.male},"
            output = f"{output}{lifeform.pregnant},"
            output = f"{output}{lifeform.gestation},"
            output = f"{output}{lifeform.birth_month},"
            output = f"{output}{lifeform.hunger},"
            output = f"{output}{lifeform.piggy},"
            output = f"{output}{lifeform.food},"
            output = f"{output}{lifeform.greed},"
            output = f"{output}{lifeform.joy},"
            output = f"{output}{lifeform.hostility},"
            output = f"{output}{lifeform.miserly},"
            output = f"{output}{lifeform.charm},"
            output = f"{output}{lifeform.beauty},"
            output = f"{output}{lifeform.reach},"
            output = f"{output}{lifeform.kinship},"
            output = f"{output}{lifeform.love},"
            output = f"{output}{lifeform.hate},"
            output = f"{output}{lifeform.hate_first},"
            output = f"{output}{'' if len(lifeform.parents)<1 else lifeform.parents[0].name},"
            output = f"{output}{'' if len(lifeform.parents)<1 else lifeform.parents[0].family},"
            output = f"{output}{'' if len(lifeform.parents)<2 else lifeform.parents[1].name},"
            output = f"{output}{'' if len(lifeform.parents)<2 else lifeform.parents[1].family},"
            output = f"{output}{len(lifeform.children)},"
            output = f"{output}{lifeform.id},"
            output = f"{output}{lifeform.fights},"
            output = f"{output}{lifeform.scars},"
            output = f"{output}{len(alive_list)},"
            output = f"{output}{begs},"
            output = f"{output}{gifts},"
            output = f"{output}{thefts},"
            output = f"{output}{finds}"
            detail_csv_file.write(output)
    month = month + 1
detail_csv_file.close()
