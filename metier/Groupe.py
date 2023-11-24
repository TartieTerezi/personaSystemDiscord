from Character import Character

class Groupe(object):
    """Un groupe contient les joueurs pour les donjons"""
    def __init__(self,_nom : str,_leader : Character) -> None:
        self.nom : str = _nom 
        """Nom du groupe."""
        self.leader : Character = _leader
        """Leader du groupe."""
        self.joueurs : list[Character] = [] 
        """Liste des joueurs."""
        self.limite : int = 3
        """Limite du nombre de joueur dans un groupe."""
        self.navi : Character = None 
        """Navi : A implementer plus tard."""

    def addPlayer(self,_player : Character) -> bool:
        """Ajoute un joueur dans l'equipe et renvoie un bool si l'ajout s'est effectue."""
        if(len(self.joueurs) < self.limite and not self.searchPlayer(_player)):
            self.joueurs.append(_player)
            return True #ajout du joueur

        return False #ne peut pas ajouter de joueurs car il y a déjà trop de personnages
  
    def searchPlayer(self,_player : Character) -> bool:
        """Cherche si le joueur est present dans le groupe.""" 
        if(_player == self.leader):
            return True

        for joueur in self.joueurs:
            if(joueur == _player):
                return True
        return False

    def getPlayersId(self) -> list[int]:
        """Recupere la liste des id des Joueurs dans le groupe."""
        playersId : list[int] = []
        playersId.append(self.leader.id)

        for joueur in self.joueurs:
            playersId.append(joueur.id)

        return playersId

    def removePlayer(self,_player : Character) -> bool:
        """Enleve le joueur passe en parametre, retourne Vrai ou Faux si le joueur a bien ete enleve."""
        if(self.searchPlayer(_player)):
            self.joueurs.remove(_player)
            return True

        return False

    def tag(self,_player : Character) -> bool:
        """Change le leader de l'equipe pour un autre membre de l'equipe, Retourne Vrai ou Faux si le Tag a fonctionne."""
        if(not self.searchPlayer(_player)):
            return False
        
        beforeLeader : Character = self.leader
        newLeader : Character = _player
        self.joueurs.remove(_player)    
        self.joueurs.append(beforeLeader)
        
        # Met le leader en None pour eviter d'ecraser l'ancien leader par ptr.
        self.leader = None 
        self.leader = newLeader
        return True
