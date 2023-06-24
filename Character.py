from Element import Element
from Skill import Skill
from Persona import Persona
from Item import *

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

		#inventaire
		self.inventaire =  {}

		self.arme = None

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
		items = ""
		for oneItem in self.inventaire:
			items += str(oneItem.nom) + " x " + str(self.inventaire[oneItem]) + ", "

		return f"(nom={self.nom},prenom={self.prenom},persona={self.persona},arme={self.arme},items={items},trickster={self.trickster})"

	def in_inventory(self,item):
		return (item not in self.inventaire.keys())

	def useItem(self,item):
		#si l'item n'est pas utilisable
		if(item.is_useable() == False):
			return False

		#verifie le nombre d'objets disponible
		if(self.remove_item(item)):
			item.use(self)
		else:
			return False

	def add_item(self,item,amount = 1):
		if self.in_inventory(item):
			self.inventaire[item] = amount
		else:
			self.inventaire[item] += amount

	def equip_item(self,item):
		if(self.in_inventory(item)):
			return

		if(item.is_equipeable()):
			item.equip(self)


	#renvoie true si l'item a été enlevé, renvoir False sinon
	def remove_item(self,item,amount=1):
		#seulement si un item est déjà présent
		if(self.in_inventory(item)):
			return False

		#regarde si il y aassez d'item dans l'inventaire
		if(self.inventaire[item]-amount>=0):
			self.inventaire[item] -= amount
			return True
		else:
			return False

pomme = Item(0,"pomme")
tarte = Item(2,"tarte","Une bonne tarte bien juteuse.")
hache = Weapon(1,"Hache",10,90)


pierre = Character(0,"Jean pierre","Test",None,100,50)
pierre.add_item(pomme)
pierre.add_item(tarte)


pierre.equip_item(hache)
print(pierre)