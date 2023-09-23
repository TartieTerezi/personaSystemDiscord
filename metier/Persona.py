from Entity import Entity
from Element import Element
from Skill import Skill

import math
import random

class Persona(Entity):
	"""docstring for Persona"""
	def __init__(self,nom : str,idElement : int,level : int, force : int, magic : int, endurance : int, agilite : int, chance : int,skills : list[Skill]):
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.level = level
		self.force = force
		self.magic = magic
		self.endurance = endurance
		self.agilite = agilite
		self.chance = chance
		self.skills = skills


	def __str__(self):
		result = f"Persona(nom={self.nom},Element={self.element}"
		result += self.getSkills()
		result += ")"

		return result

	def getSkills(self):
		result = ""
		for oneSkill in self.skills:
			result += "- "
			result += oneSkill.nom + " cout : " + str(oneSkill.getCount()) + "\n"
		return result

	def attackSkill(self,skill):

		attack_calc = 0

		attack_calc = math.sqrt(skill.puissance) 

		if(skill.element == 1):
			attack_calc *= math.sqrt(self.force)
		else:
			attack_calc *= math.sqrt(self.magic)

		return int(attack_calc)

	def levelUp(self):
		#force magic endurance agilite chance
		growthRates = [0,0,0,0,0]
		numberAddRate = 7

		while numberAddRate > 0:
			choice = random.randint(0,(len(growthRates)-1))
			if(growthRates[choice] < 3):
				numberAddRate-=1
				growthRates[choice]+=1

		self.force += growthRates[0]
		self.magic += growthRates[1]
		self.endurance += growthRates[2]
		self.agilite += growthRates[3]
		self.chance += growthRates[4]

		self.level += 1

