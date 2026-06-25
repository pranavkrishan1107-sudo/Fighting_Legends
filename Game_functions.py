from entities import all_moves, all_chars, Warrior, Mage
import copy
import random
import sqlite3
def init_db():
    with sqlite3.connect("fighting_legends.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS players (
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            char_name TEXT,
                            hp INTEGER,
                            max_hp INTEGER,
                            level INTEGER DEFAULT 1,
                            xp INTEGER DEFAULT 0,
                            required_xp INTEGER,
                            strength INTEGER,
                            defense INTEGER,
                            char_type TEXT,
                            moves TEXT,
                            max_moves INTEGER
                       
                            )
                       ''')
        print("Database Initialized Successfully")
def save_player_data(player, username, password):
    move_text = ','.join([move.name for move in player.moves])
    with sqlite3.connect("fighting_legends.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT OR REPLACE INTO players (username, password, char_name, hp, max_hp, level, xp, required_xp, strength, defense, char_type, moves, max_moves)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (username, password, player.name, player.hp, player.max_hp, player.level, player.xp, player.required_xp, player.strength, player.defense, type(player).__name__, move_text, player.max_moves))
    print("Player data saved successfully.")
def get_player_data(username):
    with sqlite3.connect("fighting_legends.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT *FROM players WHERE username = ?''' , (username,))
        row = cursor.fetchone()
        return row
        

def handle_status_effects(entity):
    if entity.status == "Burn" and entity.status_duration > 0:
        entity.take_damage(10)
        entity.status_duration -= 1
    elif entity.status == "Poison" and entity.status_duration > 0:
        entity.take_damage(15)
        entity.status_duration -= 1
    elif entity.status == "Paralyzed" and entity.status_duration > 0:
        entity.status_duration -= 1
    if entity.status_duration == 0 and entity.status is not None:
        print(f"✨ {entity.name} recovered from their status effect.")
        entity.status = None
def character_selection():
    print("1 . Create Your Character\n2 . Select A Character")
    choice = input("Enter your choice(1 or 2):")
    if choice == "1":
        char_class = input("Enter Your Character Class (Warrior/Mage):").strip().lower()
        char_name = input("Enter Your Character Name:")
        if char_class == "warrior":
            char_hp = random.randint(675, 790)
            char_str = random.randint(30, 55)
            char_def = random.randint(15, 27)
            Protagonist = Warrior(char_name, char_hp, strength=char_str, defense=char_def)
        elif char_class == "mage":
            char_hp = random.randint(615, 680)
            char_str = random.randint(35, 60)
            char_def = random.randint(10, 24)
            Protagonist = Mage(char_name, char_hp, strength=char_str, defense=char_def)
        else:
            print("Invalid Class! Your character is now Goku!")
            Protagonist = all_chars["goku"]
        print(f"Your Character\nName | {Protagonist.name}\nHP | {Protagonist._Character__hp}\nStrength | {Protagonist.strength}\nDefense | {Protagonist.defense}")
    elif choice == "2":
        for i, char in enumerate(all_chars.keys(), 1):
            print(f"{i}. {char.capitalize().ljust(15)} | HP: {all_chars[char].hp} | Strength: {all_chars[char].strength} | Defense: {all_chars[char].defense}")
        char_choice = input("Enter your choice(in index):")
        if char_choice.isdigit() and 1 <= int(char_choice) <= len(all_chars):
            char_name = list(all_chars.keys())[int(char_choice) - 1]
            selected_char = all_chars[char_name]
            Protagonist = copy.deepcopy(selected_char)
            print(f"Your Character\nName | {Protagonist.name}\nHP | {Protagonist._Character__hp}\nStrength | {Protagonist.strength}\nDefense | {Protagonist.defense}")
        else:
            print("Invalid Choice! Your character is now Goku!")
            Protagonist = all_chars["goku"]
    else:
        print("Invalid Choice! Your character is now Goku!")
        Protagonist = all_chars["goku"]
    return Protagonist
def move_selection(Protagonist):
    Protagonist.moves = []
    print("Select Your Moves :")
    for i, char in enumerate(all_moves.keys(), 1):
            print(f"{i}. {char.capitalize().ljust(15)} | DMG: {all_moves[char].power} | Type: {all_moves[char].type} | Description: {all_moves[char].description}")
    while len(Protagonist.moves) < Protagonist.max_moves:
        move_choice = input("Enter The Index Of The Move:")
        if move_choice.isdigit() and 1 <= int(move_choice) <= len(all_moves):
            move_name = list(all_moves.keys())[int(move_choice) - 1]
            selected_move = all_moves[move_name]
            if selected_move in Protagonist.moves:
                print("You already have this move! Please select another one.")
                continue
            else:
                Protagonist.add_move(selected_move)
                print(f"Move {selected_move.name} Added!")
        else:
            print("Invalid choice! Please try again.")
    return Protagonist

def start_battle(player, opponent):
    print(f"⚔️ Battle Start! {player.name} vs {opponent.name} ⚔️")
    print("------- Player Stats -------")
    player.display_stats()
    opponent.max_hp += opponent.max_hp // 5
    print("------- Opponent Stats -------")
    opponent.display_stats()
    if opponent.moves:
        print("------- Opponent Moves -------")
        for i, move in enumerate(opponent.moves, 1):
            print(f"{i}. {move.name} | DMG: {move.power} | Type: {move.type} | Description: {move.description}")
    player.hp = player.max_hp
    opponent.hp = opponent.max_hp
    while player.is_alive() and opponent.is_alive():
        handle_status_effects(player)
        handle_status_effects(opponent)
        if player.status == "Paralyzed":
            print(f"⚡ {player.name} is paralyzed and can't move this turn!")
            print("-" * 30)
        else:
            print(f"\n{player.name}'s Turn:")
            for i, move in enumerate(player.moves, 1):
                print(f"{i}. {move.name} | DMG: {move.power} | Type: {move.type} | Description: {move.description}")
            print("-" * 30)
            move_choice = input("Select a move (enter index):")
            if move_choice.isdigit() and 1 <= int(move_choice) <= len(player.moves):
                selected_move = player.moves[int(move_choice) - 1]
                result = player.execute_move(selected_move, opponent)
                if result[0] == "attack":
                    print(f"{player.name} used {result[1]} and dealt {result[2]} damage!")
                elif result[0] == "heal":
                    print(f"{player.name} used {result[1]} and healed {result[2]} HP!")
                else:
                    print(result[2])
            else:
                print("Invalid choice! Turn skipped.")
            print("-" * 30)
        if not opponent.is_alive():
            print(f"🎉 {player.name} wins the battle!")
            gained_xp = random.randint((player.required_xp // 4), player.required_xp // 2)
            player.add_xp(gained_xp)
            print(f"{player.name} gained {gained_xp} XP!")
            break
        if opponent.status == "Paralyzed":
            print(f"⚡ {opponent.name} is paralyzed and can't move this turn!")
            print("-" * 30)
        else:
            print(f"\n{opponent.name}'s Turn:")
            for i, move in enumerate(opponent.moves, 1):
                print(f"{i}. {move.name} | DMG: {move.power} | Type: {move.type} | Description: {move.description}")
            opponent_move = random.choice(opponent.moves)
            result = opponent.execute_move(opponent_move, player)
            if result[0] == "attack":
                print(f"{opponent.name} used {result[1]} and dealt {result[2]} damage!")
            elif result[0] == "heal":
                print(f"{opponent.name} used {result[1]} and healed {result[2]} HP!")
            else:
                print(result[2])
            print("-" * 30)
        print(f"{player.name} HP: {player.hp}/{player.max_hp} | {opponent.name} HP: {opponent.hp}/{opponent.max_hp}")
        print("-" * 30)
        if not player.is_alive():
            print(f"💀 {player.name} has been defeated! Game Over.")
            print("-" * 30)
            break

def opponent_selection(player_level):
    opponent_original = random.choice(list(all_chars.keys()))
    opponent = copy.deepcopy(all_chars[opponent_original])

    while player_level > opponent.level:
        opponent.level_up()
    all_moves_keys = list(all_moves.keys())
    selected_move_key = random.sample(all_moves_keys, opponent.max_moves)
    for move_key in selected_move_key:
        opponent.add_move(all_moves[move_key])
    return opponent













