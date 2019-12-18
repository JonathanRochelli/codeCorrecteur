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
    return (np.append(np.array(np.eye(l) ,int), np.transpose(M),axis=1))


def matriceG (H, l):
    matrice = []
    for elt in H:
        matrice.append(list(elt[l:]))
    M = np.array(matrice)
    return (np.append(np.transpose(M), np.array(np.eye(len(M[0])) ,int),axis=1))

def encodage (matrice, mot):
    M = np.dot(mot,matrice)
    for i in range (np.size(M)):
        M[0][i] = M[0][i]%2

    print(M)
    return M

def bruitage (mot, l):
    rdm = randint(0,pow(2,l)-2)
    mot[0][rdm] = (mot[0][rdm]+1) %2
    return mot

def decodage (matrice, mot, l):
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
    

byte=b"101010"
var=byte.decode("utf-8")
print (var)

print("Starting...")

l=3
mot= gen_mot(l)

print("Mot :")
print(mot)

print("Matrice H:")
print(matriceH(l))

print("Matrice G:")
print(matriceG(matriceH(l), l))

print("Encodage de : ",mot)
mot_encode = encodage(matriceG(matriceH(l), l),mot)
print(mot_encode)

print("Bruitage de : ",mot_encode)
mot_altere = bruitage(mot_encode,l)
print(mot_altere)

print("Decodage de : ",mot_altere)
print(decodage(matriceH(l),mot_altere.T, l))


mot = '1011101100011000110011111010001110000111011011111';
mot_decode = ""
phrase = [mot[i:i+pow(2,l)-1] for i in range(0, len(mot), pow(2,l)-1)]
print(phrase)
for elt in phrase:
    liste = [list(elt)]
    for i in range (len(liste[0])):
        liste[0][i] = int(liste[0][i])
    print(np.array(liste).T)
    mot_decode += ''.join(map(str,decodage(matriceH(l),np.array(liste).T, l)[0]))
    print(decodage(matriceH(l),np.array(liste).T, l)[0])
    print(''.join(map(str,decodage(matriceH(l),np.array(liste).T, l)[0])))
print(mot_decode)
print(binascii.unhexlify('%x' % int('0b' + mot_decode, 2)))
1011101100011000110011111010001110000111011011111


