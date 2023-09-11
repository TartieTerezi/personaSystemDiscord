from Element import Element
from Skill import Skill

import random
import math

class Ennemy(object):
	"""docstring for Character"""
	def __init__(self,nom : str, pv : int,pc : int, element : Element,level : int, force : int, magic : int, endurance : int, agilite : int, chance : int,skills : list[Skill]):
		self.nom = nom

		#stats en combat
		self.pv = pv
		self.maxPv = self.pv
		self.pc = pc
		self.maxPc = self.pc

		self.element = element
		self.level = level
		self.force = force
		self.magic = magic
		self.endurance = endurance
		self.agilite = agilite
		self.chance = chance
		self.skills = skills

		self.isProtect = False

	def attack(self):
		attack_calc = 1
		if(self.arme != None):
			attack_calc = math.sqrt((1/2)*self.arme.puissance)
		else:
			pass

		if(self.persona != None):
			attack_calc *= math.sqrt(self.persona.force)
		else:
			pass

		return int(attack_calc)

	def attackSkill(self,skill):

		attack_calc = 1

		if(self.persona != None):
			attack_calc = self.persona.attackSkill(skill)

		return int(attack_calc)

	def takeDamage(self,damage,skill = None):
		
		if(self.isProtect):
			damage = int(damage / 2)
			self.isProtect = False		
								
		if(skill == None):
			#attaque physique 
			self.pv -=  damage
		elif(skill.element == Element.PHYSIQUE):
			#attaque physique skill
			self.pv -=  damage
		else:
			#attaque magique skill
			self.pv -= damage

		#retourne les attaques subis
		return damage

	def __str__(self):
		return f"(nom={self.nom},level={self.level},pv={self.pv}/{self.maxPv},pc={self.pc}/{self.maxPc})"
