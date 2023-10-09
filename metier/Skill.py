from Element import Element
import sqlite3
from Dao import Dao
from StatutEffect import StatutEffect
from contextCombat import contextCombat

class BaseSkill(object):
	"""docstring for baseSkill, base de tout les skills, comparable a une classe abstraite en c++"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "") -> None:
		self.index = index
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.description = description

	# Effet du skill, a changer a chaque classe fille
	async def effect(self,userSkill,contextCombat : contextCombat):
		pass

	def __str__(self):
		return f"{self.nom}"

	def isUseable(self):
		return False

	def canChoiceTarget(self) -> bool:
		return False

	async def canUse(self,characterTurn,contextCombat : contextCombat) -> bool:
		return False

	def getCount(self):
		return ""

class SkillAttackOneTarget(BaseSkill):
	"""docstring for Skill, attack one character"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,puissance : int = 0,precision : int = 0):
		super().__init__(index,nom,idElement,description)
		self.cout = cout
		self.puissance = puissance
		self.precision = precision

	def canChoiceTarget(self) -> bool:
		return True

	async def effect(self,characterTurn,contextCombat : contextCombat):
		nextTurn = True
		damage = characterTurn.attackSkill(self)

		# differencie si c'est un skill physique ou non
		if(self.element.nom == "PHYSIQUE"):
			cout = int(characterTurn.maxPv * self.cout / 100)
			characterTurn.pv -= cout		
			nextTurn = False
			damage = contextCombat.characterTarget.takeDamage(damage,self)
		else:
			characterTurn.pc -= self.cout
			nextTurn = False
			damage = contextCombat.characterTarget.takeDamage(damage,self)	
									
		await contextCombat.mess.edit(content=str("```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+self.nom+" ]\n```\n```diff\n- [ "+contextCombat.characterTarget.getName()+" perd "+str(damage)+" PV a cause de "+self.nom+" ]\n```"),embed=None,view=None)
		return nextTurn

	async def canUse(self,characterTurn,contextCombat : contextCombat) -> bool:		
		if(self.element.nom == "PHYSIQUE"):
			cout = int(characterTurn.maxPv * self.cout / 100)

			if(characterTurn.pv - cout > 0):
				return True
			else:
				await contextCombat.ctx.channel.send(content=str("Pas assez de Pv pour lancer "+ str(self.nom)))
		else:
			if(characterTurn.pc - self.cout >= 0):
				return True
			else:
				await contextCombat.ctx.channel.send(content=str("Pas assez de pc pour lancer "+ str(self.nom)))
		return False

	def isUseable(self):
		return True

	def getCount(self):
		typeDeCout = ""

		typeDeCout += str(self.cout)
		
		if(self.element.index == 1):
			typeDeCout += "% pv"
		else:
			typeDeCout += " pc"

		return typeDeCout

class SkillAttackMultipleTarget(SkillAttackOneTarget):
	"""docstring for Skill, attack multiple character"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,puissance : int = 0,precision : int = 0):
		super().__init__(index,nom,idElement,description,cout,puissance,precision)

	def canChoiceTarget(self) -> bool:
		return False

	async def effect(self,characterTurn,contextCombat : contextCombat):
		nextTurn = True
		damage = characterTurn.attackSkill(self)

		# differencie si c'est un skill physique ou non
		if(self.element.nom == "PHYSIQUE"):
			cout = int(characterTurn.maxPv * self.cout / 100)
			characterTurn.pv -= cout		
			nextTurn = False
			damage = contextCombat.characterTarget.takeDamage(damage,self)
		else:
			message = str("```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+self.nom+" ]\n```\n")

			characterTurn.pc -= self.cout
			nextTurn = False

			for oneEnnemi in contextCombat.ennemi:
				
				damage = characterTurn.attackSkill(self)
				damage = oneEnnemi.takeDamage(damage,self)	

				message += "```diff\n- [ "+oneEnnemi.getName()+" perd "+str(damage)+" PV a cause de "+self.nom+" ]\n```"
									
		await contextCombat.mess.edit(content=message,embed=None,view=None)
		return nextTurn

	def isUseable(self):
		return True
