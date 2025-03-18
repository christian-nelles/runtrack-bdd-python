import mysql.connector
import pwinput

def mdp():
    user_password = pwinput.pwinput("Entrez votre mot de passe : ")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=user_password,
        database="LaPlateforme"
    )
    cursor = conn.cursor()
    return conn, cursor
        
conn, cursor = mdp()
        
query = "SELECT SUM(capacite) FROM salle;"
cursor.execute(query)

capacite_totale = cursor.fetchone()[0]

print(f"La capacité totale des salles est de {capacite_totale} places.")

if conn and conn.is_connected():
    cursor.close()
    conn.close()