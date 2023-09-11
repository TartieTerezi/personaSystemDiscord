from Character import Character

class Groupe(object):
    #"""Un groupe contient les joueurs pour les donjons"""
    def __init__(self,nom,leader):
        self.nom = nom #nom du groupe
        self.leader = leader
        self.joueurs = [] #liste des joueurs
        self.joueurs.append(leader)
        self.limite = 4 #limite du nombre de joueur dans un groupe
        self.navi = None #Navi : A implementer plus tard

    def addPlayer(self,player):
        if(len(self.joueurs) < self.limite):
            self.joueurs.append(player)
            return True #ajout du joueur

        return False #ne peut pas ajouter de joueurs car il y a déjà trop de personnages

    #cherche le joueur 
    def searchPlayer(self,player):
        for joueur in self.joueurs:
            if(joueur == player):
                return True
        return False

    def removePlayer(self,player):
        if(self.searchPlayer(player)):
            self.joueurs.remove(player)
            return True

        return False
