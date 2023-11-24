from types import NoneType
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
		self.id : int = index
		self.nom : str = nom
		self.prenom : str = prenom
		self.persona : Persona = Persona.byBdd(idPersona) 
		self.trickster : bool = False
		#stats en combat
		self.pv : int = pv
		self.maxPv : int = MaxPv
		self.pc : int = pc
		self.maxPc : int = MaxPc

		self.level : int = level
		self.xp : int = xp
		self.xp_next : int = self.calcul_xp_next()

		#inventaire
		self.inventaire : dict =  {}

		self.arme : Weapon = None

		self.argent : int = 500 # valeur par defaut a changer

		#stats sociale 
		self.connaissance : int = 1
		self.stat_connaissance : int = 0
		self.charme : int = 1
		self.stat_charme : int = 0
		self.gentilesse : int = 1
		self.stat_gentilesse : int = 0
		self.competence : int = 1
		self.stat_competence : int = 0
		self.maitrise : int = 1
		self.stat_maitrise : int = 0

		self.statutEffect : bool = None
		self.isProtect : bool = False
		self.isFight : bool = False

	@classmethod
	def byBdd(cls,index : list[int]):
		"""Recupere un character dans la bdd."""
		result = Dao.getOneDataBdd("SELECT * FROM Character where id = ?",[index])
		return Character(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9])

	def getAgilite(self) -> int:
		"""Recupere l'agilite du character pour la stat de vitesse."""
		if(self.persona != None):
			return self.persona.getAgilite()
		else:
			return 1

	def getName(self) -> str:
		return self.prenom

	def addStats(self,_persona : Persona,_pv : int, _pc : int) -> None:
		"""Ajoute les stats pour le personnage."""
		self.persona = _persona
		self.pv = _pv
		self.maxPv = self.pv
		self.pc = _pc
		self.maxPc = self.pc

	def __str__(self) -> str:
		return f"{self.nom} {self.prenom}"

	def in_inventory(self,item) -> bool:
		"""Retourne Vrai ou Faux si un item se trouve dans l'inventaire du joueur."""
		return (item not in self.inventaire.keys())
	
	def deleteItem(self) -> None:
		"""Supprime les items dont le joueur n'as plus en stock."""
		itemsToDelete : list[Item] = []

		for item in self.inventaire:
			if(self.inventaire[item] == 0):
				itemsToDelete.append(item)

		for item in itemsToDelete:
			self.inventaire.pop(item)
	
	def useItem(self,_item) -> bool:
		""""Utilise un item et renvoie si l'item a ete utilise."""
		#si l'item n'est pas utilisable
		if(_item.is_useable() == False):
			return False

		#verifie le nombre d'objets disponible
		if(self.remove_item(_item)):
			_item.use(self)
		else:
			return False

	def add_item(self,_item,_amount : int = 1) -> None:
		"""Ajoute un Item dans l'inventaire."""
		if self.in_inventory(_item):
			self.inventaire[_item] = _amount
		else:
			self.inventaire[_item] += _amount

	def get_item(self,_item) -> int:
		"""Recupere le nombre d'item dans l'inventaire."""
		return self.inventaire[_item]

	def equip_item(self,_item) -> bool:
		""""Equipe l'item si possible et si dans l'inventaire, Retourne False Sinon"""
		if(self.in_inventory(_item)):
			return False

		if(not _item.is_equipeable()):
			return False
		
		_item.equip(self)
		return True

	def getItemByName(self,_nameItem : str):
		"""Recupere l'item selon son nom."""
		for item in self.inventaire:
			if(item.nom == _nameItem):
				return item

	def levelUp(self) -> None:
		"""Level up du personnage."""
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

	def attack(self) -> int:
		"""Calcule l'attaque avec les armes et la personna."""
		attack_calc = 1
		if(self.arme != None):
			attack_calc = math.sqrt((1/2)*self.arme.puissance)

		if(self.persona != None):
			attack_calc *= math.sqrt(self.persona.force)

		return int(attack_calc)

	def attackSkill(self,skill) -> int:
		"""Calcule et Retourne les degats d'une attaque magique."""

		attack_calc = 1

		if(self.persona != None):
			attack_calc = self.persona.attackSkill(skill)

		return int(attack_calc)

	def takeDamage(self,damage,skill = None) -> int:
		"""Subis les degats des attaques."""
		
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

	def add_xp(self,_xp_amount : int ) -> int:
		"""Ajoute l'experience obtenue."""

		nbrLevelTake = 0
		self.xp += _xp_amount
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