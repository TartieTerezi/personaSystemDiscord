from Element import Element
from Skill import *
from Persona import Persona
from Dao import Dao
from StatutEffect import StatutEffect

import random
import math

class Character(object):
	"""docstring for Character"""
	def __init__(self,index : int,nom : str,prenom : str,idPersona : int = None, MaxPv : int = 0,MaxPc : int = 0,pv : int = 0,pc : int = 0,level : int = 1,xp : int = 0):
		self.id = index
		self.nom = nom
		self.prenom = prenom
		self.persona = Persona.byBdd(idPersona) 
		self.trickster = False
		#stats en combat
		self.pv = pv
		self.maxPv = MaxPv
		self.pc = pc
		self.maxPc = MaxPc

		self.level = level
		self.xp = xp
		self.xp_next = self.calcul_xp_next()

		#inventaire
		self.inventaire =  {}

		self.arme = None

		self.argent = 100 # valeur par defaut a changer

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

		self.statutEffect = None
		self.isProtect = False
		self.isFight = False

	@classmethod
	def byBdd(cls,index : int):

		result = Dao.getOneDataBdd("SELECT * FROM Character where id = ?",[index])

		return Character(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9])

	def getAgilite(self) -> int:
		if(self.persona != None):
			return self.persona.getAgilite()
		else:
			return 1

	def getName(self) -> str:
		return self.prenom

	def addStats(persona : Persona,pv : int, pc : int):
		self.persona = persona
		self.pv = pv
		self.maxPv = self.pv
		self.pc = pc
		self.maxPc = self.pc

	def __str__(self):
		return f"{self.nom} {self.prenom}"

	def in_inventory(self,item):
		return (item not in self.inventaire.keys())

	def deleteItem(self):
		listItemToDelete = []

		for item in self.inventaire:
			if(self.inventaire[item] == 0):
				listItemToDelete.append(item)

		for item in listItemToDelete:
		    self.inventaire.pop(item)

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

	def get_item(self,item):
		return self.inventaire[item]

	def equip_item(self,item):
		if(self.in_inventory(item)):
			return

		if(item.is_equipeable()):
			item.equip(self)

	def getItemByName(self,nameItem):
		for item in self.inventaire:
			if(item.nom == nameItem):
				return item

	def levelUp(self):
		addHp = random.randint(3,10)
		addPc = random.randint(2,6)

		self.pv += addHp
		self.maxPv += addHp
		self.pc += addPc
		self.maxPc += addPc

		self.level += 1
		self.xp -= self.xp_next
		if(self.xp < 0):
			self.xp = 0

		self.xp_next = self.calcul_xp_next() 

		if(self.persona != None):
			self.persona.levelUp()

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
		elif(skill.element.nom == "PHYSIQUE"):
			#attaque physique skill
			self.pv -=  damage
		else:
			#attaque magique skill
			self.pv -= damage


		#regarde si le personnage est vaincu pour mettre ses pv a zero
		if(self.pv < 0):
			self.pv = 0

		#retourne les attaques subis
		return damage

	def add_xp(self,xp_amount) -> int:
		nbrLevelTake = 0
		self.xp += xp_amount
		while(self.xp >= self.xp_next):
			self.levelUp()
			nbrLevelTake += 1

		return nbrLevelTake

	def calcul_xp_next(self):
		return int(round((1.1 * (self.level ** 2.5)) / 2)) + 50
		#return int(math.pow(self.level,0.5)*100)

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


from Item import *