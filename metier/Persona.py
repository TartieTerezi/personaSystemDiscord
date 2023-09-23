from Entity import Entity
from Element import Element
from Skill import Skill
import sqlite3

import math
import random

class Persona(Entity):
	"""docstring for Persona"""
	def __init__(self,id : int = 0,idElement : int = 0,nom : str = "",level : int = 0, force : int = 0, magic : int = 0, endurance : int = 0, agilite : int = 0, chance : int = 0):
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.level = level
		self.force = force
		self.magic = magic
		self.endurance = endurance
		self.agilite = agilite
		self.chance = chance
		self.skills = []
		#enregistre les skill par rapport a la bdd

	@classmethod
	def byBdd(cls,index : int):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute("SELECT * FROM Persona where id = ?",(index,))

		result = res.fetchone()

		return Persona(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8])


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

