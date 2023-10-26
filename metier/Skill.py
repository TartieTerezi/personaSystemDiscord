from Element import Element
import sqlite3
from Dao import Dao
from StatutEffect import StatutEffect
from View import *
from contextCombat import contextCombat
from random import choice
from Talent import *

def ifIsInArray(array,objectToCompare) -> bool:
	for oneObject in array:
		if(objectToCompare == oneObject):
			return True

	return False

class BaseSkill(object):
	"""docstring for baseSkill, base de tout les skills, comparable a une classe abstraite en c++"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "") -> None:
		self.index = index
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.description = description

	# Effet du skill, a changer a chaque classe fille
	async def effect(self,characterTurn,contextCombat : contextCombat):
		pass

	
	async def choiceTarget(self):
		pass

	def __str__(self):
		return f"{self.nom}"

	def isUseable(self):
		return False

	def canChoiceTarget(self) -> bool:
		return False

	async def canUse(self,characterTurn,contextCombat : contextCombat) -> bool:
		return False

	def isForAllie(self):
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

	# choisis le personnge a toucher 
	async def choiceTarget(self,contextcbt) -> bool:
		contextcbt.characterTarget = None	
		
		if(ifIsInArray(contextcbt.allie,contextcbt.characterTurn)):
			if(len(contextcbt.ennemi)==1):
				contextcbt.characterTarget = contextcbt.ennemi[0]
			else:
				view = viewSelectEnnemie(contextcbt.ennemi,contextcbt.characterTurn)
				await contextcbt.mess.edit(content="",view=view)
				await view.wait() 
				
				if(view.choice != -1):
					contextcbt.characterTarget = contextcbt.ennemi[view.choice]
			
				"""
			else:
				if(len(contextcbt.allie)==1):
					contextcbt.characterTarget = contextcbt.allie[0]
				else:
					view = viewSelectEnnemie(contextcbt.allie,contextcbt.characterTurn)
					await contextcbt.mess.edit(content="",view=view)
					await view.wait() 
						
					if(view.choice != -1):
						contextcbt.characterTarget = contextcbt.allie[view.choice]
						selectIsValid = False
					else:
						skillIsValid = False
						selectIsValid = False"""
		
		if(contextcbt.characterTarget != None):
			return await self.effect(contextcbt.characterTurn,contextcbt)
		else:
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
			characterTurn.pc -= self.cout
			nextTurn = False
			damage = contextCombat.characterTarget.takeDamage(damage,self)	
		
		message = str("```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+self.nom+" ]\n```\n```diff\n- [ "+contextCombat.characterTarget.getName()+" perd "+str(damage)+" PV a cause de "+self.nom+" ]\n```")
		for skill in contextCombat.characterTurn.persona.skills:
			if(isinstance(skill, BaseTalent)):
				message += skill.onAttackMultiplePunch(contextCombat)
			
				message += skill.onAttackSkill(contextCombat)

				message += skill.onUseSkill(contextCombat)
		
		await contextCombat.mess.edit(content=message,embed=None,view=None)
		return nextTurn

	async def canUse(self,characterTurn,contextCombat : contextCombat) -> bool:	
		for skill in contextCombat.characterTurn.persona.skills:
			if(isinstance(skill, BaseTalent)):
				if(skill.canUseSkill(contextCombat)):
					return True


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

class SkillAttackSeveralTargetAlea(SkillAttackOneTarget):
	"""docstring for Skill, attack several character"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,puissance : int = 0,precision : int = 0, numberTouch : int = 1):
		super().__init__(index,nom,idElement,description)
		self.cout = cout
		self.puissance = puissance
		self.precision = precision
		self.numberTouch = numberTouch

	def canChoiceTarget(self) -> bool:
		return False

	# choisis le personnge a toucher 
	async def choiceTarget(self,contextcbt) -> bool:
		return await self.effect(contextcbt.characterTurn,contextcbt)

	async def effect(self,characterTurn,contextCombat : contextCombat):
		nextTurn = True
		contextCombat.damage = characterTurn.attackSkill(self)

		# differencie si c'est un skill physique ou non
		if(self.element.nom == "PHYSIQUE"):
			cout = int(characterTurn.maxPv * self.cout / 100)
			characterTurn.pv -= cout		
			nextTurn = False
		else:
			characterTurn.pc -= self.cout
			nextTurn = False

		message = "```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+self.nom+" ]\n```\n"
		for i in range(self.numberTouch):

			contextCombat.characterTarget = choice(contextCombat.ennemi)

			contextCombat.damage = contextCombat.characterTarget.takeDamage(contextCombat.damage,self)
			message += str("```diff\n- [ "+contextCombat.characterTarget.getName()+" perd "+str(contextCombat.damage)+" PV a cause de "+self.nom+" ]\n```")

			for skill in contextCombat.characterTurn.persona.skills:
				if(isinstance(skill, BaseTalent)):
					message += skill.onAttackMultiplePunch(contextCombat)
			
					message += skill.onAttackSkill(contextCombat)

					message += skill.onUseSkill(contextCombat)
			
		await contextCombat.mess.edit(content=message,embed=None,view=None)

		return nextTurn

class SkillAttackMultipleTarget(SkillAttackOneTarget):
	"""docstring for Skill, attack multiple character"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,puissance : int = 0,precision : int = 0):
		super().__init__(index,nom,idElement,description,cout,puissance,precision)

	async def choiceTarget(self,contextcbt) -> bool:
		return await self.effect(contextcbt.characterTurn,contextcbt)

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
				contextCombat.characterTarget = oneEnnemi
				damage = characterTurn.attackSkill(self)
				damage = oneEnnemi.takeDamage(damage,self)	

				for skill in contextCombat.characterTurn.persona.skills:
					if(isinstance(skill, BaseTalent)):
						message += skill.onAttackMultiplePunch(contextCombat)
			
						message += skill.onAttackSkill(contextCombat)

						message += skill.onUseSkill(contextCombat)

				message += "```diff\n- [ "+oneEnnemi.getName()+" perd "+str(damage)+" PV a cause de "+self.nom+" ]\n```"
	
		
		await contextCombat.mess.edit(content=message,embed=None,view=None)
		return nextTurn

	def isUseable(self):
		return True

class SkillHealingOneTarget(BaseSkill):
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,healPower : int = 0) -> None:
		super().__init__(index,nom,idElement,description)
		self.cout = cout
		self.healPower = healPower

	async def effect(self,characterTurn,contextCombat : contextCombat):
		nextTurn = True
		heal = int(contextCombat.characterTarget.maxPv * self.healPower / 100)

		characterTurn.pc -= self.cout
		nextTurn = False
		
		contextCombat.characterTarget.pv += heal


		message = " "
		for skill in contextCombat.characterTurn.persona.skills:
			if(isinstance(skill, BaseTalent)):
				message += skill.onUseSkill(contextCombat)

		if(contextCombat.characterTarget.pv > contextCombat.characterTarget.maxPv):
			contextCombat.characterTarget.pv = contextCombat.characterTarget.maxPv
		
		message += str("```diff\n  [ "+characterTurn.getName()+" lance "+self.nom+" ]\n```\n```diff\n+ [ "+contextCombat.characterTarget.getName()+" gagne "+str(heal)+" PV ]\n```")
		await contextCombat.mess.edit(content=str("```diff\n  [ "+characterTurn.getName()+" lance "+self.nom+" ]\n```\n```diff\n+ [ "+contextCombat.characterTarget.getName()+" gagne "+str(heal)+" PV ]\n```"),embed=None,view=None)
		
		return nextTurn

	def isUseable(self):
		return True

	def canChoiceTarget(self) -> bool:
		return True

	async def choiceTarget(self,contextcbt) -> bool:

		if(ifIsInArray(contextcbt.allie,contextcbt.characterTurn)):
			if(len(contextcbt.allie)==1):
				contextcbt.characterTarget = contextcbt.allie[0]
			else:
				view = viewSelectEnnemie(contextcbt.allie,contextcbt.characterTurn)
				await contextcbt.mess.edit(content="",view=view)
				await view.wait() 
				
				if(view.choice != -1):
					contextcbt.characterTarget = contextcbt.allie[view.choice]

		return await self.effect(contextcbt.characterTurn,contextcbt)

	async def canUse(self,characterTurn,contextCombat : contextCombat) -> bool:
		if(characterTurn.pc - self.cout >= 0):
				return True
		else:
			await contextCombat.ctx.channel.send(content=str("Pas assez de pc pour lancer "+ str(self.nom)))
			return False

	def isForAllie(self):
		return True
	
	def getCount(self):
		return str(self.cout) + " pc "