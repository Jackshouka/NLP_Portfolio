import sqlite3

def add_character(connection, name):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM characters WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO characters (name) VALUES (?)", (name,))
        connection.commit()
        return cursor.lastrowid


def add_moves(connection, character_id, name, move_type, description):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO moves (character_id, name, move_type, description) VALUES (?, ?, ?, ?)",
                   (character_id, name, move_type, description))
    connection.commit()
    return cursor.lastrowid

def add_frame_data(connection, move_id, startup, active, recovery, on_block):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO frame_data (move_id, startup, active, recovery, on_block) VALUES (?, ?, ?, ?, ?)",
                   (move_id, startup, active, recovery, on_block))
    connection.commit()
    return cursor.lastrowid



def addBadguy(connection):
    character_id = add_character(connection, 'Sol Badguy')
    badguy_moves = [
        ('5p', 'Normal', 'Fast jab. Useful for stagger pressure as well.', 4, 4, 6, 0),
        ('5k', 'Normal' ,'Versitile, 3 frame jab. Jack of all trades.', 3, 1, 25, -16),
        ('c.S', 'Normal', 'Your primary pressure tool. Great combo starter.', 7, 6, 10, 3),
        ('f.S', 'Normal', 'Powerful pressure tool, cranks up opponent R.I.S.C. Great mid-range poke.', 10, 2, 13, 2),
        ('5h', 'Normal', 'Go-to for frame traps. Also viable mid-range poke.', 11, 4, 20, 4),
        ('5D', 'Normal', 'Fastest grounded overhead. Vital to your high/low mixup game.', 20, 3, 26, -15),
        ('5D (charge)', 'Normal' ,'Much slower and more dangerous, but will lead to a damaging homing jump combo.', 28, 3, 26, -10),
        ('2p', 'Normal', 'Slower than 5p and 5k, but can a useful mash option while crouch-blocking.' ,5, 4, 8, -2),
        ('2k', 'Normal', 'Fastest low-hitting move.' ,6, 3, 11, -2),
        ('2s', 'Normal', 'Fantastic poke. Disjointed low that helps control neutral.' ,10, 6, 15, -7),
        ('2h', 'Normal', 'Combo filler. Also a high risk/high reward anti-air.', 11, 5, 31, -17),
        ('2d', 'Normal','Universal sweep. Also low profiles.', 10, 3, 18, -4),
        ('6p', 'Normal', 'Upper body invincibility anti air.',  9, 5, 20, -11),
        ('6s', 'Normal', 'Slow startup, but great damage and disjointed.', 15, 6, 20, -9),
        ('6h', 'Normal', 'Niche normal move, particularly useful for punishes.' ,9, 3, 43, -27),
        ('j.p', 'Normal', 'Basic and safe air jab.', 5, 3, 8, 0),
        ('j.k', 'Normal', 'Long range and fast. Useful for air-to-air combat.', 6,3, 20, 0),
        ('j.s', 'Normal', 'Air combo filler and your primary jump-in.', 10, 3, 23, 2),
        ('j.h', 'Normal', 'Advanced combo tool. No recovery frames allows to link into follow ups easily.',11, 4, 0, 0),
        ('j.d', 'Normal', 'Disjointed air option. Corner combo staple.',9, 3, 17, 0),

        ('Ground Throw', 'Universal', 'Standard throw.' ,2, 3, 38, 0),
        ('Air Throw', 'Universal', 'Standard air-throw.' ,2, 3, 38, 0),

        ('Gunflame', 'Special', 'Long startup projectile. Sees the most use in pressure and okizeme.' , 18, 8, 54, -10),
        ('Gunflame (Feint)', 'Special', 'Much shorter recovery, allowing for resetting pressure or baiting a choice from the opponent. No projectile, as the attack is a feint.', 0, 0, 25, 0),
        ('Volcanic Viper (S)', 'Special','Fast, strike invincible reversal. Use to call out poor okizeme setups and predictable pressure. However it loses to throws. Sol\'s Dragon Punch.' , 9, 14, 18, -28),
        ('Volcanic Viper (H)', 'Special' , 'More powerful version of Volcanic Viper(S). Sol is left far more vulreble on whiff. Also loses to throws. Sol\'s Dragon Punch.', 13, 5, 19, -26),
        ('Bandit Revolver', 'Special' ,'Main mid-screen combo ender and gives strong corner carry.' , 12, 6, 9, -7),
        ('Bandit Revolver, 2nd Kick', 'Special' ,'Main mid-screen combo ender and gives strong corner carry.' , 6, 2, 6, -11),
        ('Bandit Bringer', 'Special', 'Reactable overhead. But can grant some powerful okizeme.', 30, 7, 12, -2),
        ('Bandit Bringer [AIR]', 'Special', 'Reactable overhead. But can grant some powerful okizeme.' ,22, 7, 12, 0),
        ('Wild Throw', 'Special', 'Command throw. Offers worse okizeme but deals more damage and has greater range.' ,6, 2, 41, 0),
        ('Night Raid Vortex', 'Special','Can travel underneath pokes and projectiles, allowing Sol to bully his way through neutral.' ,32, 8, 26, -17),
        ('Fafnir', 'Special', 'Strong okizeme tool. Leaves Sol at a significant frame advantage if opponent blocks.' ,24, 3, 16, 11),

        ('Tyrant Rave', 'Overdrive', 'High damage combo ender. Great wall break option as well.' , 9, 20, 41, -44),
        ('Heavy Mob Cemetery', 'Overdrive', 'Situational whiff punish at best. But funny to land.' , 21, 16, 49, 0)
    ]

    for move_name, move_type, description, startup, active, recovery, on_block in badguy_moves:
        move_id = add_moves(connection, character_id, move_name, move_type, description)
        frame_data_id = add_frame_data(connection, move_id, startup, active, recovery, on_block)


def addKyle(connection):
    character_id = add_character(connection, 'Ky Kiske')
    kyle_moves = [
        ('5p', 'Normal', 'A quick jab and useful anti-air.' ,5, 4, 7, -1),
        ('5k', 'Normal', 'Great normal that allows for meaty setups. Gatlings to sweep/2d for a hard knockdown.', 7,8, 6, -2),
        ('c.S', 'Normal', 'Great for close range pressure or meaty setups after a knockdown. Additionally a great tool for punishes.', 7, 6, 10, 1),
        ('f.S', 'Normal', 'Strong mid-range poke, also disjointed. A bit slow however, but more than makes up for that in distance covered.' ,12, 6, 13, -5),
        ('5h', 'Normal', 'CHUNKY swing with a lot of range. Sees the most use when hit confirming into ride the lightning or stun dipper.' ,14, 6, 21, -8),
        ('5D', 'Normal', 'Ky\'s only grounded overhead. Pretty quick as well.' , 20, 4, 25, -15),
        ('5D (charge)', 'Normal', 'Much slower and more dangerous, but will lead to a damaging homing jump combo.' , 28, 4, 25, -10),
        ('2p', 'Normal', 'Go-to fast normal. Great for mashing, establishing light pressure, and light punishes.' ,5, 4, 8, -2),
        ('2k', 'Normal', 'Fastest low mixup. A low risk check in neutral.' ,6, 4, 10, -2),
        ('2s', 'Normal', 'One of Ky\'s main pokes. Good balance of speed, range and cancel options.' ,10, 2, 20, -8),
        ('2h', 'Normal', 'Commital anti-air or frame trap. Can deal a world of hurt on counter hit, but leaves Ky at risk. Best not to swing around in neutral.', 11, 4, 28, -13),
        ('2d', 'Normal', 'Sweeping kick that leads to hard knockdown and allows Ky to run potent okizeme game.' ,10, 6, 18, -10),
        ('6p', 'Normal', 'Upper body invincibility anti air.', 9, 5, 17, -8),
        ('6k', 'Normal', 'Slow starter and risky pressure reset. Use in tandem with frame traps after conditioning opponent to block.', 25,2,11,4),
        ('6h', 'Normal', 'Risky poke. Better for whiff punishes.' ,15, 4, 20, -7),
        ('j.p', 'Normal', 'Fast and short-ranged air attack. Punishes empty air-dashes.' ,6, 3, 9, 0),
        ('j.k', 'Normal', 'Main air to air normal for Ky. ' ,7, 4, 8, 0),
        ('j.s', 'Normal', 'Disjointed air to air, also useful for air-to-ground approaches as well.' , 7, 3, 21, 0),
        ('j.h', 'Normal', 'Ky\'s main jump in normal.' ,13, 4, 23, 5),
        ('j.d', 'Normal', 'An air move that stalls Ky\'s momentum. Great combo filler as well.' , 13, 6, 15, 0),

        ('Ground Throw', 'Universal', 'Standard throw.' , 2, 3, 38, 0),
        ('Air Throw', 'Universal', 'Standard air-throw.' , 2, 3, 38, 0),

        ('Stun Edge', 'Special', 'Basic projectile. Great against hyper-aggressive opponents that rely on grounded normals.' , 13, 0, 46, -15),
        ('Stun Edge (Charged)', 'Special', 'Main okizeme tool after a hard knockdown. Excellent setup for mixups.' , 39, 0, 62, 25),
        ('Stun Edge (Air)', 'Special', 'Air projectile to keep opponents grounded, also a measure against your opponent\'s anti-air.' , 21, 0, 10, 0),
        ('Stun Dipper', 'Special', 'Fast sliding attack that low profiles. Can do a meaty with 5k afterwards to continue pressure.', 5, 12, 26, -15),
        ('Foudre Arc', 'Special', 'Great tool for corner carrying and combos.' ,24,11, 6, 12),
        ('Vapor Thrust', 'Special','Invincible reversal that reaches behind the head. Ky\'s Dragon Punch.' ,11, 4,43, -33),
        ('Vapor Thrust (H)', 'Special', 'Invincible reversal, a bit slower but with more active frames. Ky\'s Dragon Punch.' ,13, 8, 44, -38),
        ('Dire Eclat', 'Special', 'Main combo ender. Grants hard knockdown.' ,14, 3, 25, -6),

        ('Ride the Lightning', 'Overdrive', 'Powerful, fast attack that grants a wall-break.' ,9, 20, 99, -82),
        ('Sacred Edge', 'Overdrive', 'Large and fast moving projectile.' ,7, 0, 38, 10),
        ('Dragon Install', 'Overdrive', 'A transformation secret that charges all of Ky\'s moves. Can only be used when Ky is at low hp, and is considered to be a comeback mechanic.' ,12, 5, 25, 4)
    ]

    for move_name, move_type, description, startup, active, recovery, on_block in kyle_moves:
        move_id = add_moves(connection, character_id, move_name, move_type, description)
        frame_data_id = add_frame_data(connection, move_id, startup, active, recovery, on_block)


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS moves (
        id INTEGER PRIMARY KEY,
        character_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        move_type TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (character_id) REFERENCES characters (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS frame_data (
        id INTEGER PRIMARY KEY,
        move_id INTEGER NOT NULL,
        startup INTEGER NOT NULL,
        active INTEGER NOT NULL,
        recovery INTEGER NOT NULL,
        on_block INTEGER NOT NULL,
        FOREIGN KEY (move_id) REFERENCES moves (id)
    )
    """)

    connection.commit()


def main():
    # Connect to the SQLite database
    connection = sqlite3.connect("guilty_gear_data.db")
    create_tables(connection)
    
    addBadguy(connection)
    addKyle(connection)

    # Close the connection
    connection.close()
