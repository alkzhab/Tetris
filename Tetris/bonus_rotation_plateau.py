from fltk import *
from random import randrange
from time import time
from datetime import datetime
import os


###################DIMENSION###########################################
largeur_jeu_bonus_rotation = 400
hauteur_jeu_bonus_rotation = 800
colonne_jeu_bonus_rotation = 12
ligne_jeu_bonus_rotation = 24

largeur_jeu_bonus_rotation2 = 800
hauteur_jeu_bonus_rotation2 = 400
colonne_jeu_bonus_rotation2 = 24
ligne_jeu_bonus_rotation2 = 12
#######################################################################

##################TAILLE D'UN BLOC####################################
largeur_bloc_bonus_rotation2 = largeur_jeu_bonus_rotation2 / colonne_jeu_bonus_rotation2
hauteur_bloc_bonus_rotation2 = hauteur_jeu_bonus_rotation2 / ligne_jeu_bonus_rotation2

largeur_bloc_bonus_rotation = largeur_jeu_bonus_rotation / colonne_jeu_bonus_rotation
hauteur_bloc_bonus_rotation = hauteur_jeu_bonus_rotation / ligne_jeu_bonus_rotation
######################################################################


####################DESSINER LA PIECE###############################
def dessiner_piece_bonus_rotation(piece, x, y):
    couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
    for i in range(len(piece)):
        for j in range(len(piece[i])):       # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:             # Si il rencontre un 1 alors
                x1 = (x + j) * largeur_bloc_bonus_rotation  # On définis les coordonnées en fonction de la taille d'un bloc
                y1 = (y + i) * hauteur_bloc_bonus_rotation
                x2 = x1 + largeur_bloc_bonus_rotation
                y2 = y1 + hauteur_bloc_bonus_rotation
                rectangle(x1, y1, x2, y2, remplissage=couleurs[piece[i][j]])  # Dessine un rectangle pour représenter un bloc
###################################################################


####################DESSINER LA PIECE###############################
def dessiner_piece_bonus_rotation2(piece, x, y):
    couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
    for i in range(len(piece)):
        for j in range(len(piece[i])):       # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:             # Si il rencontre un 1 alors
                x1 = (x + j) * largeur_bloc_bonus_rotation2  # On définis les coordonnées en fonction de la taille d'un bloc
                y1 = (y + i) * hauteur_bloc_bonus_rotation2
                x2 = x1 + largeur_bloc_bonus_rotation2
                y2 = y1 + hauteur_bloc_bonus_rotation2
                rectangle(x1, y1, x2, y2, remplissage=couleurs[piece[i][j]])  # Dessine un rectangle pour représenter un bloc
###################################################################

##################CONTACT AVEC LE SOL OU UN BLOC###################
def contact_bonus_rotation(piece, x, y, matrice_jeu):
    for i in range(len(piece)):
        for j in range(len(piece[i])):        # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:              
                x2 = x + j
                y2 = y + i
                
                if x2 < 0 or x2 >= colonne_jeu_bonus_rotation or y2 >= ligne_jeu_bonus_rotation or (y2 >= 0 and matrice_jeu[y2][x2] != 0):   # Regarde si le bloc ne dépasse pas la fenetre
                    return True
    return False
######################################################################

##################CONTACT AVEC LE SOL OU UN BLOC###################
def contact_bonus_rotation2(piece, x, y, matrice_jeu):
    for i in range(len(piece)):
        for j in range(len(piece[i])):        # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:              
                x2 = x + j
                y2 = y + i
                
                if x2 < 0 or x2 >= colonne_jeu_bonus_rotation2 or y2 >= ligne_jeu_bonus_rotation2 or (y2 >= 0 and matrice_jeu[y2][x2] != 0):   # Regarde si le bloc ne dépasse pas la fenetre
                    return True
    return False
######################################################################

###################MATRICE DU JEU#########################################
def dessiner_matrice_jeu_bonus_rotation(matrice, score, niveau, piece, x, y):
    liste_couleur=[0, "midnightblue", "navy", "midnightblue", "navy", "midnightblue"]
    rectangle(0,0,400,800, remplissage=liste_couleur[niveau])
    texte(280, 10, "Score :", taille=18)
    texte(360, 10, score, taille=18)
    texte(10, 10, "Niveau :", taille=18)
    texte(100, 10, niveau, taille=18)
    
    for i in range(ligne_jeu_bonus_rotation):                   
        for j in range(colonne_jeu_bonus_rotation):             # Parcours la matrice du jeu
            for k in range(1,19):
                if matrice[i][j] == k:
                    toutes_couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
                    couleur_bloc = toutes_couleurs[k]
                    x1 = j * largeur_bloc_bonus_rotation        # Coordonnées en fonction de la taille d'un bloc
                    y1 = i * hauteur_bloc_bonus_rotation
                    x2 = (j+1) * largeur_bloc_bonus_rotation
                    y2 = (i+1) * hauteur_bloc_bonus_rotation
                    rectangle(x1, y1, x2, y2, remplissage=couleur_bloc) # Dessine la piece ce qui permet d'enregistrer les pieces en continue

############################################################################

####################ROTATION DE LA PIECE###############################
def rotation(piece):
    rotation = []
    
    for j in range(len(piece[0])):  # Parcours les colonnes de la matrice
        ligne = []                  
        for i in range(len(piece) - 1, -1, -1):       # Parcours les lignes à l'envers
            ligne.append(piece[i][j])                 # Ajoute la colonne dans ligne
        rotation.append(ligne)                        # Ajoute la ligne dans la nouvelle liste
    return rotation
########################################################################


###################MATRICE DU JEU#########################################
def dessiner_matrice_jeu_bonus_rotation2(matrice, score, niveau, piece, x, y):
    liste_couleur=[0, "midnightblue", "navy", "midnightblue", "navy", "midnightblue"]
    rectangle(0,0,800,400, remplissage=liste_couleur[niveau])
    texte(680, 10, "Score :", taille=18)
    texte(760, 10, score, taille=18)
    texte(10, 10, "Niveau :", taille=18)
    texte(100, 10, niveau, taille=18)
    
    for i in range(ligne_jeu_bonus_rotation2):                   
        for j in range(colonne_jeu_bonus_rotation2):             # Parcours la matrice du jeu
            for k in range(1,19):
                if matrice[i][j] == k:
                    toutes_couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
                    couleur_bloc = toutes_couleurs[k]
                    x1 = j * largeur_bloc_bonus_rotation2         # Coordonnées en fonction de la taille d'un bloc
                    y1 = i * hauteur_bloc_bonus_rotation2
                    x2 = (j+1) * largeur_bloc_bonus_rotation2
                    y2 = (i+1) * hauteur_bloc_bonus_rotation2
                    rectangle(x1, y1, x2, y2, remplissage=couleur_bloc) # Dessine la piece ce qui permet d'enregistrer les pieces en continue

############################################################################

###########################CLAVIER########################################
def touche_jeu_bonus_rotation(piece, x, y, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute):
    
    if touche_pressee('Right') and temps - chrono_droitegauche >= 0.1 :        # Si la fleche droite est préssée et que le delay est repecté
            if not contact_bonus_rotation(piece, x + 1, y, matrice_jeu):
                x += 1
            chrono_droitegauche = time()
            
    if touche_pressee('Left') and temps - chrono_droitegauche >= 0.1 :         
            if not contact_bonus_rotation(piece, x - 1, y, matrice_jeu):
                x -= 1
            chrono_droitegauche = time()
           
    if touche_pressee('Up') and temps - chrono_rotation >= 0.2 :
            nouvelle_piece = rotation(piece)
            if not contact_bonus_rotation(nouvelle_piece, x, y, matrice_jeu):
                piece = nouvelle_piece
            
            else:
                if contact_bonus_rotation(nouvelle_piece , x+1, y, matrice_jeu):
                    x -= 1
                    if contact_bonus_rotation(nouvelle_piece , x, y, matrice_jeu):
                        x -= 1
                else :
                    if contact_bonus_rotation(nouvelle_piece , x-1, y, matrice_jeu):
                        x += 1
                        if contact_bonus_rotation(nouvelle_piece , x, y, matrice_jeu):
                            x += 1
                            
                while contact_bonus_rotation(nouvelle_piece , x, y, matrice_jeu):
                    y -= 1
                piece = nouvelle_piece
                
            chrono_rotation = time()
            
    if touche_pressee('Down'):
        if not contact_bonus_rotation(piece, x, y + 1, matrice_jeu):
            y += 1
       
    if touche_pressee('Escape'):
        ferme_fenetre()
                
    return piece, x, y, chrono_droitegauche, chrono_rotation, chrono_chute
##########################################################################

###########################CLAVIER########################################
def touche_jeu_bonus_rotation2(piece, x, y, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute):
    
    if touche_pressee('Right') and temps - chrono_droitegauche >= 0.1 :        # Si la fleche droite est préssée et que le delay est repecté
            if not contact_bonus_rotation2(piece, x + 1, y, matrice_jeu):
                x += 1
            chrono_droitegauche = time()
            
    if touche_pressee('Left') and temps - chrono_droitegauche >= 0.1 :         
            if not contact_bonus_rotation2(piece, x - 1, y, matrice_jeu):
                x -= 1
            chrono_droitegauche = time()
           
    if touche_pressee('Up') and temps - chrono_rotation >= 0.2 :
            nouvelle_piece = rotation(piece)
            if not contact_bonus_rotation2(nouvelle_piece, x, y, matrice_jeu):
                piece = nouvelle_piece
            
            else:
                if contact_bonus_rotation2(nouvelle_piece , x+1, y, matrice_jeu):
                    x -= 1
                    if contact_bonus_rotation2(nouvelle_piece , x, y, matrice_jeu):
                        x -= 1
                else :
                    if contact_bonus_rotation2(nouvelle_piece , x-1, y, matrice_jeu):
                        x += 1
                        if contact_bonus_rotation2(nouvelle_piece , x, y, matrice_jeu):
                            x += 1
                            
                while contact_bonus_rotation2(nouvelle_piece , x, y, matrice_jeu):
                    y -= 1
                piece = nouvelle_piece
                
            chrono_rotation = time()
            
    if touche_pressee('Down'):
        if not contact_bonus_rotation2(piece, x, y + 1, matrice_jeu):
            y += 1
       
    if touche_pressee('Escape'):
        ferme_fenetre()
                
    return piece, x, y, chrono_droitegauche, chrono_rotation, chrono_chute
##########################################################################

#######################Rotation matrice#####################################
def tourner_matrice_droite(matrice):
    
    lignes = len(matrice)
    colonnes = len(matrice[0])
    
    matrice_tournee = [[0] * lignes for _ in range(colonnes)]
    
    for i in range(lignes):
        for j in range(colonnes):
            matrice_tournee[j][lignes - 1 - i] = matrice[i][j]
    
    return matrice_tournee


def tourner_matrice_gauche(matrice):
    
    lignes = len(matrice)
    colonnes = len(matrice[0])
    
    matrice_tournee = [[0] * lignes for _ in range(colonnes)]
    
    for i in range(lignes):
        for j in range(colonnes):
            matrice_tournee[colonnes - 1 - j][i] = matrice[i][j]
    
    return matrice_tournee
###########################################################################

###################Faire chuter les pieces vers le bas#####################
def chutes_des_pieces(matrice):
    
    lignes = len(matrice)
    colonnes = len(matrice[0])
    
    
    for colonne in range(colonnes):
        
        elements = [matrice[ligne][colonne] for ligne in range(lignes) if matrice[ligne][colonne] != 0]
        

        for ligne in range(lignes):
            if ligne < lignes - len(elements):
                matrice[ligne][colonne] = 0
            else:
                matrice[ligne][colonne] = elements[ligne - (lignes - len(elements))]
    
    return matrice
##########################################################################

##################SUPPRESSION D'UNE LIGNE COMPLETE###########################
def sup_ligne_bonus_rotation(matrice_jeu):

    resultat= []
    lignes_effaces = 0

    for ligne in matrice_jeu:                    # Regarde les lignes de la matrice du jeu
        if all(bloc != 0 for bloc in ligne):     # Si tous les colonnes de la ligne sont à 1 alors
            lignes_effaces += 1                  # On ajoute 1
        else:                                    # Sinon
            resultat.append(ligne)               # On rajoute la ligne actuelle
            
    for i in range(lignes_effaces):              # En fonction de nombre de ligne qu'on a supprimé 
        resultat.insert(0, [0] * colonne_jeu_bonus_rotation2)    # En ajoute une ligne vide à l'endroit ou on a supprimé la ligne
            
    return lignes_effaces, resultat
##############################################################################
