from Element import Element
from Skill import Skill

import random
import math

class Character(object):
	"""docstring for Character"""
	def __init__(self,index : int,nom : str,prenom : str,persona : Persona = None, pv : int = 0,pc : int = 0):
		self.id = index
		self.nom = nom
		self.prenom = prenom
		self.persona = persona 
		self.trickster = False
		#stats en combat
		self.pv = pv
		self.maxPv = self.pv
		self.pc = pc
		self.maxPc = self.pc

		self.level = 1
		self.xp = 0
		self.xp_next = self.calcul_xp_next()