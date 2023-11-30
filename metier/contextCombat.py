class contextCombat(object):
    def __init__(self,turn,xp,allie,ennemi,charactersToFight,characterTarget,ctx,mess,characterTurn) -> None:
        """Information sur le combat"""
        self.xp : int = xp
        """Xp gagne a la fin du combat"""
        self.turn : int = turn
        """Tour actuel du combat"""
        self.allie : list[Fighter] = allie
        """Liste des allies dans le combat."""
        self.ennemi : list[Fighter] = ennemi 
        """Liste des ennemis dans le combat."""
        self.charactersToFight : list[Fighter] = charactersToFight
        """Liste des ennemis du joueur en cours"""
        self.characterTarget : list[Fighter] = characterTarget
        """character qui sera vise dans l'attaque"""
        self.ctx = ctx
        """Contexte discord"""
        self.mess = mess
        """Message discord"""
        self.characterTurn : Fighter = characterTurn
        """Character Actuel"""
        self.damage : int = 0
        """Dommage genere a la fin du tour"""
        self.skill : BaseSkill = None
        """Skill qui va etre utilise"""