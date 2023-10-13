
class contextCombat(object):
    def __init__(self,turn,xp,allie,ennemi,charactersToFight,characterTarget,ctx,mess,characterTurn) -> None:
        self.xp = xp
        self.turn = turn
        self.allie = allie
        self.ennemi = ennemi 
        self.charactersToFight = charactersToFight
        self.characterTarget = characterTarget
        self.ctx = ctx
        self.mess = mess
        self.characterTurn = characterTurn
