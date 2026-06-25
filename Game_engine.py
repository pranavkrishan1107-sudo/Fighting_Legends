from Game_functions import init_db, save_player_data, get_player_data, character_selection, move_selection, opponent_selection, handle_status_effects, start_battle
from entities import Warrior, Mage, all_moves
init_db()
key = 17
def encryption(text):
    encrypted_text=""
    for char in text:
        encrypted_text += chr(ord(char) + key)
    return encrypted_text
def decryptions(text):
    decrypted_text=""
    for char in text:
        decrypted_text += chr(ord(char) - key)
    return decrypted_text
def update_user_stats(username, user_char):
    save_player_data(user_char, username, get_player_data(username)[1])

def start():
    print("Select An Option From The Following\n1. Login\n2. Register")
    choice = input("Enter your choice(in index):")
    if choice == "1":
        username = input("Enter your username:")
        users_data = get_player_data(username)
        if users_data != None:            
            print("Username Found!")
            passkey = input("Enter your password:")
            encrypt_pass = users_data[1]
            if passkey == decryptions(encrypt_pass):
                print("Suceesful Login")
                print(f"Welcome Back {username}!")
                current_user = username
                if users_data[10] == "Warrior":
                    user_char = Warrior(users_data[2], users_data[3])
                elif users_data[10] == "Mage":
                    user_char = Mage(users_data[2], users_data[3])
                user_char.strength = users_data[8]
                user_char.defense = users_data[9]
                user_char.xp = users_data[6]
                user_char.required_xp = users_data[7]
                user_char.level = users_data[5]
                user_char.max_moves = users_data[12]
                user_char.max_hp = users_data[4]
                user_char.hp = users_data[3]
                users_moves = users_data[11].split(",")
                for m_name in users_moves:
                    user_char.moves.append(all_moves[m_name.lower().replace(" ", "_")])
                return current_user, user_char
            else:
                print("Invalid Password")
        else:
            print("Username Not Found!")
    elif choice == "2":
        new_user = input("Enter Your Username:")
        new_pass = input("Enter Your Password:")
        e_password = encryption(new_pass)
        if get_player_data(new_user) != None:
            print("This Username Is already Occupied")
        else:
            user_char = move_selection(character_selection())
            save_player_data(user_char, new_user, e_password)
            return new_user, user_char
    return None, None
def game_hub(username, user_char):
    while True:
        print(f"Welcome To The Game Hub {username}!".center(45, "-"))
        print("Select An Option From The Following\n1. Battle\n2. View Stats\n3. Re-Select Moves\n4. Log Out")
        choice = input("Enter your choice(in index):")
        if choice == "1":
            opponent = opponent_selection(user_char.level)
            start_battle(user_char, opponent)
            update_user_stats(username, user_char)
        elif choice == "2":
            user_char.display_stats()
        elif choice == "3":
            user_char = move_selection(user_char)
            update_user_stats(username, user_char)
        elif choice == "4":
            print("Logging Out...")
            break
        else:
            print("Invalid Input")
if __name__ == "__main__":
    username, user_char = start()
    if user_char != None:
        game_hub(username, user_char)
    else:
        print("Exiting Game...")



