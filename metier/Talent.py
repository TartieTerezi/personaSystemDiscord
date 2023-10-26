from email import message
from Element import Element
import sqlite3
from Dao import Dao
from StatutEffect import StatutEffect
from View import *
from contextCombat import contextCombat
from random import randint

class BaseTalent(object):
    """Classe de base des talents, doit integrer tout les trigger et les return sans effectuer d'actions"""
    def __init__(self, index : int = 0,nom : str = "", description : str = "") -> None:
        self.index = index
        self.nom = nom
        self.description = description
    
    # lors d'une attaque a multiple cout 
    def onAttackMultiplePunch(self,contextCombat : contextCombat):
        return " "

    def canUseSkill(self,contextCombat : contextCombat):
        return False

    def onAttackSkill(self,contextCombat : contextCombat):
        return " "

    def onKillEnnemie(self,contextCombat : contextCombat):
        return " "

    def onUseSkill(self,contextCombat : contextCombat):
        return " "

    def getCount(self):
        return " "

    def isUseable(self):
        return False

class TalentOnAttackMultiplePunch(BaseTalent):
    def __init__(self, index: int = 0, nom: str = "", description: str = "",pourcentage : int = 0) -> None:
        super().__init__(index, nom, description)
        self.pourcentage = pourcentage # pourcentage d'activation
    
    def onAttackMultiplePunch(self,contextCombat : contextCombat):
        message = ""
        if(randint(0,100)<self.pourcentage):
            message = "```diff\n+ [ Activation de "+self.nom+" ]\n"
            message += str("- [ "+contextCombat.characterTarget.getName()+" perd "+str(contextCombat.damage)+" PV ]\n```")
        
            contextCombat.characterTarget.takeDamage(contextCombat.damage)

        return message

class TalentNoKillSkill(BaseTalent):
    def __init__(self, index: int = 0, nom: str = "", description: str = "") -> None:
        super().__init__(index, nom, description)

    def onAttackSkill(self,contextCombat : contextCombat):
        message = ""

        if(contextCombat.characterTarget.pv <= 0):
            message = "```diff\n+ [ Activation de "+self.nom+" ]```\n"
            contextCombat.characterTarget.pv = 1

        return message

class TalentOnKillEnnemie(BaseTalent):
    def __init__(self, index: int = 0, nom: str = "", description: str = "") -> None:
        super().__init__(index, nom, description)
        self.isActive = False

    def onKillEnnemie(self,contextCombat : contextCombat):
        self.isActive = True

        return  "```diff\n+ [ "+self.nom+" est charge ! ]```\n"

    def onUseSkill(self,contextCombat : contextCombat):
        if(self.isActive):
            self.isActive = False

            if(contextCombat.skill.element.nom == "PHYSIQUE"):
                cout = int(contextCombat.characterTurn.maxPv * contextCombat.skill.cout / 100)
                contextCombat.characterTurn.pv += cout 

            else:
                contextCombat.characterTurn.pc +=  contextCombat.skill.cout
            
            return "```diff\n+ [ Activation de "+self.nom+" ]```\n"
        return " "

    def canUseSkill(self,contextCombat : contextCombat):
        return self.isActive


# Meurtrier : si tu tues un ennemis, le prochain Skill ne coûtera rien 
# Retenue : Tout les skills utilisé laisse l'ennemi a 1pv.
# Rapide comme l'éclair : chaque coup d'une attaque multi coup a 50% de chance de declencher un autre coup 


# classe des skill talent

# Trigger des activations des talents
# Quand tu attaques
# Quand tu te buff
# quand tu te debuff
# en debut de combat
# en fin de combat 
# quand tu te protege
# Quand un alié revit 
# quand un allié meurt
# quand un ennemis meurt
# Quand un ennemis apparait en combat
# a la fin de chaque tour
# 