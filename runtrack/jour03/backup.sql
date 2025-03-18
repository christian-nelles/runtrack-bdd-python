-- 1. Création de la base de données
CREATE DATABASE IF NOT EXISTS store;
USE store;

-- 2. Création de la table category
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- 3. Création de la table product
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    quantity INT NOT NULL,
    id_category INT,
    FOREIGN KEY (id_category) REFERENCES category(id) ON DELETE SET NULL
);

-- 4. Insertion de quelques catégories
INSERT INTO category (name) VALUES
('Électronique'),
('Vêtements'),
('Alimentation');

-- 5. Insertion de quelques produits
INSERT INTO product (name, description, price, quantity, id_category) VALUES
('Ordinateur portable', 'PC puissant avec 16 Go RAM', 1200, 10, 1),
('T-shirt noir', '100% coton, taille M', 20, 50, 2),
('Chocolat', 'Tablette de chocolat noir 70%', 3, 100, 3);
