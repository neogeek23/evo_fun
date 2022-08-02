# To Do
#   poop
#   love/hate bonus
#   kin affects movement (kin can do more in general)
#   rewrite stats method :(
#   modularize this whole thing
#   society detection/shift mechanism
#   performance

import os
import random
import math
from datetime import datetime
import names
import pygame

log_details = True
draw_world = True
save_all_drawings = True
save_some_drawings = 0     # 0 for no, otherwise months for how frequent to snap a shot

genesis_count = 2000         # how many lifeforms to start intellecth
world_size = 500             # how big is the flat earth
apocalypse_years = 9999      # how many years until no more months can pass
months_in_a_year = 12       # how many months in a year
world_difficulty = 100      # the upper bound for rolls, the pve aspect of the simulation
lifeform_draw_size = 3      # how many pixels a lifeform will get when drawn on the world_board
thanos_angry = 0.95         # what fill percentage Thanos will snap half of e/1 out of existance
tip_the_scale = False       # starts the sim off favoring cooperation

font_size = world_size*lifeform_draw_size//16
min_health = 800
max_health = 1000
lifetime_min_start = 15
lifetime_max_start = 30
maturity_min_start = 13
maturity_max_start = 17
old_age_factor = 2
ancient_age_factor = 5
luck_min_start = 1
luck_max_start = 6
willpower_min_start = 1
willpower_max_start = 7
intellect_min_start = 1
intellect_max_start = 7
speed_min_start = 1
speed_max_start = 7
gestation_min_start = 7
gestation_max_start = 10
hunger_start = 0
piggy_min_start = 19
piggy_max_start = 24
food_min_start = 100
food_max_start = 200
greed_min_start = 3
greed_max_start = 8
happiness_min_start = 0
happiness_max_start = 7
happiness_max = 1000
agression_min_start = 3
agression_max_start = 8
miserly_min_start = 3
miserly_max_start = 25
charm_min_start = 3
charm_max_start = 14
beauty_min_start = 20
beauty_max_start = 40
reach_min_start = 1
reach_max_start = 4
skill_min_start = 1
skill_max_start = 4
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
run_path = os.path.join(os.path.join(os.path.dirname(__file__), "trials"), f"{run_id}")
if not os.path.exists(run_path):
    os.makedirs(run_path)
detail_csv_file = open(os.path.join(run_path, f"{run_id}.csv"), "a+")
default_font_color = (255, 255, 255)
if draw_world:
    pygame.init()
    world_board=pygame.display.set_mode([world_size*lifeform_draw_size*6 + 5, world_size*lifeform_draw_size*2 + 1]) # [x_dim*cell_dim*#_of_cols + #_of_horizontal_line_dividers, y_dim*cell_dim*#_of_rows + #_of_vertical_dividers]
    font = pygame.font.SysFont(None, font_size)
    pygame.display.set_caption("LifeForms")

class LifeFormColors:
    class Food:
        low = (255, 165, 0)
        medium = (255, 255, 0)
        high = (0, 255, 0)
        finder = (0, 0, 255)
        hungry = (255, 0, 0)

    class Skill:
        expert = (222, 204, 166)
        proficient = (164, 167, 38)
        competent = (148, 91, 20)
        beginner = (112, 100, 84)
        novice = (56, 29, 10)
        apprentice = (142, 0, 0)
        child = (0, 0, 0)

    class Hates:
        agression = (94, 15, 35)
        piggy = (108, 193, 178)
        greed = (166, 197, 0)
        miserly = (41, 84, 67)
        lifetime = (242, 105, 12)
        mature_age = (253, 229, 0)
        gestation = (255, 255, 214)

    class Loves:
        intellect = (65, 105, 225)
        luck = (127, 255, 0)
        skill = (138, 43, 226)
        willpower = (0, 255, 255)
        charm = (244, 164, 96)
        beauty = (240, 255, 255)
        food = (245, 222, 179)
        health = (255, 0, 255)
        happiness = (255, 20, 147)
        agression = (255, 69, 0)
        kinship = (139, 69, 19)
    
    class Health:
        excess = (246, 189, 192)
        high = (241, 149, 155)
        medium = (240, 116, 112)
        low = (234, 76, 70)
        dying = (220, 28, 19)

    class Happiness:
        elated = (237, 28, 36)
        happy = (248, 24, 117)
        pleased = (223, 80, 186)
        content = (169, 123, 232)
        sad = (96, 154, 249)
        depressed = (0, 174, 239)

    class Lifetime:
        kid = (0, 204, 255)
        teen = (204, 153, 255)
        adult = (153, 204, 102)
        old = (247, 192, 3)
        ancient = (238, 44, 44)

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
        child = (0, 0, 0)

    class Beauty:
        gold = (252, 205, 18)
        silver = (170, 169, 173)
        bronze = (208, 180, 159)
        rose = (203, 133, 124)
        midnight = (43, 66, 87)

    class Luck:
        blessed = (3, 248, 255)
        lucky = (64, 201, 241)
        normal = (108, 155, 201)
        unlucky = (115, 113, 145)
        cursed = (92, 80, 92)

    class Heart:
        give_fight_trade = (192, 192, 192)  # grey
        give_fight = (155, 38, 182)         # purple
        give_trade = (0, 128, 128)          # teal
        fight_trade = (255, 165, 0)         # orange
        giver = (0, 0, 255)                 # blue
        entrepreneur = (0, 255, 0)          # green
        fighter = (255, 0, 0)               # red
        lover = (255, 156, 136)             # pink
        hater = (255, 255, 0)               # yellow

class LifeForm:
    loves = ["intellect", "luck", "skill", "willpower", "charm", "beauty", "food", "health", "happiness", "agression", "kinship"]
    hates = ["agression", "gestation", "greed", "miserly", "lifetime", "piggy", "mature_age"]

    def __init__(self):
        # broad properties
        self.luck = 0           # catch all positive value - always works in the lifeform's favor, can be used for anything
        self.willpower = 0      # the sticking to it-ness of the lifeform
        self.skill = 0          # value of individual performance capability
        self.intellect = 0      # how many turns ahead a lifeform can try to optimize strategies for dependent props

        # death properties
        self.health = 0         # how far from death the lifeform is
        self.lifetime = 0       # how many turns a lifeform has been alive

        # movement properties
        self.speed = 0          # movements per round

        # reproduction properties
        self.mature = False     # whether or not entity can reproduce
        self.mature_age = 0     # age when mature
        self.male = False       # whether the lifeform is male or female
        self.pregnant = False   # whether or not for the current turn the lifeform is pregnant
        self.gestation = 0      # how many turns it takes for a new lifeform to birth
        self.birth_month = 0    # what month the lifeform was born

        # health properties
        self.hunger = 0         # numerical value representing current hunger, affects health
        self.piggy = 0          # how much food a lifeform tries to eat a turn
        self.baby_piggy = 0     # piggy value but for starting out life
        self.food = 0           # how much food a lifeform owns
        self.greed = 0          # factor of actual need greater that lifeform requires

        # social properties
        self.happiness = 0          # how positive the lifeform is
        self.agression = 0      # how many fights a turn a lifeform can have
        self.miserly = 0        # how willing a lifeform is to assist others
        self.charm = 0          # how much this lifeform affects other lifeforms nearby
        self.beauty = 0         # how preferable a lifeform is for mating
        self.reach = 0          # how far from the lifeform does it care about other lifeform's charm & attractiveness
        self.kinship = 0        # how much a lifeform cares about its kin
        self.family = ""
        self.name = ""
        self.love = ""          # which lifeform property a lifeform wants to be around [intellect, luck, skill, willpower, charm, beauty, food, health]
        self.hate = ""          # which lifeform property a lifeform wants to avoid [fights, piggy, greed, miserly, lifetime]
        self.hate_first = False # whether or not the love or its hate is more driving

        # purely derivied meta properties
        self.actions = []
        self.parents = []
        self.children = []
        self.countrymen = []
        self.neighbors = []
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
        self.fought_recently = False
        self.gave_recently = False
        self.trade_recently = False
        self.food_found_recently = False
        self.scars = 0
        self.juvenile = False
        self.previous_happiness = 0
        self.neighbor_count = 0
        self.countrymen_count = 0

    # primary repeated method
    def take_turn(self, month):
        self._find_neighbors()
        self._decay()
        for action in self.actions:
            action(month)
    
    # lifecycle methods
    def _spawn(self, x, y, id, male, birth_month, luck=0, willpower=0, intellect=0, skill=0, health=0, lifetime=0,
              speed=0, mature=False, gestation=0, hunger=0, piggy=0, food=0, greed=0, happiness=0,
              miserly=0, charm=0, beauty=0, reach=0, kinship=0, name="", family="", mature_age=0, agression=0):
        self.luck=luck
        self.willpower=willpower
        self.intellect=intellect
        self.skill=skill
        self.health=health
        self.lifetime=lifetime
        self.speed=speed
        self.willpower=willpower
        self.mature=mature
        self.mature_age=mature_age
        self.male=male
        self.pregnant=False
        self.gestation=gestation
        self.hunger=hunger
        self.baby_piggy=piggy
        self.piggy=piggy*3
        self.food=food
        self.greed=greed
        self.happiness=happiness
        self.agression=agression
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
        self.actions = [self.move, self.forage, self.interact, self.pregnancy, self.eat, self.push_pull]
        self.love = random.choice(self.loves)
        self.hate = random.choice(self.hates)
        if tip_the_scale:
            self.hate_first = random.choices([True, False], weights=(self.luck*self.luck/world_difficulty, 1 - (self.luck*self.luck/world_difficulty)), k=1)[0]
        else:
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
        self.actions = [self.move, self.interact, self.pregnancy, self.eat, self.push_pull]
        random.shuffle(self.actions)
        self.actions.append(self.age)
        self.actions.insert(0, self.forage)

        for key in mother_genes.keys():
            mod = [mother_genes[key], father_genes[key]]
            mod.sort()
            setattr(self, key, random.randrange(mod[0], mod[1] + 1))

        luck_improve_roll = random.randrange(0, self.luck*self.luck) # maybe [0, luck^2), some social component should be in here when switching to {{society style}}
        if luck_improve_roll <= self.luck:
            self.luck = self.luck + 1

        beauty_improve_roll = random.randrange(0, max(self.beauty*self.beauty - self.luck, 1)) # maybe [0, beauty*beauty - luck)
        if beauty_improve_roll <= self.luck + self.beauty:
            self.beauty = self.beauty + 1

        intellect_improve_roll = random.randrange(0, max(self.intellect*self.intellect - self.luck, 1))
        if intellect_improve_roll <= self.luck + self.intellect:
            self.intellect = self.intellect + 1

        willpower_improve_roll = random.randrange(0, max(self.willpower*self.willpower - self.luck, 1))
        if willpower_improve_roll <= self.luck + self.willpower:
            self.willpower = self.willpower + 1
        
        charm_improve_roll = random.randrange(0, max(self.charm*self.charm - self.luck, 1))
        if charm_improve_roll <= self.luck + self.charm:
            self.charm = self.charm + 1

        reach_improve_roll = random.randrange(0, max(self.reach*self.reach - self.luck, 1))
        if reach_improve_roll <= self.luck + self.reach:
            self.reach = self.reach + 1

        kinship_improve_roll = random.randrange(0, max(self.kinship*self.kinship - self.luck, 1))
        if kinship_improve_roll <= self.luck + self.kinship:
            self.kinship = self.kinship + 1
        
        greed_improve_roll = random.randrange(0, max(self.greed*self.greed - self.luck, 1))
        if greed_improve_roll <= self.luck + self.greed:
            self.greed = max(self.greed - 1, 0) # maybe negative could be generosity

        miserly_improve_roll = random.randrange(0, max(self.miserly*self.miserly - self.luck, 1))
        if miserly_improve_roll <= self.luck + self.miserly:
            self.miserly = max(self.miserly - 1, 0)
        
        love_hate_flip_roll = random.randrange(0, world_difficulty)
        if love_hate_flip_roll <= self.luck:
            self.hate_first = not self.hate_first
        
        love_change_roll = random.randrange(0, world_difficulty)
        if love_change_roll <= self.luck:
            self.love = random.choice(self.loves)

        hate_change_roll = random.randrange(0, world_difficulty)
        if hate_change_roll <= self.luck:
            self.hate = random.choice(self.hates)
        
        self.baby_piggy=self.piggy
        harden_or_soften = random.choice([-1,1])
        setattr(self, self.love, max(getattr(self, self.love) + harden_or_soften, self._get_min_value(self.love)))
        setattr(self, self.hate, max(getattr(self, self.hate) + harden_or_soften, self._get_min_value(self.hate)))

    def _die(self):
        child_luck_sum = 0
        for child in self.children:
            child_luck_sum = child_luck_sum + child.luck
        inheritance_roll = random.randrange(0, world_difficulty)
        if inheritance_roll < child_luck_sum//(len(self.children) + 1):
            inheritance_split = len(self.children) + 1
            for child in self.children:
                child.food = child.food + self.food//inheritance_split
        self.food = 0
        for child in self.children:
            child.parents.remove(self)
        alive_list.remove(self)
        world[self.x][self.y] = None
        del self

    # core actions
    def move(self, _):
        steps_taken = self.rounds_pregnant
        original_x = self.x
        original_y = self.y
        target_x = original_x
        target_y = original_y
        delta_x = random.randrange(-1, 2)
        delta_y = random.randrange(-1, 2)
        while steps_taken < self.speed:
            target_x = self.x + delta_x
            target_y = self.y + delta_y
            delta_x = random.randrange(-1, 2)
            delta_y = random.randrange(-1, 2)
            if self.intellect > 0 and not self.pregnant:
                target_neighbor = None
                for neighbor in self.countrymen:    # may want to change later, neighbors uses reach and countrymen uses intellect (probably should be charm though)
                    if target_neighbor is None:
                        target_neighbor = neighbor
                    # kids go with family
                    elif not self.mature and neighbor in self.parents:
                        target_neighbor = neighbor
                    elif not self.mature and self._is_sibling(neighbor) and target_neighbor not in self.parents:
                        target_neighbor = neighbor
                    # parents be parents plz
                    elif self.mature and neighbor in self.children and neighbor.food < neighbor.piggy*neighbor.greed and self._distance_to(neighbor) > self.reach/2 and \
                        (target_neighbor not in self.children or (target_neighbor in self.children and target_neighbor.food - target_neighbor.piggy*target_neighbor.greed > neighbor.food - neighbor.piggy*neighbor.greed) or \
                        (target_neighbor in self.children and target_neighbor.food - target_neighbor.piggy*target_neighbor.greed == neighbor.food - neighbor.piggy*neighbor.greed and target_neighbor.lifetime > neighbor.lifetime)):
                        target_neighbor = neighbor
                    # echo chambers echo plz
                    elif self.hate_first and neighbor.hate_first and not target_neighbor.hate_first and ((self.hate == neighbor.hate and self.hate != target_neighbor.hate) or getattr(target_neighbor, self.hate) > getattr(neighbor, self.hate)):
                        target_neighbor = neighbor
                    elif not self.hate_first and not neighbor.hate_first and target_neighbor.hate_first and ((self.love == neighbor.love and self.love != target_neighbor.love) or getattr(target_neighbor, self.love) < getattr(neighbor, self.love)):
                        target_neighbor = neighbor
                    # follow your heart
                    elif self.hate_first and getattr(target_neighbor, self.hate) > getattr(neighbor, self.hate):
                        target_neighbor = neighbor
                    elif not self.hate_first and getattr(target_neighbor, self.love) < getattr(neighbor, self.love):
                        target_neighbor = neighbor
                    # follow your demagogue
                    elif self.hate_first and neighbor.hate_first and not target_neighbor.hate_first:
                        target_neighbor = neighbor
                    elif not self.hate_first and not neighbor.hate_first and target_neighbor.hate_first:
                        target_neighbor = neighbor
                    target_x = target_neighbor.x
                    target_y = target_neighbor.y
                if target_neighbor is not None and self.hate_first:
                    if target_neighbor.x > self.x:
                        delta_x = -1
                    elif target_neighbor.x < self.x:
                        delta_x = 1
                    else:
                        delta_x = random.choice([1,-1])
                    if target_neighbor.y > self.y:
                        delta_y = -1
                    elif target_neighbor.y < self.y:
                        delta_y = 1
                    else:
                        delta_y = random.choice([1,-1])
                elif target_neighbor is not None:
                    if target_neighbor.x > self.x:
                        delta_x = 1
                    elif target_neighbor.x < self.x:
                        delta_x = -1
                    else:
                        delta_x = 0
                    if target_neighbor.y > self.y:
                        delta_y = 1
                    elif target_neighbor.y < self.y:
                        delta_y = -1
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
        if self.x == original_x and self.y == original_y and target_x != original_x and target_y != original_y and not self.pregnant:
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

    def push_pull(self, _):
        temptation_roll = random.randrange(0, world_difficulty)
        if temptation_roll < self.agression:
            moved = 0
            for neighbor in self.neighbors:
                distance = random.randrange(0, self.reach//2 + 1)
                if moved < self.agression:
                    x = neighbor.x
                    y = neighbor.y
                    if self.hate_first and getattr(neighbor, self.hate) > getattr(self, self.hate):
                        dx = random.choice([1,-1])
                        dy = random.choice([1,-1])
                        x = (neighbor.x + dx*distance + world_size) % world_size
                        y = (neighbor.y + dy*distance + world_size) % world_size
                    if not self.hate_first and getattr(neighbor, self.love) > getattr(self, self.love):
                        dx = abs(self.x - neighbor.x)
                        dy = abs(self.y - neighbor.y)
                        x_mod = 1
                        if dx > world_size/2.0:
                            dx = world_size - dx
                            x_mod = -1
                        y_mod = 1
                        if dy > world_size/2.0:
                            dy = world_size - dy
                            y_mod = -1
                        dxr = x_mod*random.randrange(0, dx//2 + 1)
                        dyr = y_mod*random.randrange(0, dy//2 + 1)
                        x = (neighbor.x + dxr + world_size) % world_size
                        y = (neighbor.y + dyr + world_size) % world_size
                    if world[x][y] is None:
                        world[x][y] = neighbor
                        world[neighbor.x][neighbor.y] = None
                        neighbor.x = x
                        neighbor.y = y
                        moved = moved + 1
                        if self.hate_first:
                            neighbor.health = neighbor.health - (distance*distance)
                            if moved > 0 :
                                self.fought_recently = True

    def forage(self, _):
        def attempt_food_find(penalty=0):
            attempts = 0
            while attempts < self.willpower and not self.food_found_recently:
                effort_score = self.luck*max(self.intellect, self.willpower)*max(self.skill, self.speed)
                food_roll = random.randrange(0, len(alive_list) + self.countrymen_count + 1)
                self.food_found_recently = self.food_found_recently or food_roll < effort_score
                if food_roll < effort_score:
                    found_ammount_found = int(math.ceil(self.luck + 1)*(max(self.skill, self.speed)*max(self.intellect, self.willpower) - (attempts if attempts < max(self.skill, self.speed)*max(self.intellect, self.willpower) else 0))*(1+(len(self.children)/(1+len(self.children)))))
                    self.food = self.food + found_ammount_found
                    if found_ammount_found > penalty:
                        self.food = self.food + found_ammount_found - penalty
                    global finds; finds = finds + 1
                elif self.happiness > self.hunger and self.hunger < 0:
                    self.happiness = self.happiness + self.hunger
                elif self.happiness > self.hunger and self.hunger >= 0:
                    self.happiness = self.happiness - self.hunger
                attempts = attempts + 1
        self.food_found_recently = False
        if self.mature and self.food < self.greed*self.piggy:
            attempt_food_find()
        elif not self.mature and self.juvenile and \
            (self.hunger < 0 or self.food < self.piggy):
            attempt_food_find(self.mature_age - self.luck - self.lifetime)

    def eat(self, _):
        if self.food > self.piggy + self.extra_pregnancy_food:
            self.food = self.food - self.piggy - self.extra_pregnancy_food
            if self.health + self.piggy + self.luck <= max_health:
                self.health = self.health + self.piggy + self.luck
            else:
                self.health = max_health + self.luck
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
            self.health = self.health + self.hunger
            self.happiness = self.happiness + self.hunger
        elif self.luck > 0:
            satisfaction_roll = random.randrange(0, world_difficulty)
            if satisfaction_roll < self.luck:
                self.happiness = self.happiness + random.randrange(0, self.luck)

    def interact(self, _):
        self.fought_recently = False
        self.mated_recently = False
        self.gave_recently = False
        self.trade_recently = False
        interactions = [self._charity, self._trade, self._steal, self._ire, self._mingle, self._mate, self._minister]
        random.shuffle(interactions)

        i = 0
        j = 0
        while i in range(self.neighbor_count) and i < self.charm:
            neighbor = self.neighbors[i]
            while j in range(len(interactions)) and i*j < self.charm*self.luck:
                interactions[j](neighbor)
                j = j + 1
            i = i + 1

    def pregnancy(self, month):
        if not self.male and self.pregnant:
            if self.rounds_pregnant < self.gestation:
                self.rounds_pregnant = self.rounds_pregnant + 1
                self.extra_pregnancy_food = round(self.baby_piggy*(self.rounds_pregnant/self.gestation))
            else:
                maternal_genes = {
                    "luck": self.luck,
                    "willpower": self.willpower,
                    "intellect": self.intellect,
                    "health": self.health,
                    "speed": self.speed,
                    "gestation": self.gestation,
                    "piggy": self.baby_piggy,
                    "greed": self.greed,
                    "agression": self.agression,
                    "miserly": self.miserly,
                    "charm": self.charm,
                    "beauty": self.beauty,
                    "mature_age": self.mature_age,
                    "reach": self.reach,
                    "kinship": self.kinship
                }
                baby_place = self._find_nearest_touchable_opening()
                if baby_place is not None:
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
                            food=self.food//2+self.paternal_genes["food"],
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
                        self.food = self.food//2
                        self.children.append(child)
                        self.baby_daddy.children.append(child)
                        world[child.x][child.y] = child
                        alive_list.append(child)
                elif self.happiness > 0:
                    self.happiness = 0    # baby was lost
                self.paternal_genes = {}
                self.rounds_pregnant = 0
                self.extra_pregnancy_food = 0
                self.pregnant = False

    def age(self, month):
        if month > 0 and month % months_in_a_year == self.birth_month:
            self.lifetime = self.lifetime + 1
            self.happiness = self.happiness + self.lifetime//(self.birth_month+1) # happy birthda...month
        scar_heal_roll = random.randrange(0, self.beauty + 1)
        if self.scars < 0 and scar_heal_roll < self.luck:
            self.scars = self.scars + 1
        if not self.mature:
            self.mature = self.mature_age <= self.lifetime
            if self.mature:
                self.piggy = self.piggy + self.piggy//3
            if not self.juvenile:
                self.juvenile = self.mature_age <= self.lifetime + self.luck
                if self.juvenile:
                    self.piggy = self.piggy + self.piggy//2
        if self.lifetime//self.mature_age > self.luck//2:
            self.health = self.health - self.lifetime
        if self.health < 0 or (self.happiness < 0 and abs(self.happiness) > max(max(self.luck, self.willpower),self.intellect)):
            self._die()

    # interaction methods
    def _discern(self):
        skill_up_roll = random.randrange(0, self.skill*self.skill + 1)
        if self.luck + self.charm + self.intellect > skill_up_roll:
            self.skill = self.skill + 1

    def _mingle(self, target):
        if target.beauty + target.scars > self.beauty + self.scars or target.charm + target.luck > self.charm:
            if target.love == self.love:
                self.happiness = self.happiness + self.luck*target.luck
                self._discern()
            if target.hate == self.hate:
                self.happiness = self.happiness + self.luck*target.luck
                self._discern()
            if getattr(target, self.love) + target.charm > getattr(self, self.love):
                delta_love = getattr(target, self.love) + target.charm - getattr(self, self.love)
                self.happiness = self.happiness + delta_love
                target.happiness = target.happiness + delta_love//4
                self._discern()
            if getattr(target, self.hate) - target.charm < getattr(self, self.hate):
                delta_hate = getattr(target, self.hate) - target.charm + getattr(self, self.hate)
                self.happiness = self.happiness + delta_hate
                target.happiness = target.happiness + delta_hate//4
                self._discern()
            
            if target.hate == self.love and target.beauty + target.scars + target.luck < self.beauty + self.scars:
                if target.happiness > self.luck*self.charm:
                    target.happiness = target.happiness - self.luck*self.charm
                else:
                    target.happiness = 0

                if self.happiness > target.luck*target.charm:
                    self.happiness = self.happiness - target.luck*target.charm
                else:
                    self.happiness = 0
            if self.hate == target.love and target.beauty + target.scars + target.luck < self.beauty + self.scars:
                if target.happiness > self.luck*self.charm:
                    target.happiness = target.happiness - self.luck*self.charm
                else:
                    target.happiness = 0

                if self.happiness > target.luck*target.charm:
                    self.happiness = self.happiness - target.luck*target.charm
                else:
                    self.happiness = 0
            if getattr(target, self.love) + target.charm < getattr(self, self.love) and target.beauty + target.scars + target.luck < self.beauty + self.scars:
                delta_love = getattr(self, self.love) - target.charm - getattr(target, self.love)
                if target.happiness > delta_love:
                    target.happiness = target.happiness - delta_love
                else:
                    target.happiness = 0
                self.happiness = self.happiness + delta_love//4
            if getattr(target, self.hate) - target.charm > getattr(self, self.hate) and target.beauty + target.scars + target.luck < self.beauty + self.scars:
                delta_hate = getattr(target, self.hate) - target.charm + getattr(self, self.hate)
                if target.happiness > delta_hate:
                    target.happiness = target.happiness - delta_hate
                else:
                    target.happiness = 0
                self.happiness = self.happiness + delta_hate//4

    def _minister(self, target):
        if self.family == target.family or self.miserly < target.piggy - target.food + target.hunger:
            target._charity(self)

    def _give(self, target, ammount):
        global begs

        def give_food(self, target, ammount, do_miserly, teach_skill):
            global gifts
            if self.food >= ammount:
                self.food = self.food - ammount
                target.food = target.food + ammount
                self.happiness = self.happiness + ammount
            else:
                target.food = target.food + self.food
                self.happiness = self.happiness + self.food
                self.food = 0
            if do_miserly:
                miserly_roll = random.randrange(0, world_difficulty)
                if miserly_roll < target.miserly:
                    target.miserly = target.miserly - 1
            if teach_skill and self.skill + self.luck > target.skill:
                target.skill = target.skill + 1
            else:
                skill_up_roll = random.randrange(0, target.luck + target.skill)
                if skill_up_roll > target.skill:
                    target.skill = target.skill + 1
            gifts = gifts + 1

        kinship_roll = random.randrange(0, target.kinship*target.kinship//self.luck + 1)
        weak_kin_bond = kinship_roll < self.kinship + target.kinship
        strong_kin_bond = kinship_roll < self.kinship
        if (self.food > self.greed*self.piggy + ammount - target.luck - target.charm \
            and self.hunger >= 0 \
            and (target.luck + target.charm > self.miserly or \
                target.luck + target.beauty > self.miserly or \
                target.luck + target.intellect > self.miserly)):
            give_food(self, target, ammount, True, False)
        elif (target in self.children and \
                self.food >= ammount and \
                target.hunger < 0 and \
                weak_kin_bond) or \
              (self._is_sibling(target) and \
              (self.food >= ammount or \
                target.hunger < 0 and \
                weak_kin_bond)) or \
              (target in self.children and \
              (self.food >= ammount or \
                target.hunger < 0 or \
                strong_kin_bond)) or \
              (self._is_sibling(target) and \
              (self.food >= ammount or \
                target.hunger < 0 or \
                strong_kin_bond)):
            give_food(self, target, ammount, False, True)
        begs = begs + 1

    def _trade(self, target):
        if self.happiness > target.happiness and \
            self.charm + self.luck > target.charm and \
            target.food > 0 and \
            self.food < self.greed*self.piggy:
            happiness_split = round(self.happiness - target.happiness)
            if target.food > self.greed*self.piggy - self.food:
                target.food = target.food - (self.greed*self.piggy - self.food)
                self.food = self.food + (self.greed*self.piggy - self.food)
            else:
                self.food = self.food + target.food
                target.food = 0
            target.happiness = target.happiness + happiness_split
            self.happiness = self.happiness - happiness_split
            self.trade_recently = True

    def _take(self, target, ammount):
        if self.health + self.luck > target.health + target.luck:
            health_delta = self.health + self.luck - target.health - target.luck
            target.health = target.health - health_delta
            self.health = self.health - health_delta//2

            if target.happiness > ammount - target.luck:
                target.happiness = target.happiness - ammount + target.luck
            else:
                target.happiness = 0

            if target.food > ammount:
                target.food = target.food - ammount
                self.food = self.food + ammount
            else:
                self.food = self.food + target.food
                target.food = 0
        else:
            health_delta = target.health + target.luck - self.health - self.luck
            target.health = target.health - health_delta//2
            self.health = self.health - health_delta

            if self.happiness > ammount - self.luck:
                self.happiness = self.happiness - ammount + self.luck
            else:
                self.happiness = 0

            if self.food > 0:
                target.food = target.food + self.food//2
                self.food = self.food//2
        self.fights = self.fights + 1
        global thefts; thefts = thefts + 1

    def _mate(self, target):
        if ((self.male and not target.male) or (target.male and not self.male)) and \
            not self.mated_recently and \
            not target.mated_recently and \
            not target.pregnant and \
            not self.pregnant and \
            self.mature and \
            target.mature and \
            not self._is_sibling(target) and target not in self.parents and target not in self.children and \
            target.health + (target.beauty + target.scars)*target.luck//2 > self.health and \
            target.happiness + target.charm + getattr(target, target.love) > self.happiness and \
            (self.health + self.beauty + self.scars > target.beauty + target.scars + target.health or \
            self.happiness + self.charm + self.luck > target.happiness + target.charm + target.luck):

            self_after_glow = max(abs(self.beauty - target.beauty), abs(getattr(self, self.love) - getattr(target, self.love)))
            target_after_glow = max(abs(self.beauty - target.beauty), abs(getattr(target, target.love) - getattr(self, target.love)))
            self.happiness = self.happiness + self_after_glow
            target.happiness = target.happiness + target_after_glow
            if self.male and not target.male and not target.pregnant:
                target.pregnant = True
                target.rounds_pregnant = 0
                target.paternal_genes = {
                    "luck": self.luck,
                    "willpower": self.willpower,
                    "intellect": self.intellect,
                    "health": self.health,
                    "speed": self.speed,
                    "gestation": self.gestation,
                    "piggy": self.baby_piggy,
                    "greed": self.greed,
                    "agression": self.agression,
                    "miserly": self.miserly,
                    "charm": self.charm,
                    "beauty": self.beauty,
                    "mature_age": self.mature_age,
                    "reach": self.reach,
                    "kinship": self.kinship,
                    "food": self.food//2      # This is not a property on the maternal list, daddy pays up front
                    }
                self.food = self.food//2
                target.baby_daddy = self
            elif target.male and not self.male and not self.pregnant:
                self.pregnant = True
                self.rounds_pregnant = 0
                self.paternal_genes = {
                    "luck": target.luck,
                    "willpower": target.willpower,
                    "intellect": target.intellect,
                    "health": target.health,
                    "speed": target.speed,
                    "gestation": target.gestation,
                    "piggy": target.baby_piggy,
                    "greed": target.greed,
                    "agression": target.agression,
                    "miserly": target.miserly,
                    "charm": target.charm,
                    "beauty": target.beauty,
                    "mature_age": target.mature_age,
                    "reach": target.reach,
                    "kinship": target.kinship,
                    "food": target.food//2    # This is not a property on the maternal list, daddy pays up front
                }
                self.baby_daddy = target
                target.food = target.food//2
            if self.luck > 0 and self.greed > 0:
                self.mated_recently = self.luck + self.greed > random.randrange(0, self.luck*self.greed)
            else:
                self.mated_recently = True

    def _ire(self, target):
        if self.happiness < target.happiness and \
            self.health > target.health and \
            self.health > 0 and \
            target.health > 0 and \
            not self.pregnant and \
            not target.pregnant and \
            not self.fought_recently and \
            (((self.mature and target.mature) or (not self.mature and not target.mature)) or \
            (((not self.mature and target.mature) or (not target.mature and self.mature)) and \
                ((not self._is_sibling(target) and target not in self.parents and \
                target not in self.children) or self.kinship <= target.kinship + target.luck) and \
                self.lifetime + self.luck > target.lifetime and \
                target.lifetime + target.luck > self.lifetime and \
                self.health > target.health)) and \
            (self.luck + target.luck < target.luck or \
                self.beauty + target.luck < target.beauty or \
                self.intellect + target.luck < target.intellect or \
                self.food + target.luck < target.food or \
                self.hunger + target.luck < target.hunger):
            grievances = []
            if self.food + target.luck < target.food:
                grievances.append("food")
            if self.hunger + target.luck < target.hunger:
                grievances.append("hunger")
            if self.beauty + target.luck + self.scars < target.beauty + target.scars:
                grievances.append("beauty")
            if self.intellect + target.luck < target.intellect:
                grievances.append("intellect")
            if self.luck + target.luck < target.luck:
                grievances.append("luck")

            random.shuffle(grievances)
            if len(grievances) > 0:
                if grievances[0] == "food":
                    self._take(target, target.food - self.food + target.happiness - self.happiness)
                elif grievances[0] == "hunger":
                    self._take(target, (-1*self.hunger) + target.hunger + target.happiness - self.happiness)
                elif grievances[0] == "beauty":
                    delta_beauty = target.beauty + target.scars - (self.beauty + self.scars + target.luck)
                    self.health = self.health - delta_beauty
                    self.happiness = self.happiness + delta_beauty//2
                    if -1*target.scars <= target.beauty//2:
                        target.scars = target.scars - delta_beauty//2
                    else:
                        target.scars = target.beauty*-1
                    if target.happiness > delta_beauty:
                        target.happiness = target.happiness - delta_beauty
                    else:
                        target.happiness = 0
                elif grievances[0] == "intellect":
                    delta_intellect = target.intellect - self.intellect
                    self.health = self.health - delta_intellect
                    self.happiness = self.happiness + delta_intellect//2
                    target.intellect = target.intellect - delta_intellect
                    if target.happiness > delta_intellect:
                        target.happiness = target.happiness - delta_intellect
                    else:
                        target.happiness = 0
                elif grievances[0] == "luck":
                    delta_luck = target.intellect - self.intellect
                    self.health = self.health - delta_luck
                    self.happiness = self.happiness + delta_luck//2
                    if target.happiness > delta_luck:
                        target.happiness = target.happiness - delta_luck
                    else:
                        target.happiness = 0

                if self.luck < target.beauty + target.scars:
                    target.scars = target.scars - 1
                if target.luck < self.beauty + self.scars:
                    self.scars = self.scars - 1
                self.fights = self.fights + 1
                self.fought_recently = True

    def _steal(self, target):
        if (self.hunger < 0 or self.food < self.greed*self.piggy//2) and \
            self.health > 0 and target.health > 0 and not self.fought_recently and \
            (((self.mature and target.mature) or (not self.mature and not target.mature)) or \
            (((not self.mature and target.mature) or (not target.mature and self.mature)) and \
                ((not self._is_sibling(target) and target not in self.parents and \
                target not in self.children) or self.kinship <= target.kinship + target.luck) and \
                self.lifetime + self.luck > target.lifetime and \
                target.lifetime + target.luck > self.lifetime and \
                self.health > target.health)):
            self._take(target, self.greed*self.piggy - self.food)
            self.fought_recently = True

    def _charity(self, target):
        if self.hunger < 0:
            original_food = self.food
            target._give(self, -1*self.hunger)
            target.gave_recently = original_food < self.food or target.gave_recently
        if self.food < self.greed*self.piggy:
            original_food = self.food
            target._give(self, self.greed*self.piggy - self.food)
            target.gave_recently = original_food < self.food or target.gave_recently
        if self.food < self.piggy:
            original_food = self.food
            target._give(self, self.piggy - self.food)
            target.gave_recently = original_food < self.food or target.gave_recently

    # useful support methods
    def _is_sibling(self, target):
        for parent in self.parents:
            if parent in target.parents:
                return True
        return False

    def _find_neighbors(self):
        self.neighbors = [world[(i + world_size) % world_size][(j + world_size) % world_size]
                          for i in range(self.x - self.reach, self.x + self.reach + 1)
                          for j in range(self.y - self.reach, self.y + self.reach + 1)
                          if world[(i + world_size) % world_size][(j + world_size) % world_size] is not None 
                          and world[(i + world_size) % world_size][(j + world_size) % world_size] is not self]
        self.countrymen = [world[(i + world_size) % world_size][(j + world_size) % world_size]
                          for i in range(self.x - self.intellect, self.x + self.intellect + 1)
                          for j in range(self.y - self.intellect, self.y + self.intellect + 1)
                          if world[(i + world_size) % world_size][(j + world_size) % world_size] is not None 
                          and world[(i + world_size) % world_size][(j + world_size) % world_size] is not self]
        self.neighbor_count = len(self.neighbors)
        self.countrymen_count = len(self.countrymen)
        random.shuffle(self.neighbors)
        random.shuffle(self.countrymen)

    def _find_nearest_touchable_opening(self):
        open_place = None
        open_place_found = False
        reach = 0
        while reach < self.reach and not open_place_found:
            open_place_cords = [((i + world_size) % world_size, (j + world_size) % world_size)
                                for i in range(self.x - reach, self.x + reach + 1)
                                for j in range(self.y - reach, self.y + reach + 1)]
            index = 0
            while index < len(open_place_cords) and not open_place_found:
                open_place_found = world[open_place_cords[index][0]][open_place_cords[index][1]] is None
                if open_place_found:
                    open_place = open_place_cords[index]
                index = index + 1
            reach = reach + 1
        return open_place

    def _decay(self):
        rot_roll = random.randrange(0, self.food + 1)
        if self.piggy*self.greed*self.luck < rot_roll:
            rot_prevention = 2*random.randrange(self.willpower//2, self.willpower + self.luck + 1)
            self.food = self.food - (self.food//4 - (rot_prevention if rot_prevention <= self.food//8 else self.food//8))
        if self.happiness - self.previous_happiness > 0 and (random.randrange(0, self.happiness - self.previous_happiness) > self.luck*max(self.charm, self.beauty + self.scars) or self.happiness > happiness_max + self.luck):
            factor = math.ceil(self.happiness/(self.previous_happiness if self.previous_happiness > 0 else 1)) if self.previous_happiness > 0 else 1
            self.happiness = self.happiness//factor + (self.willpower + self.luck if self.willpower + self.luck < self.happiness//factor else (self.willpower + self.luck)//factor)
        lonliness = self.reach*self.reach*4 - self.neighbor_count
        self.happiness = self.happiness - round(lonliness/(32*math.exp(-((len(alive_list) + genesis_count)/genesis_count))))
        self.previous_happiness = self.happiness

    def _distance_to(self, target):
        dx = abs(target.x - self.x)
        dy = abs(target.y - self.y)
        
        if dx > world_size/2.0:
            dx = world_size - dx

        if dy > world_size/2.0:
            dy = world_size - dy

        return math.sqrt(dx*dx + dy*dy)

    def _get_min_value(self, prop):
        if prop == "intellect":
            return intellect_min_start
        elif prop == "luck":
            return luck_min_start
        elif prop == "skill":
            return skill_min_start
        elif prop == "willpower":
            return willpower_min_start
        elif prop == "charm":
            return charm_min_start
        elif prop == "beauty":
            return beauty_min_start
        elif prop == "agression":
            return agression_min_start
        elif prop == "kinship":
            return kinship_min_start
        elif prop == "gestation":
            return gestation_min_start
        elif prop == "greed":
            return greed_min_start
        elif prop == "miserly":
            return miserly_min_start
        elif prop == "piggy":
            return piggy_min_start
        elif prop == "mature_age":
            return maturity_min_start
        return getattr(self, prop)

drawn_msgs = [
    [("Blocks from Top Left to Bottom Right:", default_font_color),
     ("Top Far Left (FL): Food", default_font_color),
     ("Top Left Center (LC): Health", default_font_color),
     ("Top Center Left (CL): Happiness", default_font_color),
     ("Top Center Right (CR)  Love", default_font_color),
     ("Top Right Center (RC): Hate", default_font_color),
     ("Top Far Right (FR): Heart", default_font_color),
     ("Bot Far Left (FL): Hunger", default_font_color),
     ("Bot Left Center (LC): Gender", default_font_color),
     ("Bot Center Left (CL): Age", default_font_color),
     ("Bot Center Right (CR): Luck", default_font_color),
     ("Bot Right Center (RC): Beauty + Scars", default_font_color),
     ("Bot Far Right (FR): Key/Msg", default_font_color)],
    [("Food Block (Top FL) Key:", default_font_color),
     ("Finder:  Food Found", LifeFormColors.Food.finder),
     ("High: Food > Greed*Piggy", LifeFormColors.Food.high),
     ("Medium: Piggy < Food < Piggy*Greed", LifeFormColors.Food.medium),
     ("Low:  Food < Piggy", LifeFormColors.Food.low),
     ("Hungry :(", LifeFormColors.Food.hungry)],
    [("Skill Block (Bot FL) Key:", default_font_color),
     ("Expert:  Skill > 60", LifeFormColors.Skill.expert),
     ("Proficient:  45 < Skill <= 60", LifeFormColors.Skill.proficient),
     ("Competent:  30 < Skill <= 45", LifeFormColors.Skill.competent),
     ("Beginner:  15 < Skill <= 30", LifeFormColors.Skill.beginner),
     ("Novice:  Skill <= 15", LifeFormColors.Skill.novice),
     ("Apprentice:  Teen in training", LifeFormColors.Skill.apprentice),
     ("Child:  Immature", LifeFormColors.Skill.child)],
    [("Health Block (Top LC) Key:", default_font_color),
     ("Excess:  Health > 1000", LifeFormColors.Health.excess),
     ("High:  750 < Health <= 1000", LifeFormColors.Health.high),
     ("Medium:  400 < Health <= 750", LifeFormColors.Health.medium),
     ("Low:  100 < Health <= 400", LifeFormColors.Health.low),
     ("Dying:  Health <= 100", LifeFormColors.Health.dying)],
    [("Happiness Block (Top CL) Key:", default_font_color),
     ("Elated:  Happiness > 1000", LifeFormColors.Happiness.elated),
     ("Happy: 650 < Happiness <= 1000", LifeFormColors.Happiness.happy),
     ("Pleased: 350 < Happiness <= 650", LifeFormColors.Happiness.pleased),
     ("Content:  100 < Happiness <= 350", LifeFormColors.Happiness.content),
     ("Sad: 0 < Happiness <= 100", LifeFormColors.Happiness.sad),
     ("Depressed: Happiness <= 0", LifeFormColors.Happiness.depressed)],
    [("Love Block (Top CR) Key:", default_font_color),
     ("Intellect", LifeFormColors.Loves.intellect),
     ("Luck", LifeFormColors.Loves.luck),
     ("Skill", LifeFormColors.Loves.skill),
     ("Willpower", LifeFormColors.Loves.willpower),
     ("Charm", LifeFormColors.Loves.charm),
     ("Beauty", LifeFormColors.Loves.beauty),
     ("Food", LifeFormColors.Loves.food),
     ("Health", LifeFormColors.Loves.health),
     ("Happiness", LifeFormColors.Loves.happiness),
     ("Agression", LifeFormColors.Loves.agression),
     ("Kinship", LifeFormColors.Loves.kinship)],
    [("Hate Block (Top RC) Key:", default_font_color),
     ("Agression", LifeFormColors.Hates.agression),
     ("Piggy", LifeFormColors.Hates.piggy),
     ("Greed", LifeFormColors.Hates.greed),
     ("Miserly", LifeFormColors.Hates.miserly),
     ("Lifetime", LifeFormColors.Hates.lifetime),
     ("Gestation Period", LifeFormColors.Hates.gestation),
     ("Maturity", LifeFormColors.Hates.mature_age)],
    [("Heart Block (Top FR) Key:", default_font_color),
     ("Lover", LifeFormColors.Heart.lover),
     ("Fighter (F)", LifeFormColors.Heart.fighter),
     ("Hater", LifeFormColors.Heart.hater),
     ("Entrepreneur (E)", LifeFormColors.Heart.entrepreneur),
     ("Giver (G)", LifeFormColors.Heart.giver),
     ("Philantropist (G & E)", LifeFormColors.Heart.give_trade),
     ("Scammer (F & E)", LifeFormColors.Heart.fight_trade),
     ("Predator (G & F)", LifeFormColors.Heart.give_fight),
     ("Villian (G,F,E)", LifeFormColors.Heart.give_fight_trade)],
    [("Gender Block (Bot LC) Key:", default_font_color),
     ("Female Pregnancy Pre-Start", LifeFormColors.Gender.pregnant),
     ("Female Pregnancy Start", LifeFormColors.Gender.pregnant_round_1),
     ("Female Pregnancy End", LifeFormColors.Gender.pregnant_round_12),
     ("Recently Mated", LifeFormColors.Gender.mated_recently),
     ("Male", LifeFormColors.Gender.male),
     ("Female", LifeFormColors.Gender.female),
     ("Child", LifeFormColors.Gender.child)],
    [("Age Block (Bot CL) Key:", default_font_color),
     ("Kid: Immature", LifeFormColors.Lifetime.kid),
     ("Teen: Age + Luck >= Maturity", LifeFormColors.Lifetime.teen),
     (f"Adult: Maturity < Age <= Maturity*{old_age_factor}", LifeFormColors.Lifetime.adult),
     (f"Old: Maturity*{old_age_factor} < Age <= Maturity*{ancient_age_factor}", LifeFormColors.Lifetime.old),
     (f"Ancient: Maturity*{ancient_age_factor} < Age", LifeFormColors.Lifetime.ancient)],
    [("Luck Block (Bot CR) Key:", default_font_color),
     (f"Blessed: Luck > {5*luck_max_start}", LifeFormColors.Luck.blessed),
     (f"Lucky: {5*luck_max_start} >= Luck > {3*luck_max_start}", LifeFormColors.Luck.lucky),
     (f"Normal: {3*luck_max_start} >= Luck > {luck_max_start}", LifeFormColors.Luck.normal),
     (f"Unlucky: {luck_max_start} >= Luck > {(luck_min_start - luck_max_start)//2 + luck_min_start}", LifeFormColors.Luck.unlucky),
     (f"Cursed: {(luck_max_start - luck_min_start)//2 + luck_min_start} >= Luck ", LifeFormColors.Luck.cursed)],
    [("Beauty + Scars Block (Bot RC) Key:", default_font_color),
     (f"Gold: Beauty > {beauty_max_start}", LifeFormColors.Beauty.gold),
     (f"Silver: {beauty_max_start} >= Beauty > {3*(beauty_max_start - beauty_min_start)//4 + beauty_min_start}", LifeFormColors.Beauty.silver),
     (f"Bronze: {3*(beauty_max_start - beauty_min_start)//4 + beauty_min_start} >= Beauty > {(beauty_min_start + beauty_max_start)//2}", LifeFormColors.Beauty.bronze),
     (f"Rose: {(beauty_min_start + beauty_max_start)//2} >= Beauty > {(beauty_max_start - beauty_min_start)//4 + beauty_min_start}", LifeFormColors.Beauty.rose),
     (f"Midnight: {(beauty_max_start - beauty_min_start)//4 + beauty_min_start} >= Beauty ", LifeFormColors.Beauty.midnight)]
    ]

def print_world(month):
    adults = adult_count()
    pygame.display.set_caption(f"LifeForms - {len(alive_list)} alive on {month//months_in_a_year}.{month % months_in_a_year + 1} {len(alive_list)-adults}:{adults} (child:adult)")
    world_board.fill((0, 0, 0))
    for x in range(world_size):
        for y in range(world_size):
            if world[x][y] is not None:
                if world[x][y].food_found_recently:
                    lifeform_food = LifeFormColors.Food.finder
                elif world[x][y].hunger < 0:
                    lifeform_food = LifeFormColors.Food.hungry
                elif world[x][y].food > world[x][y].greed*world[x][y].piggy:
                    lifeform_food = LifeFormColors.Food.high
                elif world[x][y].food > world[x][y].piggy:
                    lifeform_food = LifeFormColors.Food.medium
                else:
                    lifeform_food = LifeFormColors.Food.low

                if world[x][y].health > 1000:
                    lifeform_health = LifeFormColors.Health.excess
                elif world[x][y].health > 750:
                    lifeform_health = LifeFormColors.Health.high
                elif world[x][y].health > 400:
                    lifeform_health = LifeFormColors.Health.medium
                elif world[x][y].health > 100:
                    lifeform_health = LifeFormColors.Health.low
                else:
                    lifeform_health = LifeFormColors.Health.dying

                if world[x][y].happiness > 1000:
                    lifeform_happiness = LifeFormColors.Happiness.elated
                elif world[x][y].happiness > 650:
                    lifeform_happiness = LifeFormColors.Happiness.happy
                elif world[x][y].happiness > 350:
                    lifeform_happiness = LifeFormColors.Happiness.pleased
                elif world[x][y].happiness > 100:
                    lifeform_happiness = LifeFormColors.Happiness.content
                elif world[x][y].happiness > 0:
                    lifeform_happiness = LifeFormColors.Happiness.sad
                else:
                    lifeform_happiness = LifeFormColors.Happiness.depressed

                if world[x][y].fought_recently and world[x][y].gave_recently and world[x][y].trade_recently:
                    lifeform_heart = LifeFormColors.Heart.give_fight_trade
                elif world[x][y].fought_recently and world[x][y].gave_recently:
                    lifeform_heart = LifeFormColors.Heart.give_fight
                elif world[x][y].fought_recently and world[x][y].trade_recently:
                    lifeform_heart = LifeFormColors.Heart.fight_trade
                elif world[x][y].gave_recently and world[x][y].trade_recently:
                    lifeform_heart = LifeFormColors.Heart.give_trade
                elif world[x][y].gave_recently:
                    lifeform_heart = LifeFormColors.Heart.giver
                elif world[x][y].trade_recently:
                    lifeform_heart = LifeFormColors.Heart.entrepreneur
                elif world[x][y].fought_recently:
                    lifeform_heart = LifeFormColors.Heart.fighter
                elif world[x][y].hate_first:
                    lifeform_heart = LifeFormColors.Heart.hater
                else:
                    lifeform_heart = LifeFormColors.Heart.lover

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
                elif not world[x][y].mature:
                    lifeform_gender = LifeFormColors.Gender.child
                elif world[x][y].male:
                    lifeform_gender = LifeFormColors.Gender.male
                else:
                    lifeform_gender = LifeFormColors.Gender.female
                
                if world[x][y].mature:
                    if world[x][y].lifetime < world[x][y].mature_age*2:
                        lifeform_lifetime = LifeFormColors.Lifetime.adult
                    elif world[x][y].lifetime < world[x][y].mature_age*5:
                        lifeform_lifetime = LifeFormColors.Lifetime.old
                    else:
                        lifeform_lifetime = LifeFormColors.Lifetime.ancient
                else:
                    if world[x][y].juvenile:
                        lifeform_lifetime = LifeFormColors.Lifetime.teen
                    else:
                        lifeform_lifetime = LifeFormColors.Lifetime.kid

                if world[x][y].luck > 5*luck_max_start:
                    lifeform_luck = LifeFormColors.Luck.blessed
                elif world[x][y].luck > 3*luck_max_start:
                    lifeform_luck = LifeFormColors.Luck.lucky
                elif world[x][y].luck > luck_max_start:
                    lifeform_luck = LifeFormColors.Luck.normal
                elif world[x][y].luck > (luck_max_start - luck_min_start)//2 + luck_min_start:
                    lifeform_luck = LifeFormColors.Luck.unlucky
                else:
                    lifeform_luck = LifeFormColors.Luck.cursed

                if world[x][y].beauty + world[x][y].scars > beauty_max_start:
                    lifeform_beauty = LifeFormColors.Beauty.gold
                elif world[x][y].beauty + world[x][y].scars > 3*(beauty_max_start - beauty_min_start)//4 + beauty_min_start:
                    lifeform_beauty = LifeFormColors.Beauty.silver
                elif world[x][y].beauty + world[x][y].scars > (beauty_min_start + beauty_max_start)//2:
                    lifeform_beauty = LifeFormColors.Beauty.bronze
                elif world[x][y].beauty + world[x][y].scars > (beauty_max_start - beauty_min_start)//4 + beauty_min_start:
                    lifeform_beauty = LifeFormColors.Beauty.rose
                else:
                    lifeform_beauty = LifeFormColors.Beauty.midnight

                if world[x][y].skill > 60 and world[x][y].mature:
                    lifeform_skill = LifeFormColors.Skill.expert
                elif world[x][y].skill > 45 and world[x][y].mature:
                    lifeform_skill = LifeFormColors.Skill.proficient
                elif world[x][y].skill > 30 and world[x][y].mature:
                    lifeform_skill = LifeFormColors.Skill.competent
                elif world[x][y].skill > 15 and world[x][y].mature:
                    lifeform_skill = LifeFormColors.Skill.beginner
                elif world[x][y].mature:
                    lifeform_skill = LifeFormColors.Skill.novice
                elif world[x][y].juvenile:
                    lifeform_skill = LifeFormColors.Skill.apprentice
                else:
                    lifeform_skill = LifeFormColors.Skill.child

                lifeform_love = getattr(LifeFormColors.Loves, world[x][y].love)
                lifeform_hate = getattr(LifeFormColors.Hates, world[x][y].hate)
                pygame.draw.rect(world_board, lifeform_food, (x*lifeform_draw_size + 0*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (1*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_health, (x*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (2*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_happiness, (x*lifeform_draw_size + 2*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (3*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_love, (x*lifeform_draw_size + 3*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (4*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_hate, (x*lifeform_draw_size + 4*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))
                pygame.draw.rect(world_board, (255,255,255), (5*(world_size*lifeform_draw_size + 1) - 1, 0, 1, world_size*lifeform_draw_size))
                pygame.draw.rect(world_board, lifeform_heart, (x*lifeform_draw_size + 5*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size, lifeform_draw_size, lifeform_draw_size))

                pygame.draw.rect(world_board, (255,255,255), (0, 1*(world_size*lifeform_draw_size + 1), world_size*lifeform_draw_size*6 + 5, 1))

                pygame.draw.rect(world_board, lifeform_skill, (x*lifeform_draw_size + 0*(world_size*lifeform_draw_size + 1), y*lifeform_draw_size + 1*(world_size*lifeform_draw_size + 1), lifeform_draw_size, lifeform_draw_size))
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
    text = font.render(f"Alive:  {len(alive_list)} ({round(len(alive_list)/(world_size*world_size)*100, 2)}%) {len(alive_list)-adults}:{adults} (child:adult)", True, default_font_color)
    world_board.blit(text, (5*(world_size*lifeform_draw_size + 1) + font_size//2, 1*(world_size*lifeform_draw_size + 1) + line_counter*font_size + font_size//2))
    line_counter = line_counter + 1
    text = font.render(f"Year {month//months_in_a_year}.{month % months_in_a_year + 1} - Avg Neighbors:  {avg_neighbors()}", True, default_font_color)
    world_board.blit(text, (5*(world_size*lifeform_draw_size + 1) + font_size//2, 1*(world_size*lifeform_draw_size + 1) + line_counter*font_size + font_size//2))
    line_counter = line_counter + 1
    for msg in drawn_msgs[month % len(drawn_msgs)]:
        text = font.render(msg[0], True, msg[1])
        world_board.blit(text, (5*(world_size*lifeform_draw_size + 1) + font_size//2, 1*(world_size*lifeform_draw_size + 1) + line_counter*font_size + font_size//2))
        line_counter = line_counter + 1
    pygame.display.update()
    if save_all_drawings or (save_some_drawings > 0 and month % save_some_drawings == 0):
        try:
            pygame.image.save(world_board, os.path.join(run_path, f"sim_{run_id}_{month//months_in_a_year}.{month % months_in_a_year + 1}.jpg"))
        except:
            # Fucking Windows 98
            pass

def find_in_world(target):
    i = 0
    j = 0
    target_found = False
    while i in range(world_size) and not target_found:
        while j in range(world_size) and not target_found:
            target_found = world[i][j] == target
            j = j + 1
        i = i + 1
    return target_found, (i, j)

def thanos_snap():
    for target in alive_list[:round(len(alive_list)*thanos_angry)]:
        target._die()

def adult_count():
    count = 0
    for creature in alive_list:
        if creature.mature:
            count = count + 1
    return count

def avg_neighbors():
    count = 0
    for creature in alive_list:
        count = count + creature.neighbor_count
    return round(count/max(len(alive_list), 1), 2)

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
        willpower=random.randrange(willpower_min_start, willpower_max_start),
        intellect=random.randrange(intellect_min_start, intellect_max_start),
        health=random.randrange(min_health, max_health),
        lifetime=random.randrange(lifetime_min_start, lifetime_max_start),
        speed=random.randrange(speed_min_start, speed_max_start),
        mature=True,
        mature_age=random.randrange(maturity_min_start, maturity_max_start),
        gestation=random.randrange(gestation_min_start, gestation_max_start),
        hunger=hunger_start,
        piggy=random.randrange(piggy_min_start, piggy_max_start),
        food=random.randrange(food_min_start, food_max_start),
        greed=random.randrange(greed_min_start, greed_max_start),
        happiness=random.randrange(happiness_min_start, happiness_max_start),
        agression=random.randrange(agression_min_start, agression_max_start),
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
if log_details:
    detail_csv_file.write("date,name,family,x,y,lifetime,health,luck,willpower,skill,intellect,speed,mature,"
                        "mature_age,male,pregnant,gestation,birth_month,hunger,piggy,food,greed,happiness,agression,"
                        "miserly,charm,beauty,reach,kinship,love,hate,hate_first,parent_0_name,parent_0_family,"
                        "parent_1_name,parent_1_family,children_count,id,fights,scars,alive,begs,gifts,thefts,finds")
while month < apocalypse and len(alive_list) < world_size*world_size:
    random.shuffle(alive_list)
    if len(alive_list) > world_size*world_size*thanos_angry:
        thanos_snap()
    for lifeform in alive_list:
        if world[lifeform.x][lifeform.y] is lifeform:
            lifeform.take_turn(month)
            if log_details:
                output = f"\n{month//months_in_a_year}.{month % months_in_a_year + 1},"
                output = f"{output}{lifeform.name},"
                output = f"{output}{lifeform.family},"
                output = f"{output}{lifeform.x},"
                output = f"{output}{lifeform.y},"
                output = f"{output}{lifeform.lifetime},"
                output = f"{output}{lifeform.health},"
                output = f"{output}{lifeform.luck},"
                output = f"{output}{lifeform.willpower},"
                output = f"{output}{lifeform.skill},"
                output = f"{output}{lifeform.intellect},"
                output = f"{output}{lifeform.speed},"
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
                output = f"{output}{lifeform.happiness},"
                output = f"{output}{lifeform.agression},"
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
        else:
            print(f"I, {lifeform.name} {lifeform.family}, believed I was at ({lifeform.x},{lifeform.y}) but {None if world[lifeform.x][lifeform.y] is None else f'{world[lifeform.x][lifeform.y].name} {world[lifeform.x][lifeform.y].family}'} is there instead.")
            lifeform_search = find_in_world(lifeform)
            if lifeform_search[0]:
                print(f"I, {lifeform.name} {lifeform.family} was found at {lifeform_search[1]}.")
                if world[lifeform_search[1][0]][lifeform_search[1][1]] is None:
                    lifeform.x = lifeform_search[1][0]
                    lifeform.y = lifeform_search[1][0]
                    print(f"I, {lifeform.name} {lifeform.family}, now know that I'm at ({lifeform.x},{lifeform.y}).")
                else:
                    print(f"I, {lifeform.name} {lifeform.family}, wanted to go to ({lifeform_search[1][0]},{lifeform_search[1][0]}) since that is where I was found, but now I see {world[lifeform_search[1][0]][lifeform_search[1][1]].name} {world[lifeform_search[1][0]][lifeform_search[1][1]].family} there.")
            else:
                print(f"I, {lifeform.name} {lifeform.family}, am not in the world.")
                if lifeform.health > 0:
                    print(f"I, {lifeform.name} {lifeform.family}, am healthy.  I guess I should just die.")
                    lifeform._die()
                else:
                    print(f"I, {lifeform.name} {lifeform.family}, am dead.  I guess I'm a zombie'.  I should not be counted amoung the living anymore.")
                    alive_list.remove(lifeform)
    if draw_world:
        print_world(month)
    month = month + 1
detail_csv_file.close()
