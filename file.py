from Element import Element
from Skill import Skill
from Persona import Persona
from Character import Character
from Date import Date

import os

script_dir = os.path.dirname(__file__) 
rel_path = "Files/"
abs_file_path = os.path.join(script_dir, rel_path)

abs_file_path_skill = abs_file_path +"Skills/"
abs_file_path_personas = abs_file_path + "Personas/"
abs_file_path_characters = abs_file_path + "Characters/"

def supprBakward(mot):
	return str(mot)[:(len(str(mot))-1)]

def getSkills():
	skills = []

	listFile = os.listdir(abs_file_path_skill)

	for file in listFile:
		fileName = abs_file_path_skill + file

		with open(fileName,"r") as f:
			lines = f.readlines()

			nom = str(supprBakward(lines[0]))
			element = Element(int(supprBakward(lines[1])))
			description = str(supprBakward(lines[2]))
			cout = int(supprBakward(lines[3]))
			puissance = int(supprBakward(lines[4]))
			precision = int(supprBakward(lines[5]))
			isHealing = bool(supprBakward(lines[6]))

			skills.append(Skill(nom,element,description,cout,puissance,precision,isHealing))
	
	return skills

def newSkill(skill):
	script_dir = os.path.dirname(__file__)
	rel_path = "Files/Skills/"
	abs_file_path = os.path.join(script_dir, rel_path)

	abs_file_path += str(skill.nom+".txt")

	f = open(abs_file_path,"w")

	f.write(str(skill.nom)+"\n")
	f.write(str(skill.element)+"\n")
	f.write(str(skill.description)+"\n")
	f.write(str(skill.cout)+"\n")
	f.write(str(skill.puissance)+"\n")
	f.write(str(skill.precision)+"\n")
	f.write(str(skill.isHealing)+"\n")

	f.close()

def getPersonas(skillList):
	personas = []

	listFile = os.listdir(abs_file_path_personas)

	for file in listFile:
		fileName = abs_file_path_personas + file

		with open(fileName,"r") as f:
			lines = f.readlines()

			nom = str(supprBakward(lines[0]))
			element = Element(int(supprBakward(lines[1])))
			level = int(supprBakward(lines[2]))
			xp = int(supprBakward(lines[3]))
			force = int(supprBakward(lines[4]))
			magic = int(supprBakward(lines[5]))
			endurance = int(supprBakward(lines[6]))
			agilite = int(supprBakward(lines[7]))
			chance = int(supprBakward(lines[8]))

			#enleve les deux premiers elements
			listSkillsPersona = []
			for indexLine in range(len(lines)-2):
				nomSkill = str(supprBakward(lines[indexLine+2]))
				for oneSkill in skillList:
					if(nomSkill == oneSkill.nom):
						listSkillsPersona.append(oneSkill)

			personas.append(Persona(nom,element,level,xp,force,magic,endurance,agilite,chance,listSkillsPersona))

	return personas

def newCharacter(character):
	script_dir = os.path.dirname(__file__)
	rel_path = "Files/Characters/"
	abs_file_path = os.path.join(script_dir,rel_path)

	abs_file_path += str(character.nom+"_"+character.prenom+".txt")

	f = open(abs_file_path,"w")

	f.write(str(character.id)+"\n")
	f.write(str(character.nom)+"\n")
	f.write(str(character.prenom)+"\n")
	if(character.persona != None):
		f.write(str(character.persona.nom)+"\n")
	else:
		f.write(str(0)+"\n")
	f.write(str(character.maxPv)+"\n")
	f.write(str(character.maxPc)+"\n")

	f.close()

def reset():
	listSkill = getSkills()
	listPersonas = getPersonas(listSkill)
	listCharacters = getCharacters(listPersonas)
	date = getDate()

	return listSkill,listPersonas,listCharacters,date

def getCharacters(personaList):
	characters = []

	listFile = os.listdir(abs_file_path_characters)

	for file in listFile:
		fileName = abs_file_path_characters + file

		with open(fileName,"r") as f:
			lines = f.readlines()

			index = int(supprBakward(lines[0]))
			nom = str(supprBakward(lines[1]))
			prenom = str(supprBakward(lines[2]))
			personaName = str(supprBakward(lines[3]))

			persona = None
			
			for onePersona in personaList:
				if(onePersona.nom == personaName):
					persona = onePersona

			pv = int(supprBakward(lines[4]))
			pc = int(supprBakward(lines[5]))

			characters.append(Character(index,nom,prenom,persona,pv,pc))

	return characters

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