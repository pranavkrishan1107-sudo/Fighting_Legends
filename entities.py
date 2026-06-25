from abc import ABC, abstractmethod
import random
class Character(ABC):
    def __init__(self, name, hp, level, xp, required_xp, type, strength, defense, is_player=False):
        self.name = name
        self.__hp = hp
        self.__level = level
        self.__xp = xp
        self.__max_hp = hp
        self.__required_xp = required_xp
        self.type = type
        self.strength = strength
        self.defense = defense
        self.is_player = is_player
        self.moves = []
        self.max_moves =  5
        self.status = None
        self.status_duration = 0
    @property 
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, value):
        self.__hp = value
    @property 
    def xp(self):
        return self.__xp
    @xp.setter
    def xp(self, value):
        self.__xp = value
    @property 
    def required_xp(self):
        return self.__required_xp
    @required_xp.setter
    def required_xp(self, value):
        self.__required_xp = value
    @property 
    def level(self):
        return self.__level
    @level.setter
    def level(self, value):
        self.__level = value
    @property
    def max_hp(self):
        return self.__max_hp
    @max_hp.setter
    def max_hp(self, value):
        self.__max_hp = value
    @abstractmethod
    def attack(self, opponent, damage):
        print(f"{self.name} attacked {opponent.name}")
        return opponent.take_damage(damage)
    def take_damage(self, damage):
        effect = max(0, damage - self.defense)
        self.__hp -= effect
        if self.__hp <= 0:
            self.__hp = 0
            print(f"💀 {self.name} is down!")
        else:
            print(f"🛡️ {self.name} HP left: {self.__hp}")
        return effect
    def add_move(self, move):
        if self.max_moves > len(self.moves):
            self.moves.append(move)
        else:
            print("Maximum Move Limit Reached")
    def increase_move_capacity(self):
        move_number = self.__level // 10
        self.max_moves =  5 + move_number
            
    def add_xp(self, amount):
        self.__xp += amount
        while self.__xp >= self.__required_xp:
            self.level_up()
    def level_up(self):
        self.__level += 1
        self.__xp -= self.__required_xp
        self.__max_hp += 25
        self.__hp = self.__max_hp
        self.__required_xp = round(self.__required_xp * 1.2)
        self.increase_move_capacity()
        print(f"Level Up! You are now {self.__level} Level")
    def execute_move(self, move, opponent):
        if move.type == "Physical" or move.type == "Magical":
            damage = self.attack(opponent, move.power)
            return ("attack", move.name, damage)
        elif move.type == "Heal":
            healed = min(self.__max_hp, self.__hp + move.power) - self.__hp
            self.__hp += healed
            print(f"{self.name} increased their HP! HP : {self.__hp}")
            return ("heal", move.name, healed)
        elif move.type == "Buff":
            self.strength += move.power
            print(f"{self.name} Increased its strength")
            return ("buff", move.name, move.power)
        elif move.type == "Paralysis":
            opponent.status = "Paralyzed"
            opponent.status_duration = 2
            return ("paralysis", move.name, f"{opponent.name} is paralyzed for 2 turns!")
        elif move.type == "Burn":
            opponent.status = "Burn"
            opponent.status_duration = 2
            return ("burn", move.name, f"{opponent.name} is burning for 2 turns!")
        else:
            opponent.status = "Poisoned"
            opponent.status_duration = 2
            return ("poison", move.name, f"{opponent.name} is poisoned for 2 turns!")
    def is_alive(self):
        return self.__hp > 0
    def __str__(self):
        return f"{self.name} (HP: {self.__hp}/{self.__max_hp}, Level: {self.__level}, XP: {self.__xp}/{self.__required_xp}, Type: {self.type}, Strength: {self.strength}, Defense: {self.defense})"
    def display_stats(self):
        print(f"Character Name : {self.name}\nCharacter HP : {self.__hp}\nCharacter Level : {self.__level}\nCharacter XP : {self.__xp}\nCharacter Max HP : {self.__max_hp}\nCharacter Required XP : {self.__required_xp}\nCharacter Type : {self.type}\nCharacter Strength : {self.strength}\nCharacter Defense : {self.defense}\nCharacter Move Limit : {self.max_moves}")
class Warrior(Character):
    def __init__(self, name, hp, **kwargs):
        stats = {
            "level": 1,
            "xp": 0,
            "required_xp": 100,
            "type": "Physical",
            "strength": 30,
            "defense": 32
        }
        stats.update(kwargs)
        super().__init__(name=name,hp=hp, **stats)
    def attack(self, opponent, damage):
        power = int((self.strength * (random.randrange(12, 16) / 10)) + damage)
        print(f"{self.name} attacked {opponent.name}")
        return opponent.take_damage(power)
class Mage(Character):
    def __init__(self, name, hp, **kwargs):
        stats = {
            "level": 1,
            "xp": 0,
            "required_xp": 100,
            "type": "Magical",
            "strength": 42,
            "defense": 25
        }
        stats.update(kwargs)
        super().__init__(name=name, hp=hp, **stats)
    def attack(self, opponent, damage):
        power = int((self.strength * (random.randrange(18, 21) / 10)) + damage)
        print(f"{self.name} attacked {opponent.name}")
        return opponent.take_damage(power)

                # Creating Move Class

class Move:
    def __init__(self, name, power, type, description=""):
        self.name = name
        self.power = power
        self.type = type
        self.description = description
    def info(self):
        print(F"Move Name : {self.name}\nMove Power : {self.power}\nMove Type : {self.type}\n{self.description}")

# --- Move Database ---
# Format: Move(name, power, type, description)

all_moves = {
    # --- PHYSICAL MOVES (10) ---
    "iron_slash": Move("Iron Slash", 20, "Physical", "A reliable sword swing."),
    "heavy_slam": Move("Heavy Slam", 35, "Physical", "Hits hard but slow."),
    "dual_strike": Move("Dual Strike", 25, "Physical", "Two quick hits in succession."),
    "bone_crusher": Move("Bone Crusher", 30, "Physical", "Blunt force that rattles bones."),
    "sonic_leap": Move("Sonic Leap", 22, "Physical", "A fast jumping strike."),
    "shield_bash": Move("Shield Bash", 15, "Physical", "Simple hit with a shield."),
    "phantom_strike": Move("Phantom Strike", 28, "Physical", "An unpredictable shadow attack."),
    "dragon_claw": Move("Dragon Claw", 32, "Physical", "Sharp slash with dragon energy."),
    "skyward_uppercut": Move("Skyward Uppercut", 24, "Physical", "Launches the enemy upward."),
    "final_reckoning": Move("Final Reckoning", 50, "Physical", "Extreme damage, high risk."),

    # --- MAGICAL MOVES (10) ---
    "fireball": Move("Fireball", 30, "Magical", "A ball of scorching flames."),
    "ice_shard": Move("Ice Shard", 22, "Magical", "Sharp piercing ice crystal."),
    "thunderbolt": Move("Thunderbolt", 35, "Magical", "A powerful bolt of lightning."),
    "arcane_blast": Move("Arcane Blast", 25, "Magical", "Pure burst of magical energy."),
    "shadow_orbs": Move("Shadow Orbs", 28, "Magical", "Floating spheres of darkness."),
    "solar_flare": Move("Solar Flare", 33, "Magical", "Intense light that burns."),
    "wind_scythe": Move("Wind Scythe", 20, "Magical", "A blade made of sharp wind."),
    "abyssal_gate": Move("Abyssal Gate", 38, "Magical", "Energy from the deep void."),
    "mana_burst": Move("Mana Burst", 26, "Magical", "Releases raw mana stores."),
    "meteor_fall": Move("Meteor Fall", 55, "Magical", "A giant rock from the sky."),

    # --- TACTICAL MOVES (10) ---
    "quick_fix": Move("Quick Fix", 25, "Heal", "Small bandage for quick recovery."),
    "zen_meditation": Move("Zen Meditation", 50, "Heal", "Focuses energy to restore a lot of HP."),
    "war_cry": Move("War Cry", 8, "Buff", "Shout that increases Strength."),
    "iron_skin": Move("Iron Skin", 6, "Buff", "Hardens skin to boost stats."),
    "burning_touch": Move("Burning Touch", 0, "Burn", "Sets the enemy on fire."),
    "toxic_vapor": Move("Toxic Vapor", 0, "Poisoned", "Spreads a deadly poison gas."),
    "static_shock": Move("Static Shock", 0, "Paralysis", "Electrocuted and slows down."),
    "vampiric_bite": Move("Vampiric Bite", 15, "Heal", "Steals life from the enemy."),
    "power_surge": Move("Power Surge", 8, "Buff", "A massive surge in power."),
    "shadow_curse": Move("Shadow Curse", 0, "Poisoned", "A curse that drains life slowly."),
    "lighting_strike": Move("Lightning Strike", 5, "Magic", "A strike that can paralyze the opponent."),

    # --- New Physical Moves ---
    "dragon_fist_barrage": Move("Dragon Fist Barrage", 28, "Physical", "Unleashes a flurry of dragon-powered punches."),
    "shadow_wolf_fang": Move("Shadow Wolf Fang", 32, "Physical", "A shadowy bite that tears through defenses."),
    "crimson_lotus_strike": Move("Crimson Lotus Strike", 25, "Physical", "A graceful strike blooming with deadly petals."),
    "titans_hammer_fall": Move("Titan's Hammer Fall", 35, "Physical", "A massive hammer swing from the heavens."),
    "phantom_dance_slash": Move("Phantom Dance Slash", 22, "Physical", "Illusory slashes that confuse and cut."),
    "beast_kings_roar": Move("Beast King's Roar", 30, "Physical", "A powerful roar that shakes and strikes."),

    # --- New Magical Moves ---
    "eternal_flame_inferno": Move("Eternal Flame Inferno", 38, "Magical", "Summons an unending blaze of hellfire."),
    "void_dimension_slash": Move("Void Dimension Slash", 33, "Magical", "Cuts through reality with void energy."),
    "celestial_star_burst": Move("Celestial Star Burst", 26, "Magical", "Explodes with the power of falling stars."),
    "abyssal_nightmare_wave": Move("Abyssal Nightmare Wave", 30, "Magical", "A wave of dark dreams that engulfs foes."),
    "aurora_borealis_storm": Move("Aurora Borealis Storm", 28, "Magical", "Northern lights that unleash magical fury."),
    "divine_thunder_cascade": Move("Divine Thunder Cascade", 35, "Magical", "Heavenly lightning rains down relentlessly."),

    # --- New Status Moves ---
    "thunder_gods_wrath": Move("Thunder God's Wrath", 0, "Paralysis", "Zeus-like lightning that paralyzes the soul."),
    "frozen_eternity": Move("Frozen Eternity", 0, "Paralysis", "Freezes time and movement in eternal ice."),
    "hellfire_phoenix": Move("Hellfire Phoenix", 0, "Burn", "Reborn flames that burn eternally."),
    "scorching_sun_beam": Move("Scorching Sun Beam", 0, "Burn", "A beam of pure solar fire."),
    "venomous_serpent_strike": Move("Venomous Serpent Strike", 0, "Poison", "A poisonous bite from a mythical serpent."),
    "toxic_shadow_mist": Move("Toxic Shadow Mist", 0, "Poison", "A mist of deadly shadows that poisons the air."),
    "celestial_healing_wave": Move("Celestial Healing Wave", 40, "Heal", "Waves of heavenly energy restore vitality."),
    "divine_power_ascension": Move("Divine Power Ascension", 10, "Buff", "Ascends strength to godly levels.")
}

# Format: Warrior(name, hp, strength, defense) or Mage(name, hp, mana, defense)
# Note: Stats slighty high for the 'Big Three'

all_chars = {
    # --- The Big Three (Slightly Stronger) ---
    "goku": Warrior("Goku", 750, strength=45, defense=20),      # High HP & Strength
    "vegeta": Warrior("Vegeta", 780, strength=48, defense=24),  # Glass Cannon (High Attack)
    "aizen": Mage("Aizen", 690, strength=60, defense=22),       # High Mana & Defense

    # --- Other Warriors ---
    "zoro": Warrior("Zoro", 640, strength=35, defense=15),
    "thor": Warrior("Thor", 640, strength=38, defense=12),
    "madara": Warrior("Madara", 640, strength=40, defense=14),
    "tanjiro": Warrior("Tanjiro", 640, strength=30, defense=10),
    "naruto": Warrior("Naruto", 680, strength=42, defense=18),
    "ichigo": Warrior("Ichigo", 660, strength=40, defense=16),
    "luffy": Warrior("Luffy", 700, strength=44, defense=20),
    "sanji": Warrior("Sanji", 620, strength=36, defense=14),
    "usopp": Warrior("Usopp", 600, strength=34, defense=12),
    "brook": Warrior("Brook", 580, strength=32, defense=10),
    "franky": Warrior("Franky", 650, strength=36, defense=18),

    # --- Other Mages ---
    "itachi": Mage("Itachi", 610, strength=50, defense=15),
    "gojo": Mage("Gojo", 610, strength=55, defense=20),
    "albus": Mage("Dumbledore", 610, strength=52, defense=10),
    "scarlet_witch": Mage("Wanda", 610, strength=58, defense=8),
    "dr_strange": Mage("Dr. Strange", 610, strength=54, defense=12),
    "sasuke": Mage("Sasuke", 630, strength=56, defense=14),
    "kakashi": Mage("Kakashi", 620, strength=53, defense=16),
    "hinata": Mage("Hinata", 590, strength=48, defense=12),
    "sakura": Mage("Sakura", 600, strength=50, defense=15),
    "nami": Mage("Nami", 580, strength=46, defense=10),
    "robin": Mage("Robin", 640, strength=55, defense=18)
}




        


    
    
    
        
