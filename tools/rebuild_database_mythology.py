#!/usr/bin/env python3
"""
MEDUSA CTF - Database Rebuild Script with Greek Mythology Theme
Creates medusa.db with 12 tables filled with ancient Greek mythology themed data
Uses Google Gemini API to generate realistic mythological content
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta
import json

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDLpuZBNP2zoJqencq95gGB1EIwn2kcrZ8"

DB_PATH = "../assets/medusa.db"

# Ancient Greek Mythology Data
GREEK_GODS = [
    "Zeus", "Hera", "Poseidon", "Demeter", "Athena", "Apollo", "Artemis", "Ares",
    "Aphrodite", "Hephaestus", "Hermes", "Dionysus", "Hades", "Persephone", "Hestia"
]

GREEK_HEROES = [
    "Perseus", "Hercules", "Achilles", "Odysseus", "Theseus", "Jason", "Bellerophon",
    "Orpheus", "Atalanta", "Castor", "Pollux", "Cadmus", "Meleager", "Peleus"
]

GREEK_MONSTERS = [
    "Medusa", "Minotaur", "Cerberus", "Hydra", "Chimera", "Sphinx", "Cyclops",
    "Scylla", "Charybdis", "Typhon", "Echidna", "Orthrus", "Ladon", "Python"
]

TITANS = [
    "Cronus", "Rhea", "Oceanus", "Tethys", "Hyperion", "Theia", "Coeus", "Phoebe",
    "Iapetus", "Themis", "Mnemosyne", "Crius", "Prometheus", "Atlas", "Epimetheus"
]

NYMPHS = [
    "Calypso", "Daphne", "Echo", "Eurydice", "Galatea", "Arethusa", "Syrinx",
    "Thetis", "Amphitrite", "Nereid", "Oceanid", "Naiad", "Dryad", "Oreiad"
]

MYTHICAL_PLACES = [
    "Mount Olympus", "Delphi", "Thebes", "Athens", "Sparta", "Troy", "Crete",
    "Colchis", "Ithaca", "Argos", "Corinth", "Mycenae", "Eleusis", "Delos"
]

DIVINE_ITEMS = [
    "Aegis Shield", "Thunderbolt", "Trident", "Helm of Darkness", "Caduceus",
    "Golden Fleece", "Winged Sandals", "Cap of Invisibility", "Bow of Apollo",
    "Girdle of Aphrodite", "Lyre of Orpheus", "Sword of Perseus", "Club of Hercules"
]

MYTHICAL_CREATURES = [
    "Pegasus", "Griffin", "Phoenix", "Centaur", "Satyr", "Harpy", "Gorgon",
    "Siren", "Fury", "Muse", "Grace", "Fate", "Nemean Lion", "Stymphalian Birds"
]

GREEK_QUESTS = [
    "Twelve Labors of Hercules", "Quest for Golden Fleece", "Slaying of Medusa",
    "Trojan War", "Odyssey", "Theseus and Minotaur", "Orpheus in Underworld",
    "Perseus and Andromeda", "Bellerophon and Chimera", "Cadmus and Dragon"
]

DIVINE_DOMAINS = [
    "Sky", "Sea", "Underworld", "War", "Wisdom", "Hunt", "Love", "Fire",
    "Wine", "Agriculture", "Hearth", "Moon", "Sun", "Death", "Dreams"
]

MYTHICAL_EVENTS = [
    "Titanomachy", "Gigantomachy", "Typhonomachy", "Trojan War", "Calydonian Boar Hunt",
    "Wedding of Peleus and Thetis", "Judgement of Paris", "Rape of Persephone",
    "Deucalion's Flood", "Creation of Pandora", "War of Seven Against Thebes"
]

# Greek-style names generator
GREEK_NAME_PREFIXES = [
    "Theo", "Nico", "Alex", "Demo", "Pyth", "Peri", "Philo", "Aristo", "Chry",
    "Andro", "Leoni", "Dion", "Heli", "Soph", "Steph", "Xeno", "Cleo", "Melo"
]

GREEK_NAME_SUFFIXES = [
    "cles", "phon", "dorus", "stratus", "menos", "genes", "polis", "nikos",
    "laus", "doros", "menes", "theus", "phanes", "kles", "dotos", "crates"
]

def generate_greek_name():
    """Generate a random Greek-style name"""
    return random.choice(GREEK_NAME_PREFIXES) + random.choice(GREEK_NAME_SUFFIXES)

def generate_email(name):
    """Generate an email address"""
    domains = ["olympus.gr", "delphi.gr", "sparta.gr", "athens.gr", "mythology.gr"]
    return f"{name.lower()}@{random.choice(domains)}"

def generate_divine_power():
    """Generate a random divine power description"""
    powers = [
        "Control over storms and lightning",
        "Command of ocean waves and earthquakes",
        "Mastery of death and souls",
        "Divine wisdom and strategic warfare",
        "Immortal beauty and charm",
        "Prophetic visions and healing",
        "Supernatural strength and valor",
        "Shape-shifting abilities",
        "Time manipulation",
        "Fire conjuring and metalwork"
    ]
    return random.choice(powers)

def random_date(start_year=400, end_year=1200):
    """Generate a random date BCE"""
    year = random.randint(start_year, end_year)
    return f"{year} BCE"

def random_modern_date(start_year=2020, end_year=2025):
    """Generate a random modern date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def rebuild_database():
    """Rebuild the entire database with Greek mythology themed data"""
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DB_PATH)
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️  Removed existing database")
    
    # Ensure assets directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("⚡ Creating mythological database with 12 tables...")
    
    # ========================================================================
    # Table 1: credentials (Divine Access Credentials)
    # ========================================================================
    print("  📋 Creating table 1/12: credentials (Divine Access)")
    cursor.execute("""
        CREATE TABLE credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Add the actual credentials
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", 
                   ("admin","medusa_r2_secret_key"))
    
    # Add Greek god credentials
    god_passwords = {
        "perseus": "m3dus4_sl4y3r",
        "hercules": "n3m34n_l10n",
        "athena": "0w1_of_w1sd0m",
        "poseidon": "tr1d3nt_k1ng",
        "aphrodite": "b34uty_qu33n",
        "ares": "w4r_g0d",
        "artemis": "hunt3r_m00n",
        "zeus": "thund3r_b0lt",
        "apollo": "s0lar_fl4r3",
        "hephaestus": "f0rg3_m4st3r",
        "dionysus": "w1n3_g0d",
        "hermes": "m3ss3ng3r",
        "hades": "und3rw0rld_k1ng",
        "demeter": "h4rv3st_g0dd3ss",
    }
    
    for username, password in god_passwords.items():
        cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", 
                       (username, password))
    
    # Add 120 mortal credentials
    for i in range(120):
        username = f"mortal_{i+1:03d}"
        password = f"olympus{random.randint(1000, 9999)}"
        cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", 
                       (username, password))
    
    # ========================================================================
    # Table 2: olympian_gods (The Twelve Olympians + more)
    # ========================================================================
    print("  📋 Creating table 2/12: olympian_gods")
    cursor.execute("""
        CREATE TABLE olympian_gods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            god_name TEXT NOT NULL,
            domain TEXT,
            symbol TEXT,
            sacred_animal TEXT,
            divine_power TEXT,
            palace_location TEXT,
            worshipers INTEGER
        )
    """)
    
    olympian_data = [
        ("Zeus", "King of Gods, Sky, Thunder", "Thunderbolt, Eagle, Oak", "Eagle", "Control over storms and lightning", "Mount Olympus", random.randint(100000, 1000000)),
        ("Hera", "Queen of Gods, Marriage", "Peacock, Cow, Pomegranate", "Peacock", "Divine marriage bonds", "Mount Olympus", random.randint(50000, 500000)),
        ("Poseidon", "God of Sea, Earthquakes", "Trident, Horse, Dolphin", "Horse", "Command of ocean waves", "Underwater Palace", random.randint(80000, 800000)),
        ("Demeter", "Goddess of Agriculture", "Wheat, Torch, Poppy", "Snake", "Fertility and harvest", "Eleusis", random.randint(60000, 600000)),
        ("Athena", "Goddess of Wisdom, War", "Owl, Olive Tree, Aegis", "Owl", "Divine wisdom and strategy", "Athens Parthenon", random.randint(90000, 900000)),
        ("Apollo", "God of Sun, Music, Prophecy", "Lyre, Laurel, Bow", "Swan", "Light and prophecy", "Delphi", random.randint(95000, 950000)),
        ("Artemis", "Goddess of Hunt, Moon", "Bow, Deer, Cypress", "Deer", "Mastery of the hunt", "Forest of Arcadia", random.randint(70000, 700000)),
        ("Ares", "God of War", "Spear, Helmet, Dog", "Vulture", "Bloodlust and battle rage", "Thrace", random.randint(65000, 650000)),
        ("Aphrodite", "Goddess of Love, Beauty", "Dove, Rose, Swan", "Dove", "Irresistible charm", "Cyprus", random.randint(100000, 1000000)),
        ("Hephaestus", "God of Fire, Forge", "Hammer, Anvil, Tongs", "Donkey", "Divine craftsmanship", "Volcanic Forge", random.randint(55000, 550000)),
        ("Hermes", "Messenger God, Trade", "Caduceus, Winged Sandals", "Tortoise", "Super speed", "Mount Cyllene", random.randint(85000, 850000)),
        ("Dionysus", "God of Wine, Festivity", "Grapevine, Thyrsus", "Leopard", "Ecstasy and madness", "Mount Nysa", random.randint(75000, 750000)),
        ("Hades", "God of Underworld", "Helm of Darkness, Cerberus", "Serpent", "Rule over the dead", "Underworld Palace", random.randint(50000, 500000)),
        ("Hestia", "Goddess of Hearth", "Sacred Fire, Kettle", "Pig", "Eternal flame", "Olympus Hearth", random.randint(40000, 400000)),
        ("Persephone", "Queen of Underworld", "Pomegranate, Torch", "Bat", "Spring renewal", "Underworld", random.randint(45000, 450000)),
    ]
    
    for god_data in olympian_data:
        cursor.execute("""
            INSERT INTO olympian_gods (god_name, domain, symbol, sacred_animal, divine_power, palace_location, worshipers)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, god_data)
    
    # Add more gods with random data
    for i in range(135):
        cursor.execute("""
            INSERT INTO olympian_gods (god_name, domain, symbol, sacred_animal, divine_power, palace_location, worshipers)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            generate_greek_name(),
            random.choice(DIVINE_DOMAINS),
            random.choice(DIVINE_ITEMS),
            random.choice(["Eagle", "Owl", "Serpent", "Lion", "Wolf", "Dolphin", "Horse"]),
            generate_divine_power(),
            random.choice(MYTHICAL_PLACES),
            random.randint(10000, 500000)
        ))
    
    # ========================================================================
    # Table 3: legendary_heroes (Heroes and Demigods)
    # ========================================================================
    print("  📋 Creating table 3/12: legendary_heroes")
    cursor.execute("""
        CREATE TABLE legendary_heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hero_name TEXT NOT NULL,
            parent_god TEXT,
            famous_deed TEXT,
            divine_gift TEXT,
            fate TEXT,
            birthplace TEXT,
            glory_level INTEGER
        )
    """)
    
    hero_deeds = [
        ("Perseus", "Zeus", "Slaying Medusa and saving Andromeda", "Winged Sandals from Hermes", "Became constellation", "Argos", 95),
        ("Hercules", "Zeus", "Completed Twelve Labors", "Immortal strength", "Ascended to Olympus", "Thebes", 100),
        ("Achilles", "Thetis", "Greatest warrior of Trojan War", "Near invulnerability", "Killed by arrow to heel", "Phthia", 98),
        ("Odysseus", "Laertes", "Epic journey home from Troy", "Cunning intelligence", "Returned to Ithaca", "Ithaca", 92),
        ("Theseus", "Poseidon", "Slaying the Minotaur", "Ariadne's thread", "King of Athens", "Athens", 90),
        ("Jason", "Aeson", "Quest for Golden Fleece", "Argo ship", "Tragic end", "Iolcus", 85),
    ]
    
    for hero in hero_deeds:
        cursor.execute("""
            INSERT INTO legendary_heroes (hero_name, parent_god, famous_deed, divine_gift, fate, birthplace, glory_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, hero)
    
    # Add more heroes
    for i in range(174):
        cursor.execute("""
            INSERT INTO legendary_heroes (hero_name, parent_god, famous_deed, divine_gift, fate, birthplace, glory_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            generate_greek_name(),
            random.choice(GREEK_GODS),
            f"Defeated {random.choice(GREEK_MONSTERS)}",
            random.choice(DIVINE_ITEMS),
            random.choice(["Became constellation", "Tragic death", "Eternal glory", "Lost to history"]),
            random.choice(MYTHICAL_PLACES),
            random.randint(50, 100)
        ))
    
    # ========================================================================
    # Table 4: mythical_creatures (Monsters and Beasts)
    # ========================================================================
    print("  📋 Creating table 4/12: mythical_creatures")
    cursor.execute("""
        CREATE TABLE mythical_creatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creature_name TEXT NOT NULL,
            creature_type TEXT,
            origin TEXT,
            defeated_by TEXT,
            location TEXT,
            danger_level INTEGER,
            description TEXT
        )
    """)
    
    creatures = [
        ("Medusa", "Gorgon", "Cursed by Athena", "Perseus", "Cave in distant isle", 95, "Serpent-haired monster whose gaze turns mortals to stone"),
        ("Minotaur", "Bull-headed beast", "Born of Pasiphaë", "Theseus", "Labyrinth of Crete", 85, "Half-man half-bull imprisoned in maze"),
        ("Cerberus", "Three-headed dog", "Offspring of Typhon", "Hercules (captured)", "Gates of Hades", 90, "Guardian of the Underworld"),
        ("Hydra", "Multi-headed serpent", "Child of Echidna", "Hercules", "Swamps of Lerna", 92, "Regenerating heads when cut"),
        ("Chimera", "Fire-breathing hybrid", "Offspring of Typhon", "Bellerophon", "Mountains of Lycia", 88, "Lion-goat-serpent creature"),
    ]
    
    for creature in creatures:
        cursor.execute("""
            INSERT INTO mythical_creatures (creature_name, creature_type, origin, defeated_by, location, danger_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, creature)
    
    # Add more creatures
    for i in range(195):
        cursor.execute("""
            INSERT INTO mythical_creatures (creature_name, creature_type, origin, defeated_by, location, danger_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            generate_greek_name() + " Beast",
            random.choice(["Dragon", "Giant", "Monster", "Beast", "Demon"]),
            f"Born of {random.choice(TITANS)}",
            random.choice(GREEK_HEROES),
            random.choice(MYTHICAL_PLACES),
            random.randint(40, 100),
            f"Fearsome creature that terrorized ancient {random.choice(MYTHICAL_PLACES)}"
        ))
    
    # ========================================================================
    # Table 5: epic_quests (Legendary Journeys and Labors)
    # ========================================================================
    print("  📋 Creating table 5/12: epic_quests")
    cursor.execute("""
        CREATE TABLE epic_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_name TEXT NOT NULL,
            hero TEXT,
            objective TEXT,
            reward TEXT,
            difficulty INTEGER,
            duration_years INTEGER,
            success INTEGER
        )
    """)
    
    for i in range(220):
        cursor.execute("""
            INSERT INTO epic_quests (quest_name, hero, objective, reward, difficulty, duration_years, success)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            random.choice(GREEK_QUESTS) if i < 10 else f"Quest of {generate_greek_name()}",
            random.choice(GREEK_HEROES),
            f"Retrieve {random.choice(DIVINE_ITEMS)} from {random.choice(MYTHICAL_PLACES)}",
            random.choice(["Eternal glory", "Divine favor", "Magical artifact", "Kingdom"]),
            random.randint(1, 10),
            random.randint(1, 20),
            random.randint(0, 1)
        ))
    
    # ========================================================================
    # Table 6: divine_artifacts (Sacred Objects and Weapons)
    # ========================================================================
    print("  📋 Creating table 6/12: divine_artifacts")
    cursor.execute("""
        CREATE TABLE divine_artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_name TEXT NOT NULL,
            forged_by TEXT,
            owner TEXT,
            power TEXT,
            location TEXT,
            power_level INTEGER
        )
    """)
    
    artifacts = [
        ("Thunderbolt of Zeus", "Cyclopes", "Zeus", "Ultimate lightning weapon", "Mount Olympus", 100),
        ("Trident of Poseidon", "Cyclopes", "Poseidon", "Control over seas", "Underwater Palace", 98),
        ("Aegis Shield", "Hephaestus", "Athena", "Impenetrable defense", "Parthenon", 95),
        ("Helm of Darkness", "Cyclopes", "Hades", "Invisibility", "Underworld", 92),
        ("Caduceus", "Hephaestus", "Hermes", "Guide souls, bring sleep", "Olympus", 85),
    ]
    
    for artifact in artifacts:
        cursor.execute("""
            INSERT INTO divine_artifacts (artifact_name, forged_by, owner, power, location, power_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, artifact)
    
    for i in range(245):
        cursor.execute("""
            INSERT INTO divine_artifacts (artifact_name, forged_by, owner, power, location, power_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            random.choice(DIVINE_ITEMS),
            random.choice(["Hephaestus", "Cyclopes", "Daedalus"]),
            random.choice(GREEK_GODS + GREEK_HEROES),
            generate_divine_power(),
            random.choice(MYTHICAL_PLACES),
            random.randint(30, 100)
        ))
    
    # ========================================================================
    # Table 7: oracle_prophecies (Divine Predictions)
    # ========================================================================
    print("  📋 Creating table 7/12: oracle_prophecies")
    cursor.execute("""
        CREATE TABLE oracle_prophecies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prophecy_text TEXT,
            oracle_location TEXT,
            given_to TEXT,
            date_spoken TEXT,
            fulfilled INTEGER,
            interpretation TEXT
        )
    """)
    
    prophecies = [
        ("You shall slay the Gorgon but beware her sisters' wrath", "Delphi", "Perseus", "1250 BCE", 1, "Perseus killed Medusa"),
        ("The child of prophecy shall overthrow his father", "Delphi", "Cronus", "Beginning of Time", 1, "Zeus overthrew Cronus"),
        ("Ten years war, ten years wandering home", "Delphi", "Odysseus", "1184 BCE", 1, "The Odyssey"),
    ]
    
    for prophecy in prophecies:
        cursor.execute("""
            INSERT INTO oracle_prophecies (prophecy_text, oracle_location, given_to, date_spoken, fulfilled, interpretation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, prophecy)
    
    for i in range(177):
        cursor.execute("""
            INSERT INTO oracle_prophecies (prophecy_text, oracle_location, given_to, date_spoken, fulfilled, interpretation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            f"When {random.choice(['moon', 'sun', 'stars'])} align, {random.choice(['hero', 'god', 'mortal'])} shall {random.choice(['rise', 'fall', 'triumph'])}",
            random.choice(["Delphi", "Dodona", "Delos", "Olympia"]),
            random.choice(GREEK_HEROES + GREEK_GODS),
            random_date(),
            random.randint(0, 1),
            f"Foretold the {random.choice(['rise', 'fall', 'glory'])} of {generate_greek_name()}"
        ))
    
    # ========================================================================
    # Table 8: titan_wars (Epic Battles)
    # ========================================================================
    print("  📋 Creating table 8/12: titan_wars")
    cursor.execute("""
        CREATE TABLE titan_wars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            war_name TEXT NOT NULL,
            faction_a TEXT,
            faction_b TEXT,
            victor TEXT,
            duration_years INTEGER,
            casualties INTEGER,
            date_fought TEXT
        )
    """)
    
    wars = [
        ("Titanomachy", "Olympians led by Zeus", "Titans led by Cronus", "Olympians", 10, 999999, "Dawn of Time"),
        ("Gigantomachy", "Olympian Gods", "Giants", "Olympians with Heroes", 7, 500000, "After Titanomachy"),
        ("Trojan War", "Greeks", "Trojans", "Greeks", 10, 100000, "1184 BCE"),
    ]
    
    for war in wars:
        cursor.execute("""
            INSERT INTO titan_wars (war_name, faction_a, faction_b, victor, duration_years, casualties, date_fought)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, war)
    
    for i in range(147):
        cursor.execute("""
            INSERT INTO titan_wars (war_name, faction_a, faction_b, victor, duration_years, casualties, date_fought)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"War of {generate_greek_name()}",
            f"Army of {random.choice(MYTHICAL_PLACES)}",
            f"Forces of {random.choice(MYTHICAL_PLACES)}",
            random.choice(["Faction A", "Faction B", "Draw"]),
            random.randint(1, 20),
            random.randint(1000, 100000),
            random_date()
        ))
    
    # ========================================================================
    # Table 9: sacred_temples (Places of Worship)
    # ========================================================================
    print("  📋 Creating table 9/12: sacred_temples")
    cursor.execute("""
        CREATE TABLE sacred_temples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temple_name TEXT NOT NULL,
            dedicated_to TEXT,
            location TEXT,
            built_year TEXT,
            priests INTEGER,
            pilgrims_yearly INTEGER
        )
    """)
    
    for i in range(120):
        cursor.execute("""
            INSERT INTO sacred_temples (temple_name, dedicated_to, location, built_year, priests, pilgrims_yearly)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            f"Temple of {random.choice(GREEK_GODS)}",
            random.choice(GREEK_GODS),
            random.choice(MYTHICAL_PLACES),
            random_date(),
            random.randint(5, 100),
            random.randint(1000, 100000)
        ))
    
    # ========================================================================
    # Table 10: underworld_souls (Spirits of the Dead)
    # ========================================================================
    print("  📋 Creating table 10/12: underworld_souls")
    cursor.execute("""
        CREATE TABLE underworld_souls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soul_name TEXT NOT NULL,
            death_cause TEXT,
            judgment TEXT,
            realm TEXT,
            entrance_date TEXT,
            sins TEXT
        )
    """)
    
    realms = ["Elysium", "Asphodel Meadows", "Tartarus", "Fields of Punishment"]
    death_causes = [
        "Slain in battle", "Divine punishment", "Old age", "Betrayal",
        "Monster attack", "Hubris against gods", "Plague", "Shipwreck"
    ]
    
    for i in range(300):
        cursor.execute("""
            INSERT INTO underworld_souls (soul_name, death_cause, judgment, realm, entrance_date, sins)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            generate_greek_name(),
            random.choice(death_causes),
            random.choice(["Virtuous", "Average", "Wicked", "Heroic"]),
            random.choice(realms),
            random_date(),
            random.choice(["None", "Pride", "Greed", "Wrath", "Murder", "Blasphemy"])
        ))
    
    # ========================================================================
    # Table 11: divine_genealogy (Family Tree of Gods)
    # ========================================================================
    print("  📋 Creating table 11/12: divine_genealogy")
    cursor.execute("""
        CREATE TABLE divine_genealogy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deity_name TEXT NOT NULL,
            father TEXT,
            mother TEXT,
            generation TEXT,
            siblings TEXT,
            children TEXT
        )
    """)
    
    genealogy = [
        ("Zeus", "Cronus", "Rhea", "2nd (Olympian)", "Hades, Poseidon, Hera, Demeter, Hestia", "Many including Athena, Apollo, Artemis"),
        ("Athena", "Zeus", "Metis", "3rd", "Apollo, Artemis, Ares", "None"),
        ("Hercules", "Zeus", "Alcmene", "4th (Demigod)", "Many half-siblings", "None"),
    ]
    
    for entry in genealogy:
        cursor.execute("""
            INSERT INTO divine_genealogy (deity_name, father, mother, generation, siblings, children)
            VALUES (?, ?, ?, ?, ?, ?)
        """, entry)
    
    for i in range(157):
        cursor.execute("""
            INSERT INTO divine_genealogy (deity_name, father, mother, generation, siblings, children)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            generate_greek_name(),
            random.choice(GREEK_GODS + TITANS),
            random.choice(NYMPHS + ["Unknown"]),
            random.choice(["1st (Primordial)", "2nd (Titan)", "3rd (Olympian)", "4th (Minor Deity)"]),
            ", ".join(random.sample(GREEK_GODS, min(3, len(GREEK_GODS)))),
            f"{random.randint(0, 10)} children"
        ))
    
    # ========================================================================
    # Table 12: mystical_events (Legendary Occurrences)
    # ========================================================================
    print("  📋 Creating table 12/12: mystical_events")
    cursor.execute("""
        CREATE TABLE mystical_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            date_occurred TEXT,
            location TEXT,
            participants TEXT,
            divine_intervention TEXT,
            outcome TEXT,
            significance INTEGER
        )
    """)
    
    events = [
        ("Birth of Athena from Zeus's head", "Dawn of Olympian Era", "Mount Olympus", "Zeus, Hephaestus", "Zeus swallowed Metis", "Athena born fully armed", 95),
        ("Pandora Opens the Box", "Early Mortal Age", "Earth", "Pandora, Epimetheus", "Gift from Zeus", "Evil released to world", 100),
        ("The Great Flood", "Bronze Age", "All of Greece", "Deucalion, Pyrrha", "Zeus sent flood", "Humanity reborn from stones", 98),
    ]
    
    for event in events:
        cursor.execute("""
            INSERT INTO mystical_events (event_name, date_occurred, location, participants, divine_intervention, outcome, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, event)
    
    for i in range(217):
        cursor.execute("""
            INSERT INTO mystical_events (event_name, date_occurred, location, participants, divine_intervention, outcome, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            random.choice(MYTHICAL_EVENTS) if i < 11 else f"{random.choice(['Battle', 'Curse', 'Blessing', 'Transformation'])} of {generate_greek_name()}",
            random_date(),
            random.choice(MYTHICAL_PLACES),
            ", ".join(random.sample(GREEK_GODS + GREEK_HEROES, min(3, len(GREEK_GODS)))),
            f"{random.choice(GREEK_GODS)} intervened",
            random.choice(["Victory", "Tragedy", "Transformation", "Exile", "Apotheosis"]),
            random.randint(50, 100)
        ))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n" + "⚡" * 60)
    print("✅ Mythological Database Created Successfully!")
    print("⚡" * 60)
    print(f"📁 Location: {db_path}")
    print("\n📊 Summary of Ancient Greek Mythology Data:")
    print(f"   - credentials: 134 divine access codes")
    print(f"   - olympian_gods: 150 deities and divine beings")
    print(f"   - legendary_heroes: 180 heroes and demigods")
    print(f"   - mythical_creatures: 200 monsters and beasts")
    print(f"   - epic_quests: 220 legendary journeys")
    print(f"   - divine_artifacts: 250 sacred objects")
    print(f"   - oracle_prophecies: 180 divine predictions")
    print(f"   - titan_wars: 150 epic battles")
    print(f"   - sacred_temples: 120 places of worship")
    print(f"   - underworld_souls: 300 spirits of the dead")
    print(f"   - divine_genealogy: 160 family lineages")
    print(f"   - mystical_events: 220 legendary occurrences")
    print(f"\n   TOTAL: 2,264 rows of mythological data across 12 tables")
    print("\n⚡ Valid credentials for the challenge:")
    print(f"   🏆 CORRECT: zeus / thund3r_b0lt")
    print(f"   📜 Decoys: perseus, hercules, athena, apollo, etc.")
    print("\n" + "⚡" * 60)


if __name__ == "__main__":
    rebuild_database()
