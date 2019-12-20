import numpy as np
from itertools import *
import math
from random import *

#Fonction permettant de générer une matrice H en sachant l
def matriceH (l):
    matrice = []
    #Pour chaque combinaisons
    for y in product([0,1], repeat=l):
	#Convertion en int
        res = int(''.join(map(str,y)),2)
	#Si ce n'est pas 0 et que ce n'est pas une puissance valide
        if (int(res) != 0 and len(str(math.log2(res))) != 3):
	    #Ajout dans la matrice
            matrice.append(list(y))
    #Conversion en matrice
    M = np.array(matrice)
    #Renvoie la matrice + la matrice identité
    return (np.append(np.transpose(M), np.array(np.eye(l) ,int),axis=1))

#Fonction permettant de générer une matrice G en sachant l et H
def matriceG (H, l):
    matrice = []
    #Pour chaques élements de H
    for elt in H:
	#Sélection de la partie sans l'identité
        matrice.append(list(elt[:pow(2,l)-l-1]))
    #Conversion en matrice
    M = np.array(matrice)
    #Renvoie la matrice identité + la matrice
    return (np.append(np.array(np.eye(len(M[0])) ,int), np.transpose(M) ,axis=1))

#Fonction qui encode un mot en connaissent G et le mot
def encodage (matrice, mot):
    #Multiplication de matrice
    M = np.dot(mot,matrice)
    #Conversion de chaque élement dans F2
    for i in range (np.size(M)):
        M[0][i] = M[0][i]%2
    return M

#Fonction qui altère au hasard un bit du mot 
def bruitage (mot, l):
    #Sélection de l'indice au hasard
    rdm = randint(0,pow(2,l)-2)
    #Changement de bit
    mot[0][rdm] = (mot[0][rdm]+1) %2
    return mot

#Fonction qui corrige un mot par syndrome
def correction (matrice, mot, l):
    #Sélection de toutes les colonnes de H
    res = [elt for elt in range (len(mot))]
    #Mutiplication de la matrice H et du mot à corriger
    M = np.dot(matrice,mot)
    #Conversion de chaques élements dans F2
    for i in range (np.size(M)):
        M[i][0] = M[i][0]%2
    #Recherche de la colonne de H qui convient
    #Recherche pour chaque ligne l'indice de l'élement
    #Réalisation de l'intersection avec le tableau précédent
    #Le résultat qui reste est l'indice de la colonne à corriger
    for i in range (len(M)):
        res = list(set(res).intersection([indice for indice, valeur in enumerate(matrice[i]) if M[i]==valeur]))
    #Si il y a une erreur
    if (len(res) >= 1):
        #Echange de bit
        mot[res[0]] = (mot[res[0]]+1) %2
    return mot.T

#Fonction qui génére tous les mots possibles du code
def gen_mot (l):
    liste = []
    H = matriceH(l)
    G = matriceG(matriceH(l), l)
    for y in product([0,1], repeat=pow(2,l)-l-1):
        liste.append(y)
        encodage(G, [y])
    rdm = randint(0,len(liste)-1)
    return np.array([list(liste[rdm])])

#Fonction qui découpe un phrase selon la l donné
def Hachage (phrase, l):
    return [phrase[i:i+pow(2,l)-1] for i in range(0, len(phrase), pow(2,l)-1)]


print("\n")   
print("//////////////// Exemple avec un l choisi ////////////////")
print("\n")

#Saisi utilisateur pour la valeur de l
l = int(input("Entrer la valeur de l : "))
#Génération d'un mot du code pour un l donné
mot= gen_mot(l)
print("\n")
print("Génération du mot : ",mot)

print("\n")
print("Matrice H : ")
print("\n")
#Génération de la matrice H pour un l donné
print(matriceH(l))

print("\n")
print("Matrice G : ")
print("\n")
#Génération de la matrice H pour un l donné et une matrice H
print(matriceG(matriceH(l), l))

print("\n")
print("Encodage de : ",mot)
#Encodage du mot généré un peu plus haut grâce à la matrice G
mot_encode = encodage(matriceG(matriceH(l), l),mot)
print("\n")
print(mot_encode)

print("\n")
print("Bruitage de : ",mot_encode)
#Bruitage du mot encodé précedement pour un l donné
mot_altere = bruitage(mot_encode,l)
print("\n")
print(mot_altere)

print("\n")
print("Correction du mot : ",mot_altere)
print("\n")
#Décodage du mot encodé et altéré => Le résultat doit être le mote donné précedement
print(correction(matriceH(l),mot_altere.T, l))
print("\n")
print("Mot decodé : ", correction(matriceH(l),mot_altere.T, l)[0][:4])
print("\n")

print("//////////////// Exemple avec 'un mot à decoder' ////////////////")
print("\n")
l = 3
#Phrase donnée dans le fichier d'exemple de IRIS
phrase = '1011101100011000110011111010001110000111011011111'
print("Un mot à decoder : ", phrase)
print("\n")
mot_decode = ""
mots = Hachage(phrase, l)
for elt in mots:
    liste = [list(elt)]
    for i in range (len(liste[0])):
        liste[0][i] = int(liste[0][i])
    mot_decode += ''.join(map(str,correction(matriceH(l),np.array(liste).T, l)[0]))[:4]
print("Phrase décoder : ", mot_decode,"\n")



