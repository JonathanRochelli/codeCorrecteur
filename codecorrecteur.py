import numpy as np
from itertools import *
import math
from random import *
import binascii

def matriceH (l):
    matrice = []
    for y in product([0,1], repeat=l):
        res = int(''.join(map(str,y)),2)
        if (int(res) != 0 and len(str(math.log2(res))) != 3):
            matrice.append(list(y))

    M = np.array(matrice)
    return (np.append(np.transpose(M), np.array(np.eye(l) ,int),axis=1))


def matriceG (H, l):
    matrice = []
    for elt in H:
        matrice.append(list(elt[:pow(2,l)-l-1]))
    M = np.array(matrice)
    return (np.append(np.array(np.eye(len(M[0])) ,int), np.transpose(M) ,axis=1))

def encodage (matrice, mot):
    M = np.dot(mot,matrice)
    for i in range (np.size(M)):
        M[0][i] = M[0][i]%2
    return M

def bruitage (mot, l):
    rdm = randint(0,pow(2,l)-2)
    mot[0][rdm] = (mot[0][rdm]+1) %2
    return mot

def correction (matrice, mot, l):
    res = [elt for elt in range (len(mot))]
    M = np.dot(matrice,mot)
    for i in range (np.size(M)):
        M[i][0] = M[i][0]%2
    for i in range (len(M)):
        res = list(set(res).intersection([indice for indice, valeur in enumerate(matrice[i]) if M[i]==valeur]))
    if (len(res) >= 1):
        mot[res[0]] = (mot[res[0]]+1) %2
    return mot.T

def gen_mot (l):
    liste = []
    H = matriceH(l)
    G = matriceG(matriceH(l), l)
    for y in product([0,1], repeat=pow(2,l)-l-1):
        liste.append(y)
        encodage(G, [y])
    rdm = randint(0,len(liste)-1)
    return np.array([list(liste[rdm])])

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
print("Phrase décoder : ", mot_decode)
#print(binascii.unhexlify('%x' % int('0b' + mot_decode, 2)))



