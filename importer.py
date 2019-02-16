# Créer une base de données Bar
# Créer une table boissons avec un ID, produit et catégorie
# importer le contenu complet du fichier csv dans votre table boissons
# Le programme n'importera qu'une seul fois ce fichier !
# Afficher un menu qui permettra ensuite :
# 1 - afficher la liste des bières ( catégorie 1)
# 2 - afficher le liste des soft ( catégorie 2)
# 3 - afficher la liste des boissons chaude ( catégorie 3)
# 4 - afficher le nombre de produits par catégorie
# 5 - quitter le programme

import sqlite3, csv
from sqlite3 import Error
dbName = 'bar'

def connexion(dbName):
    try:
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS boissons(id INTEGER PRIMARY KEY, nom TEXT, categorie INTEGER);")
        conn.commit()
        return conn, cursor
    except Error as e:
        print("Une erreur s'est produite: "+e)
        return False

def checkIfImported(dbName) :
    conn, cursor = connexion(dbName)
    try:
        cursor.execute("SELECT count(id) FROM boissons;")
        quantite = cursor.fetchone()
        if quantite[0] == 0:
            with open('Boissons.csv', 'r') as csvfile:
                boiss = csv.reader(csvfile, delimiter=';')
                bsns = []
                query = "INSERT INTO Boissons(nom, categorie) values (? , ?)"
                for row in boiss :
                    name, cat = row[0].split(',')
                    bsns.append([name, cat])
                cursor.executemany(query, bsns)
                conn.commit()
            return True
        else:
            return True
    except Error as e :
        print("Une erreur s'est produite: " + e)
    finally:
        conn.close()

def showByCat(dbName, cat):
    conn, cursor = connexion(dbName)
    try:
        cursor.execute("SELECT id, nom FROM Boissons WHERE categorie = ?;", (cat,))
        boissons = cursor.fetchall()
        for boisson in boissons:
            print(str(boisson[0])+" : "+boisson[1])
    except Error as e:
        print("Une erreur s'est produite: " + e)
    finally:
        conn.close()

def numberOfEach(dbName):
    conn, cursor = connexion(dbName)
    try:
        for cat in range(1,4):
            cursor.execute("SELECT COUNT(id) FROM Boissons WHERE categorie = ?;", (cat,))
            nb = cursor.fetchone()
            print("Il y a " + str(nb[0]) + " boissons dans la catégorie "+ str(cat))
    except Error as e:
        print("Une erreur s'est produite: " + e)
    finally:
        conn.close()


checkIfImported(dbName)
choice = 0
while choice != 5 :
    choice = input('''
                1 - afficher la liste des bières ( catégorie 1)
                2 - afficher le liste des soft ( catégorie 2)   
                3 - afficher la liste des boissons chaude ( catégorie 3)
                4 - afficher le nombre de produits par catégorie
                5 - quitter le programme
            ''')
    if choice == str(1):
        showByCat(dbName, 1)
    elif choice == str(2):
        showByCat(dbName, 2)
    elif choice == str(3):
        showByCat(dbName, 3)
    elif choice == str(4):
        numberOfEach(dbName)

