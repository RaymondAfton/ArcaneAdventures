import random

# ===========================
# Player Class
# ===========================
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_cap = 100
        self.upgrade_points = 0

        # Base Stats
        self.base_damage = 10
        self.max_health = 100
        self.health = self.max_health
        self.max_shield = 100
        self.shield = self.max_shield

        # Equipment
        self.equipped_items = []
        self.crit_chance = 0
        self.dodge_chance = 0
        self.stun_chance = 0
        self.health_regen = 0
        self.extra_action_chance = 0

    def reset(self):
        """Respawn player after death."""
        print("\n💀 You have died! Respawning...\n")
        self.__init__(self.name)

    def equip(self, item):
        """Equip an item if less than 3 are equipped"""
        if len(self.equipped_items) < 3:
            self.equipped_items.append(item)
            item.apply(self)
            print(f"\n✅ Equipped {item.name}!\n")
        else:
            print("\n❌ You can only equip 3 items!\n")

    def attack(self, enemy):
        """Calculate attack damage and check for critical hits"""
        base_dmg = self.base_damage
        if random.random() < self.crit_chance:
            print("🔥 Critical Hit!")
            base_dmg *= 2  # Double damage on crit

        if random.random() < self.stun_chance:
            print("💫 Enemy Stunned!")
            enemy.stunned = True

        return int(base_dmg)

    def take_damage(self, damage):
        """Reduce shield first, then health"""
        if self.shield > 0:
            absorbed = min(damage, self.shield)
            self.shield -= absorbed
            damage -= absorbed

        self.health -= max(damage, 0)
        if self.health <= 0:
            self.reset()
            return True
        return False

    def heal_after_fight(self):
        """Fully restore health and shield after each fight"""
        self.health = self.max_health
        self.shield = self.max_shield
        print("\n🛡️ You have fully recovered after the battle!\n")

    def level_up(self):
        """Increase level, heal fully, and allow stat upgrades"""
        while self.exp >= self.exp_cap:
            self.level += 1
            self.exp -= self.exp_cap
            self.exp_cap += 25
            self.upgrade_points += 4
            self.health = self.max_health
            self.shield = self.max_shield
            print(f"\n🎉 Level Up! You are now Level {self.level}!")
            print(f"You have {self.upgrade_points} upgrade points to spend!\n")
            self.upgrade_stats()

    def upgrade_stats(self):
        """Upgrade player stats using available upgrade points"""
        while self.upgrade_points > 0:
            print("\nChoose a stat to upgrade:")
            print("[1] Damage +3")
            print("[2] Health +10")
            print("[3] Shield +5")
            print(f"[0] Exit (Remaining Points: {self.upgrade_points})")
            choice = input("Your choice: ")

            if choice == "1":
                self.base_damage += 3
                print("🗡️ Damage increased by 3!")
            elif choice == "2":
                self.max_health += 10
                print("❤️ Health increased by 10!")
            elif choice == "3":
                self.max_shield += 5
                print("🛡️ Shield increased by 5!")
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice!")

            self.upgrade_points -= 1

# ===========================
# Equipment Class
# ===========================
class Equipment:
    def __init__(self, name, apply_effect):
        self.name = name
        self.apply = apply_effect

# Equipment Effects
def crimson_slime_fang_effect(player):
    player.crit_chance += 0.25
    player.base_damage += player.base_damage / 4

def kolkallum_usurper_effect(player):
    player.crit_chance += 0.35
    player.base_damage *= 1.25

def nature_cloak_effect(player):
    player.max_health += 400
    player.health_regen += 0.10

def steel_greatsword_effect(player):
    player.stun_chance += 0.30
    player.base_damage += 20

def samurai_hat_effect(player):
    player.dodge_chance += 0.20
    player.crit_chance += 0.10
    player.extra_action_chance += 0.30

# Equipment List
equipment_list = [
    Equipment("Crimson Slime Fang", crimson_slime_fang_effect),
    Equipment("Kolkallum's Usurper", kolkallum_usurper_effect),
    Equipment("Nature's Cloak", nature_cloak_effect),
    Equipment("Steel Greatsword", steel_greatsword_effect),
    Equipment("Samurai Hat", samurai_hat_effect)
]

# ===========================
# Enemy Class
# ===========================
class Enemy:
    def __init__(self, name, health, damage, exp_reward):
        self.name = name
        self.health = health
        self.damage = damage
        self.exp_reward = exp_reward
        self.stunned = False

# Enemy List
enemies = [
    Enemy("Green Slime", 125, 7, 25),
    Enemy("Blue Slime", 200, 20, 35),
    Enemy("Fox", 200, 30, 50),
    Enemy("Wolf", 250, 45, 75),
    Enemy("Crimson Slime", 300, 60, 100),
    Enemy("Hardmode Wolf", 500, 75, 125)
]

# ===========================
# Game Start & Main Loop
# ===========================
print("======================================")
print("       Welcome to Arcane Adventures! ")
print("======================================")

player_name = ""
while not player_name.strip():
    player_name = input("Enter your name, adventurer: ").strip()

player = Player(player_name)
print(f"\nGreetings, {player.name}! Your journey begins now...\n")

# Equip Items
print("\nChoose 3 items to equip:")
for idx, item in enumerate(equipment_list):
    print(f"[{idx+1}] {item.name}")
selected_indexes = list(map(int, input("Enter the numbers (e.g., 1 2 3): ").split()))

for i in selected_indexes:
    if 1 <= i <= len(equipment_list):
        player.equip(equipment_list[i - 1])

# Main Game Loop
while True:
    print("\n[1] Fight an enemy")
    print("[0] Upgrade stats")
    print("[9] Exit game")
    choice = input("Your choice: ")

    if choice == "9":
        print("Exiting game...")
        break

    elif choice == "0":
        player.upgrade_stats()

    elif choice == "1":
        enemy = random.choice(enemies)
        print(f"\n⚔️ You encountered a {enemy.name}!")

        while enemy.health > 0 and player.health > 0:
            damage = player.attack(enemy)
            enemy.health -= damage
            print(f"🗡️ You dealt {damage} damage to {enemy.name}!")

            if enemy.health <= 0:
                print(f"💀 {enemy.name} defeated! You gained {enemy.exp_reward} EXP!")
                player.exp += enemy.exp_reward
                player.level_up()
                player.heal_after_fight()
                break

            if not enemy.stunned:
                if player.take_damage(enemy.damage):
                    break