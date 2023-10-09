from Element import Element
from Skill import *

class Entity(object):
	"""Entity qui va servir de base pour l'heritage"""
	def __init__(self,nom : str,element : Element,level : int, force : int, magic : int, endurance : int, agilite : int, chance : int,skills ):
		self.nom = nom

		self.element = element
		self.level = level
		self.force = force
		self.magic = magic
		self.endurance = endurance
		self.agilite = agilite
		self.chance = chance
		self.skills = skills

		self.StatutEffect = None

	def getAgilite(self) -> int:
		return self.agilite

	def getName(self) -> str:
		return self.nom