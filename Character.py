from Element import Element
from Skill import Skill
from Persona import Persona

import random

class Character(object):
	"""docstring for Character"""
	def __init__(self,index : int,nom : str,prenom : str,persona : Persona, pv : int,pc : int):
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

		#stats sociale
		self.connaissance = 1
		self.stat_connaissance = 0
		self.charme = 1
		self.stat_charme = 0
		self.gentilesse = 1
		self.stat_gentilesse = 0
		self.competence = 1
		self.stat_competence = 0
		self.maitrise = 1
		self.stat_maitrise = 0

	def __str__(self):
		return f"(nom={self.nom},prenom={self.prenom},persona={self.persona},trickster={self.trickster}"
