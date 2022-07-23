import random
import names

genesis_count = 1000        # how many lifeforms to start with
apocalypse = 1000           # how many yaers until the world takes no more turns
world_size = 42             # how big is the flat earth
roll_max = 100              # the upper bound for rolls
min_health = 800
max_health = 1000
lifetime_min_start = 20
lifetime_max_start = 50
maturity_upper_bound_age = 13
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
gestation_min_start = 5
gestation_max_start = 8
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

begs = 0
gifts = 0
thefts = 0
finds = 0
last_id = 0

world = [[None for i in range(world_size)] for j in range(world_size)]
alive_list = []

class LifeForm:
    def __init__(self):
        # broad properties
        self.luck = 0            # catch all positive/negative value
        self.resilence = 0       # how many failures a lifeform can tollerate in a turn
        self.skill = 0           # value of individual performance capability
        self.intelligence = 0    # how many turns ahead a lifeform can try to optimize strategies for dependent props

        # death properties
        self.health = 0          # how far from death the lifeform is
        self.lifetime = 0        # how many turns a lifeform has been alive

        # movement properties
        self.speed = 0           # movements per round
        self.restless = 0        # likihood of trying to move per round

        # reproduction properties
        self.mature = False      # whether or not entity can reproduce
        self.male = False        # whether the lifeform is male or female
        self.pregnant = False    # whether or not for the current turn the lifeform is pregnant
        self.gestation = 0       # how many turns it takes for a new lifeform to birth

        # energy properties
        self.hunger = 0          # numerical value representing current hunger, affects health
        self.eat_rate = 0        # how much food a lifeform tries to eat a turn
        self.food = 0            # how much food a lifeform owns
        self.greed = 0           # factor of actual need greater that lifeform requires

        # social properties
        self.happiness = 0       # how happy the lifeform is
        self.stingy = 0          # how willing a lifeform is to assist others against happiness
        self.charm = 0           # how much this lifeform affects other lifeforms nearby
        self.beauty = 0          # how preferable a lifeform is for mating
        self.reach = 0           # how far from the lifeform does it care about other lifeform's charm & attractiveness
        self.kinship = 0         # how much a lifeform cares about its kin
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
    def take_turn(self):
        self.move()
        self.forage()
        self.mingle()
        self.pregnancy()
        self.eat()
        self.age()
    
    def spawn(self, x, y, id, male, luck=0, resilence=0, intelligence=0, skill=0, health=0, lifetime=0, speed=0,
              restless=0, mature=False, gestation=0, hunger=0, eat_rate=0, food=0, greed=0, happiness=0, stingy=0,
              charm=0, beauty=0, reach=0, kinship=0, name="", family=""):
        self.luck = luck
        self.resilence = resilence
        self.intelligence = intelligence
        self.skill = skill
        self.health = health
        self.lifetime = lifetime
        self.speed = speed
        self.restless = restless
        self.resilence = resilence
        self.mature = mature
        self.male = male
        self.pregnant = False
        self.gestation = gestation
        self.hunger = hunger
        self.eat_rate = eat_rate
        self.food = food
        self.greed = greed
        self.happiness = happiness
        self.stingy = stingy
        self.charm = charm
        self.beauty = beauty
        self.reach = reach
        self.kinship = kinship
        self.name=name
        self.family=family
        self.x = x
        self.y = y
        self.id = id

    def birth(self, x, y, id, male, food, mother_genes, father_genes, name, family):
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

        for key in mother_genes.keys():
            mod = [mother_genes[key], father_genes[key]]
            mod.sort()
            if key == "skill":
                mod[0] = round(mod[0]/2)
            setattr(self, key, random.randrange(mod[0], mod[1] + 1))

        luck_improve_roll = random.randrange(0, roll_max)
        if luck_improve_roll <= self.luck:
            self.luck = self.luck + 1

        beauty_improve_roll = random.randrange(0, roll_max)
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
            self.happiness = self.happiness + self.luck + self.stingy + target.charm
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
            target.health = target.health - round(health_delta/2)
            self.health = self.health - health_delta

            if self.happiness > ammount - self.luck:
                self.happiness = self.happiness - ammount + self.luck
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

    def age(self):
        self.lifetime = self.lifetime + 1
        self.mated_recently = False
        age_roll = random.randrange(0, roll_max)
        if age_roll > self.luck:
            self.health = self.health - self.lifetime
        maturity_offset = random.randrange(0, self.luck)
        if not self.mature and maturity_upper_bound_age <= self.lifetime + maturity_offset:
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
        if self.health + self.beauty*self.luck*self.charm > target.beauty + target.health:
            self.happiness = self.happiness + self.health + self.beauty*self.luck*self.charm - target.beauty
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
                    "reach": target.reach,
                    "kinship": target.kinship,
                    "food": round(target.food/2)    # This is not a property on the maternal list, daddy pays up front
                }
                self.baby_daddy = target
                target.food = round(target.food/2)
            self.mated_recently = self.luck*self.greed > random.randrange(0, roll_max)
        else:
            # if rejected, happiness transfer
            self.happiness = self.happiness + self.beauty*self.luck*self.charm + self.health - target.beauty \
                - target.health
            target.happiness = target.happiness + target.beauty*target.luck*target.charm + target.health \
                - self.beauty - self.health

    def pregnancy(self):
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
                    "reach": self.reach,
                    "kinship": self.kinship
                }
                local_x = random.randrange(0, world_size)
                local_y = random.randrange(0, world_size)
                while world[local_x][local_y] is not None:
                    local_x = random.randrange(0, world_size)
                    local_y = random.randrange(0, world_size)
                global last_id; last_id = last_id + 1
                xy = random.choice([True, False])
                gender_text = 'male' if xy else 'female'
                family_name = self.baby_daddy.family if xy else self.family
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
                    family=family_name
                    )
                child.parents.append(self)
                child.parents.append(self.baby_daddy)
                self.paternal_genes = {}
                self.rounds_pregnant = 0
                self.pregnant = False
                self.food = round(self.food/2)
                self.children.append(child)
                self.baby_daddy.children.append(child)
                world[local_x][local_y] = child
                alive_list.append(child)

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
            self.happiness = self.happiness + random.randrange(happiness_mods[0], happiness_mods[1] + 1)
        elif self.luck > 0:
            self.happiness = self.happiness + random.randrange(0, self.luck)


def print_world():
    pass

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
        family=names.get_last_name()
        )
    world[local_x][local_y] = new_creature
    alive_list.append(new_creature)
    last_id = creation

for year in range(apocalypse):
    for lifeform in alive_list:
        lifeform.take_turn()
        print_world()
        output = f"{year}\t"
        output = f"{output}alive: {len(alive_list)}\t"
        output = f"{output}begs: {begs}\t"
        output = f"{output}gifts: {gifts}\t"
        output = f"{output}thefts: {thefts}\t"
        output = f"{output}finds: {finds}\t{lifeform.name} {lifeform.family} \t"
        output = f"{output}luck: {lifeform.luck}\t\t"
        output = f"{output}food:\t{lifeform.food}\t"
        output = f"{output}eat: {lifeform.eat_rate}\t\t"
        output = f"{output}hunger: {lifeform.hunger}\t"
        output = f"{output}health: {lifeform.health}\t"
        output = f"{output}happiness: {lifeform.happiness}\t"
        output = f"{output}age: {lifeform.lifetime}\t"
        output = f"{output}position: ({lifeform.x},{lifeform.y})"
        print(output)

