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
        
query = "SELECT * FROM etudiant;"
cursor.execute(query)

etudiants = cursor.fetchall()
print("Liste des étudiants :")
for etudiant in etudiants:
    print(etudiant)

if conn and conn.is_connected():
    cursor.close()
    conn.close()