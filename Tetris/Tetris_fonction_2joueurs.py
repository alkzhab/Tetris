from fltk import *
from random import randrange
from time import time
from datetime import date

###################DIMENSION###########################################
largeur_jeu_2joueurs = 800
hauteur_jeu_2joueurs = 800
colonne_jeu_2joueurs = 24
ligne_jeu_2joueurs = 24
#######################################################################

##################TAILLE D'UN BLOC####################################
largeur_bloc_2joueurs = largeur_jeu_2joueurs / colonne_jeu_2joueurs
hauteur_bloc_2joueurs = hauteur_jeu_2joueurs / ligne_jeu_2joueurs
#######################################################################

##################Dessiner piece#######################################
def dessiner_piece_2joueurs(piece, x, y):
    couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
    for i in range(len(piece)):
        for j in range(len(piece[i])):   
            if piece[i][j] != 0:            
                x1 = (x + j) * largeur_bloc_2joueurs  
                y1 = (y + i) * hauteur_bloc_2joueurs
                x2 = x1 + largeur_bloc_2joueurs
                y2 = y1 + hauteur_bloc_2joueurs
                rectangle(x1, y1, x2, y2, remplissage=couleurs[piece[i][j]])
#######################################################################

##################CONTACT AVEC LE SOL OU UN BLOC###################
def contact1(piece1, x1, y1, matrice_jeu1):
    for i in range(len(piece1)):
        for j in range(len(piece1[i])):     
            if piece1[i][j] != 0:              
                x2 = x1 + j
                y2 = y1 + i
                
                if x2 < 0 or x2 >= 12 or y2 >= ligne_jeu_2joueurs or (y2 >= 0 and matrice_jeu1[y2][x2] != 0):
                    return True
    return False


def contact2(piece2, x2, y2, matrice_jeu_2joueurs):
    for i in range(len(piece2)):           
        for j in range(len(piece2[i])):     
            if piece2[i][j] != 0:            
                x3 = x2 + j                  
                y3 = y2 + i

                
                if x3 < 12 or x3 >= 24 or y3 >= ligne_jeu_2joueurs or (y3 >= 0 and matrice_jeu_2joueurs[y3][x3 - 12] != 0):
                    return True
    return False
#######################################################################

####################ROTATION DE LA PIECE###############################
def rotation(piece):
    rotation = []
    
    for j in range(len(piece[0])):  # Parcours les colonnes de la matrice
        ligne = []                  
        for i in range(len(piece) - 1, -1, -1):       # Parcours les lignes à l'envers
            ligne.append(piece[i][j])                 # Ajoute la colonne dans ligne
        rotation.append(ligne)                        # Ajoute la ligne dans la nouvelle liste
    return rotation
#######################################################################

################Dessiner matrice###########################
def dessiner_matrice_jeu_2joueurs(matrice1, matrice2, prochaine_piece1, prochaine_piece2):
    
    rectangle(0,0,400,800, remplissage="midnightblue")
    rectangle(400, 0, 800, 800, remplissage="seagreen")
    rectangle(800, 0, 1000, 400, remplissage="silver")
    rectangle(800, 400, 1000, 800, remplissage="dark grey")
    
    texte(840, 60, "Prochaine piece :" , taille=12)
    texte(860, 5, "Joueur 1", taille=16, couleur="midnightblue")
    
    texte(840, 460, "Prochaine piece :" , taille=12)
    texte(860, 405, "Joueur 2", taille=16, couleur="seagreen")
    
    dessiner_piece_2joueurs(prochaine_piece1, 25, 4)
    dessiner_piece_2joueurs(prochaine_piece2 , 25, 16)
    
    for i in range(ligne_jeu_2joueurs):                   
        for j in range(colonne_jeu_2joueurs//2): 
            for k in range (1,19):
                if matrice1[i][j] == k:               
                    couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
                    couleur_bloc = couleurs[k]
                    x1 = j * largeur_bloc_2joueurs            
                    y1 = i * hauteur_bloc_2joueurs
                    x2 = (j+1) * largeur_bloc_2joueurs
                    y2 = (i+1) * hauteur_bloc_2joueurs
                    rectangle(x1, y1, x2, y2, remplissage=couleur_bloc) 
                          
    
    for i in range(ligne_jeu_2joueurs):                   
        for j in range(colonne_jeu_2joueurs//2):       
            for k in range (1,19):
                if matrice2[i][j] == k:             
                    couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
                    couleur_bloc = couleurs[k]
                    x1 = 400 + j * largeur_bloc_2joueurs          
                    y1 = i * hauteur_bloc_2joueurs
                    x2 = 400 + (j+1) * largeur_bloc_2joueurs
                    y2 = (i+1) * hauteur_bloc_2joueurs
                    rectangle(x1, y1, x2, y2, remplissage=couleur_bloc) 
           
###########################################################################

###########################CLAVIER########################################
def touche_jeu1(piece1, x1, y1, matrice_jeu, temps, chrono_droitegauche1, chrono_rotation1, chrono_chute1):
    
    if touche_pressee('d') and temps - chrono_droitegauche1 >= 0.1 :        
            if not contact1(piece1, x1 + 1, y1, matrice_jeu):
                x1 += 1
            chrono_droitegauche1 = time()
            
    if touche_pressee('q') and temps - chrono_droitegauche1 >= 0.1 :         
            if not contact1(piece1, x1 - 1, y1, matrice_jeu):
                x1 -= 1
            chrono_droitegauche1 = time()
           
    if touche_pressee('z') and temps - chrono_rotation1 >= 0.2 :
            nouvelle_piece = rotation(piece1)
            if not contact1(nouvelle_piece, x1, y1, matrice_jeu):
                piece1 = nouvelle_piece
            
            else:
                if contact1(nouvelle_piece , x1+1, y1, matrice_jeu):
                    x1 -= 1
                    if contact1(nouvelle_piece , x1, y1, matrice_jeu):
                        x1 -= 1
                else :
                    if contact1(nouvelle_piece , x1-1, y1, matrice_jeu):
                        x1 += 1
                        if contact1(nouvelle_piece , x1, y1, matrice_jeu):
                            x1 += 1
                            
                while contact1(nouvelle_piece , x1, y1, matrice_jeu):
                    y1 -= 1
                piece1 = nouvelle_piece
                
            chrono_rotation1 = time()
            
    if touche_pressee('s'):
        if not contact1(piece1, x1, y1 + 1, matrice_jeu):
            y1 += 1
       
    if touche_pressee('Escape'):
        ferme_fenetre()
                
    return piece1, x1, y1, chrono_droitegauche1, chrono_rotation1, chrono_chute1
#######################################################################

########################Clavier du deuxième joueur#################################
def touche_jeu2(piece2, x2, y2, matrice_jeu, temps, chrono_droitegauche2, chrono_rotation2, chrono_chute2):
    
    if touche_pressee('Right') and temps - chrono_droitegauche2 >= 0.1 :        # Si la fleche droite est préssée et que le delay est repecté
            if not contact2(piece2, x2 + 1, y2, matrice_jeu):
                x2 += 1
            chrono_droitegauche2 = time()
            
    if touche_pressee('Left') and temps - chrono_droitegauche2 >= 0.1 :         
            if not contact2(piece2, x2 - 1, y2, matrice_jeu):
                x2 -= 1
            chrono_droitegauche2 = time()
           
    if touche_pressee('Up') and temps - chrono_rotation2 >= 0.2 :
            nouvelle_piece = rotation(piece2)
            if not contact2(nouvelle_piece, x2, y2, matrice_jeu):
                piece2 = nouvelle_piece
            
            else:
                if contact2(nouvelle_piece , x2+1, y2, matrice_jeu):
                    x2 -= 1
                    if contact2(nouvelle_piece , x2, y2, matrice_jeu):
                        x2 -= 1
                else :
                    if contact2(nouvelle_piece , x2-1, y2, matrice_jeu):
                        x2 += 1
                        if contact2(nouvelle_piece , x2, y2, matrice_jeu):
                            x2 += 1
                            
                while contact2(nouvelle_piece , x2, y2, matrice_jeu):
                    y2 -= 1
                piece2 = nouvelle_piece
                
            chrono_rotation2= time()
            
    if touche_pressee('Down'):
        if not contact2(piece2, x2, y2 + 1, matrice_jeu):
            y2 += 1
                
    return piece2, x2, y2, chrono_droitegauche2, chrono_rotation2, chrono_chute2
#######################################################################

#####################Supprimer ligne compléte########################### 
def supprimer_ligne1(matrice_jeu):
     resultat= []
     lignes_effaces = 0

     for ligne in matrice_jeu :
         if all(bloc != 0 for bloc in ligne):     
             lignes_effaces += 1                  
         else:                                  
             resultat.append(ligne)              
             
     for i in range(lignes_effaces):      
         resultat.insert(0, [0] * (colonne_jeu_2joueurs//2))  
             
     return resultat, lignes_effaces
###################################################################
        


