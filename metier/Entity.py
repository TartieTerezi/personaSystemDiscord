import math
from Element import Element
from Skill import *

class Entity(object):
	"""Entity qui va servir de base pour l'heritage, contient les pv"""
	def __init__(self,nom : str,element : Element,level : int, force : int, magic : int, endurance : int, agilite : int, chance : int,skills ):
		self.nom : str = nom

		self.element : Element = element
		self.level : int = level
		self.force : int = force
		self.magic : int = magic
		self.endurance : int = endurance
		self.agilite : int = agilite
		self.chance : int = chance
		self.skills : int = skills
		
	def getAgilite(self) -> int:
		return self.agilite

	def getName(self) -> str:
		return self.nom
	
	def attackSkill(self,skill) -> int:
		"""Calcule et Retourne les degats d'une attaque d'une Entity avec un Skill."""

		attack_calc : int = 1

		attack_calc = math.sqrt(skill.puissance) 

		if(skill.element == 1):
			attack_calc *= math.sqrt(self.force)
		else:
			attack_calc *= math.sqrt(self.magic)
			
		return int(attack_calc)
	
	