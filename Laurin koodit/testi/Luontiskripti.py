# 1. Luo uusi tietokanta
CREATE DATABASE ohjelmistopeli;
USE ohjelmistopeli;

# 2. Tuo flight_game-data (airport + country)
SOURCE C:\o1\lp1.sql;

# 3. Poista flight_gamein vanhat taulut, joita ei tarvita
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS goal_reached;
SET FOREIGN_KEY_CHECKS = 1;

# 4. Luo uusi game-taulu
CREATE TABLE game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    screen_name VARCHAR(40) NOT NULL UNIQUE,
    location VARCHAR(40) NOT NULL,
    co2_consumed FLOAT DEFAULT 0,
    co2_budget FLOAT DEFAULT 5000,
    current_item INT DEFAULT 0,
    attempts INT DEFAULT 0,
    difficulty VARCHAR(40) NOT NULL
) CHARSET=latin1;

# 5. Luo uusi item-taulu
CREATE TABLE item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nimi VARCHAR(100),
    iso_country VARCHAR(40),
    vihje1 VARCHAR(255),
    vihje2 VARCHAR(255),
    vihje3 VARCHAR(255),
    CONSTRAINT fk_item_country FOREIGN KEY (iso_country)
        REFERENCES country(iso_country)
) CHARSET=latin1;

# 6. Lisää esineet
INSERT INTO item (nimi, iso_country, vihje1, vihje2, vihje3) VALUES
('Kultainen teelusikka', 'SE',
 'Kultainen teelusikka sijaitsee maassa, joka tunnetaan kolmesta kruunusta.',
 'Kultainen teelusikka sijaitsee maassa, jossa on paremmat lihapullat.',
 'Kultainen teelusikka sijaitsee maassa, jossa juhlitaan keskikesän juhlaa.'),

('Taskukello', 'IT',
 'Taskukello sijaitsee maassa, jossa Egyptin prinssi syntyi.',
 'Taskukello sijaitsee maassa, joka tunnetaan eräästä diktaattorista.',
 'Taskukello sijaitsee maassa, jossa syödään pizzaa ja pastaa.'),

('Kaulakoru', 'GB',
 'Kaulakoru sijaitsee maassa, jossa sinua tarkkaillaan jatkuvasti.',
 'Kaulakoru sijaitsee maassa, jossa sää on yleensä kamala.',
 'Kaulakoru sijaitsee maassa, jossa juodaan paljon teetä.'),

('Nahkahanskat', 'FR',
 'Nahkahanskat sijaitsevat maassa, jossa ilma savuaa.',
 'Nahkahanskat sijaitsevat maassa, johon kaikki haluavat matkustaa, mutta eivät pidä paikallisista.',
 'Nahkahanskat sijaitsevat maassa, jossa patonki ja croissantit ovat iso juttu.'),

('Kirje', 'RO',
 'Kirje sijaitsee maassa, jossa jokainen ajaa vanhalla mersulla.',
 'Kirje sijaitsee maassa, joka on hyvin köyhä.',
 'Kirje sijaitsee maassa, mistä Dracula on kotoisin.');

# 7. Luo game_items-taulu
CREATE TABLE game_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    item_id INT NOT NULL,
    CONSTRAINT fk_gameitems_game FOREIGN KEY (game_id) REFERENCES game(id),
    CONSTRAINT fk_gameitems_item FOREIGN KEY (item_id) REFERENCES item(id),
    CONSTRAINT unique_game_item UNIQUE (game_id, item_id)
) CHARSET=latin1;

