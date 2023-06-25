from Element import Element
from Skill import Skill
from Persona import Persona
from Item import *

import random
import math

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

		self.level = 1
		self.xp = 0
		self.xp_next = self.calcul_xp_next()

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
		items = "("
		for oneItem in self.inventaire:
			items += str(oneItem.nom) + " x" + str(self.inventaire[oneItem]) + ","
		items += ")"

		return f"(nom={self.nom},prenom={self.prenom},level={self.level},xp={self.xp}/{self.xp_next},pv={self.pv}/{self.maxPv},pc={self.pc}/{self.maxPc},persona={self.persona},arme={self.arme},items={items},trickster={self.trickster})"

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

	def levelUp(self):
		addHp = random.randint(3,10)
		addPc = random.randint(2,6)

		self.pv += addHp
		self.maxPv += addHp
		self.pc += addPc
		self.maxPc += addPc

		self.level += 1
		self.xp -= self.xp_next

		self.xp_next = self.calcul_xp_next() 

	def attack(self):
		attack_calc = 1
		if(self.arme != None):
			attack_calc = math.sqrt((1/2)*self.arme.puissance)
		else:
			attack_calc = 1

		if(self.persona != None):
			attack_calc *= math.sqrt(self.persona.force)
		else:
			attack_calc *= 1

		return int(attack_calc)

	def attackSkill(self,skill):
		attack_calc = 0

		attack_calc = math.sqrt(skill.puissance) 

		if(skill.element == 1):
			attack_calc *= math.sqrt(self.persona.force)
		else:
			attack_calc *= math.sqrt(self.persona.magic)

		return int(attack_calc)

	def add_xp(self,xp_amount):
		self.xp += xp_amount
		while(self.xp >= self.xp_next):
			self.levelUp()

	def calcul_xp_next(self):
		return int(math.pow(self.level,0.5)*100)

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


test = Skill("test",2,"test",10,50,99,False)
p = Persona("Izanagi",2,5,0,3,2, 10, 5,6,[test])

pomme = HealingObject(0,"pomme",10,10,False,"une simple pomme")
potion = HealingObject(4,"Potion",50,0,True,"Potion a base de plante")
tarte = Item(2,"tarte","Une bonne tarte bien juteuse.")
hache = Weapon(1,"Hache",290,90)

pierre = Character(0,"Jean pierre","Test",p,100,50)
pierre.add_item(potion,5)
pierre.add_item(hache)
pierre.equip_item(hache)
pierre.useItem(potion)

print(pierre.attackSkill(test))
