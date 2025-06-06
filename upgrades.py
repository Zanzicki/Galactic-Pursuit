import random

upgrade_dict = [
                {"Bigger barrels":1},
                 {"Reinforced Armour":2},
                 {"Sturdy Bulk":3},
                 {"Lass Canons":4},
                 {"Improved Thrusters":5},
                 {"Experimental energy shield generator":6}
]

selected_dictionaries = []

random_selection = random.sample(upgrade_dict,3)

selected_dictionaries.extend(random_selection)