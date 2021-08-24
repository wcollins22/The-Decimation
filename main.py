import random
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Room:
    connections: List[str]
    objects: List[str]


@dataclass
class Player:
    health: int
    hunger: int
    thirst: int
    sanity: int
    inventory: List[str]
    backpack: bool


@dataclass
class Enemy:
    health: int


@dataclass
class Item:
    number: int
    effect: str


home = {
    "Foyer": Room(
        ["Living Room", "Bedroom", "Bathroom", "Living Room", "Pantry", "Bunker"], []
    ),
    "Living Room": Room(["Foyer", "Kitchen"], ["Cards", "Checkers", "Harmonica"]),
    "Kitchen": Room(["Living Room", "Pantry"], ["Canned Food", "Water", "Radio"]),
    "Bedroom": Room(["Foyer", "Closet"], ["Blankets", "Books", "Water"]),
    "Closet": Room(["Bedroom"], ["Axe", "Gas Mask", "Canned Food", "Backpack"]),
    "Bathroom": Room(["Foyer"], ["Soap", "First Aid Kit"]),
    "Pantry": Room(["Foyer", "Kitchen"], ["Canned Food", "Water"]),
    "Bunker": Room(["Foyer"], []),
}

walmart = {
    "Entrance": Room(["Grocery", "Games", "Pharmacy", "Hygiene", "Leave"], []),
    "Grocery": Room(["Entrance"], ["Canned Food", "Canned Food", "Water", "Water"]),
    "Games": Room(["Entrance"], ["Cards", "Checkers"]),
    "Hygiene": Room(["Entrance"], ["Soap", "Soap", "Soap"]),
    "Pharmacy": Room(["Entrance"], ["Bandages", "Bandages"]),
}

clinic = {
    "Entrance": Room(["Pharmacy", "Leave"], []),
    "Pharmacy": Room(["Entrance"], ["Bandages", "Bandages", "First Aid Kit"]),
}

basspro = {
    "Entrance": Room(["Camping Gear", "Gun Rack", "Leave"], []),
    "Camping Gear": Room(["Entrance", "Gun Rack"], ["Backpack", "Radio", "Gas Mask"]),
    "Gun Rack": Room(["Entrance", "Camping Gear"], ["Rifle"]),
}


def print_info(location: str) -> None:
    if location == "Foyer":
        for room, item in home.items():
            if location == room:
                print("Connections:")
                for items in item.connections:
                    print(items)
    else:
        for room, item in home.items():
            if location == room:
                print("Items:")
                for thing in item.objects:
                    print(thing)
                print("\nConnections:")
                for items in item.connections:
                    print(items)


def destination_input(location: str, home: Dict[str, Room], player: Player) -> str:
    while True:
        destination = input("\nWhich [room], [item], or [drop] an item?\n> ").title()
        if destination == "Drop":
            drop_input = input("Which item?\n> ").title()
            if drop_input in player.inventory:
                player.inventory.remove(drop_input)
                print(f"{drop_input} dropped!")
            else:
                print("You do not have this item.")
        elif valid_destination(location, destination):
            print()
            break
        elif valid_item(home, location, destination):
            if len(player.inventory) >= 4:
                print("You do not have enough space.")
            else:
                for k, v in home.items():
                    if k == location:
                        v.objects.remove(destination)
                player.inventory.append(destination)
                print("Inventory:", "[%s]" % ", ".join(map(str, player.inventory)))
        else:
            print("Invalid Option.")
    return destination


def valid_destination(location: str, destination: str) -> bool:
    return destination in home[location].connections


def valid_item(home: Dict[str, Room], location: str, destination: str) -> bool:
    return destination in home[location].objects


def bunker_input(
    home: Dict[str, Room], player: Player, enemy: Enemy, days: int
) -> None:
    print("\nYou are now in the bunker")
    print("You may [explore], [view] inventory.")
    action = input("> ")
    print()
    if action == "explore":
        if days == 1:
            print(
                "Exiting the bunker, you're met with the sight of ruin. Luckily the bomb was far enough away to not cause significant damage, but your world will forever be changed.\n"
            )
        explore(home, player, walmart, enemy)
    elif action == "view":
        view_inventory(home, player)

        bunker_input(home, player, enemy, days)
    else:
        print("This is an invalid action.")
        bunker_input(home, player, enemy, days)


def view_inventory(home: Dict[str, Room], player: Player) -> None:
    print("Inventory:")
    for item in home["Bunker"].objects:
        if (
            item != "Canned Food"
            and item != "Water"
            and item != "Axe"
            and item != "Gas Mask"
            and item != "Backpack"
        ):
            print(item)
    print()
    inventory_input(home, player)


def inventory_input(home: Dict[str, Room], player: Player) -> None:
    item_input = input(
        "Which item do you want to use? (Input [None] if you don't want to use an item.)\n> "
    ).title()
    if item_input in home["Bunker"].objects:
        if item_input == "Cards":
            print("You played a lonely hand of Solitaire.\nSanity increased!")
            player.sanity += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "Checkers":
            print(
                "Gaining inspiration from an old Pixar short, you play a round of checkers against yourself.\n\nYou lost.\n\nSanity increased!"
            )
            player.sanity += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "Books":
            print(
                "You read a story you have literally no interest in, but it passes the time.\nSanity increased!"
            )
            player.sanity += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "Blankets":
            print(
                "Laying in the bundle of blankets, you take a rest for the day.\nSanity increased!"
            )
            player.sanity += 1
        elif item_input == "Radio":
            print(f"\n{broadcasts()}")
            player.sanity += 1
        elif item_input == "Soap":
            print("You take a nice, soothing shower.\nSanity Increased!")
            player.sanity += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "First Aid Kit":
            print(
                "You spend some time tending to your wounds, hoping to rid yourself of your ailments.\nHealth increased!"
            )
            player.health += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "Harmonica":
            print(
                "Channeling your inner blues, you play a soulful tune.\nSanity increased!"
            )
            player.sanity += 1
            home["Bunker"].objects.remove(item_input)
        elif item_input == "Bandages":
            print(
                "Dressing your wounds, you attempt to heal your injuries.\nHealth increased!"
            )
            player.health += 0.5
            home["Bunker"].objects.remove(item_input)
        elif item_input == "None":
            pass
        else:
            print("Please input a valid item.")


def print_info_wal(location: str) -> None:
    if location == "Entrance":
        for room, item in walmart.items():
            if location == room:
                print("\nConnections:")
                for items in item.connections:
                    print(items)
    else:
        for room, item in walmart.items():
            if location == room:
                print("Items:")
                for thing in item.objects:
                    print(thing)
                print("\nConnections:")
                for items in item.connections:
                    print(items)


def explore(
    home: Dict[str, Room], player: Player, walmart: Dict[str, Room], enemy: Enemy
) -> None:
    while True:
        if "Gas Mask" not in home["Bunker"].objects:
            player.health -= 0.5
            print("The air, now and forever irradiated, stings your every breath.\n")
        action = input(
            "You are outside. You can go to [Walmart], The [Clinic], or [Bass Pro]\n> "
        ).title()
        encounter(player, enemy, home)
        if action == "Walmart":
            walmart_main(walmart, player)
            for item in player.inventory:
                home["Bunker"].objects.append(item)
            player.inventory.clear()
            return
        elif action == "Clinic":
            clinic_main(clinic, player)
            for item in player.inventory:
                home["Bunker"].objects.append(item)
            player.inventory.clear()
            return
        elif action == "Bass Pro":
            basspro_main(basspro, player)
            for item in player.inventory:
                home["Bunker"].objects.append(item)
                player.inventory.clear()
            if "Rifle" in home["Bunker"].objects:
                player.rifle = True
            return


def walmart_main(walmart: Dict[str, Room], player: Player) -> None:
    location = "Entrance"
    while True:
        print_info_wal(location)
        destination = walmart_input(walmart, player, location)
        location = destination
        if location == "Leave":
            print()
            break


def walmart_input(walmart: Dict[str, Room], player: Player, location: str) -> str:
    while True:
        destination = input("\nWhich [room], [item], or [drop] an item?\n> ").title()
        if destination == "Drop":
            drop_input = input("Which item?\n> ").title()
            if drop_input in player.inventory:
                player.inventory.remove(drop_input)
                print(f"{drop_input} dropped!")
            else:
                print("You do not have this item.")
        elif valid_destination_wal(walmart, destination, location):
            break
        elif valid_item_wal(walmart, location, destination):
            if len(player.inventory) >= 4 and not player.backpack:
                print("You do not have enough space.")
            elif len(player.inventory) >= 8 and player.backpack:
                print("You don't have enough space.")
            else:
                for k, v in walmart.items():
                    if k == location:
                        v.objects.remove(destination)
                player.inventory.append(destination)
                print("Inventory:", "[%s]" % ", ".join(map(str, player.inventory)))
        else:
            print("Invalid Option.")
    return destination


def valid_destination_wal(
    walmart: Dict[str, Room], destination: str, location: str
) -> bool:
    return destination in walmart[location].connections


def valid_item_wal(walmart: Dict[str, Room], location: str, destination: str) -> bool:
    return destination in walmart[location].objects


def basspro_main(basspro: Dict[str, Room], player: Player) -> None:
    location = "Entrance"
    while True:
        print_info_bp(location)
        destination = bp_input(basspro, player, location)
        location = destination
        if location == "Leave":
            print()
            break


def bp_input(basspro: Dict[str, Room], player: Player, location: str) -> str:
    while True:
        destination = input("Which [room], [item], or [drop] an item?\n> ").title()
        if destination == "Drop":
            drop_input = input("Which item?\n> ").title()
            if drop_input in player.inventory:
                player.inventory.remove(drop_input)
                print(f"{drop_input} dropped!")
            else:
                print("You do not have this item.")
        elif valid_destination_bp(basspro, location, destination):
            break
        elif valid_item_bp(basspro, location, destination):
            if len(player.inventory) >= 4 and not player.backpack:
                print("You do not have enough space.")
            elif len(player.inventory) >= 8 and player.backpack:
                print("You don't have enough space.")
            else:
                for k, v in basspro.items():
                    if k == location:
                        v.objects.remove(destination)
                player.inventory.append(destination)
                print("Inventory:", "[%s]" % ", ".join(map(str, player.inventory)))
        else:
            print("Invalid Option.")
    return destination


def print_info_bp(location: str) -> None:
    if location == "Entrance":
        for room, item in basspro.items():
            if location == room:
                print("\nConnections:")
                for items in item.connections:
                    print(items)
    else:
        for room, item in basspro.items():
            if location == room:
                print("Items:")
                for thing in item.objects:
                    print(thing)
                print("\nConnections:")
                for items in item.connections:
                    print(items)


def valid_destination_bp(
    basspro: Dict[str, Room], location: str, destination: str
) -> bool:
    return destination in basspro[location].connections


def valid_item_bp(basspro: Dict[str, Room], location: str, destination: str) -> bool:
    return destination in basspro[location].objects


def clinic_input(clinic: Dict[str, Room], player: Player, location: str) -> str:
    while True:
        destination = input("\nWhich [room], [item], or [drop] an item?\n> ").title()
        if destination == "Drop":
            drop_input = input("Which item?\n> ").title()
            if drop_input in player.inventory:
                player.inventory.remove(drop_input)
                print(f"{drop_input} dropped!")
            else:
                print("You do not have this item.")
        elif valid_destination_clinic(clinic, destination, location):
            break
        elif valid_item_clinic(clinic, destination, location):
            if len(player.inventory) >= 4 and not player.backpack:
                print("You do not have enough space.")
            elif len(player.inventory) >= 8 and player.backpack:
                print("You don't have enough space.")
            else:
                for k, v in clinic.items():
                    if k == location:
                        v.objects.remove(destination)
                player.inventory.append(destination)
                print("Inventory:", "[%s]" % ", ".join(map(str, player.inventory)))
        else:
            print("Invalid Option.")
    return destination


def valid_item_clinic(clinic: Dict[str, Room], destination: str, location: str) -> bool:
    return destination in clinic[location].objects


def valid_destination_clinic(
    clinic: Dict[str, Room], destination: str, location: str
) -> bool:
    return destination in clinic[location].connections


def clinic_main(clinic: Dict[str, Room], player: Player) -> None:
    location = "Entrance"
    while True:
        print_info_clinic(location)
        destination = clinic_input(clinic, player, location)
        location = destination
        if location == "Leave":
            print()
            break


def print_info_clinic(location: str) -> None:
    if location == "Entrance":
        for room, item in clinic.items():
            if location == room:
                print("\nConnections:")
                for items in item.connections:
                    print(items)
    else:
        for room, item in clinic.items():
            if location == room:
                print("Items:")
                for thing in item.objects:
                    print(thing)
                print("\nConnections:")
                for items in item.connections:
                    print(items)


def items_respawn(
    walmart: Dict[str, Room], basspro: Dict[str, Room], clinic: Dict[str, Room]
) -> None:
    walmart["Grocery"].objects = ["Canned Food", "Canned Food", "Water", "Water"]
    walmart["Pharmacy"].objects = ["Bandages", "Bandages"]
    walmart["Games"].objects = ["Cards", "Harmonica"]
    walmart["Hygiene"].objects = ["Soap"]
    clinic["Pharmacy"].objects = ["Bandages", "Bandages", "First Aid Kit"]


def save(home: Dict[str, Room], days: int, player: Player) -> None:
    with open("save_file/bunker_inventory.txt", "w") as f:
        for item in home["Bunker"].objects:
            f.write(f"{item}\n")
    with open("save_file/day_count.txt", "w") as f:
        f.write(str(days))
    with open("save_file/player_stats.txt", "w") as f:
        f.write(f"{str(player.health)}\n")
        f.write(f"{str(player.hunger)}\n")
        f.write(f"{str(player.thirst)}\n")
        f.write(f"{str(player.sanity)}\n")
        f.write(f"{str(player.backpack)}\n")


def broadcasts() -> str:
    with open("broadcasts", "r") as f:
        quotes = f.readlines()
    broadcast = random.choice(quotes)
    return broadcast


def random_int() -> bool:
    x = random.randint(1, 4)
    if x == 1:
        return True
    else:
        return False


def encounter(player: Player, enemy: Enemy, home: Dict[str, Room]) -> None:
    with open("Encounters", "r") as f:
        set_up = f.readlines()
    if random_int():
        x = random.choice(set_up)
        print()
        print(x)
        action = input("What do you do? [Fight]/[Run]\n>  ").title()
        if action == "Fight":
            combat(player, enemy, home)
            return
        elif action == "Run":
            run_possibility = random.randint(1, 2)
            if run_possibility == 1:
                return
            else:
                combat(player, enemy, home)
        else:
            print("That is not a valid option.")
    else:
        return


def combat(player: Player, enemy: Enemy, home: Dict[str, Room]) -> None:
    enemy_moves = [
        "They threw a can at you!",
        "The scavenger tackles you!",
        "They punch you, in the face!",
    ]
    while True:
        enemy_choice = random.choice(enemy_moves)
        if player.health > 0:
            if enemy.health > 0:
                move = input("\nDo you want to [Attack] or [Heal]?\n> ").title()
                if move == "Attack":
                    if "Rifle" in home["Bunker"].objects:
                        print("You shot the scavenger!")
                        enemy.health -= 1
                    elif "Axe" in home["Bunker"].objects:
                        print("You axe the scavenger a question!")
                        enemy.health -= 0.5
                    else:
                        print("You punched the scavenger in the face!")
                        enemy.health -= 0.25
                elif move == "Heal":
                    for item in home["Bunker"].objects:
                        if item == "Bandages" or item == "First Aid Kit":
                            print(item)
                    heal_input = input(
                        "Do you want to use [Bandages] or [First Aid Kit]?"
                    ).title()
                    if (
                        "Bandages" in home["Bunker"].objects
                        and heal_input == "Bandages"
                    ):
                        print("You used your bandages!")
                        player.health += 0.5
                    elif (
                        "First Aid Kit" in home["Bunker"].objects
                        and heal_input == "First Aid Kit"
                    ):
                        print("You used a First Aid Kit!")
                        player.health += 1
                print(enemy_choice)
                player.health -= 0.5
                print(f"Player health: {player.health}")
                print(f"Scavenger health: {enemy.health}")
            else:
                print("You crack a final blow, ending the scavenger's life.")
                break
        else:
            print(
                "At the previous blow, you fall backwards, dead at the scavenger's feet."
            )
            quit()


def new_game(days: int, home: Dict[str, Room], player: Player) -> None:
    enemy = Enemy(5)
    location = "Foyer"
    moves = 0
    # preparation phase
    while moves < 11:
        print(f"You have {11 - moves} moves left.\n")
        if location != "Bunker":
            print(f"You are in {location}")
            print_info(location)
        else:
            print("You are in the Bunker, you can only reach the Foyer.")
        destination = destination_input(location, home, player)
        location = destination
        moves += 1
        if moves == 11 and location != "Bunker":
            print(
                "You're out of time. The nuclear blast blows your house to bits, along with you.\nThe end."
            )
            quit()
        if location == "Bunker":
            user_input = input("Dump or Enter?\n> ").title()
            if user_input == "Dump":
                print()
                for item in player.inventory:
                    home["Bunker"].objects.append(item)
                player.inventory.clear()
            elif user_input == "Enter":
                for item in player.inventory:
                    home["Bunker"].objects.append(item)
                player.inventory.clear()
                print(
                    "\nAs you shut the door of the bunker, the sirens blaring, the ground you stand on trembles as a booming explosion goes off."
                )
                break
    if "Backpack" in home["Bunker"].objects:
        player.backpack = True
    # bunker phase
    while True:
        bunker_input(home, player, enemy, days)
        while True:
            eat_input = input("Do you want to eat?\n> ").title()
            if eat_input == "Yes" and player.hunger == 5:
                if "Canned Food" in home["Bunker"].objects:
                    print("You ate some canned soup.")
                    home["Bunker"].objects.remove("Canned Food")
                else:
                    print("You don't have any food.\n")
                    player.hunger -= 1
                break
            elif eat_input == "Yes" and player.hunger < 5:
                if "Canned Food" in home["Bunker"].objects:
                    print("You ate some canned soup.\n")
                    home["Bunker"].objects.remove("Canned Food")
                    player.hunger += 1
                else:
                    print("You don't have any food.\n")
                    player.hunger -= 1
                break
            elif eat_input == "No":
                print("You decided to ration for today.")
                player.hunger -= 1
                break
            else:
                print("Please input a valid option. (Yes or No)")
        while True:
            drink_input = input("Do you want to drink?\n> ").title()
            if drink_input == "Yes" and player.thirst == 5:
                if "Water" in home["Bunker"].objects:
                    print("You drank a bottle of water.\n")
                    home["Bunker"].objects.remove("Water")
                else:
                    print("You don't have any water.\n")
                    player.thirst -= 1
                break
            elif drink_input == "Yes" and player.thirst < 5:
                if "Water" in home["Bunker"].objects:
                    print("You drank a bottle of water.\n")
                    home["Bunker"].objects.remove("Water")
                    player.thirst += 1
                else:
                    print("You don't have any water.\n")
                    player.thirst -= 1
                break
            elif drink_input == "No":
                print("You decided to ration your water for the day.\n")
                player.thirst -= 1
                break
            else:
                print("Please input a valid option. (Yes or No)")
        player.sanity -= 0.5
        days += 1
        if days % 6 == 0:
            items_respawn(walmart, basspro, clinic)
        if player.hunger <= 0 and player.thirst <= 0:
            player.health -= 2
        elif player.hunger <= 0 or player.thirst <= 0:
            player.health -= 1
        if "Radio" in home["Bunker"].objects:
            print(f"\n{broadcasts()}")
        print(f"Day {days}")
        if player.health > 5:
            player.health = 5
        print(f"\nHealth: {player.health} out of 5")
        if player.hunger >= 1:
            print(f"Hunger: {player.hunger} out of 5")
        elif player.hunger < 1:
            player.hunger = 0
            print("You feel the hunger of a feral animal.")
        elif player.hunger >= 6:
            player.hunger = 5
            print("You are as stuffed as the Prince of Persia.")
        if player.thirst >= 1:
            print(f"Thirst: {player.thirst} out of 5")
        elif player.thirst < 1:
            print("Your tongue is as dry as a desert.")
        elif player.thirst >= 6:
            player.thirst = 5
            print("You're essentially drowning yourself at this point.")
        if player.sanity > 5:
            player.sanity = 5.0
            print(f"Sanity: {player.sanity} out of 5.0\n")
        elif player.sanity >= 1:
            print(f"Sanity: {player.sanity} out of 5.0\n")
        save_input = input("Would you like to save the game? (Yes or No)\n> ").title()
        if save_input == "Yes":
            save(home, days, player)


def load_game(home: Dict[str, Room], days: int, player: Player, enemy: Enemy) -> None:
    while True:
        bunker_input(home, player, enemy, days)
        while True:
            eat_input = input("Do you want to eat?\n> ").title()
            if eat_input == "Yes" and player.hunger == 5:
                if "Canned Food" in home["Bunker"].objects:
                    print("You ate some canned soup.")
                    home["Bunker"].objects.remove("Canned Food")
                else:
                    print("You don't have any food.\n")
                    player.hunger -= 1
                break
            elif eat_input == "Yes" and player.hunger < 5:
                if "Canned Food" in home["Bunker"].objects:
                    print("You ate some canned soup.\n")
                    home["Bunker"].objects.remove("Canned Food")
                    player.hunger += 1
                else:
                    print("You don't have any food.\n")
                    player.hunger -= 1
                break
            elif eat_input == "No":
                print("You decided to ration for today.")
                player.hunger -= 1
                break
            else:
                print("Please input a valid option. (Yes or No)")
        while True:
            drink_input = input("Do you want to drink?\n> ").title()
            if drink_input == "Yes" and player.thirst == 5:
                if "Water" in home["Bunker"].objects:
                    print("You drank a bottle of water.\n")
                    home["Bunker"].objects.remove("Water")
                else:
                    print("You don't have any water.\n")
                    player.thirst -= 1
                break
            elif drink_input == "Yes" and player.thirst < 5:
                if "Water" in home["Bunker"].objects:
                    print("You drank a bottle of water.\n")
                    home["Bunker"].objects.remove("Water")
                    player.thirst += 1
                else:
                    print("You don't have any water.\n")
                    player.thirst -= 1
                break
            elif drink_input == "No":
                print("You decided to ration your water for the day.\n")
                player.thirst -= 1
                break
            else:
                print("Please input a valid option. (Yes or No)")
        player.sanity -= 0.5
        days += 1
        if days % 6 == 0:
            items_respawn(walmart, basspro, clinic)
        if player.hunger <= 0 and player.thirst <= 0:
            player.health -= 2
        elif player.hunger <= 0 or player.thirst <= 0:
            player.health -= 1
        if "Radio" in home["Bunker"].objects:
            print(f"\n{broadcasts()}")
        print(f"Day {days}")
        if player.health > 5:
            player.health = 5
        print(f"\nHealth: {player.health} out of 5")
        if player.hunger >= 1:
            print(f"Hunger: {player.hunger} out of 5")
        elif player.hunger < 1:
            player.hunger = 0
            print("You feel the hunger of a feral animal.")
        elif player.hunger >= 6:
            player.hunger = 5
            print("You are as stuffed as the Prince of Persia.")
        if player.thirst >= 1:
            print(f"Thirst: {player.thirst} out of 5")
        elif player.thirst < 1:
            print("Your tongue is as dry as a desert.")
        elif player.thirst >= 6:
            player.thirst = 5
            print("You're essentially drowning yourself at this point.")
        if player.sanity > 5:
            player.sanity = 5.0
            print(f"Sanity: {player.sanity} out of 5.0\n")
        elif player.sanity >= 1:
            print(f"Sanity: {player.sanity} out of 5.0\n")
        save_input = input("Would you like to save the game? (Yes or No)\n> ").title()
        if save_input == "Yes":
            save(home, days, player)


def main() -> None:
    player = Player(5, 5, 5, 5, [], False)
    enemy = Enemy(5)
    days = 1
    action = input("Do you want to start a [New] game or [Load]? ").title()
    if action == "New":
        new_game(days, home, player)
    elif action == "Load":
        with open("save_file/day_count.txt", "r") as f:
            a = f.readline()
        days = int(a)
        with open("save_file/bunker_inventory.txt", "r") as f:
            b = f.readlines()
        for line in b:
            home["Bunker"].objects.append(line.strip())
        with open("save_file/player_stats.txt", "r") as f:
            c = f.readlines()

        player.health = float(c[0].strip())
        player.hunger = int(c[1].strip())
        player.thirst = int(c[2].strip())
        player.sanity = float(c[3].strip())
        player.inventory = []
        player.backpack = bool(c[4].strip())
        load_game(home, days, player, enemy)


if __name__ == "__main__":
    main()