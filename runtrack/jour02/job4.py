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
        
query = "SELECT nom, capacite FROM salle;"
cursor.execute(query)
            
l = []
salles = cursor.fetchall()
for salle in salles:
    l.append((salle[0], salle[1]))
print(l)

if conn and conn.is_connected():
    cursor.close()
    conn.close()