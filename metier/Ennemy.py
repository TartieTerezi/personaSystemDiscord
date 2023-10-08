from Entity import Entity

from Element import Element
from Skill import Skill

import math
import random


class Ennemy(Entity):
	"""docstring for Ennemy"""
	def __init__(self, nom: str,pv : int , pc : int, element: Element, level: int, force: int, magic: int, endurance: int, agilite: int, chance: int, skills: list[Skill]):
		super().__init__(nom, element, level, force, magic, endurance, agilite, chance, skills)
		#stats en combat
		self.pv = pv
		self.maxPv = self.pv
		self.pc = pc
		self.maxPc = self.pc

		self.isProtect = False

	def attack(self):
		#fonction d'attaque a finir
		return int( math.sqrt(self.force))

	def updateStatutEffect(self) -> str:
		if(self.StatutEffect != None):

			if(self.StatutEffect.id == 1):
				self.pv -= int(self.maxPv /10)

				return self.nom+" subit a cause du statut de brulure de " +str(int(self.maxPv /10)) + " pv"

		return None

	def attackSkill(self,skill):
		#fonction d'attaque a finir
		attack_calc = 0

		attack_calc = math.sqrt(skill.puissance) 

		if(skill.element == 1):
			attack_calc *= math.sqrt(self.force)
		else:
			attack_calc *= math.sqrt(self.magic)

		return int(attack_calc)

	def takeDamage(self,damage,skill = None):
		self.pv -= damage

		if(skill != None):
			skill.effect(self)

		return damage
	
	#fonction pour retourner de l'exp
	def getXp(self):
		return (self.maxPv + self.force + self.magic + self.endurance + self.agilite + (self.chance / 2))/5

	def __str__(self):
		return f"{self.nom}"
