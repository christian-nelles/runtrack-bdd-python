import mysql.connector
import pwinput

class Zoo:
    def __init__(self):
        self.user_password = pwinput.pwinput("Entrez votre mot de passe : ")
        if self.user_password:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=self.user_password,
                database="zoo"
            )
            self.cursor = self.conn.cursor()
        else:
            self.conn = None
            self.cursor = None
            print("Connexion refusée.")

    def ajouter_cage(self, superficie, capacite_max):
        if self.conn:
            query = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
            self.cursor.execute(query, (superficie, capacite_max))
            self.conn.commit()
            print("Cage ajoutée.")

    def supprimer_cage(self, cage_id):
        if self.conn:
            query = "DELETE FROM cage WHERE id = %s"
            self.cursor.execute(query, (cage_id,))
            self.conn.commit()
            print("Cage supprimée.")

    def ajouter_animal(self, nom, race, id_cage, date_naissance, pays_origine):
        if self.conn:
            query = "INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (nom, race, id_cage, date_naissance, pays_origine))
            self.conn.commit()
            print("Animal ajouté.")

    def modifier_cage_animal(self, animal_id, new_cage_id):
        if self.conn:
            query = "UPDATE animal SET id_cage = %s WHERE id = %s"
            self.cursor.execute(query, (new_cage_id, animal_id))
            self.conn.commit()
            print("Cage de l'animal modifiée.")

    def supprimer_animal(self, animal_id):
        if self.conn:
            query = "DELETE FROM animal WHERE id = %s"
            self.cursor.execute(query, (animal_id,))
            self.conn.commit()
            print("Animal supprimé.")

    def afficher_animaux(self):
        if self.conn:
            self.cursor.execute("SELECT * FROM animal")
            for row in self.cursor.fetchall():
                print(row)

    def afficher_animaux_dans_cages(self):
        if self.conn:
            query = """
                SELECT animal.nom, animal.race, cage.id, cage.superficie
                FROM animal 
                LEFT JOIN cage ON animal.id_cage = cage.id;
            """
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                print(f"{row[0]} ({row[1]}) - Cage {row[2]}, Superficie: {row[3]} m²")

    def calcul_superficie_totale(self):
        if self.conn:
            self.cursor.execute("SELECT SUM(superficie) FROM cage")
            result = self.cursor.fetchone()[0]
            print(f"La superficie totale du zoo est de {result} m².")

    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    zoo = Zoo()
    
    while True:
        print("\n📌 MENU DU ZOO 📌")
        print("1 Ajouter une cage")
        print("2 Supprimer une cage")
        print("3 Ajouter un animal")
        print("4 Modifier la cage d’un animal")
        print("5 Supprimer un animal")
        print("6 Afficher tous les animaux")
        print("7 Afficher les animaux et leurs cages")
        print("8 Calculer la superficie totale des cages")
        print("9 Quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            superficie = float(input("Superficie : "))
            capacite_max = int(input("Capacité max : "))
            zoo.ajouter_cage(superficie, capacite_max)

        elif choix == "2":
            cage_id = int(input("ID de la cage à supprimer : "))
            zoo.supprimer_cage(cage_id)

        elif choix == "3":
            nom = input("Nom de l'animal : ")
            race = input("Race : ")
            id_cage = input("ID de la cage (laisser vide si pas de cage) : ")
            id_cage = int(id_cage) if id_cage else None
            date_naissance = input("Date de naissance (AAAA-MM-JJ) : ")
            pays_origine = input("Pays d’origine : ")
            zoo.ajouter_animal(nom, race, id_cage, date_naissance, pays_origine)

        elif choix == "4":
            animal_id = int(input("ID de l'animal : "))
            new_cage_id = int(input("Nouvelle cage : "))
            zoo.modifier_cage_animal(animal_id, new_cage_id)

        elif choix == "5":
            animal_id = int(input("ID de l'animal à supprimer : "))
            zoo.supprimer_animal(animal_id)

        elif choix == "6":
            zoo.afficher_animaux()

        elif choix == "7":
            zoo.afficher_animaux_dans_cages()

        elif choix == "8":
            zoo.calcul_superficie_totale()

        elif choix == "9":
            zoo.close_connection()
            break

        else:
            print("Option invalide.")
