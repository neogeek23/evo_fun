# To Do
#   birth near moms
#   non-random movements
#       move away from theieves
#       group by charming lifeforms
#       group by kin
#   intelligence grants predictive movements
#   bonus for kin in requests
#   bonus for children in requests
#   world full apocalypse
#   graphical output
#   csv outputs
#   rewrite stats method :(
#   more happiness balancing (not having it inherited)
#   modularize this whole thing

import random
import math
import names

genesis_count = 100        # how many lifeforms to start with
world_size = 64             # how big is the flat earth
apocalypse_years = 99       # how many yaers until no more months can pass
months_in_a_year = 12       # how many months in a year
roll_max = 100              # the upper bound for rolls
min_health = 800
max_health = 1000
lifetime_min_start = 20
lifetime_max_start = 50
maturity_min_start = 12
maturity_max_start = 19
luck_min_start = 1
luck_max_start = 8
resilence_min_start = 1
resilence_max_start = 5
intelligence_min_start = 1
intelligence_max_start = 3
speed_min_start = 1
speed_max_start = 5
restless_min_start = 0
restless_max_start = 4
gestation_min_start = 7
gestation_max_start = 10
hunger_start = 0
eat_rate_min_start = 2
eat_rate_max_start = 7
food_min_start = 20
food_max_start = 50
greed_min_start = 1
greed_max_start = 8
happiness_min_start = 0
happiness_max_start = 7
stingy_min_start = 1
stingy_max_start = 14
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
month_avgs = []
month_lows = []
month_highs = []

apocalypse = apocalypse_years*months_in_a_year
world = [[None for i in range(world_size)] for j in range(world_size)]
alive_list = []

class LifeForm:
    def __init__(self):
        # broad properties
        self.luck = 0           # catch all positive/negative value
        self.resilence = 0      # how many failures a lifeform can tollerate in a turn
        self.skill = 0          # value of individual performance capability
        self.intelligence = 0   # how many turns ahead a lifeform can try to optimize strategies for dependent props

        # death properties
        self.health = 0         # how far from death the lifeform is
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
        self.hunger = 0         # numerical value representing current hunger, affects health
        self.eat_rate = 0       # how much food a lifeform tries to eat a turn
        self.food = 0           # how much food a lifeform owns
        self.greed = 0          # factor of actual need greater that lifeform requires

        # social properties
        self.happiness = 0      # how happy the lifeform is
        self.stingy = 0         # how willing a lifeform is to assist others against happiness
        self.charm = 0          # how much this lifeform affects other lifeforms nearby
        self.beauty = 0         # how preferable a lifeform is for mating
        self.reach = 0          # how far from the lifeform does it care about other lifeform's charm & attractiveness
        self.kinship = 0        # how much a lifeform cares about its kin
        self.family = ""
        self.name = ""

        # purely derivied meta properties
        self.parents = []
        self.children = []
        self.prediction_success_rate = 0
        self.x = 0                          # current x position in the world
        self.y = 0                          # current y position in the world
        self.id = 0
        self.rounds_pregnant = 0
        self.extra_pregnancy_food = 0
        self.paternal_genes = {}
        self.baby_daddy = None
        self.mated_recently = False

    # methods
    def take_turn(self, month):
        self.move()
        self.forage()
        self.mingle()
        self.pregnancy(month)
        self.eat()
        self.age(month)
    
    def spawn(self, x, y, id, male, birth_month, luck=0, resilence=0, intelligence=0, skill=0, health=0, lifetime=0,
              speed=0,restless=0, mature=False, gestation=0, hunger=0, eat_rate=0, food=0, greed=0, happiness=0,
              stingy=0, charm=0, beauty=0, reach=0, kinship=0, name="", family="", mature_age=0):
        self.luck=luck
        self.resilence=resilence
        self.intelligence=intelligence
        self.skill=skill
        self.health=health
        self.lifetime=lifetime
        self.speed=speed
        self.restless=restless
        self.resilence=resilence
        self.mature=mature
        self.mature_age=mature_age
        self.male=male
        self.pregnant=False
        self.gestation=gestation
        self.hunger=hunger
        self.eat_rate=eat_rate
        self.food=food
        self.greed=greed
        self.happiness=happiness
        self.stingy=stingy
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

    def birth(self, x, y, id, male, food, mother_genes, father_genes, name, family, birth_month):
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
        self.birth_month = birth_month

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

        intelligence_improve_roll = random.randrange(0, roll_max)
        if intelligence_improve_roll <= self.luck + self.intelligence:
            self.intelligence = self.intelligence + 1

        resilence_improve_roll = random.randrange(0, roll_max)
        if resilence_improve_roll <= self.luck + self.resilence:
            self.resilence = self.resilence + 1
        
        charm_improve_roll = random.randrange(0, roll_max)
        if charm_improve_roll <= self.luck + self.charm:
            self.charm = self.charm + 1

        kinship_improve_roll = random.randrange(0, roll_max)
        if kinship_improve_roll <= self.luck + self.kinship:
            self.kinship = self.kinship + 1
        
        greed_improve_roll = random.randrange(0, roll_max)
        if greed_improve_roll <= self.luck + self.greed:
            self.greed = self.greed - 1

        stingy_improve_roll = random.randrange(0, roll_max)
        if stingy_improve_roll <= self.luck + self.stingy:
            self.stingy = self.stingy - 1

    def die(self):
        alive_list.remove(world[self.x][self.y])
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

    def move(self):
        steps_taken = 0
        while steps_taken < self.speed:
            delta_x = random.randrange(-1, 2)
            delta_y = random.randrange(-1, 2)
            while self.x + delta_x >= world_size or self.x + delta_x < 0:
                delta_x = random.randrange(-1, 2)
            while self.y + delta_y >= world_size or self.y + delta_y < 0:
                delta_y = random.randrange(-1, 2)
            if world[self.x + delta_x][self.y + delta_y] == None:
                world[self.x + delta_x][self.y + delta_y] = self
                world[self.x][self.y] = None
                self.x = self.x + delta_x
                self.y = self.y + delta_y
            steps_taken = steps_taken + 1

    def give(self, target, ammount):
        if self.food > self.greed*self.eat_rate + ammount - target.luck - target.charm \
                and self.hunger >= 0 \
                and self.happiness + target.luck + target.charm > self.stingy:
            self.food = self.food - ammount
            target.food = target.food + ammount
            # print(f"happiness pre-bump give {self.happiness}")
            self.happiness = self.happiness + self.luck + self.stingy + target.charm
            # print(f"happiness post-bump give {self.happiness}")
            stingy_roll = random.randrange(0, roll_max)
            if stingy_roll < target.stingy:
                target.stingy = target.stingy - 1
            skill_up_roll = random.randrange(0, target.luck + target.skill)
            if skill_up_roll > target.skill:
                target.skill = target.skill + 1
            global gifts; gifts = gifts + 1
        global begs; begs = begs + 1

    def take(self, target, ammount):
        if self.health + self.luck > target.health + target.luck:
            health_delta = self.health + self.luck - target.health - target.luck
            target.health = target.health - health_delta
            self.health = self.health - round(health_delta/2)

            if target.happiness > ammount - target.luck:
                # print(f"happiness pre-bump take target {target.happiness}")
                target.happiness = target.happiness - ammount + target.luck
                # print(f"happiness post-bump take target {target.happiness}")
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
            target.health = target.health - round(health_delta/2)
            self.health = self.health - health_delta

            if self.happiness > ammount - self.luck:
                # print(f"happiness pre-bump take self {self.happiness}")
                self.happiness = self.happiness - ammount + self.luck
                # print(f"happiness post-bump take self {self.happiness}")
            else:
                self.happiness = 0

            if self.food > 0:
                target.food = target.food + round(self.food/2)
                self.food = round(self.food/2)
        global thefts; thefts = thefts + 1

    def forage(self):
        if self.mature and self.food < self.greed*self.eat_rate:
            food_found = False
            attempts = 0
            while attempts < self.resilence and not food_found:
                food_roll = random.randrange(0, roll_max)
                if food_roll < (self.luck + self.skill + self.intelligence):
                    food_found = True
                attempts = attempts + 1
            if food_found:
                luck_imapct = random.randrange(0, self.luck)
                found_ammount_found = luck_imapct*(self.skill*self.intelligence - attempts - 1)
                self.food = self.food + found_ammount_found
                global finds; finds = finds + 1
            else:
                self.happiness = self.happiness + self.hunger

    def age(self, month):
        if month > 0 and month % months_in_a_year == self.birth_month:
            self.lifetime = self.lifetime + 1
        self.mated_recently = False
        age_roll = random.randrange(0, round(self.lifetime/months_in_a_year) + 1)
        if age_roll > self.luck:
            self.health = self.health - self.lifetime
        maturity_offset = random.randrange(0, self.luck)
        if not self.mature and self.mature_age <= self.lifetime + maturity_offset:
            self.mature = True
        if self.health < 0:
            self.die()

    def mingle(self):
        neighbors = [world[i][j] 
                    for i in range(self.x - self.reach, self.x + self.reach + 1) 
                    for j in range(self.y - self.reach, self.y + self.reach + 1) 
                    if i > -1 and j > -1 and j < len(world[0]) and i < len(world)]
        random.shuffle(neighbors)
        trade_requests = 0
        for neighbor in neighbors:
            if neighbor is not None:
                # trade/steal
                if self.hunger < 0:
                    neighbor.give(self, -1*self.hunger)
                    trade_requests = trade_requests + 1
                if self.food < self.greed*self.eat_rate:
                    neighbor.give(self, self.greed*self.eat_rate - self.food)
                    trade_requests = trade_requests + 1
                if trade_requests > self.resilence and \
                        (self.hunger < 0 or self.food < round(self.greed*self.eat_rate/2)):
                    self.take(neighbor, self.greed*self.eat_rate - self.food)
                    trade_requests = trade_requests + 1

                # mate/conceive
                if self.male is not neighbor.male and \
                        not self.mated_recently and \
                        not neighbor.pregnant and \
                        not self.pregnant and \
                        self.mature and \
                        neighbor.mature and \
                        neighbor.health + neighbor.beauty*neighbor.luck*neighbor.charm > self.health:
                    self.mate(neighbor)
                
                # attack/ignore

    def mate(self, target):
        if self.health + self.beauty > target.beauty + target.health:
            # print(f"happiness pre-bump mate success {self.happiness} {self.beauty} {target.beauty}")
            self.happiness = self.happiness + abs(self.beauty - target.beauty) + self.luck
            target.happiness = target.happiness + abs(target.beauty - self.beauty) + target.luck
            # print(f"happiness post-bump mate success {self.happiness}")
            if self.male and not target.male and not target.pregnant:
                target.pregnant = True
                target.rounds_pregnant = 0
                target.paternal_genes = {
                    "luck": self.luck,
                    "resilence": self.resilence,
                    "intelligence": self.intelligence,
                    "skill": self.skill,
                    "health": self.health,
                    "speed": self.speed,
                    "restless": self.restless,
                    "gestation": self.gestation,
                    "eat_rate": self.eat_rate,
                    "greed": self.greed,
                    "happiness": self.happiness,
                    "stingy": self.stingy,
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
                    "resilence": target.resilence,
                    "intelligence": target.intelligence,
                    "skill": target.skill,
                    "health": target.health,
                    "speed": target.speed,
                    "restless": target.restless,
                    "gestation": target.gestation,
                    "eat_rate": target.eat_rate,
                    "greed": target.greed,
                    "happiness": target.happiness,
                    "stingy": target.stingy,
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
            # if rejected, happiness transfer
            # print(f"happiness pre-bump mate reject self {self.happiness}")
            self.happiness = self.happiness + self.beauty - target.beauty 
            # print(f"happiness post-bump mate reject self {self.happiness}")
            # print(f"happiness pre-bump mate reject target {target.happiness}")
            target.happiness = target.happiness + target.beauty - self.beauty
            # print(f"happiness post-bump mate reject target {target.happiness}")

    def pregnancy(self, month):
        if not self.male and self.pregnant:
            if self.rounds_pregnant < self.gestation:
                self.rounds_pregnant = self.rounds_pregnant + 1
                self.extra_pregnancy_food = round(self.eat_rate*(self.rounds_pregnant/self.gestation))
            else:
                maternal_genes = {
                    "luck": self.luck,
                    "resilence": self.resilence,
                    "intelligence": self.intelligence,
                    "skill": self.skill,
                    "health": self.health,
                    "speed": self.speed,
                    "restless": self.restless,
                    "gestation": self.gestation,
                    "eat_rate": self.eat_rate,
                    "greed": self.greed,
                    "happiness": self.happiness,
                    "stingy": self.stingy,
                    "charm": self.charm,
                    "beauty": self.beauty,
                    "mature_age": self.mature_age,
                    "reach": self.reach,
                    "kinship": self.kinship
                }
                local_x = random.randrange(0, world_size)
                local_y = random.randrange(0, world_size)
                while world[local_x][local_y] is not None and len(alive_list) < world_size*world_size:
                    local_x = random.randrange(0, world_size)
                    local_y = random.randrange(0, world_size)
                global last_id; last_id = last_id + 1
                xy = random.choice([True, False])
                gender_text = 'male' if xy else 'female'
                family_name = self.baby_daddy.family if xy else self.family
                if len(alive_list) < world_size*world_size:
                    child = LifeForm()
                    child.birth(
                        x=local_x,
                        y=local_y,
                        id=last_id,
                        male=xy,
                        food=round(self.food/2)+self.paternal_genes["food"],
                        mother_genes=maternal_genes,
                        father_genes=self.paternal_genes,
                        name=names.get_first_name(gender=gender_text),
                        family=family_name,
                        birth_month=month%months_in_a_year
                        )
                    child.parents.append(self)
                    child.parents.append(self.baby_daddy)
                    self.food = round(self.food/2)
                    self.children.append(child)
                    self.baby_daddy.children.append(child)
                    world[local_x][local_y] = child
                    alive_list.append(child)
                self.paternal_genes = {}
                self.rounds_pregnant = 0
                self.pregnant = False

    def eat(self):
        if self.food > self.eat_rate + self.extra_pregnancy_food:
            self.food = self.food - self.eat_rate - self.extra_pregnancy_food
            if self.health + self.eat_rate + self.luck <= max_health:
                self.health = self.health + self.eat_rate + self.luck
            else:
                self.health = max_health + self.luck
        else:
            self.hunger = self.hunger + self.food - self.eat_rate - self.extra_pregnancy_food
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
            happiness_mods = [self.hunger, self.luck]
            happiness_mods.sort()
            # print(f"happiness pre-bump eat hungry {self.happiness}")
            self.happiness = self.happiness + random.randrange(happiness_mods[0], happiness_mods[1] + 1)
            # print(f"happiness post-bump eat hungry {self.happiness}")
        elif self.luck > 0:
            # print(f"happiness pre-bump eat hungerless {self.happiness}")
            self.happiness = self.happiness + random.randrange(0, self.luck)
            # print(f"happiness post-bump eat hungerless {self.happiness}")


def print_world():
    pass

def lifeform_stats(month):
    # To any future critic... I felt lazy... sue me
    precision = 2
    new_average = {
        "luck": 0,
        "resilence": 0,
        "skill": 0,
        "intelligence": 0,
        "health": 0,
        "lifetime": 0,
        "speed": 0,
        "restless": 0,
        "mature": 0,
        "male": 0,
        "pregnant": 0,
        "gestation": 0,
        "hunger": 0,
        "eat_rate": 0,
        "food": 0,
        "greed": 0,
        "happiness": 0,
        "stingy": 0,
        "charm": 0,
        "beauty": 0,
        "reach": 0,
        "kinship": 0,
        "alive": len(alive_list)
    }
    new_high = {
        "luck": 0,
        "resilence": 0,
        "skill": 0,
        "intelligence": 0,
        "health": 0,
        "lifetime": 0,
        "speed": 0,
        "restless": 0,
        "gestation": 0,
        "hunger": 0,
        "eat_rate": 0,
        "food": 0,
        "greed": 0,
        "happiness": 0,
        "stingy": 0,
        "charm": 0,
        "beauty": 0,
        "reach": 0,
        "kinship": 0
    }
    new_low = {
        "luck": luck_max_start*apocalypse,
        "resilence": resilence_max_start*apocalypse,
        "skill": skill_max_start*apocalypse,
        "intelligence": intelligence_max_start*apocalypse,
        "health": max_health*apocalypse,
        "lifetime": lifetime_max_start*apocalypse,
        "speed": speed_max_start*apocalypse,
        "restless": restless_max_start*apocalypse,
        "gestation": gestation_max_start*apocalypse,
        "hunger": apocalypse*apocalypse,
        "eat_rate": eat_rate_max_start*apocalypse,
        "food": food_max_start*apocalypse,
        "greed": greed_max_start*apocalypse,
        "happiness": happiness_max_start*apocalypse,
        "stingy": stingy_max_start*apocalypse,
        "charm": charm_max_start*apocalypse,
        "beauty": beauty_max_start*apocalypse,
        "reach": reach_max_start*apocalypse,
        "kinship": kinship_max_start*apocalypse
    }
    for lifeform in alive_list:
        new_average["luck"] = new_average["luck"] + lifeform.luck
        new_average["resilence"] = new_average["resilence"] + lifeform.resilence
        new_average["skill"] = new_average["skill"] + lifeform.skill
        new_average["intelligence"] = new_average["intelligence"] + lifeform.intelligence
        new_average["health"] = new_average["health"] + lifeform.health if lifeform.health > 0 else 0
        new_average["lifetime"] = new_average["lifetime"] + lifeform.lifetime
        new_average["speed"] = new_average["speed"] + lifeform.speed
        new_average["restless"] = new_average["restless"] + lifeform.restless
        new_average["mature"] = new_average["mature"] + 1 if lifeform.mature else 0
        new_average["male"] = new_average["male"] + 1 if lifeform.male else -1
        new_average["pregnant"] = new_average["pregnant"] + 1 if not lifeform.male and lifeform.pregnant else 0
        new_average["gestation"] = new_average["gestation"] + lifeform.gestation if not lifeform.male else new_average["gestation"]
        new_average["hunger"] = new_average["hunger"] + lifeform.hunger
        new_average["eat_rate"] = new_average["eat_rate"] + lifeform.eat_rate
        new_average["food"] = new_average["food"] + lifeform.food
        new_average["greed"] = new_average["greed"] + lifeform.greed
        new_average["happiness"] = new_average["happiness"] + lifeform.happiness
        new_average["stingy"] = new_average["stingy"] + lifeform.stingy
        new_average["charm"] = new_average["charm"] + lifeform.charm
        new_average["beauty"] = new_average["beauty"] + lifeform.beauty
        new_average["reach"] = new_average["reach"] + lifeform.reach
        new_average["kinship"] = new_average["kinship"] + lifeform.kinship

        new_high["luck"] = lifeform.luck if new_high["luck"] < lifeform.luck else new_high["luck"]
        new_high["resilence"] = lifeform.resilence if new_high["resilence"] < lifeform.resilence else new_high["resilence"]
        new_high["skill"] = lifeform.skill if new_high["skill"] < lifeform.skill else new_high["skill"]
        new_high["intelligence"] = lifeform.intelligence if new_high["intelligence"] < lifeform.intelligence else new_high["intelligence"]
        new_high["health"] = lifeform.health if new_high["health"] < lifeform.health else new_high["health"]
        new_high["lifetime"] = lifeform.lifetime if new_high["lifetime"] < lifeform.lifetime else new_high["lifetime"]
        new_high["speed"] = lifeform.speed if new_high["speed"] < lifeform.speed else new_high["speed"]
        new_high["restless"] = lifeform.restless if new_high["restless"] < lifeform.restless else new_high["restless"]
        new_high["gestation"] = lifeform.gestation if new_high["gestation"] < lifeform.gestation and not lifeform.male else new_high["gestation"]
        new_high["hunger"] = lifeform.hunger if new_high["hunger"] < lifeform.hunger else new_high["hunger"]
        new_high["eat_rate"] = lifeform.eat_rate if new_high["eat_rate"] < lifeform.eat_rate else new_high["eat_rate"]
        new_high["food"] = lifeform.food if new_high["food"] < lifeform.food else new_high["food"]
        new_high["greed"] = lifeform.greed if new_high["greed"] < lifeform.greed else new_high["greed"]
        new_high["happiness"] = lifeform.happiness if new_high["happiness"] < lifeform.luck else new_high["happiness"]
        new_high["stingy"] = lifeform.stingy if new_high["stingy"] < lifeform.stingy else new_high["stingy"]
        new_high["charm"] = lifeform.charm if new_high["charm"] < lifeform.charm else new_high["charm"]
        new_high["beauty"] = lifeform.beauty if new_high["beauty"] < lifeform.beauty else new_high["beauty"]
        new_high["reach"] = lifeform.reach if new_high["reach"] < lifeform.reach else new_high["reach"]
        new_high["kinship"] = lifeform.kinship if new_high["kinship"] < lifeform.kinship else new_high["kinship"]
        
        new_low["luck"] = lifeform.luck if new_low["luck"] >= lifeform.luck else new_low["luck"]
        new_low["resilence"] = lifeform.resilence if new_low["resilence"] >= lifeform.resilence else new_low["resilence"]
        new_low["skill"] = lifeform.skill if new_low["skill"] >= lifeform.skill else new_low["skill"]
        new_low["intelligence"] = lifeform.intelligence if new_low["intelligence"] >= lifeform.intelligence else new_low["intelligence"]
        new_low["health"] = lifeform.health if new_low["health"] >= lifeform.health else new_low["health"]
        new_low["lifetime"] = lifeform.lifetime if new_low["lifetime"] >= lifeform.lifetime else new_low["lifetime"]
        new_low["speed"] = lifeform.speed if new_low["speed"] >= lifeform.speed else new_low["speed"]
        new_low["restless"] = lifeform.restless if new_low["restless"] >= lifeform.restless else new_low["restless"]
        new_low["gestation"] = lifeform.gestation if new_low["gestation"] >= lifeform.gestation and not lifeform.male else new_low["gestation"]
        new_low["hunger"] = lifeform.hunger if new_low["hunger"] >= lifeform.hunger else new_low["hunger"]
        new_low["eat_rate"] = lifeform.eat_rate if new_low["eat_rate"] >= lifeform.eat_rate else new_low["eat_rate"]
        new_low["food"] = lifeform.food if new_low["food"] >= lifeform.food else new_low["food"]
        new_low["greed"] = lifeform.greed if new_low["greed"] >= lifeform.greed else new_low["greed"]
        new_low["happiness"] = lifeform.happiness if new_low["happiness"] >= lifeform.happiness else new_low["happiness"]
        new_low["stingy"] = lifeform.stingy if new_low["stingy"] >= lifeform.stingy else new_low["stingy"]
        new_low["charm"] = lifeform.charm if new_low["charm"] >= lifeform.charm else new_low["charm"]
        new_low["beauty"] = lifeform.beauty if new_low["beauty"] >= lifeform.beauty else new_low["beauty"]
        new_low["reach"] = lifeform.reach if new_low["reach"] >= lifeform.reach else new_low["reach"]
        new_low["kinship"] = lifeform.kinship if new_low["kinship"] >= lifeform.kinship else new_low["kinship"]

    new_average["luck"] = round(new_average["luck"]/len(alive_list), precision)
    new_average["resilence"] = round(new_average["resilence"]/len(alive_list), precision)
    new_average["skill"] = round(new_average["skill"]/len(alive_list), precision)
    new_average["intelligence"] = round(new_average["intelligence"]/len(alive_list), precision)
    new_average["health"] = round(new_average["health"]/len(alive_list), precision)
    new_average["lifetime"] = round(new_average["lifetime"]/len(alive_list), precision)
    new_average["speed"] = round(new_average["speed"]/len(alive_list), precision)
    new_average["restless"] = round(new_average["restless"]/len(alive_list), precision)
    new_average["mature"] = round(new_average["mature"]/len(alive_list)*100, precision)
    new_average["male"] = new_average["male"] + math.ceil(len(alive_list)/2)
    new_average["pregnant"] = round(new_average["pregnant"]/(len(alive_list) - new_average["male"])*100, precision) if len(alive_list) - new_average["male"] > 0 else 0
    new_average["gestation"] = round(new_average["gestation"]/(len(alive_list) - new_average["male"]), precision) if len(alive_list) - new_average["male"] > 0 else 0
    new_average["male"] = round(new_average["male"]/len(alive_list)*100,precision)
    new_average["hunger"] = round(new_average["hunger"]/len(alive_list), precision)
    new_average["eat_rate"] = round(new_average["eat_rate"]/len(alive_list), precision)
    new_average["food"] = round(new_average["food"]/len(alive_list), precision)
    new_average["greed"] = round(new_average["greed"]/len(alive_list), precision)
    new_average["happiness"] = round(new_average["happiness"]/len(alive_list), precision)
    new_average["stingy"] = round(new_average["stingy"]/len(alive_list), precision)
    new_average["charm"] = round(new_average["charm"]/len(alive_list), precision)
    new_average["beauty"] = round(new_average["beauty"]/len(alive_list), precision)
    new_average["reach"] = round(new_average["reach"]/len(alive_list), precision)
    new_average["kinship"] = round(new_average["kinship"]/len(alive_list), precision)
    month_avgs.append(new_average)
    month_lows.append(new_low)
    month_highs.append(new_high)

for creation in range(genesis_count):
    local_x = random.randrange(0, world_size)
    local_y = random.randrange(0, world_size)
    while world[local_x][local_y] is not None:
        local_x = random.randrange(0, world_size)
        local_y = random.randrange(0, world_size)
    new_creature = LifeForm()
    xy = random.choice([True, False])
    gender_text = 'male' if xy else 'female'
    new_creature.spawn(
        x=local_x, 
        y=local_y, 
        id=creation, 
        male=xy,
        luck=random.randrange(luck_min_start, luck_max_start),
        resilence=random.randrange(resilence_min_start, resilence_max_start),
        intelligence=random.randrange(intelligence_min_start, intelligence_max_start),
        health=random.randrange(min_health, max_health),
        lifetime=random.randrange(lifetime_min_start, lifetime_max_start),
        speed=random.randrange(speed_min_start, speed_max_start),
        restless=random.randrange(restless_min_start, restless_max_start),
        mature=True,
        mature_age=random.randrange(maturity_min_start, maturity_max_start),
        gestation=random.randrange(gestation_min_start, gestation_max_start),
        hunger=hunger_start,
        eat_rate=random.randrange(eat_rate_min_start, eat_rate_max_start),
        food=random.randrange(food_min_start, food_max_start),
        greed=random.randrange(greed_min_start, greed_max_start),
        happiness=random.randrange(happiness_min_start, happiness_max_start),
        stingy=random.randrange(stingy_min_start, stingy_max_start),
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
while month < apocalypse and len(alive_list) < world_size*world_size:
    for lifeform in alive_list:
        lifeform.take_turn(month)
        print_world()
        output = f"{int(month/months_in_a_year)}.{month % months_in_a_year + 1}\t"
        output = f"{output}alive: {len(alive_list)}\t"
        # output = f"{output}begs: {begs}\t"
        # output = f"{output}gifts: {gifts}\t"
        # output = f"{output}thefts: {thefts}\t"
        output = f"{output}finds: {finds}\t{lifeform.name[:5]} {lifeform.family[:8]} \t"
        output = f"{output}luck: {lifeform.luck}\t\t"
        output = f"{output}food:\t{lifeform.food}\t"
        output = f"{output}eat: {lifeform.eat_rate}\t\t"
        output = f"{output}hunger: {lifeform.hunger}\t"
        output = f"{output}health: {lifeform.health}\t"
        output = f"{output}happiness: {lifeform.happiness}\t"
        output = f"{output}age: {lifeform.lifetime}\t"
        output = f"{output}adult: {lifeform.mature_age}\t"
        output = f"{output}position: ({lifeform.x},{lifeform.y})"
        print(output)
    if len(alive_list) > 0:
        lifeform_stats(month)
    month = month + 1

# Make a report
for month in range(len(month_avgs)):
    output = f"{int(month/months_in_a_year)}.{month % months_in_a_year + 1}:"
    output = f"{output}\talive:\t\t\t[ \t{month_avgs[month]['alive']}\t ]\n"
    output = f"{output}\tmale %:\t\t\t[ \t{month_avgs[month]['male']}\t ]\n"
    output = f"{output}\tfemale pregnant %:\t[ \t{month_avgs[month]['pregnant']}\t ]\n"
    output = f"{output}\tfemale gestation %:\t[{month_lows[month]['gestation']}\t{month_avgs[month]['gestation']}\t{month_highs[month]['gestation']}]\n"
    output = f"{output}\tmaturity %:\t\t[ \t{month_avgs[month]['mature']}\t ]\n"
    output = f"{output}\tluck:\t\t\t[{month_lows[month]['luck']}\t{month_avgs[month]['luck']}\t{month_highs[month]['luck']}]\n"
    output = f"{output}\tresilence:\t\t[{month_lows[month]['resilence']}\t{month_avgs[month]['resilence']}\t{month_highs[month]['resilence']}]\n"
    output = f"{output}\tskill:\t\t\t[{month_lows[month]['skill']}\t{month_avgs[month]['skill']}\t{month_highs[month]['skill']}]\n"
    output = f"{output}\tintelligence:\t\t[{month_lows[month]['intelligence']}\t{month_avgs[month]['intelligence']}\t{month_highs[month]['intelligence']}]\n"
    output = f"{output}\thealth:\t\t\t[{month_lows[month]['health']}\t{month_avgs[month]['health']}\t{month_highs[month]['health']}]\n"
    output = f"{output}\tlifetime:\t\t[{month_lows[month]['lifetime']}\t{month_avgs[month]['lifetime']}\t{month_highs[month]['lifetime']}]\n"
    output = f"{output}\tspeed:\t\t\t[{month_lows[month]['speed']}\t{month_avgs[month]['speed']}\t{month_highs[month]['speed']}]\n"
    output = f"{output}\trestless:\t\t[{month_lows[month]['restless']}\t{month_avgs[month]['restless']}\t{month_highs[month]['restless']}]\n"
    output = f"{output}\thunger:\t\t\t[{month_lows[month]['hunger']}\t{month_avgs[month]['hunger']}\t{month_highs[month]['hunger']}]\n"
    output = f"{output}\teat_rate:\t\t[{month_lows[month]['eat_rate']}\t{month_avgs[month]['eat_rate']}\t{month_highs[month]['eat_rate']}]\n"
    output = f"{output}\tfood:\t\t\t[{month_lows[month]['food']}\t{month_avgs[month]['food']}\t{month_highs[month]['food']}]\n"
    output = f"{output}\tgreed:\t\t\t[{month_lows[month]['greed']}\t{month_avgs[month]['greed']}\t{month_highs[month]['greed']}]\n"
    output = f"{output}\thappiness:\t\t[{month_lows[month]['happiness']}\t{month_avgs[month]['happiness']}\t{month_highs[month]['happiness']}]\n"
    output = f"{output}\tstingy:\t\t\t[{month_lows[month]['stingy']}\t{month_avgs[month]['stingy']}\t{month_highs[month]['stingy']}]\n"
    output = f"{output}\tcharm:\t\t\t[{month_lows[month]['charm']}\t{month_avgs[month]['charm']}\t{month_highs[month]['charm']}]\n"
    output = f"{output}\tbeauty:\t\t\t[{month_lows[month]['beauty']}\t{month_avgs[month]['beauty']}\t{month_highs[month]['beauty']}]\n"
    output = f"{output}\tkinship:\t\t[{month_lows[month]['kinship']}\t{month_avgs[month]['kinship']}\t{month_highs[month]['kinship']}]\n"
    # print(output)
