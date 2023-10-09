from Skill import *
from Persona import Persona
from Character import Character
from Date import Date
from Item import *
from Dao import Dao

import sqlite3

import os

script_dir = os.path.dirname(__file__) 
rel_path = "Files/"
abs_file_path = os.path.join(script_dir, rel_path)

abs_file_path_dates = abs_file_path + "Dates/"
abs_file_path_items = abs_file_path + "Objects/"

def supprBakward(mot):
	return str(mot)[:(len(str(mot))-1)]

def getSkills():
	skills = []

	con = sqlite3.connect("bdd/persona.db")
	cur = con.cursor()

	res = cur.execute("SELECT COUNT(*) FROM Skill")

	result = res.fetchone()[0]

	for i in range(result):
		skills.append(Skill.byBdd(i+1))
	
	return skills

def newSkill(skill):
	pass

def getPersonas():
	personas = []

	res = Dao.getAll("SELECT id FROM Persona")

	result = res.fetchone()
	
	while(result != None):
		personas.append(Persona.byBdd(result[0]))

		result = res.fetchone()

	return personas

def newCharacter(character):
	pass

def getItems():
	items = []

	listFolder = os.listdir(abs_file_path_items)

	for folderName in listFolder:
		folder = abs_file_path_items + folderName + "/"
		if(folderName=="Items"):
			listFiles = os.listdir(folder)

			for file in listFiles:
				fileName = folder + file
				with open(fileName,'r') as f:
					lines = f.readlines()

					index = int(supprBakward(lines[0]))
					nom = str(supprBakward(lines[1]))
					info = str(supprBakward(lines[2]))

					items.append(Item(index,nom,info))
		elif(folderName=="Weapons"):
			listFiles = os.listdir(folder)

			for file in listFiles:
				fileName = folder + file
				with open(fileName,'r') as f:
					lines = f.readlines()

					index = int(supprBakward(lines[0]))
					nom = str(supprBakward(lines[1]))
					puissance = int(supprBakward(lines[2]))
					precision = int(supprBakward(lines[3]))
					info = str(supprBakward(lines[4]))

					items.append(Weapon(index,nom,puissance,precision,info))
		elif(folderName=="HealingObjects"):
			listFiles = os.listdir(folder)

			for file in listFiles:
				fileName = folder + file
				with open(fileName,'r') as f:
					lines = f.readlines()

					index = int(supprBakward(lines[0]))
					nom = str(supprBakward(lines[1]))
					pvHeal = int(supprBakward(lines[2]))
					pcHeal = int(supprBakward(lines[3]))
					isPercent = bool(supprBakward(lines[4]))
					info = str(supprBakward(lines[5]))

					items.append(HealingObject(index,nom,pvHeal,pcHeal,isPercent,info))

	return items

def newItem(item):
	script_dir = os.path.dirname(__file__)
	rel_path = "Files/Objects/"
	if(type(item)==Item):
		rel_path += "Items/"
	elif(type(item)==Weapon):
		rel_path += "Weapons/"
	elif(type(item)==HealingObject):
		rel_path += "HealingObjects/"


	abs_file_path = os.path.join(script_dir,rel_path)

	abs_file_path += str(item.nom)+".txt"

	f = open(abs_file_path,"w")
	f.write(str(item.id)+"\n")
	f.write(str(item.nom)+"\n")

	if(type(item)==Weapon):
		f.write(str(item.puissance)+"\n")
		f.write(str(item.precision)+"\n")
	elif(type(item)==HealingObject):
		f.write(str(item.pvHeal)+"\n")
		f.write(str(item.pcHeal)+"\n")
		f.write(str(item.isPercent)+"\n")

	f.write(str(item.info)+"\n")

	f.close()

def reset():
	listPersonas = getPersonas()
	listCharacters = getCharacters()
	date = getDate()
	objects = getItems()

	return listPersonas,listCharacters,date,objects

def getCharacters():
	characters = []

	res = Dao.getAll("SELECT id FROM Character")

	result = res.fetchone()

	while(result != None):
		characters.append(Character.byBdd(result[0]))

		result = res.fetchone()
	
	return characters


def getInfoDay(date : Date):
	fileName = abs_file_path_dates + date.getFileDay()

	try:
		#retourne les informations du jour
		with open(fileName,"r") as f:
			lines = f.readlines()

			return lines[0]
	except Exception as e:
		return None
	
def getDate():
	date = None
	with open(abs_file_path+"date.txt","r") as f:
		lines = f.readlines()

		jour = int(supprBakward(lines[0]))
		jourName = int(supprBakward(lines[1]))
		mois = int(supprBakward(lines[2]))
		annee = int(supprBakward(lines[3]))
		step = int(supprBakward(lines[4]))

		date = Date(jour,jourName,mois,annee,step)

	return date