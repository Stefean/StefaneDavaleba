
def log_action(func):
    def wrapper(self, *args ,**kwargs):
        print(f"{self.name} -> {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper
class Character: 
    count = 0
    def __init__(self, name, hp=100, level=1):
        self.name = name
        self.hp = hp
        self.level = level
        Character.count += 1

    def __str__(self):
        return f"{self.name}(Lv {self.level}, HP {self.hp})"

    def take_damage(self, amount):
        self.hp = self.hp - amount
        if self.hp < 0:
            self.hp = 0
    
    @log_action
    def attack(self, target):
        target.take_damage(5)

    @classmethod
    def from_string(cls, char_str):
        parts = char_str.strip().split(";")
        if len(parts) == 2:
            return cls(parts[0], int(parts[1]))
        return False

    @staticmethod
    def is_valid_name(name):
        return  2<len(name)<20

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name
        else:
            return False

    @property
    def is_alive(self):
        return self.hp > 0 

class Warrior(Character):
    def __init__(self, name,hp=100, level=1, strength=10):
        super().__init__(name, hp, level)
        self.strength = strength

    @log_action
    def attack(self, target):
        target.take_damage(self.strength)

class Mage(Character):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp, level)
        self.mana = mana
    @log_action
    def attack(self, target):
        if self.mana < 10:
            super().attack(target)
            return
            
        self.mana -= 10
        target.take_damage(20)

    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str} MP {self.mana}"

class Inventory:
    def __init__(self):
        self.inventory = []

    def add(self, **kwargs):
        self.inventory.append(kwargs)

    def find(self, **kwargs):
        result = {}
        for item in self.inventory:
            match = True
            for key, value in kwargs.items():
                if item.get(key) != value:
                    match = False 
                    break
            if match:
                result[key] = value
        return result

    def __len__(self):
        return len(self.inventory)
                           

class HealerMixin:
    @log_action
    def heal(self, target, amount):
        target.hp += int(amount)

class Priest(HealerMixin, Mage):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp, level, mana)

def battle(char1, char2):
    if not isinstance(char1, Character) and not isinstance(char2, Character):
        raise TypeError("Both character should be 'Character' object!!!")
    winner = None
    while True:
        char1.attack(char2)
        char2.attack(char1)
        if char1.hp == 0    :
            winner = char2
            break
        elif char2.hp == 0:
            winner = char1
            break
    return winner
        

# a = Character("Tariel")
# b = Character("Avtandil", hp=50)
# b.take_damage(70)

# print(a)                 # Tariel (Lv 1, HP 100)
# print(b)                 # Avtandil (Lv 1, HP 0)
# print(b.is_alive)        # False
# print(Character.count)   # 2

# t = Warrior("Tariel", hp=120, strength=15)
# n = Mage("Nestan", hp=80, mana=15)

# t.attack(n)
# print(n)    # Nestan (Lv 1, HP 65) MP 15

# n.attack(t)   # 20 ზიანი, mana-ს 5 რჩება
# n.attack(t)   # mana არ ჰყოფნის: 5 ზიანი
# print(t)    # Tariel (Lv 1, HP 95)

# p = Priest("Nestan", hp=60)
# w = Warrior.from_string("Tariel;120")

# p.heal(w, 30)
# print(w)                                   # Tariel (Lv 1, HP 150)
# print(type(w).__name__)                    # Warrior
# print(Character.is_valid_name("T"))        # False
# print(Character("A") == Character("A"))    # True

# inv = Inventory()
# inv.add(name="sword", kind="weapon", power=10)
# inv.add(name="potion", kind="heal", power=30)

# print(len(inv))                  # 2
# print(inv.find(kind="weapon"))   # [{'name': 'sword', 'kind': 'weapon', 'power': 10}]
# print(inv.find(kind="heal", power=30))   # [{'name': 'potion', 'kind': 'heal', 'power': 30}]

# t = Warrior("Tariel")
# n = Mage("Nestan")
# t.attack(n)                      # Tariel → attack

# winner = battle(Warrior("Tariel", hp=120), Mage("Nestan", hp=80))
# print(f"გამარჯვებული: {winner.name}")