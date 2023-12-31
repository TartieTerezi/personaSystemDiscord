from Element import Element
from Skill import *
from Persona import Persona
from Dao import Dao
from SocialStats import SocialStats
import random
import math

from metier.Fighter import Fighter

class Character(Fighter):
	"""docstring for Character"""
	def __init__(self,index : int,nom : str,prenom : str,idPersona : int = None, MaxPv : int = 0,MaxPc : int = 0,pv : int = 0,pc : int = 0,level : int = 1,xp : int = 0):
		self.id : int = index
		self.nom : str = nom
		self.prenom : str = prenom
		self.persona : Persona = Persona.byBdd(idPersona) 
		
		#stats en combat
		Fighter.__init__(self,level,pv,MaxPv,pc,MaxPc)
		self.xp  : int = xp
		self.xp_next : int = self.calcul_xp_next()

		#inventaire
		self.inventaire : Inventory = Inventory()
		self.argent : int = 500 # valeur par defaut a changer

		self.socialStats : SocialStats = SocialStats()
		
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

	def __str__(self) -> str:
		return f"{self.nom} {self.prenom}"

	def equip_item(self,_item) -> bool:
		""""Equipe l'item si possible et si dans l'inventaire, Retourne False Sinon"""
		if(self.inventaire.in_inventory(_item)):
			return False

		if(not _item.is_equipeable()):
			return False
		
		_item.equip(self)
		return True

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
		"""Calcule et Retourne les degats d'une attaque de Persona."""
		return self.persona.attackSkill(skill)

	def takeDamage(self,damage,skill = None) -> int:
		"""Subis les degats des attaques."""
		
		if(self.isProtect):
			damage = int(damage / 2)
			self.isProtect = False		
								
		if(skill == None or skill.element.nom == "PHYSIQUE"):
			#attaque physique 
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
		"""Ajoute l'experience obtenue. et retourne le nombre de niveau que le character gagne"""
		nbrLevelTake : int = 0
		self.xp += _xp_amount
		while(self.xp >= self.xp_next):
			self.levelUp()
			nbrLevelTake += 1

		return nbrLevelTake

	def calcul_xp_next(self):
		return int(round((1.1 * (self.level ** 2.5)) / 2)) + 50


from Inventory import Inventory