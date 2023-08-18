import random

def roll_stat():
    # Roll 4d6 and keep the highest 3 rolls for a stat.
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls, reverse=True)[:3])

def generate_stats(possible_importances):
    # Generate stats based on one of the possible importance orders.
    importance_order = random.choice(possible_importances)  # Choose one of the possible importance orders
    return _generate_stats_for_order(importance_order)

def _generate_stats_for_order(importance_order):
    # Generate stats for a specific importance order.
    rolled_stats = sorted([roll_stat() for _ in range(6)], reverse=True)
    return {stat: rolled_stats[importance_order.index(stat)] for stat in importance_order}

def lambda_handler(event, context):
    races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome", "Half-Orc", "Half-Elf", "Tiefling"]
    classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
    gear = {
        'Barbarian': 'Great Axe, Leather Armor',
        'Bard': 'Rapier, Leather Armor, Musical Instrument',
        'Cleric': 'Mace, Chain Mail, Holy Symbol',
        'Druid': 'Staff, Leather Armor, Druidic Focus',
        'Fighter': 'Longsword, Shield, Chain Mail',
        'Monk': 'Staff, Unarmored Defense',
        'Paladin': 'Longsword, Shield, Chain Mail, Holy Symbol',
        'Ranger': 'Longbow, Arrows, Leather Armor',
        'Rogue': 'Dagger, Shortsword, Leather Armor',
        'Sorcerer': 'Wand, Robes',
        'Warlock': 'Pact Blade, Robes, Arcane Focus',
        'Wizard': 'Staff, Spellbook, Robes'
        }
    # The stat allocation is not fully random here. 
    class_stat_importance = {
        "Barbarian": [
            ["Strength", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Charisma"]
        ],
        "Bard": [
            ["Charisma", "Dexterity", "Constitution", "Wisdom", "Intelligence", "Strength"],
            ["Charisma", "Constitution", "Strength", "Dexterity", "Intelligence", "Wisdom"]
        ],
        "Cleric": [
            ["Wisdom", "Constitution", "Strength", "Charisma", "Intelligence", "Dexterity"]
        ],
        "Druid": [
            ["Wisdom", "Constitution", "Dexterity", "Intelligence", "Charisma", "Strength"]
        ],
        "Fighter": [
            ["Strength", "Constitution", "Dexterity", "Intelligence", "Charisma", "Wisdom"],
            ["Dexterity", "Constitution", "Strength", "Charisma", "Wisdom", "Intelligence"]
        ],
        "Monk": [
            ["Dexterity", "Wisdom", "Constitution", "Strength", "Charisma", "Intelligence"]
        ],
        "Paladin": [
            ["Strength", "Charisma", "Constitution", "Intelligence", "Wisdom", "Dexterity"],
            ["Charisma", "Strength", "Constitution", "Intelligence", "Wisdom", "Dexterity"],
            ["Strength", "Constitution", "Charisma", "Intelligence", "Wisdom", "Dexterity"],
            ["Charisma", "Constitution", "Strength", "Intelligence", "Wisdom", "Dexterity"]
        ],
        "Ranger": [
            ["Dexterity", "Wisdom", "Constitution", "Strength", "Charisma", "Intelligence"]
        ],
        "Rogue": [
            ["Dexterity", "Constitution", "Intelligence", "Charisma", "Wisdom", "Strength"]
        ],
        "Sorcerer": [
            ["Charisma", "Constitution", "Intelligence", "Wisdom", "Dexterity", "Strength"]
        ],
        "Warlock": [
            ["Charisma", "Constitution", "Dexterity", "Wisdom", "Strength", "Intelligence"]
        ],
        "Wizard": [
            ["Intelligence", "Constitution", "Wisdom", "Charisma", "Strength", "Dexterity"],
            ["Intelligence", "Dexterity", "Constitution", "Strength", "Charisma", "Wisdom"],
            ["Intelligence", "Charisma", "Constitution", "Wisdom", "Dexterity", "Strength"]
        ]
    }
    
    racial_bonuses = {
        "Human": {"Strength": 1, "Dexterity": 1, "Constitution": 1, "Intelligence": 1, "Wisdom": 1, "Charisma": 1},
        "Elf": {"Dexterity": 2, "Wisdom": 1},
        "Dwarf": {"Constitution": 2, "Strength": 1},
        "Halfling": {"Dexterity": 2},
        "Half-Orc": {"Strength": 2, "Constitution": 1},
        "Half-Elf": {"Charisma": 2},
        "Tiefling": {"Intelligence": 1, "Charisma": 2},
        "Gnome": {"Intelligence": 2},
        "Dragonborn": {"Strength": 2, "Charisma": 1}
    }
    
    spells_by_level = {
        'Cantrips': {
            'Bard': ['Blade Ward', 'Dancing Lights', 'Friends', 'Light', 'Mage Hand', 'Mending', 'Message', 'Minor Illusion',
                'Prestidigitation', 'True Strike', 'Vicious Mockery'],
            'Cleric': ['Guidance', 'Light', 'Mending', 'Resistance', 'Sacred Flame', 'Spare the Dying', 'Thaumaturgy'],
            'Druid': ['Druidcraft', 'Guidance', 'Mending', 'Poison Spray', 'Produce Flame', 'Resistance', 'Shillelagh', 'Thorn Whip'],
            'Sorcerer': ['Acid Splash','Blade Ward','Chill Touch','Dancing Light','Fire Bolt','Friends','Light','Mage Hand','Mending',
                'Message','Minor Illusion','Poison Spray','Prestidigitation','Ray of Frost','Shocking Grasp','True Strike'],
            'Wizard': ['Acid Splash','Blade Ward','Chill Touch','Dancing Light','Fire Bolt','Friends','Light','Mage Hand',
                'Mending','Message','Minor Illusion','Poison Spray','Prestidigitation','Ray of Frost','Shocking Grasp','True Strike'],
            'Warlock': ['Blade Ward','Chill Touch','Eldritch Blast','Friends','Mage Hands','Minor Illusion','Poison Spray',
                'Prestidigitation','True Strike']
        },
        'Level 1': {
            'Bard': ['Animal Friendship', 'Bane', 'Charm Person', 'Comprehend Languages', 'Cure Wounds', 'Detect Magic',
                'Disguise Self', 'Dissonant Whispers', "Faerie Fire", 'Feather Fall', 'Healing Word', 'Heroism',
                'Identify', 'Illusory Script', 'Longstrider', 'Silent Image', 'Sleep', 'Speak with Animals',
                "Tasha's Hideous Laughter", 'Thunderwave', 'Unseen Servant'],
            'Cleric': ['Bane', 'Bless', 'Command', 'Create or Destroy Water', 'Cure Wounds', 'Detect Evil and Good',
                'Detect Magic', 'Detect Poison or Disease', 'Guiding Bolt', 'Healing Word', 'Inflict Wounds',
                'Protection from Evil and Good', 'Purify Food and Drink', 'Sanctuary', 'Shield of Faith'],
            'Druid': ['Animal Friendship', 'Charm Person', 'Create or Destroy Water', 'Cure Wounds', 'Detect Magic', 'Detect Poison and Disease', 'Entangle',
                'Faerie Fire', 'Fog Cloud', 'Goodberry', 'Healing Word', 'Jump', 'Longstrider', 'Purify Food and Drink', 'Speak with Animals', 'Thunderwave'],
            'Paladin': ['Bless','Command','Compelled Duel','Cure Wounds','Detect Evil and Good','Detect Magic','Detect Poison and Disease',
                'Divine Favor','Heroism','Protection from Evil and Good','Purify Food and Drink','Searing Smite','Shield of Faith',
                'Thunderous Smite','Wrathful Smite'],
            'Ranger': ['Alarm','Animal Friendship','Cure Wounds','Detect Magic','Detect Poison and Disease','Ensnaring Strike',
                'Fog Cloud','Goodberry','Hail of Thorns',"Hunter's Mark",'Jump','Longstrider','Speak with Animals'],
            'Sorcerer': ['Burning Hands','Charm Person','Chromatic Orb','Color Spray','Comprehend Languages','Detect Magic',
                'Disguise Self','Expeditious Retreat','False Life','Feather Fall','Fog Cloud','Jump','Mage Armor','Magic Missile',
                'Ray of Sickness','Shield','Silent Image','Sleep','Thunderwave','Witch Bolt'],
            'Wizard': ['Alarm','Burning Hand','Charm Person','Chromatic Orb','Color Spray','Comprehend Languages',
                'Detect Magic','Disguise Self','Expeditious Retreat','False Life','Feather Fall','Find Familiar','Fog Cloud',
                'Grease','Identify','Illusory Script','Jump','Longstrider','Mage Armor','Magic Missile','Protection from Evil and Good',
                'Ray of Sickness','Shield','Silent Image','Sleep',"Tasha's Hideous Laughter","Tenser's Floating Disk",'Thunderwave',
                'Unseen Servant','Witch Bolt']
        },
        'Level 2': {
            'Bard': ['Animal Mssenger', "Blindness/Deafness", 'Calm Emotions', 'Cloud of Daggers', 'Crown of Madness',
                'Detet Thoughts', 'Enhance Ability', 'Enthrall', 'Heat Metal', 'Hold Person', 'Invisibility',
                'Knock', 'Lesser Restoration', 'Locate Animal or Plants','Locate Object', 'Magic Mouth',
                'Phantasmal Force', 'See Invisibility', 'Shatter','Silence', 'Suggestion', 'Zone of Truth'],
            'Cleric': ['Aid', 'Augury', 'Blindness/Deafness', 'Calm Emotions', 'Continual Flame', 'Enhance Ability',
                'Find Traps', 'Gentle Repose', 'Hold Person', 'Lesser Restoration', 'Locate Object', 'Prayer of Healing',
                'Protection from Poison', 'Silence', 'Spiritual Weapon', 'Warding Bond', 'Zone of Truth'],
            'Druid': ['Animal Messenger', 'Barkskin', 'Beast Sense', 'Darkvision', 'Enhance Ability', 'Find Traps', 'Flame Blade', 'Flaming Sphere',
                'Gust of Wind', 'Heat Metal', 'Hold Person', 'Lesser Restoration', 'Locate Animals or Plants', 'Locate Object', 'Moonbeam', 'Pass without Trace',
                'Protection from Poison', 'Spike Growth'],
            'Paladin': ['Aid','Branding Smite','Find Steed','Lesser Restoration','Locate Object','Magical Weapon',
                'Protection from Poison','Zone of Truth'],
            'Ranger': ['Animal Messenger','Barkskin','Beast Sense','Cordon of Arrows','Darkvision','Find Traps','Lesser Restoration',
                'Locate Animals or Plants','Locate Object','Pass without Trace','Protection from Poison','Silence','Spike Growth'],
            'Sorcerer': ['Alter Self','Blindness/Deafness','Blur','Cloud of Daggers','Crown of Madness','Darkness',
                'Darkvision','Detect Thoughts','Enhance Ability','Enlarge/Reduce','Gust of Wind','Hold Person','Invisibility',
                'Knock','Levitate','Mirror Image','Misty Step','Phantasmal Force','Scorching Ray','See Invisibility','Shatter','Spider Climb',
                'Suggestion','Web'],
            'Wizard': ['Alter Self','Arcane Lock','Blindness/Deafness','Blur','Cloud of Daggers','Continual Flame','Crown of Madness',
                'Darkness','Darkvsion','Detect Thoughts','Enlarge/Reduce','Flaming Sphere','Gentle Response','Gust of Wind','Hold Person',
                'Invisibility','Knock','Levitate','Locate Object','Magic Mouth','Magic Weapon',"Melf's Acid Arrow",'Mirror Image',
                'Misty Step',"Nystul's Magic Aura",'Phantasmal Force','Ray of Enfeeblement','Rope Trick','Scorching Ray','See Invisibility',
                'Shatter','Spider Climb','Suggestion','Web']
        },
        'Level 3': {
            'Bard': ['Bestow Curse', 'Clairvoyance', 'Dispel Magic', 'Fear', 'Feign Death', 'Glyph of Warding',
                'Hypnotic Pattern', "Leomund's Tiny Hut",'Major Image', 'Nondetection', 'Plant Growth',
                'Sending', 'Speak with Dead', 'Speak with Plants', 'Stinking Cloud', 'Tongues'],
            'Cleric': ['Animate Dead','Beacon of Hope', 'Bestow Curse', 'Clairvoyance', 'Create Food and Water',
                'Daylight', 'Dispel Magic', 'Feign Death', 'Glyph of Warding', 'Magic Circle', 'Mass HEaling Word',
                'Meld into Stone', 'Protection from Energy', 'Remove Curse', 'Revivify', 'Sending','Speak with Dead',
                'Spirit Guardian', 'Tongues', 'Water Walk'],
            'Druid': ['Call Lightning', 'Conjure Anmals', 'Daylight', 'Dispel Magic', 'Feign Death', 'Meld into Stone', 'Plant Growth',
                'Protection from Energy', 'Sleet Storm', 'Speak with Plants', 'Water Breathing', 'Water Walk', 'Wind Wall'],
            'Paladin': ['Aura of Vitality','Blinding Smite','Create Food and Water',"Crusader's Mantle",'Daylight',
                'Dispel Magic','Elemental Weapon','Magic Circle','Remove Curse','Revivify'],
            'Ranger': ['Conjure Animals','Conjure Barrage','Daylight','Lightning Arrow','Nondetection','Plant Growth',
                'Protection from Energy','Speak with Plants','Water Breathing','Water Walk','Wind Wall'],
            'Sorcerer': ['Blink','Clairvoyance','Counterspell','Daylight','Dispel Magic','Fear','Fireball','Fly','Gaseous Form',
                'Haste','Hypnotic Pattern','Lightning Bolt','Major Image','Protection from Energy','Sleet Storm','Slow','Stinking Cloud',
                'Tongues','Water Breathing','Water Walk'],
            'Wizard': ['Animate Dead','Bestow Curse','Blink','Clairvoyance','Counterspell','Dispel Magic','Fear','Feign Death','Fireball',
                'Fly','Gaseous Form','Glyph of Warding','Haste','Hypnotic Pattern',"Leomund's Tiny Hut",'Lightning Bolt','Magic Circle',
                'Major Image','Nondetection','Phantom Steed','Protection from Energy','Remove Curse','Sending','Sleet Storm','Slow',
                'Stinking CLoud','Tongues','Vampiric Touch','Water Breathing']
        },
        'Level 4': {
            'Bard': ['Compulsion', 'Confusion', 'Dimension Door', 'Freedom of Movement', 'Greater Invisibility',
                'Hallucinatory Terrain', 'Locate Creature', 'Polymorph'],
            'Cleric': ['Banishment', 'Control Water', 'Death Ward', 'Divination', 'Freedom of Movement', 'Guardian of Faith',
                'Locate Creature', 'Stone Shape'],
            'Druid': ['Blight', 'Confusion', 'Conjure Minor Elemental', 'Conjure Woodland Beigns', 'Control Water',
                'Dominate Beast', 'Freedom of Movement', 'Giant Insect', 'Grasping Vine', 'Hallucinatory Terrain', 'Ice Storm', 'Locate Creature',
                'Polymorph', 'Stone Shape','Stoneskin', 'Wall of Fire'],
            'Paladin': ['Aura of Life','Aura of Purify','Banishment','Death Ward','Locate Creatures','Staggering Smite'],
            'Ranger': ['Conjure Woodland Beings','Freedom of Movement','Grasping Vine','Locate Creature','Stoneskin'],
            'Sorcerer': ['Banishment','Blight','Confusion','Dimension Door','Dominate Beast','Greater Invisibility',
                'Ice Storm','Polymorph','Stoneskin','Wall of Fire'],
            'Wizard': ['Arcane Eye','Banishment','Blight','Confusion','Cpnjure Minor Elementals','Control Water',
                'Dimension Door',"Evard's Black Tentacles",'Fabricate','Fire Shield','Greater Invisibility','Hallucinatory','Ice Storm',
                "Leomund's Secret Chest",'Locate Creature',"Mordenkainen's Private Sanctum","Otiluke's Resilient Sphere",'Phantasmal Killer',
                'Polymorph','Stone Shape','Stoneskin','Wall of Fire']
        },
        'Level 5': {
            'Bard': ['Animate Object', 'Awaken', 'Dominate Person', 'Dream', 'Geas', 'Greater Restoration',
                'Hold Monster', 'Legend Lore', 'Mass Cure Wounds', 'Mislead', 'Modify Memory', 'Planar Binding',
                'Raise Dead', 'Scrying', 'Seeming', 'Teleportation Circle'],
            'Cleric': ['Commune', 'Contagion', 'Dispel Eil and Good', 'Flame Strike', 'Geas', 'Greater Restoration',
                'Hallow', 'Insect Plague', 'Legend Lore', 'Mass Cure Wounds', 'Planar Binding', 'Raise Dead', 'Scrying'],
            'Druid': ['Antilife Shell','Awaken','Commune with Nature','Conjure Elemental','Contagion','Geas','Greater Restoration',
                'Insect Plague','Mass Cure Wounds','Planar Binding','Reincarnate','Scrying','Tree Stride','Wall of Stone'],
            'Paladin': ['Banishment Smite','Circle of Power','Destructive Wave','Dispel Evil and Good','Geas','Raise Dead'],
            'Ranger': ['Commune with Nature','Conjure Volley','Swifft Quiver','Tree Stride'],
            'Sorcerer':['Animate Object','Cloudkill','Cone of Cold','Creation','Dominate Person','Hold Monster',
                'Insect Plague','Seeming','Telekinesis','Teleportation Circle','Wall of Stone'],
            'Wizard': ['Animate Object',"Bigby's Hand",'Cloudkill','Cone of Cold','Conjure Elemental','Contact Other Plane',
                'Creation','Dominate Person','Dream','Geas','Hold Monster','Legend Lore','Mislead','Modify Memory','Passwall',
                'Planar Binding',"Rary's Telepathy Bond",'Scrying','Seeming','Telekinesis','Teleportation Circle','Wall of Force',
                'Wall of Stone']
        },
        'Level 6': {
            'Bard': ['Eyebite', 'Find the Path', 'Guards and Wards', 'Mass Suggestion', "Otto's Irresistible Dance",
                'Programmed Illusion', 'True Seeing'],
            'Cleric': ['Blade Barrier', 'Create Undead', 'Find the Path', 'Forbiddance', 'Harm', 'Heal', 'Heroes Feast',
                'Planar Ally', 'True Seeing', 'Word of Recall'],
            'Druid': ['Conjure Fey','Find the Path','Heal',"Heroes' Feast",'Move Earth','Sunbeam','Transport via Plants',
                'Wall of Thorns','Wind Walk'],
            'Sorcerer': ['Arcane Gate','Chain Lightning','Circle of Death','Disintegrate','Eyebite','Globe of Invulnerability',
                'Mass Suggestion','Move Earth','Sunbeam','True Seeing'],
            'Wizard': ['Arcane Gate','Chain Lightning','Circle of Death','Contingency','Create Undead','Disintegrate',
                "Drawmij's Instant Summons",'Eyebite','Flesh of Stone','Globe of Invulnerability','Guards and Wards','Magic Jar',
                'Mass Suggestion','Move Earth',"Otiluke's Freezing Sphere","Otto's Irresistible Dance",'Programmed Illusion',
                'Sunbeam','True Seeing','Wall of Ice']
        },
        'Level 7': {
            'Bard': ['Ethereal', 'Forcecage', 'Mirage Arcane', "Mordenkainen's Magnificent Mansion", "Mordenkainen's Sword",
                'Project Image', 'Regenerate', 'Resurrection', 'Symbol', 'Teleport'],
            'Cleric': ['Conjure Celestial', 'Divine Word', 'Etherealness', 'Fire Storm', 'Plane Shift', 'Regenerate',
                'Resurrection', 'Symbol'],
            'Druid': ['Fire Storm','Mirage Arcane','Plane Shift','Regenerate','Reverse Gravity'],
            'Sorcerer': ['Delayed Blast Fireball','Etherealness','Finger of Death','Fire Storm','Plane Shift',
                'Prismatic Spray','Reverse Gravity','Teleport'],
            'Wizard': ['Delayed Blast Fireball','Etherealness','Finger of Death','Forcecage','Mirage Arcane',
                "Mordenkainen's Magnificent Mansion","Mordenkainen's Sword",'Plane Shift','Prismatic Spray','Project Image',
                'Reverse Gravity','Sequester','Simulacrum','Symbol','Teleport']
        },
        'Level 8': {
            'Bard': ['Dominate Monster', 'Feeblemind', 'Glibness', 'Mind Blank', 'Power Word Stun'],
            'Cleric': ['Antimagic Field', 'Control Weather','Earthquake','Holy Aura'],
            'Druid': ['Animal Shapes','Antipathy/Sympathy','Control Weather','Earthquake','Feeblemind','Sunburst','Tsunami'],
            'Sorcerer': ['Dominate Monster','Earthquake','Incendiary Cloud','Power Word Stun','Sunburst'],
            'Wizard': ['Antimagic Field','Antipathy/Sympathy','Clone','Control Weather','Demiplane','Dominate Monster',
                'Feeblemind','Incendiary Cloud','Maze','Mind Blank','Power Word Stun','Sunburst','Telepathy']
        },
        'Level 9': {
            'Bard': ['Foresight', 'Power Word Heal', 'Power Word Kill', 'True Polymorph'],
            'Cleric': ['Astral Projection', 'Gate', 'Mass Heal','True Resurrection'],
            'Druid': ['Foresight','Shapechange','Storm of Vengeance','True Resurrection'],
            'Sorcerer': ['Gate','Meteor Swarm','Power Word Kill','Time Stop','Wish'],
            'Wizard': ['Astral Projection','Foresight','Gate','Imprisonment','Meteor Swarm','Power Word Kill',
                'Prismatic Wall','Shapechange','Time Stop','True Polymorph','Weird','Wish']
        }
    }
    
    class_spell_structure = {
        'Bard': {
            1: {'Cantrips': 2, 'Level 1': 2},
            2: {'Cantrips': 2, 'Level 1': 3},
            3: {'Cantrips': 2, 'Level 1': 4, 'Level 3': 2},
            4: {'Cantrips': 3, 'Level 1': 4, 'Level 3': 3},
            5: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            6: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            7: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            8: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            9: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            10: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            11: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            12: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            13: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            14: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            15: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            16: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            17: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            18: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            19: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            20: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 2, 'Level 8': 1, 'Level 9': 1}
        },
        'Cleric': {
            1: {'Cantrips': 3, 'Level 1': 2},
            2: {'Cantrips': 3, 'Level 1': 3},
            3: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 2},
            4: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3},
            5: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            6: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            7: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            8: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            9: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            10: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            11: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            12: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            13: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            14: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            15: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            16: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            17: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            18: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            19: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            20: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 2, 'Level 8': 1, 'Level 9': 1}
        },
        'Druid': {
            1: {'Cantrips': 2, 'Level 1': 2},
            2: {'Cantrips': 2, 'Level 1': 3},
            3: {'Cantrips': 2, 'Level 1': 4, 'Level 2': 2},
            4: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3},
            5: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            6: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            7: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            8: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            9: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            10: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            11: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            12: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            13: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            14: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            15: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            16: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            17: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            18: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            19: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 2, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            20: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 2, 'Level 7': 2, 'Level 8': 1, 'Level 9': 1}
        },
        'Paladin': {
            1: {},
            2: {'Level 1': 2},
            3: {'Level 1': 3},
            4: {'Level 1': 3},
            5: {'Level 1': 4, 'Level 2': 2},
            6: {'Level 1': 4, 'Level 2': 2},
            7: {'Level 1': 4, 'Level 2': 3},
            8: {'Level 1': 4, 'Level 2': 3},
            9: {'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            10: {'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            11: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            12: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            13: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            14: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            15: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            16: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            17: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            18: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            19: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            20: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2}
        },
        'Ranger': {
            1: {},
            2: {'Level 1': 2},
            3: {'Level 1': 3},
            4: {'Level 1': 3},
            5: {'Level 1': 4, 'Level 2': 2},
            6: {'Level 1': 4, 'Level 2': 2},
            7: {'Level 1': 4, 'Level 2': 3},
            8: {'Level 1': 4, 'Level 2': 3},
            9: {'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            10: {'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            11: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            12: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            13: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            14: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            15: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            16: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            17: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            18: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            19: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            20: {'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2}
        },
        'Sorcerer': {
            1: {'Cantrips': 4, 'Level 1': 2},
            2: {'Cantrips': 4, 'Level 1': 3},
            3: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 2},
            4: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3},
            5: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            6: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            7: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            8: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            9: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            10: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            11: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            12: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            13: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            14: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            15: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            16: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            17: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            18: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            19: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            20: {'Cantrips': 6, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 2, 'Level 8': 1, 'Level 9': 1},
        },
        'Warlock': {
            1: {'Cantrips': 2},
            2: {'Cantrips': 2},
            3: {'Cantrips': 2},
            4: {'Cantrips': 3},
            5: {'Cantrips': 3},
            6: {'Cantrips': 3},
            7: {'Cantrips': 3},
            8: {'Cantrips': 3},
            9: {'Cantrips': 3},
            10: {'Cantrips': 4},
            11: {'Cantrips': 4},
            12: {'Cantrips': 4},
            13: {'Cantrips': 4},
            14: {'Cantrips': 4},
            15: {'Cantrips': 4},
            16: {'Cantrips': 4},
            17: {'Cantrips': 4},
            18: {'Cantrips': 4},
            19: {'Cantrips': 4},
            20: {'Cantrips': 4}
        },
        'Wizard': {
            1: {'Cantrips': 3, 'Level 1': 2},
            2: {'Cantrips': 3, 'Level 1': 3},
            3: {'Cantrips': 3, 'Level 1': 4, 'Level 2': 2},
            4: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3},
            5: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 2},
            6: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3},
            7: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 1},
            8: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 2},
            9: {'Cantrips': 4, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 1},
            10: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2},
            11: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            12: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1},
            13: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            14: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1},
            15: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            16: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1},
            17: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 2, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            18: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 1, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            19: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 1, 'Level 8': 1, 'Level 9': 1},
            20: {'Cantrips': 5, 'Level 1': 4, 'Level 2': 3, 'Level 3': 3, 'Level 4': 3, 'Level 5': 3, 'Level 6': 2, 'Level 7': 2, 'Level 8': 1, 'Level 9': 1}
        }
    }
    
    warlock_details = {
        1: {'spells_known': 2, 'max_spell_level': 5},
        2: {'spells_known': 3, 'max_spell_level': 5},
        3: {'spells_known': 4, 'max_spell_level': 5},
        4: {'spells_known': 5, 'max_spell_level': 5},
        5: {'spells_known': 6, 'max_spell_level': 5},
        6: {'spells_known': 7, 'max_spell_level': 5},
        7: {'spells_known': 8, 'max_spell_level': 5},
        8: {'spells_known': 9, 'max_spell_level': 5},
        9: {'spells_known': 10, 'max_spell_level': 5},
        10: {'spells_known': 10, 'max_spell_level': 5},
        11: {'spells_known': 11, 'max_spell_level': 6},
        12: {'spells_known': 11, 'max_spell_level': 6},
        13: {'spells_known': 12, 'max_spell_level': 7},
        14: {'spells_known': 12, 'max_spell_level': 7},
        15: {'spells_known': 13, 'max_spell_level': 8},
        16: {'spells_known': 13, 'max_spell_level': 8},
        17: {'spells_known': 14, 'max_spell_level': 9},
        18: {'spells_known': 14, 'max_spell_level': 9},
        19: {'spells_known': 15, 'max_spell_level': 9},
        20: {'spells_known': 15, 'max_spell_level': 9}
    }
    
    warlock_spells = {
        1: ['Armor of Agathys','Arms of Hadar','Charm Person','Comprehend Languages','Expeditious Retreat', 'Hellish Rebuke','Hex','Illosory',
            'Protection from Evil and Good','Unseen Servant','Witch Bolt'],
        2: ['Cloud of Daggers','Crown of Madness','Darkness','Enthrall','Hold Person','Hold Person',
            'Invisibility','Mirror Image','Misty Step','Ray of Enfeeblement','Shatter','Spider Climb','Suggestion'],
        3: ['Counterspell','Dispel Magic','Fear','Fly','Gaseous Form','Hunger of Hadar','Hypnotic Pattern', 
            'Magic Circle','Major Image','Remove Curse','Tongues','Vampiric Touch'],
        4: ['Banishment','Blight','Dimension Door','Hallucinatory Terrain'],
        5: ['Contact Other Plane','Dream','Hold Monster','Scrying'],
        6: ['Arcane Gate','Circle of Death','Conjure Fey','Create Undead','Eyebite','Flesh to Stone', 'Mass Suggestion','True Seeing'],
        7: ['Etherealness','Finger of Death','Forcecage','Plane Shift'],
        8: ['Demiplane','Dominate Monster','Feeblemind','Glibness','Power Word Stun'],
        9: ['Astral Projection','Foresight','Imprisonment','Power Word Kill','True Polymorph']
    }
    
    def get_warlock_spells(char_level):
        details = warlock_details[char_level]
        spells_known = details['spells_known']
        max_spell_level = details['max_spell_level']
        # Flatten all available spells into a list with their levels.
        flat_spells = [(f"Level {level}", spell) for level in range(1, max_spell_level + 1) for spell in warlock_spells[level]]
        # Sample the spells without replacement.
        sampled_spells = random.sample(flat_spells, spells_known)
    
        # Reconstruct the spell levels.
        selected_spells = {}
        for spell_level, spell in sampled_spells:
            if spell_level in selected_spells:
                selected_spells[spell_level].append(spell)
            else:
                selected_spells[spell_level] = [spell]
        # Sort by spell level
        sorted_spells = {k: selected_spells[k] for k in sorted(selected_spells.keys())}
        return sorted_spells
    
    def apply_racial_bonuses(stats, race):
        bonuses = racial_bonuses.get(race, {})
        for stat, bonus in bonuses.items():
            stats[stat] += bonus
        return stats
    
    def get_random_spells(char_class, char_level):
        selected_spells = {}
        if char_class not in ["Monk", "Fighter", "Barbarian", "Rogue"]:
            spells_for_level = class_spell_structure[char_class][char_level]
            # Iterate over each spell level (e.g., 'Level 1', 'Level 2', ...)
            for spell_level, num_spells in spells_for_level.items():
                # Randomly select the required number of spells from the appropriate list
                selected_spells[spell_level] = random.sample(spells_by_level[spell_level][char_class], num_spells)
        if char_class == "Warlock":
            warlock_spells = get_warlock_spells(char_level)
            for spell_level, spells in warlock_spells.items():
                if spell_level in selected_spells:
                    selected_spells[spell_level].extend(spells)
                else:
                    selected_spells[spell_level] = spells
        return selected_spells
    
    selected_class = event.get("queryStringParameters", {}).get("class", random.choice(classes))
    selected_race = event.get("queryStringParameters", {}).get("race", random.choice(races))
    char_level = int(event.get("queryStringParameters", {}).get("level", 1))
    
    char_class = selected_class if selected_class in classes else random.choice(classes)
    char_race = selected_race if selected_race in races else random.choice(races)

    char_spells = get_random_spells(char_class, char_level)
    char_gear = gear[char_class]
    char_stats = generate_stats(class_stat_importance[char_class])
    char_stats = apply_racial_bonuses(char_stats, char_race)
    presentation_order = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    html_content = f"""
    <html>
        <head>
            <title>D&D Character Generator</title>
        </head>
        <body>
            <h1>Your Random Character</h1>
            <p><b>Level:</b> {char_level}</p>
            <p><b>Race:</b> {char_race}</p>
            <p><b>Class:</b> {char_class}</p>
            <p><b>Gear:</b> {char_gear}</p>
            <p><b>Stats:</b></p>
            <ul>
    """
        
    for stat in presentation_order:
        html_content += f"<li>{stat}: {char_stats[stat]}</li>"

    html_content += f"""
    <p><b>Spells:</b></p>
    <ul>
    """
    if isinstance(char_spells, dict):
        for spell_level, spells in char_spells.items():
            for spell in spells:
                html_content += f"<li>{spell_level}: {spell}</li>"
    else:
        for spell in char_spells:
            html_content += f"<li>{spell}</li>"
    
    html_content += """
            </ul>
            <h2>Select Class:</h2>
    """

    for class_option in classes:
        html_content += f"<button onclick=\"window.location.href='?class={class_option}&race={selected_race}&level={char_level}'\">{class_option}</button> "
    
    html_content += """
        <h2>Select Race:</h2>
    """

    for race in races:
        html_content += f"<button onclick=\"window.location.href='?race={race}&class={selected_class}&level={char_level}'\">{race}</button> "

    html_content += '<p>Select Level:</p>'
    for level in range(1, 21):
        html_content += f"<button onclick=\"window.location.href='?class={selected_class}&race={selected_race}&level={level}'\">{level}</button> "

    
    html_content += """
        </body>
    </html>
    """

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_content
    }
