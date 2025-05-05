from fltk import *
from random import randrange
from time import time
from datetime import datetime
import os
import calendar
from Tetris_fonction_2joueurs import *
from bonus_rotation_plateau import *


###################Variable############################################
polyominos=4
#######################################################################

###################DIMENSION###########################################
largeur_jeu = 400
hauteur_jeu = 800
colonne_jeu = 12
ligne_jeu = 24
#######################################################################

##################TAILLE D'UN BLOC####################################
largeur_bloc = largeur_jeu / colonne_jeu
hauteur_bloc = hauteur_jeu / ligne_jeu
######################################################################

##################FENETRE############################################
def ecran():
    cree_fenetre(600, 800)
####################################################################

################PIECE###############################################   
def polyminos(fichier, n):
    """Charge les polyominos depuis un fichier texte."""
    pieces = []
    mot ='Taille'
    declenchement=0
    y=1
    try:
        with open(fichier, 'r') as file:
            c_piece = []
            for line in file:
                line = line.strip()
                if str(n) in line :
                    declenchement+=1
                    
                if declenchement==1:
                    if line == '':
                        if c_piece != []:
                            pieces.append(c_piece)
                            c_piece = []
                            y+=1
                            
                    elif line=='#' :
                        return pieces
                    
                    elif mot not in line:
                        c_piece.append([y if char == '+' else 0 for char in line])
            
            if c_piece:
                pieces.append(c_piece)
    except FileNotFoundError:
        print(f"Fichier {fichier} introuvable. Utilisation des pièces par défaut.")
#######################################################################
pieces = polyminos('piece.txt', polyominos)
#####################################################################
 
#####################CHOIX ALEATOIRE DES PIECES######################        
def choisir_piece():
    if polyominos == 1 or polyominos == 2:
        choix = pieces[0]
    elif polyominos == 3:
        hazard = randrange(0,2)
        choix = pieces[hazard]
    elif polyominos == 4:
        hazard = randrange(0,7)   # Choisis une chiffre entre 0 et 6
        choix = pieces[hazard]    # Avec le chiffre choisis, choisis dans la liste des pieces, la piece en question
    elif polyominos == 5:
        hazard = randrange(0,18)
        choix = pieces[hazard]
    return choix              # Renvoi la piece
#################################################################### 

####################DESSINER LA PIECE###############################
def dessiner_piece(piece, x, y, mode):
    if mode == 2:
        couleur_fond, couleur_des_blocs = personnalisation_interface_fond()
        couleurs=couleur_des_blocs
    else:
        couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
    for i in range(len(piece)):
        for j in range(len(piece[i])):       # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:             # Si il rencontre un 1 alors
                x1 = (x + j) * largeur_bloc  # On définis les coordonnées en fonction de la taille d'un bloc
                y1 = (y + i) * hauteur_bloc
                x2 = x1 + largeur_bloc
                y2 = y1 + hauteur_bloc
                rectangle(x1, y1, x2, y2, remplissage=couleurs[piece[i][j]])  # Dessine un rectangle pour représenter un bloc
###################################################################

##################CONTACT AVEC LE SOL OU UN BLOC###################
def contact(piece, x, y, matrice_jeu):
    for i in range(len(piece)):
        for j in range(len(piece[i])):        # Parcours la matrice de la piece choisis
            if piece[i][j] != 0:              
                x2 = x + j
                y2 = y + i
                
                if x2 < 0 or x2 >= colonne_jeu or y2 >= ligne_jeu or (y2 >= 0 and matrice_jeu[y2][x2] != 0):   # Regarde si le bloc ne dépasse pas la fenetre
                    return True
    return False
######################################################################

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
def dessiner_matrice_jeu(matrice, score, niveau, prochaine_piece, piece, x, y, mode):
    if mode ==2:
        couleur_fond, couleur_des_blocs = personnalisation_interface_fond()
        rectangle(0,0,400,800, remplissage=couleur_fond)
    else:
        liste_couleur=[0, "midnightblue", "navy", "midnightblue", "navy", "midnightblue"]
        rectangle(0,0,400,800, remplissage=liste_couleur[niveau])
    rectangle(400,0,600,250, remplissage='grey')                     # rectangle en haut à droite
    rectangle(400,240,600,800, remplissage='white')
    
    texte(420,350, "score :", couleur='blue', taille=18)
    texte(500, 350, score, couleur='blue', taille=18)
    texte(420, 400, "niveau :", couleur='blue', taille=18)
    texte(510, 400, niveau, couleur='blue', taille=18)
    texte(440, 20, "Prochaine piece :" , taille=12)
    
    dessiner_piece(prochaine_piece, 13.7, 2, mode)     # Dessine la prochaine piece en haut à droite
    
    for i in range(ligne_jeu):                   
        for j in range(colonne_jeu):             # Parcours la matrice du jeu
            for k in range(1,19):
                if matrice[i][j] == k:
                    if mode == 2:
                        toutes_couleurs = couleur_des_blocs
                    else:
                        toutes_couleurs=['black', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red', 'gold', 'lime', 'pink', 'brown', 'grey', 'white', 'teal', 'navy', 'maroon', 'magenta', 'olive']
                    couleur_bloc = toutes_couleurs[k]
                    x1 = j * largeur_bloc            # Coordonnées en fonction de la taille d'un bloc
                    y1 = i * hauteur_bloc
                    x2 = (j+1) * largeur_bloc
                    y2 = (i+1) * hauteur_bloc
                    rectangle(x1, y1, x2, y2, remplissage=couleur_bloc) # Dessine la piece ce qui permet d'enregistrer les pieces en continue
############################################################################

##################SUPPRESSION D'UNE LIGNE COMPLETE###########################
def sup_ligne(matrice_jeu):

    resultat= []
    lignes_effaces = 0

    for ligne in matrice_jeu:                    # Regarde les lignes de la matrice du jeu
        if all(bloc != 0 for bloc in ligne):     # Si tous les colonnes de la ligne sont à 1 alors
            lignes_effaces += 1                  # On ajoute 1
        else:                                    # Sinon
            resultat.append(ligne)               # On rajoute la ligne actuelle
            
    for i in range(lignes_effaces):              # En fonction de nombre de ligne qu'on a supprimé 
        resultat.insert(0, [0] * colonne_jeu)    # En ajoute une ligne vide à l'endroit ou on a supprimé la ligne
            
    return lignes_effaces, resultat
##############################################################################

###########################CLAVIER########################################
def touche_jeu(piece, x, y, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute, mode):
    
    if mode == 2:
        touche_gauche, touche_droite, touche_rotation, touche_chute = personnalisation_touche()
    else:
        touche_gauche, touche_droite, touche_rotation, touche_chute = "Left", "Right", "Up", "Down"
    
    if touche_pressee(touche_droite) and temps - chrono_droitegauche >= 0.1 :        # Si la fleche droite est préssée et que le delay est repecté
            if not contact(piece, x + 1, y, matrice_jeu):
                x += 1
            chrono_droitegauche = time()
            
    if touche_pressee(touche_gauche) and temps - chrono_droitegauche >= 0.1 :         
            if not contact(piece, x - 1, y, matrice_jeu):
                x -= 1
            chrono_droitegauche = time()
           
    if touche_pressee(touche_rotation) and temps - chrono_rotation >= 0.2 :
            nouvelle_piece = rotation(piece)
            if not contact(nouvelle_piece, x, y, matrice_jeu):
                piece = nouvelle_piece
            
            else:
                if contact(nouvelle_piece , x+1, y, matrice_jeu):
                    x -= 1
                    if contact(nouvelle_piece , x, y, matrice_jeu):
                        x -= 1
                else :
                    if contact(nouvelle_piece , x-1, y, matrice_jeu):
                        x += 1
                        if contact(nouvelle_piece , x, y, matrice_jeu):
                            x += 1
                            
                while contact(nouvelle_piece , x, y, matrice_jeu):
                    y -= 1
                piece = nouvelle_piece
                
            chrono_rotation = time()
            
    if touche_pressee(touche_chute):
        if not contact(piece, x, y + 1, matrice_jeu):
            y += 1
       
    if touche_pressee('Escape'):
        ferme_fenetre()
                
    return piece, x, y, chrono_droitegauche, chrono_rotation, chrono_chute
##########################################################################

############################SCORE#########################################
def systeme_point(ligne_sup, score, niveau):
    
    multiplicateur = 1 + ((niveau - 1) * 0.5)
    
    if ligne_sup == 1:
        score += 40 * multiplicateur
   
    elif ligne_sup == 2:
        score += 100 * multiplicateur
        
    elif ligne_sup == 3:
        score += 300 * multiplicateur
    
    elif ligne_sup == 4:
        score += 500 * multiplicateur
        
    return int(score)
#####################################################################

#########################NIVEAU DE DIFFICULTE########################
def niveau_difficulte(ligne_sup_total, difficulte, niveau):
    if ligne_sup_total >= 10 and niveau == 1:
        difficulte -= 0.2
        niveau += 1
        
    elif ligne_sup_total >= 20 and niveau == 2:
        difficulte -= 0.2
        niveau += 1
        
    elif ligne_sup_total >= 30 and niveau == 3:
        difficulte -= 0.2
        niveau += 1
        
    elif ligne_sup_total >= 40 and niveau == 4:
        difficulte -= 0.2
        niveau += 1
        
    return difficulte, niveau
###################################################################   

#####################MENU PRINCIPAL#######################################
def menu_principal():
    redimensionne_fenetre(600, 800)
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(145,195,455,305, remplissage='black')
    rectangle(150,200,450,300, remplissage='grey')
    
    rectangle(145,345,455,455, remplissage='black')
    rectangle(150,350,450,450, remplissage='grey')

    rectangle(145,495,455,605, remplissage='black')
    rectangle(150,500,450,600, remplissage='grey')
    
    rectangle(145,645,455,755, remplissage='black')
    rectangle(150,650,450,750, remplissage='grey')
    
    texte(90,60, "TETRIS", "red", taille=90)
    
    texte(235,230, 'Jouer' , 'Yellow', taille=40)
    texte(185,380, '2 Joueurs', "Yellow", taille=40)
    texte(165,535, 'Pourrissement' , 'Yellow', taille=32)
    texte(225,680, 'Bonus' , 'Yellow', taille=40)

    
    sauvegarde_correcte = False
    sauvegarde_2joueurs_correcte = False
    sauvegarde_variante_correcte = False
    sauvegardes = [0,"sauvegardes/sauvegarde1","sauvegardes/sauvegarde2", "sauvegardes/sauvegarde3", "sauvegardes/sauvegarde4", "sauvegardes/sauvegarde5"]
    sauvegardes_2joueurs = [0,"sauvegardes/sauvegarde_2joueurs1","sauvegardes/sauvegarde_2joueurs2", "sauvegardes/sauvegarde_2joueurs3", "sauvegardes/sauvegarde_2joueurs4", "sauvegardes/sauvegarde_2joueurs5"]
    sauvegardes_variante = [0,"sauvegardes/sauvegarde_variante1","sauvegardes/sauvegarde_variante2", "sauvegardes/sauvegarde_variante3", "sauvegardes/sauvegarde_variante4", "sauvegardes/sauvegarde_variante5"]
    
    if os.path.exists(sauvegardes[polyominos]):
        sauvegarde_correcte = True
    
    if os.path.exists(sauvegardes_2joueurs[polyominos]):
        sauvegarde_2joueurs_correcte = True
        
    if os.path.exists(sauvegardes_variante[polyominos]):
        sauvegarde_variante_correcte = True

    Pos=attend_clic_gauche()
    if  145<= Pos[0] <= 455 and 245<=Pos[1]<=355:
        if sauvegarde_correcte :
            menu_reprendre_sauvegarde(0, sauvegarde_correcte)
        else:
            jeu_principal(0, 0)
    
    elif 145<= Pos[0] <=455 and 395<=Pos[1]<=505:
        if sauvegarde_2joueurs_correcte :
            menu_reprendre_sauvegarde_2joueurs(sauvegarde_2joueurs_correcte)
        else:
            jeu_principal_2joueurs(sauvegarde_2joueurs_correcte)
            
    elif  145<= Pos[0] <= 455 and 495<=Pos[1]<=605:
        if sauvegarde_variante_correcte :
            menu_reprendre_sauvegarde(1, sauvegarde_variante_correcte)
        else:
            jeu_principal(1, 0)
            
    elif 145<= Pos[0] <=405 and 645<=Pos[1]<=755:
        menu_bonus()
    
    else:
        menu_principal()
##########################################################################

#####################MENU BONUS#######################################
def menu_bonus():
    redimensionne_fenetre(600, 800)
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(145,195,455,305, remplissage='black')
    rectangle(150,200,450,300, remplissage='grey')
    
    rectangle(145,345,455,455, remplissage='black')
    rectangle(150,350,450,450, remplissage='grey')

    rectangle(145,495,455,605, remplissage='black')
    rectangle(150,500,450,600, remplissage='grey')
    
    rectangle(145,645,455,755, remplissage='black')
    rectangle(150,650,450,750, remplissage='grey')
    
    texte(90,60, "TETRIS", "red", taille=90)
    
    texte(205,230, 'Rotation' , 'Yellow', taille=40)
    texte(205,380, 'Couleur', "Yellow", taille=40)
    texte(165,540, 'Personnalisation' , 'Yellow', taille=28)
    texte(225,680, 'Retour' , 'Yellow', taille=40)
    
    sauvegarde_bonus_rotation_correcte = False
    sauvegarde_mode_personnalisee_correcte = False
    sauvegarde_bonus_couleur_correcte = False
    sauvegardes_bonus_rotation = [0,"sauvegardes/sauvegarde_bonus_rotation1","sauvegardes/sauvegarde_bonus_rotation2", "sauvegardes/sauvegarde_bonus_rotation3", "sauvegardes/sauvegarde_bonus_rotation4", "sauvegardes/sauvegarde_bonus_rotation5"]
    sauvegardes_mode_personnalisee = [0,"sauvegardes/sauvegarde_mode_personnalisee1","sauvegardes/sauvegarde_mode_personnalisee2", "sauvegardes/sauvegarde_mode_personnalisee3", "sauvegardes/sauvegarde_mode_personnalisee4", "sauvegardes/sauvegarde_mode_personnalisee5"]
    sauvegardes_bonus_couleur = [0,"sauvegardes/sauvegarde_bonus_couleur1","sauvegardes/sauvegarde_bonus_couleur2", "sauvegardes/sauvegarde_bonus_couleur3", "sauvegardes/sauvegarde_bonus_couleur4", "sauvegardes/sauvegarde_bonus_couleur5"]
    
    
    if os.path.exists(sauvegardes_bonus_rotation[polyominos]):
        sauvegarde_bonus_rotation_correcte = True
        
    if os.path.exists(sauvegardes_mode_personnalisee[polyominos]):
        sauvegarde_mode_personnalisee_correcte = True
        
    if os.path.exists(sauvegardes_bonus_couleur[polyominos]):
        sauvegarde_bonus_couleur_correcte = True
    
    Pos=attend_clic_gauche()
    if  145<= Pos[0] <= 455 and 195<=Pos[1]<=305:
        if sauvegarde_bonus_rotation_correcte:
            menu_reprendre_sauvegarde_bonus_rotation(sauvegarde_bonus_rotation_correcte)
        else:
            bonus_rotation_plateau(0)
            
    elif 145<= Pos[0] <=405 and 345<=Pos[1]<=455:
        if sauvegarde_bonus_couleur_correcte:
            menu_reprendre_sauvegarde(3, sauvegarde_bonus_couleur_correcte)
        else:
            jeu_principal(3, 0)
    
    elif 145<= Pos[0] <=455 and 495<=Pos[1]<=605:
        if sauvegarde_mode_personnalisee_correcte:
            menu_reprendre_sauvegarde(2, sauvegarde_mode_personnalisee_correcte)
        else:
            jeu_principal(2, 0)
            
    elif 145<= Pos[0] <=455 and 645<=Pos[1]<=755:
        menu_principal()
    
    else:
        menu_bonus()
##########################################################################

#########################DEFAITE#####################################
def game_over(score,mode, sauvegarde_utilise):
    
    sauvegardes = [0,"sauvegardes/sauvegarde1","sauvegardes/sauvegarde2", "sauvegardes/sauvegarde3", "sauvegardes/sauvegarde4", "sauvegardes/sauvegarde5"]
    sauvegardes_variante = [0,"sauvegardes/sauvegarde_variante1","sauvegardes/sauvegarde_variante2", "sauvegardes/sauvegarde_variante3", "sauvegardes/sauvegarde_variante4", "sauvegardes/sauvegarde_variante5"]
    sauvegardes_mode_personnalisee = [0,"sauvegardes/sauvegarde_mode_personnalisee1","sauvegardes/sauvegarde_mode_personnalisee2", "sauvegardes/sauvegarde_mode_personnalisee3", "sauvegardes/sauvegarde_mode_personnalisee4", "sauvegardes/sauvegarde_mode_personnalisee5"]
    sauvegardes_bonus_couleur = [0,"sauvegardes/sauvegarde_bonus_couleur1","sauvegardes/sauvegarde_bonus_couleur2", "sauvegardes/sauvegarde_bonus_couleur3", "sauvegardes/sauvegarde_bonus_couleur4", "sauvegardes/sauvegarde_bonus_couleur5"]
    
    if mode==0:
        fichier = sauvegardes[polyominos]
    elif mode==1:
        fichier = sauvegardes_variante[polyominos]
    elif mode == 2:
        fichier = sauvegardes_mode_personnalisee[polyominos]
    else:
        fichier = sauvegardes_bonus_couleur[polyominos]
        
    if sauvegarde_utilise == True:
        os.remove(fichier)
    
    efface_tout()
    rectangle(0, 0, 600, 800, remplissage="blue")
    
    texte(60,100,"Vous avez perdu", couleur="red", taille=50)
    texte(220,300,"Score :", couleur="yellow", taille=28)
    texte(350,300, int(score), "yellow", taille=28)
    
    rectangle(150,420,450,525, remplissage='black')
    rectangle(155,425,445,520, remplissage='grey')
    texte(205,450,"Rejouer", couleur="yellow", taille=40)
    
    rectangle(150,570,450,675, remplissage='black')
    rectangle(155,575,445,670, remplissage='grey')
    texte(230,600,"Menu", couleur="yellow", taille=40)
    
    Pos=attend_clic_gauche()
    
    if 150<= Pos[0] <= 450 and 420<= Pos[1] <= 525:
        if mode == 0 :
            jeu_principal(0, 0)
        elif mode == 1:
            jeu_principal(1, 0)
        else:
            jeu_principal(2, 0)
            
    elif 150<= Pos[0] <= 450 and 570<= Pos[1] <= 675:
        menu_principal()
    else : 
        attend_clic_gauche()
        ferme_fenetre()
        return
#####################################################################
def game_over_bonus_rotation(score,sauvegarde_utilise):
    redimensionne_fenetre(400, 800)
    sauvegardes_bonus_rotation = [0,"sauvegardes/sauvegarde_bonus_rotation1","sauvegardes/sauvegarde_bonus_rotation2", "sauvegardes/sauvegarde_bonus_rotation3", "sauvegardes/sauvegarde_bonus_rotation4", "sauvegardes/sauvegarde_bonus_rotation5"]

    fichier = sauvegardes_bonus_rotation[polyominos]
    
    if sauvegarde_utilise == True:
        os.remove(fichier)
    
    efface_tout()
    rectangle(0, 0, 400, 800, remplissage="blue")
    
    texte(60,100,"Vous avez perdu", couleur="red", taille=30)
    texte(120,300,"Score :", couleur="yellow", taille=28)
    texte(250,300, int(score), "yellow", taille=28)
    
    rectangle(50,420,350,525, remplissage='black')
    rectangle(55,425,345,520, remplissage='grey')
    texte(105,450,"Rejouer", couleur="yellow", taille=40)
    
    rectangle(50,570,350,675, remplissage='black')
    rectangle(55,575,345,670, remplissage='grey')
    texte(130,600,"Menu", couleur="yellow", taille=40)
    
    Pos=attend_clic_gauche()
    
    if 50<= Pos[0] <= 350 and 420<= Pos[1] <= 525:
        bonus_rotation_plateau(0)
    elif 50<= Pos[0] <= 350 and 570<= Pos[1] <= 675:
        menu_principal()
    else : 
        attend_clic_gauche()
        ferme_fenetre()
        return
#####################################################################
def game_over_2joueurs(joueur1, joueur2, sauvegarde_utilise):
    redimensionne_fenetre(600,800)
    
    sauvegardes_2joueurs = [0,"sauvegardes/sauvegarde_2joueurs1","sauvegardes/sauvegarde_2joueurs2", "sauvegardes/sauvegarde_2joueurs3", "sauvegardes/sauvegarde_2joueurs4", "sauvegardes/sauvegarde_2joueurs5"]
    fichier = sauvegardes_2joueurs[polyominos]
    
    if sauvegarde_utilise == True:
        os.remove(fichier)
    
    efface_tout()
    if joueur1 == True:
        rectangle(0,0,300,800, remplissage="midnightblue")
        texte(30,200,"Vous avez perdu")
        rectangle(300,0,600,800, remplissage='seagreen')
        texte(330,200,"Vous avez gagné")
    if joueur2 == True:
        rectangle(0,0,300,800, remplissage="midnightblue")
        texte(30,200,"Vous avez gagné")
        rectangle(300,0,600,800, remplissage='seagreen')
        texte(330,200,"Vous avez perdu")
        
        
    rectangle(150,420,450,525, remplissage='black')
    rectangle(155,425,445,520, remplissage='grey')
    texte(205,450,"Rejouer", couleur="yellow", taille=40)
    
    rectangle(150,570,450,675, remplissage='black')
    rectangle(155,575,445,670, remplissage='grey')
    texte(230,600,"Menu", couleur="yellow", taille=40)
    
    Pos=attend_clic_gauche()
    
    if 150<= Pos[0] <= 450 and 420<= Pos[1] <= 525:
        jeu_principal_2joueurs(0)
    elif 150<= Pos[0] <= 450 and 570<= Pos[1] <= 675:
        menu_principal()
    else : 
        attend_clic_gauche()
        ferme_fenetre()
        return
#####################################################################

############################PAUSE##################################
def pause():
    redimensionne_fenetre(600, 800)
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(145,405,455,515, remplissage='black')
    rectangle(150,410,450,510, remplissage='grey')

    rectangle(145,530,455,640, remplissage='black')
    rectangle(150,535,450,635, remplissage='grey')
        
    rectangle(145,655,455,765, remplissage='black')
    rectangle(150,660,450,760, remplissage='grey')
            
    texte(90,50, "TETRIS", "red", taille=90)
    texte(200,200, "Pause", "black", taille =50)
            
    texte(190,440, 'Reprendre' , 'Yellow', taille=35)
    texte(165,565, 'Sauvegarder' , 'Yellow', taille=35)
    texte(230,690, 'Quitter', 'yellow', taille=35)
    mise_a_jour()
################################################################### 

################Crée une sauvegarde dans un fichier################
def sauvegarde(score, ligne_sup_total, matrice_jeu, niveau, difficulte, piece, prochaine_piece,mode):
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(150,200, 'Sauvegarde en cours...', couleur="yellow")
    attente(1)
    
    sauvegardes = [0,"sauvegardes/sauvegarde1","sauvegardes/sauvegarde2", "sauvegardes/sauvegarde3", "sauvegardes/sauvegarde4", "sauvegardes/sauvegarde5"]
    sauvegardes_variante = [0,"sauvegardes/sauvegarde_variante1","sauvegardes/sauvegarde_variante2", "sauvegardes/sauvegarde_variante3", "sauvegardes/sauvegarde_variante4", "sauvegardes/sauvegarde_variante5"]
    sauvegardes_mode_personnalisee = [0,"sauvegardes/sauvegarde_mode_personnalisee1","sauvegardes/sauvegarde_mode_personnalisee2", "sauvegardes/sauvegarde_mode_personnalisee3", "sauvegardes/sauvegarde_mode_personnalisee4", "sauvegardes/sauvegarde_mode_personnalisee5"]
    sauvegardes_bonus_couleur = [0,"sauvegardes/sauvegarde_bonus_couleur1","sauvegardes/sauvegarde_bonus_couleur2", "sauvegardes/sauvegarde_bonus_couleur3", "sauvegardes/sauvegarde_bonus_couleur4", "sauvegardes/sauvegarde_bonus_couleur5"]
    
    
    if mode==0:
        fichier = sauvegardes[polyominos]
    elif mode == 1:
        fichier = sauvegardes_variante[polyominos]
    elif mode == 2:
        fichier = sauvegardes_mode_personnalisee[polyominos]
    else:
        fichier = sauvegardes_bonus_couleur[polyominos]
    
    with open(fichier, 'w') as save:
        save.write(str(datetime.now().strftime("%H:%M:%S %A %d %Y")) + "\n")
        save.write(str(score) + "\n") 
        save.write(str(niveau) + "\n")
        save.write(str(ligne_sup_total) + "\n")
        save.write(str(difficulte) + "\n")
        save.write("\n")
        
        if polyominos>3:
            save.write(str(piece[1][1]) + "\n")
            save.write(str(prochaine_piece[1][1]) + "\n")
            save.write("\n")
        else:
            save.write(str(piece[0][0]) + "\n")
            save.write(str(prochaine_piece[0][0]) + "\n")
            save.write("\n")
            
        for i in range(len(matrice_jeu)):
            for j in range(len(matrice_jeu[i])):
                save.write(str(matrice_jeu[i][j]))
                save.write(" ")
            save.write("\n")
                    
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(170,200,'Sauvegarde réussi', couleur='yellow')
    attente(1)
    efface_tout()       
    mise_a_jour()
################################################################### 
def sauvegarde_2joueurs(matrice_jeu1, matrice_jeu2, piece1, piece2, prochaine_piece1, prochaine_piece2):
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(150,200, 'Sauvegarde en cours...', couleur="yellow")
    attente(1)
    
    sauvegardes_2joueurs = [0,"sauvegardes/sauvegarde_2joueurs1","sauvegardes/sauvegarde_2joueurs2", "sauvegardes/sauvegarde_2joueurs3", "sauvegardes/sauvegarde_2joueurs4", "sauvegardes/sauvegarde_2joueurs5"]
    
    fichier = sauvegardes_2joueurs[polyominos]

    
    with open(fichier, 'w') as save:
        save.write(str(datetime.now().strftime("%H:%M:%S %A %d %Y")) + "\n")
        
        
        if polyominos>3:
            save.write(str(piece1[1][1]) + "\n")
            save.write(str(prochaine_piece1[1][1]) + "\n")
            save.write("\n")
        else:
            save.write(str(piece1[0][0]) + "\n")
            save.write(str(prochaine_piece1[0][0]) + "\n")
            save.write("\n")
            
        for i in range(len(matrice_jeu1)):
            for j in range(len(matrice_jeu1[i])):
                save.write(str(matrice_jeu1[i][j]))
                save.write(" ")
            save.write("\n")
        
        save.write("\n")
            
        if polyominos>3:
            save.write(str(piece2[1][1]) + "\n")
            save.write(str(prochaine_piece2[1][1]) + "\n")
            save.write("\n")
        else:
            save.write(str(piece2[0][0]) + "\n")
            save.write(str(prochaine_piece2[0][0]) + "\n")
            save.write("\n")
            
        for i in range(len(matrice_jeu2)):
            for j in range(len(matrice_jeu2[i])):
                save.write(str(matrice_jeu2[i][j]))
                save.write(" ")
            save.write("\n")
                    
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(170,200,'Sauvegarde réussi', couleur='yellow')
    attente(1)
    efface_tout()       
    mise_a_jour()
################################################################### 
def sauvegarde_bonus_rotation(score, ligne_sup_total, matrice_jeu, niveau, difficulte, piece, mode_jeu):
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(150,200, 'Sauvegarde en cours...', couleur="yellow")
    attente(1)
    
    sauvegardes_bonus_rotation = [0,"sauvegardes/sauvegarde_bonus_rotation1","sauvegardes/sauvegarde_bonus_rotation2", "sauvegardes/sauvegarde_bonus_rotation3", "sauvegardes/sauvegarde_bonus_rotation4", "sauvegardes/sauvegarde_bonus_rotation5"]

    fichier = sauvegardes_bonus_rotation[polyominos]
    
    with open(fichier, 'w') as save:
        save.write(str(datetime.now().strftime("%H:%M:%S %A %d %Y")) + "\n")
        save.write(str(score) + "\n") 
        save.write(str(niveau) + "\n")
        save.write(str(ligne_sup_total) + "\n")
        save.write(str(difficulte) + "\n")
        save.write(str(mode_jeu) + "\n")
        save.write("\n")
        
        if polyominos>3:
            save.write(str(piece[1][1]) + "\n")
            save.write("\n")
        else:
            save.write(str(piece[0][0]) + "\n")
            save.write("\n")
            
        for i in range(len(matrice_jeu)):
            for j in range(len(matrice_jeu[i])):
                save.write(str(matrice_jeu[i][j]))
                save.write(" ")
            save.write("\n")
                    
    efface_tout()
    rectangle(0,0,600,800, remplissage='blue')
    texte(90,50, "TETRIS", "red", taille=90)
    texte(170,200,'Sauvegarde réussi', couleur='yellow')
    attente(1)
    efface_tout()       
    mise_a_jour()
################################################################### 

#################Reprendre la sauvegarde###########################      
def menu_reprendre_sauvegarde(mode, sauvegarde_correcte):
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(90,400,190,450, remplissage='black')
    rectangle(95,405,185,445, remplissage='grey')

    rectangle(400,400,500,450, remplissage='black')
    rectangle(405,405,495,445, remplissage='grey')
            
    texte(90,50, "TETRIS", "red", taille=90)
    texte(55,300, "Reprendre la partie sauvegardée ?", couleur="yellow")
    texte(105,415,"NON", "yellow")
    texte(420,415, "OUI", "yellow")
    
    clic_gauche = False
    while clic_gauche == False:    
        Pos=attend_clic_gauche()
    
        if 90<= Pos[0] <= 190 and 400<= Pos[1] <= 450:
            jeu_principal(mode, 0)
        elif 400<= Pos[0] <= 500 and 400<= Pos[1] <= 450:
            jeu_principal(mode, 1)
################################################################### 
def menu_reprendre_sauvegarde_2joueurs(sauvegarde_correcte):
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(90,400,190,450, remplissage='black')
    rectangle(95,405,185,445, remplissage='grey')

    rectangle(400,400,500,450, remplissage='black')
    rectangle(405,405,495,445, remplissage='grey')
            
    texte(90,50, "TETRIS", "red", taille=90)
    texte(55,300, "Reprendre la partie sauvegardée ?", couleur="yellow")
    texte(105,415,"NON", "yellow")
    texte(420,415, "OUI", "yellow")
    
    clic_gauche = False
    while clic_gauche == False:    
        Pos=attend_clic_gauche()
    
        if 90<= Pos[0] <= 190 and 400<= Pos[1] <= 450:
            jeu_principal_2joueurs(0)
        elif 400<= Pos[0] <= 500 and 400<= Pos[1] <= 450:
            jeu_principal_2joueurs(1)
###################################################################                 
def menu_reprendre_sauvegarde_bonus_rotation(sauvegarde_correcte):
    rectangle(0,0,600,800, remplissage='blue')
    
    rectangle(90,400,190,450, remplissage='black')
    rectangle(95,405,185,445, remplissage='grey')

    rectangle(400,400,500,450, remplissage='black')
    rectangle(405,405,495,445, remplissage='grey')
            
    texte(90,50, "TETRIS", "red", taille=90)
    texte(55,300, "Reprendre la partie sauvegardée ?", couleur="yellow")
    texte(105,415,"NON", "yellow")
    texte(420,415, "OUI", "yellow")
    
    clic_gauche = False
    while clic_gauche == False:    
        Pos=attend_clic_gauche()
    
        if 90<= Pos[0] <= 190 and 400<= Pos[1] <= 450:
            bonus_rotation_plateau(0)
        elif 400<= Pos[0] <= 500 and 400<= Pos[1] <= 450:
            bonus_rotation_plateau(1)
################################################################### 

########Lecture du fichier de sauvegarde pour reprendre############
def reprendre_partie(mode):
    
    sauvegardes = [0,"sauvegardes/sauvegarde1","sauvegardes/sauvegarde2", "sauvegardes/sauvegarde3", "sauvegardes/sauvegarde4", "sauvegardes/sauvegarde5"]
    sauvegardes_variante = [0,"sauvegardes/sauvegarde_variante1","sauvegardes/sauvegarde_variante2", "sauvegardes/sauvegarde_variante3", "sauvegardes/sauvegarde_variante4", "sauvegardes/sauvegarde_variante5"]
    sauvegardes_mode_personnalisee = [0,"sauvegardes/sauvegarde_mode_personnalisee1","sauvegardes/sauvegarde_mode_personnalisee2", "sauvegardes/sauvegarde_mode_personnalisee3", "sauvegardes/sauvegarde_mode_personnalisee4", "sauvegardes/sauvegarde_mode_personnalisee5"]
    sauvegardes_bonus_couleur = [0,"sauvegardes/sauvegarde_bonus_couleur1","sauvegardes/sauvegarde_bonus_couleur2", "sauvegardes/sauvegarde_bonus_couleur3", "sauvegardes/sauvegarde_bonus_couleur4", "sauvegardes/sauvegarde_bonus_couleur5"]
    
    if mode==0:
        fichier = sauvegardes[polyominos]
    elif mode == 1:
        fichier = sauvegardes_variante[polyominos]
    elif mode == 2:
        fichier = sauvegardes_mode_personnalisee[polyominos]
    else:
        fichier = sauvegardes_bonus_couleur[polyominos]
        
    with open(fichier, "r") as save:
            liste_sauvegarde = save.readlines()
            score = int(liste_sauvegarde[1])
            niveau = int(liste_sauvegarde[2])
            ligne_sup_total = int(liste_sauvegarde[3])
            difficulte = float(liste_sauvegarde[4])
            
            piece = pieces[int(liste_sauvegarde[6]) - 1]
            prochaine_piece = piece = pieces[int(liste_sauvegarde[7]) - 1]
            
            matrice_jeu = []
            for ligne_du_fichier in range(9,33):
                ligne_complete = []
                ligne = liste_sauvegarde[ligne_du_fichier]
                
                elements = ligne.split()
                
                for element in elements:
                    ligne_complete.append(int(element))
                        
                matrice_jeu.append(ligne_complete)
                
    return score, niveau, ligne_sup_total, difficulte, piece, prochaine_piece, matrice_jeu
################################################################### 
def reprendre_partie_2joueurs():
    sauvegardes_2joueurs = [0,"sauvegardes/sauvegarde_2joueurs1","sauvegardes/sauvegarde_2joueurs2", "sauvegardes/sauvegarde_2joueurs3", "sauvegardes/sauvegarde_2joueurs4", "sauvegardes/sauvegarde_2joueurs5"]

    fichier = sauvegardes_2joueurs[polyominos]
        
    with open(fichier, "r") as save:
            liste_sauvegarde = save.readlines()
            
            piece1 = pieces[int(liste_sauvegarde[1]) - 1]
            prochaine_piece1 = pieces[int(liste_sauvegarde[2]) - 1]
            
            matrice_jeu1 = []
            for ligne_du_fichier in range(4,28):
                ligne_complete = []
                ligne = liste_sauvegarde[ligne_du_fichier]
                
                elements = ligne.split()
                
                for element in elements:
                    ligne_complete.append(int(element))
                        
                matrice_jeu1.append(ligne_complete)
                
                
            piece2 = pieces[int(liste_sauvegarde[29]) - 1]
            prochaine_piece2 = pieces[int(liste_sauvegarde[30]) - 1]
            
            matrice_jeu2 = []
            for ligne_du_fichier in range(32,56):
                ligne_complete = []
                ligne = liste_sauvegarde[ligne_du_fichier]
                
                elements = ligne.split()
                
                for element in elements:
                    ligne_complete.append(int(element))
                        
                matrice_jeu2.append(ligne_complete)
    return piece1, prochaine_piece1, matrice_jeu1, piece2, prochaine_piece2, matrice_jeu2
################################################################### 
def reprendre_partie_bonus_rotation():
    
    sauvegardes_bonus_rotation = [0,"sauvegardes/sauvegarde_bonus_rotation1","sauvegardes/sauvegarde_bonus_rotation2", "sauvegardes/sauvegarde_bonus_rotation3", "sauvegardes/sauvegarde_bonus_rotation4", "sauvegardes/sauvegarde_bonus_rotation5"]

    fichier = sauvegardes_bonus_rotation[polyominos]
        
    with open(fichier, "r") as save:
            liste_sauvegarde = save.readlines()
            score = int(liste_sauvegarde[1])
            niveau = int(liste_sauvegarde[2])
            ligne_sup_total = int(liste_sauvegarde[3])
            difficulte = float(liste_sauvegarde[4])
            mode_jeu = int(liste_sauvegarde[5])
            
            piece = pieces[int(liste_sauvegarde[7]) - 1]
            
            matrice_jeu = []
            for ligne_du_fichier in range(9,33):
                ligne_complete = []
                ligne = liste_sauvegarde[ligne_du_fichier]
                
                elements = ligne.split()
                
                for element in elements:
                    ligne_complete.append(int(element))
                        
                matrice_jeu.append(ligne_complete)
                
    return score, niveau, ligne_sup_total, difficulte, piece, matrice_jeu, mode_jeu
################################################################### 

###################Personnalisation############################## 
def personnalisation_interface_fond():
    fichier = "Configuration.txt"
    
    with open(fichier, "r") as config:
        listes_sauvegardes = config.readlines()
        couleur_de_fond = listes_sauvegardes[0]
        partie = couleur_de_fond.split(':')
        couleur_fond = partie[1]
        couleur_fond = couleur_fond.strip()
        couleur_fond = couleur_fond.strip('""')
        
        couleur_des_blocs = listes_sauvegardes[1]
        partie = couleur_des_blocs.split(":")
        couleur_bloc = partie[1]
        couleur_bloc = couleur_bloc.strip()
        couleur_bloc_sans_crochet = couleur_bloc.strip("[]")
        elements = couleur_bloc_sans_crochet.split(",")
        liste_couleur_bloc = [element.strip().strip("'") for element in elements]
        
    return couleur_fond, liste_couleur_bloc
###################################################################                              
def personnalisation_touche():
    fichier = "Configuration.txt"
    
    with open(fichier, "r") as config:
        listes_sauvegardes = config.readlines()
        
        touche_gauche = listes_sauvegardes[2]
        partie = touche_gauche.split(":")
        touche_gauche = partie[1]
        touche_gauche = touche_gauche.strip()
        touche_gauche = touche_gauche.strip('""')
        
        touche_droite = listes_sauvegardes[3]
        partie = touche_droite.split(":")
        touche_droite = partie[1]
        touche_droite = touche_droite.strip()
        touche_droite = touche_droite.strip('""')
        
        touche_rotation = listes_sauvegardes[4]
        partie = touche_rotation.split(":")
        touche_rotation = partie[1]
        touche_rotation = touche_rotation.strip()
        touche_rotation = touche_rotation.strip('""')
        
        touche_chute = listes_sauvegardes[5]
        partie = touche_chute.split(":")
        touche_chute = partie[1]
        touche_chute = touche_chute.strip()
        touche_chute = touche_chute.strip('""')
        
    return touche_gauche, touche_droite, touche_rotation, touche_chute
###################################################################                 
def personnalisation_touche_pause():
    fichier = "Configuration.txt"
    
    with open(fichier, "r") as config:
        listes_sauvegardes = config.readlines()
        
        touche_pause = listes_sauvegardes[6]
        partie = touche_pause.split(":")
        touche_pause = partie[1]
        touche_pause = touche_pause.strip()
        touche_pause = touche_pause.strip('""')
    
    return touche_pause
################################################################### 

#########################Mode##################################### 
def mode_pourrissement(matrice_jeu):
    i=0
    j=0
    while matrice_jeu[i][j] == 0 : 
        i= randrange(0,23)
        j= randrange(0,11)
    matrice_jeu[i][j]=0
################################################################### 

########SUPPRIMER LES BLOCS DE MÊME COULEUR ADJACENTS##############
def supprimer_blocs_adjacents(matrice_jeu, x, y, couleur, score):
    """Supprime les blocs de la même couleur connectés."""
    lignes, colonnes = len(matrice_jeu), len(matrice_jeu[0])
    fait = set()
    atente = [(x, y)]
    blocs_a_supprimer = []
    
    while atente:
        cx, cy = atente.pop()
        if (cx, cy) in fait or not (0 <= cx < colonnes and 0 <= cy < lignes):
            continue
        if matrice_jeu[cy][cx] == couleur:
            blocs_a_supprimer.append((cx, cy))
            fait.add((cx, cy))
            voisins = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
            atente.extend(voisins)

    if len(blocs_a_supprimer)>=5:
        for bx, by in blocs_a_supprimer:
            matrice_jeu[by][bx] = 0
        score += 10
            
    return matrice_jeu, score
################################################################### 

####################Mode 2 Joueurs#################################
def jeu_principal_2joueurs(Sauvegarde):
    redimensionne_fenetre(1000,800)
    matrice_jeu1 = [[0] * 12 for i in range(ligne_jeu_2joueurs)]
    matrice_jeu2 = [[0] * 12 for i in range(ligne_jeu_2joueurs)]

    piece1 = choisir_piece()
    piece2 = choisir_piece()
    
    prochaine_piece1 = choisir_piece()
    prochaine_piece2 = choisir_piece()
    

    x1 = colonne_jeu_2joueurs // 4 - len(piece1[0]) // 2    
    y1 = 0                                          
    
    x2 = x1 + 12
    y2 = 0
    
    ligne_effaces1 = 0
    ligne_effaces2 = 0
    
    chrono_droitegauche1 = time()
    chrono_rotation1 = time()
    chrono_descente1 = time()
    chrono_chute1 = time()
    
    chrono_droitegauche2 = time() 
    chrono_rotation2 = time()
    chrono_descente2 = time()
    chrono_chute2 = time()
    
    sauvegarde_utilise = False
    
    if Sauvegarde == 1:
        piece1, prochaine_piece1, matrice_jeu1, piece2, prochaine_piece2, matrice_jeu2 = reprendre_partie_2joueurs()
        sauvegarde_utilise = True
    
    while True:
        
        temps = time()   
        
        if temps - chrono_descente1 >= 1:  
            chrono_descente1 = time()          
            if not contact1(piece1, x1, y1 + 1, matrice_jeu1):  
                y1 += 1    
                
            else :
                for i in range(len(piece1)):
                    for j in range(len(piece1[i])):
                        if piece1[i][j] != 0:
                            matrice_jeu1[y1 + i][x1 + j] = piece1[i][j]
                
                matrice_jeu1, ligne_effaces1 = supprimer_ligne1(matrice_jeu1)
                
                            
                piece1 = prochaine_piece1
                x1 = colonne_jeu_2joueurs // 4 - len(piece1[0]) // 2
                y1 = 0
                prochaine_piece1 = choisir_piece()
                
                if contact1(piece1, x1, y1, matrice_jeu1):
                    game_over_2joueurs(True, False, sauvegarde_utilise)
                
            
        if temps - chrono_descente2 >= 1:   
            chrono_descente2 = time()                
            if not contact2(piece2, x2, y2 + 1, matrice_jeu2):  
                y2 += 1     
                
            else :
                for i in range(len(piece2)):
                    for j in range(len(piece2[i])):
                        if piece2[i][j] != 0:
                            matrice_jeu2[y2 + i][x2 - 12 + j] = piece2[i][j]
                        
                matrice_jeu2, ligne_effaces2 = supprimer_ligne1(matrice_jeu2)
     
                piece2 = prochaine_piece2
                x2 = x1 + 12
                y2 = 0
                prochaine_piece2 = choisir_piece()
                
                if contact2(piece2, x2, y2, matrice_jeu2):
                    game_over_2joueurs(False, True, sauvegarde_utilise)
            
               
        if touche_pressee('space'):
            redimensionne_fenetre(600,800)
            pause()
            stop = True
            
            while stop:
                Pos=attend_clic_gauche()
                
                if  145<= Pos[0] <= 455 and 405<=Pos[1]<=515:
                    stop = False
                elif 145<= Pos[0] <=455 and 530<=Pos[1]<=640:
                    efface_tout()
                    sauvegarde_2joueurs(matrice_jeu1, matrice_jeu2, piece1, piece2, prochaine_piece1, prochaine_piece2)
                    pause()
                elif 145<= Pos[0] <=455 and 655<=Pos[1]<=765:
                    stop = False
                    menu_principal()
                else:
                    pause()
            redimensionne_fenetre(1000,800)
            
        piece1, x1, y1, chrono_droitegauche1, chrono_rotation1, chrono_chute1 = touche_jeu1(piece1, x1, y1, matrice_jeu1 , temps, chrono_droitegauche1, chrono_rotation1, chrono_chute1)       
                
        piece2, x2, y2, chrono_droitegauche2, chrono_rotation2, chrono_chute2 = touche_jeu2(piece2, x2, y2, matrice_jeu2 , temps, chrono_droitegauche2, chrono_rotation2, chrono_chute2)       
                
        if ligne_effaces2 > 1:
            hazard = randrange(len(matrice_jeu1[0]))
            for i in range(ligne_effaces2 - 1):
                nouvelle_matrice = []
                
                for ligne in matrice_jeu1[1:]:
                    nouvelle_matrice.append(ligne)
                nouvelle_ligne = [7 if j != hazard else 0 for j in range(len(matrice_jeu1[0]))]
                nouvelle_matrice.append(nouvelle_ligne)   
                matrice_jeu1 = nouvelle_matrice
            ligne_effaces2 = 0
            
        if ligne_effaces1 > 1:
            hazard = randrange(len(matrice_jeu2[0]))
            for i in range(ligne_effaces1 - 1):
                nouvelle_matrice = []
                
                for ligne in matrice_jeu2[1:]:
                    nouvelle_matrice.append(ligne)
                nouvelle_ligne = [7 if j != hazard else 0 for j in range(len(matrice_jeu2[0]))]
                nouvelle_matrice.append(nouvelle_ligne)   
                matrice_jeu2 = nouvelle_matrice
            ligne_effaces1 = 0

                    
        
        efface_tout()
        dessiner_matrice_jeu_2joueurs(matrice_jeu1, matrice_jeu2, prochaine_piece1, prochaine_piece2)
        dessiner_piece_2joueurs(piece1, x1, y1)
        dessiner_piece_2joueurs(piece2, x2, y2)
        mise_a_jour()
        attente(0.01)
###################################################################

####################Mode Normale#################################
def jeu_principal(mode, Sauvegarde):
    matrice_jeu = [[0] * colonne_jeu for i in range(ligne_jeu)]     # Definis la matrice du jeu 

    piece = choisir_piece() # Choisis une piece
    prochaine_piece = choisir_piece() # Choisis la prochaine piece à afficher en vance
    
    x = colonne_jeu // 2 - len(piece[0]) // 2      # Coordonnées pour afficher la piece au milieu
    y = 0                                          # Coordonnéés pour afficher la piece tout en haut
    
    score = 0   # Définis le score                                   
    ligne_sup_total = 49
    
    chrono_droitegauche = time()     # Chrono qui vont nous permettre de respecter les delays
    chrono_rotation = time()
    chrono_descente = time()
    chrono_chute = time()
    chrono_pourrissement = time()
    
    tours=0
    niveau = 1
    difficulte = 1
    touche_pause = 'space'
    sauvegarde_utilise = False
    
    if Sauvegarde == 1:
        score, niveau, ligne_sup_total, difficulte, piece, prochaine_piece, matrice_jeu = reprendre_partie(mode)
        sauvegarde_utilise = True
    
    if mode == 2:
        touche_pause = personnalisation_touche_pause()
    
    while True:
        
        temps = time()   
        
        if temps - chrono_descente >= difficulte:     # Si le delay est respecté
            chrono_descente = time()                  # Reinitialise le chrono
            if not contact(piece, x, y + 1, matrice_jeu):  # Regarde si il n'y a pas de contact
                y += 1     # Descend de 1 la piece
                
            else :
                for i in range(len(piece)):
                    for j in range(len(piece[i])):
                        if piece[i][j] != 0:
                            matrice_jeu[y + i][x + j] = piece[i][j]
                            
                            
                ligne_sup, matrice_jeu = sup_ligne(matrice_jeu)
                
                if ligne_sup > 0:
                    ligne_sup_total += ligne_sup
                    difficulte, niveau = niveau_difficulte(ligne_sup_total, difficulte, niveau)
                    score = systeme_point(ligne_sup, score, niveau)
                
                if mode == 3:
                    
                    for i in range(len(piece)):
                        for j in range(len(piece[i])):
                            if piece[i][j] != 0:
                                couleur = piece[i][j]
                                matrice_jeu, score = supprimer_blocs_adjacents(matrice_jeu, x + j, y + i, couleur, score)
                                
                                
                piece = prochaine_piece 
                x = colonne_jeu // 2 - len(piece[0]) // 2
                y = 0
                prochaine_piece = choisir_piece()
                
                if contact(piece, x, y, matrice_jeu):
                    game_over(score,mode, sauvegarde_utilise)
        
        if touche_pressee(touche_pause):
            pause()
            stop = True
            
            while stop:
                Pos=attend_clic_gauche()
                
                if  145<= Pos[0] <= 455 and 405<=Pos[1]<=515:
                    stop = False
                elif 145<= Pos[0] <=455 and 530<=Pos[1]<=640:
                    sauvegarde(score, ligne_sup_total, matrice_jeu, niveau, difficulte, piece, prochaine_piece,mode)
                    pause()
                elif 145<= Pos[0] <=455 and 655<=Pos[1]<=765:
                    stop = False
                    menu_principal()
                else:
                    pause()
            
        piece, x, y, chrono_droitegauche, chrono_rotation, chrono_chute = touche_jeu(piece, x, y, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute, mode)       
                
        efface_tout()
        if mode == 1 and temps - chrono_pourrissement >= 10:
            mode_pourrissement(matrice_jeu)
            chrono_pourrissement = time()
            
            
        dessiner_matrice_jeu(matrice_jeu, score, niveau, prochaine_piece, piece, x, y, mode)
        dessiner_piece(piece, x, y, mode)
        mise_a_jour()
        attente(0.01)
#################################################################

####################Mode Bonus Rotation Plateau#################################   
def bonus_rotation_plateau(Sauvegarde):
    matrice_jeu = [[0] * colonne_jeu for i in range(ligne_jeu)]     # Definis la matrice du jeu 
    

    piece = choisir_piece() # Choisis une piece
    
    x = colonne_jeu_bonus_rotation // 2 - len(piece[0]) // 2      # Coordonnées pour afficher la piece au milieu
    y = 0                                          # Coordonnéés pour afficher la piece tout en haut
    
    x2 = colonne_jeu_bonus_rotation2 // 2 - len(piece[0]) // 2      # Coordonnées pour afficher la piece au milieu
    y2 = 0 
    
    score = 0   # Définis le score                                   
    ligne_sup_total = 0
    
    chrono_droitegauche = time()     # Chrono qui vont nous permettre de respecter les delays
    chrono_rotation = time()
    chrono_descente = time()
    chrono_chute = time()
    chrono_pourrissement = time()
    
    niveau = 1
    difficulte = 1
    
    temps_rotation = time()
    mode_jeu = 1
    
    sauvegarde_utilise = False
    
    if Sauvegarde == 1:
        score, niveau, ligne_sup_total, difficulte, piece, matrice_jeu, mode_jeu = reprendre_partie_bonus_rotation()
        sauvegarde_utilise = True
    
    while True:
        temps = time()
        
        if temps - temps_rotation >= 5:
            mode_jeu = 2 if mode_jeu == 1 else 1
            temps_rotation = time()
        
        if mode_jeu == 1:
            redimensionne_fenetre(400, 800)
            
            
            if len(matrice_jeu) != 24:
                
                direction = randrange(0,2)
                if direction == 0:
                    matrice_jeu = tourner_matrice_droite(matrice_jeu)
                else:
                    matrice_jeu = tourner_matrice_gauche(matrice_jeu)
                matrice_jeu = chutes_des_pieces(matrice_jeu)
                
                
                
            
            temps = time()   
            
            if temps - chrono_descente >= difficulte:     # Si le delay est respecté
                chrono_descente = time()                  # Reinitialise le chrono
                if not contact_bonus_rotation(piece, x, y + 1, matrice_jeu):  # Regarde si il n'y a pas de contact
                    y += 1     # Descend de 1 la piece
                    
                else :
                    for i in range(len(piece)):
                        for j in range(len(piece[i])):
                            if piece[i][j] != 0:
                                matrice_jeu[y + i][x + j] = piece[i][j]
                                
                                
                    ligne_sup, matrice_jeu = sup_ligne(matrice_jeu)
                    
                    if ligne_sup > 0:
                        ligne_sup_total += ligne_sup
                        difficulte, niveau = niveau_difficulte(ligne_sup_total, difficulte, niveau)
                        score = systeme_point(ligne_sup, score, niveau)
                                
                    piece = choisir_piece()
                    x = colonne_jeu_bonus_rotation // 2 - len(piece[0]) // 2
                    y = 0
                    
                    if contact_bonus_rotation(piece, x, y, matrice_jeu):
                        game_over_bonus_rotation(score, sauvegarde_utilise)
            
            if touche_pressee('space'):
                pause()
                stop = True
                
                while stop:
                    Pos=attend_clic_gauche()
                    
                    if  145<= Pos[0] <= 455 and 405<=Pos[1]<=515:
                        stop = False
                    elif 145<= Pos[0] <=455 and 530<=Pos[1]<=640:
                        sauvegarde_bonus_rotation(score, ligne_sup_total, matrice_jeu, niveau, difficulte, piece, mode_jeu)
                        pause()
                    elif 145<= Pos[0] <=455 and 655<=Pos[1]<=765:
                        stop = False
                        menu_principal()
                    else:
                        pause()
                
            piece, x, y, chrono_droitegauche, chrono_rotation, chrono_chute = touche_jeu_bonus_rotation(piece, x, y, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute)       
                    
            efface_tout()
                
            dessiner_matrice_jeu_bonus_rotation(matrice_jeu, score, niveau, piece, x, y)
            dessiner_piece_bonus_rotation(piece, x, y)
            mise_a_jour()
            attente(0.01)
            
        
        
        
        elif mode_jeu == 2:
            
            redimensionne_fenetre(800, 400)
            
            if len(matrice_jeu) != 12:
                direction = randrange(0,2)
                if direction == 0:
                    matrice_jeu = tourner_matrice_droite(matrice_jeu)
                else:
                    matrice_jeu = tourner_matrice_gauche(matrice_jeu)
                matrice_jeu = chutes_des_pieces(matrice_jeu)
                
            temps = time()   
            
            if temps - chrono_descente >= difficulte:     # Si le delay est respecté
                chrono_descente = time()                      # Reinitialise le chrono
                if not contact_bonus_rotation2(piece, x2, y2 + 1, matrice_jeu):  # Regarde si il n'y a pas de contact
                    y2 += 1     # Descend de 1 la piece
            
                else :
                    for i in range(len(piece)):
                        for j in range(len(piece[i])):
                            if piece[i][j] != 0:
                                matrice_jeu[y2 + i][x2 + j] = piece[i][j]
                                    
                                    
                    ligne_sup, matrice_jeu = sup_ligne_bonus_rotation(matrice_jeu)
                        
                    if ligne_sup > 0:
                        ligne_sup_total += ligne_sup
                        difficulte, niveau = niveau_difficulte(ligne_sup_total, difficulte, niveau)
                        score = systeme_point(ligne_sup, score, niveau)
                                    
                    piece = choisir_piece()
                    x2 = colonne_jeu_bonus_rotation2 // 2 - len(piece[0]) // 2
                    y2 = 0
                
                        
                    if contact_bonus_rotation2(piece, x2, y2, matrice_jeu):
                        game_over_bonus_rotation(score, sauvegarde_utilise)
                
            if touche_pressee('space'):
                pause()
                stop = True
                    
                while stop:
                    Pos=attend_clic_gauche()
                        
                    if  145<= Pos[0] <= 455 and 405<=Pos[1]<=515:
                        stop = False
                    elif 145<= Pos[0] <=455 and 530<=Pos[1]<=640:
                        matrice_jeu = tourner_matrice_droite(matrice_jeu)
                        matrice_jeu = appliquer_gravite(matrice_jeu)
                        sauvegarde_bonus_rotation(score, ligne_sup_total, matrice_jeu, niveau, difficulte, piece, mode_jeu)
                        pause()
                    elif 145<= Pos[0] <=455 and 655<=Pos[1]<=765:
                        stop = False
                        menu_principal()
                    else:
                        pause()
                    
            piece, x2, y2, chrono_droitegauche, chrono_rotation, chrono_chute = touche_jeu_bonus_rotation2(piece, x2, y2, matrice_jeu, temps, chrono_droitegauche, chrono_rotation, chrono_chute)       
                        
            efface_tout()
                    
            dessiner_matrice_jeu_bonus_rotation2(matrice_jeu, score, niveau, piece, x2, y2)
            dessiner_piece_bonus_rotation2(piece, x2, y2)
            mise_a_jour()
            attente(0.01)
##################################################################
        
if __name__ == '__main__':
    ecran()
    menu_principal()