from Entity import Entity

from Element import Element
from Skill import Skill

import math
import random


class Ennemy(Entity):
	"""docstring for Ennemy"""
	def __init__(self, nom: str,pv : int , pc : int, element: Element, level: int, force: int, magic: int, endurance: int, agilite: int, chance: int, skills: list[Skill]):
		Entity.__init__(nom, element, level, force, magic, endurance, agilite, chance, skills)
		#stats en combat
		self.pv = pv
		self.maxPv = self.pv
		self.pc = pc
		self.maxPc = self.pc

		self.isProtect = False

	def attack(self):
		#fonction d'attaque a finir

		return int(0)

	def attackSkill(self,skill):
		#fonction d'attaque a finir

		return int(0)

	def takeDamage(self,damage,skill = None):
		#fonction d'attaque a finir

		return int(0)

	def __str__(self):
		return f"(nom={self.nom},level={self.level},pv={self.pv}/{self.maxPv},pc={self.pc}/{self.maxPc})"
