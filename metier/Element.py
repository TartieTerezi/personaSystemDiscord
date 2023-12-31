import sqlite3
from Dao import Dao

class Element(object):
	"""Un element est une classe qui gere les elements du jeu, prenant aussi en compte les attaques physique, c'est dans cette classe qu'est gere la couleur lie a la classe"""
	def __init__(self,index : int = 0,nom : str = "",red : int = 0 ,blue : int = 0,green : int = 0) -> None:
		self.index = index
		self.nom = nom 
		self.color = [red,blue,green]

	@classmethod
	def byBdd(cls,index):
		result = Dao.getOneDataBdd("SELECT * FROM Element where id = ?",[index])

		return Element(result[0],result[1],result[2],result[3],result[4])

	def __str__(self):
		return f"id : "+str(self.index)+ " nom : "+str(self.nom)+ " color : "+str(self.color)