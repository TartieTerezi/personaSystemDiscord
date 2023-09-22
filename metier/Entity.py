from Element import Element
from Skill import Skill

class Entity(object):
	"""Entity qui va servir de base pour l'heritage"""
	def __init__(self,nom : str,element : Element,level : int, force : int, magic : int, endurance : int, agilite : int, chance : int,skills : list[Skill]):
		self.nom = nom

		self.element = element
		self.level = level
		self.force = force
		self.magic = magic
		self.endurance = endurance
		self.agilite = agilite
		self.chance = chance
		self.skills = skills

	