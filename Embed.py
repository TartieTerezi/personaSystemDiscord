# -*-coding:utf-8 -*

from math import floor
import discord
from discord.ext import commands
from discord import app_commands

from Item import Item
from Element import Element
from Skill import *
from Persona import Persona
from Character import Character
from Date import Date
from Groupe import Groupe
from Ennemy import Ennemy
from Shop import Shop

import file

def showObjects(listItems):
	embed=discord.Embed(title="Liste des Objets")

	for item in listItems:
		embed.add_field(name=item.nom + " x"+str(listItems[item]), value=item.info, inline=True)
	return embed

def showObject(item):
	embed=discord.Embed(title=item.nom, description=item.info)
	return embed

def showDate(date : Date):
	embed = "``` ```\n"
	embed += "## " + str(date.getJour()) + " " + str(date.jour) + " " + str(date.getMois()) + "\n\n"
	embed += "**`"+str(date.getStep())+"`**\n" 

	infoDay = file.getInfoDay(date)
	if(infoDay != None):
		embed += "\n**Informations du Jour** :\n" + str(infoDay.encode("latin-1").decode("utf-8")) 
	embed += "\n\n``` ```"

	#embed=discord.Embed(title=str(date.jour)+"/"+str(date.getMois()), description=str(date.getJour()), color=0x46d9d6)
	#embed.add_field(name=str(date.getStep()), value="", inline=True)

	#infoDay = file.getInfoDay(date)
	#if(infoDay != None):
	#	embed.add_field(name="Information du jour", value=str(infoDay), inline=False)

	return embed

def showListEnnemis(listEnnemis):
	embed=discord.Embed(title="Liste des ennemi(s)")
	for i in range(len(listEnnemis)):
		embed.add_field(name=listEnnemis[i].nom, value=int(i+1), inline=True)
	return embed

def showGroupe(groupe : Groupe):
	embed=discord.Embed(title=groupe.nom, color=0x818181)
	embed.add_field(name="Leader", value=str(groupe.leader.prenom + " " + groupe.leader .nom), inline=False)

	for i in range(len(groupe.joueurs)):
		if(i == 0):
			embed.add_field(name="Membre(s)", value=str(groupe.joueurs[i].prenom + " " + groupe.joueurs[i].nom), inline=True)
		else:
			embed.add_field(name=" ", value=str(groupe.joueurs[i].prenom + " " + groupe.joueurs[i].nom), inline=True)
	return embed

def showSkill(skill : BaseSkill):
	embed = discord.Embed(title=skill.nom,color=getColorEmbed(skill.element))
	embed.add_field(name="Description",value=skill.description, inline=True)
	embed.add_field(name="Cout", value=skill.getCount(), inline=True)
	return embed

def showPersonas(personas):
	embed=discord.Embed(title="Listes des personas")
	for onePersona in personas:
		embed.add_field(name="", value=onePersona.nom, inline=True)
	return embed

def addFieldsPersona(persona : Persona,embed):
	embed.add_field(name="Level", value=str(persona.level), inline=True)
	embed.add_field(name="force", value=str(persona.force), inline=True)
	embed.add_field(name="magic", value=str(persona.magic), inline=True)
	embed.add_field(name="endurance", value=str(persona.endurance), inline=True)
	embed.add_field(name="agilite", value=str(persona.agilite), inline=True)
	embed.add_field(name="chance", value=str(persona.chance), inline=True)
	return embed

def showPersonaLevelUp(persona : Persona):
	embed=discord.Embed(title="Level up ", description=str(persona.nom)+" a gagné un niveau", color=getColorEmbed(persona.element))
	embed = addFieldsPersona(persona,embed)
	return embed

def showPersona(persona : Persona):
	embed=discord.Embed(title=persona.nom, color=getColorEmbed(persona.element))
	embed = addFieldsPersona(persona,embed)
	embed.add_field(name="Competence(s)", value="", inline=False)
	for oneSkill in persona.skills:
		embed.add_field(name=oneSkill.nom, value=oneSkill.getCount(), inline=True)
	return embed

def showCharacter(character : Character):
	embed = None

	if(character.persona != None):
		embed=discord.Embed(title=character.prenom +" "+character.nom, color=getColorEmbed(character.persona.element))
	else:
		embed=discord.Embed(title=character.prenom +" "+character.nom)


	embed.add_field(name="PV",value=str(character.pv)+"/"+str(character.maxPv), inline=True)
	embed.add_field(name="PC",value=str(character.pc)+"/"+str(character.maxPc), inline=True)

	embed.add_field(name="Level", value=str(character.level), inline=False)
	embed.add_field(name="XP", value=str(str(character.xp)+"/"+str(character.xp_next)), inline=True)

	embed.add_field(name="Stats Social",value="",inline=False)
	embed.add_field(name="Connaissance",value=character.connaissance, inline=True)
	embed.add_field(name="Charme",value=character.charme, inline=True)
	embed.add_field(name="Gentilesse",value=character.gentilesse, inline=True)
	embed.add_field(name="Competence",value=character.competence, inline=True)
	embed.add_field(name="Maitrise",value=character.maitrise, inline=True)

	if(character.persona != None):
		embed.add_field(name="Persona",value=character.persona.nom, inline=False)
		embed.add_field(name="Compétence(s)", value=character.persona.getSkills(), inline=True)

	return embed

def showNewSkill(persona : Persona,newSkill : BaseSkill):
	embed=discord.Embed(title="Nouvelle compétence", description=persona.nom + " a appris la compétence " + newSkill.nom, color=getColorEmbed(persona.element))
	return embed

def getColorEmbed(element):
	return discord.Color.from_rgb(element.color[0], element.color[1], element.color[2])

def getEmoteHpBar(character)->str:
	pvCharacterMax = float(character.maxPv / 10)

	pvCharacter = str("<:HP_Square:1157462528515915867>" * int(floor(character.pv / pvCharacterMax)))

	ecart = float(pvCharacterMax / 8)
	pvEcart = character.pv - (pvCharacterMax * int(floor(character.pv / pvCharacterMax)))

	idlistEmotes = ["<:HP_Square_0:1158554084228477009>","<:HP_Square_1:1158554086187212810>","<:HP_Square_3:1158554089026756708>","<:HP_Square_4:1158554091010654208>","<:HP_Square_5:1158554092227006504>","<:HP_Square_6:1158554093632102430>"]
	emote = ""

	i = 0
	while ecart < pvEcart:
		emote = idlistEmotes[i]
		ecart += ecart
		i+=1

	pvCharacter += str(emote)

	if(character.pv<=0):
		pvCharacter += str("<:HP_Loss_Square:1157462548245905469>" * int(10))
	else:
		pvCharacter += str("<:HP_Loss_Square:1157462548245905469>" * int(9 - int(floor(character.pv / pvCharacterMax))))

	return pvCharacter

def showShop(shop,character):
	embed=discord.Embed(title="Boutique : "+shop.nom)
	embed.set_thumbnail(url="https://static.wikia.nocookie.net/undertale/images/6/66/Tem_Shop_sprite.png")
	for oneObject in shop.objects:
		embed.add_field(name=str(str(oneObject.nom) +" : x"+ str(shop.objects[oneObject][1])),value=str(str(shop.objects[oneObject][0])+"$"), inline=True)
	embed.add_field(name="votre compte : ",value=str(character.argent)+"$",inline=False)
	return embed


def showFight(characterTurn,listCharacters,listEnnemi):
	embed=discord.Embed(title="Combat ")

	for i in range(len(listEnnemi)):
		ennemi = listEnnemi[i]

		pvEnnemi = getEmoteHpBar(ennemi)

		if(isinstance(ennemi,Ennemy)):
			

			if(ennemi == characterTurn):
				embed.add_field(name=str(ennemi) + " - actif", value=pvEnnemi, inline=True)
			else:
				embed.add_field(name=str(ennemi), value=pvEnnemi, inline=True)

		else:
			pcCharacterMax = float(ennemi.maxPc / 10)
			pcCharacter = str("<:MP_Square:1157462530495619072>" * int(floor(ennemi.pc / pcCharacterMax))) + str("<:MP_Loss_Square:1157462545855168573>" * int(10 - int(floor(ennemi.pc / pcCharacterMax))))

			valueStr = pvEnnemi + "\n" + pcCharacter

			if(ennemi == characterTurn):
				embed.add_field(name=str(ennemi) + " - actif", value=valueStr, inline=True)
			else:
				embed.add_field(name=str(ennemi), value=valueStr, inline=True)

		

	embed.add_field(name="Allié(s)", value=" ", inline=False)

	for i in range(len(listCharacters)):
		character = listCharacters[i]

		pcCharacterMax = float(character.maxPc / 10)

		pvCharacter = getEmoteHpBar(character)
		
		pcCharacter = str("<:MP_Square:1157462530495619072>" * int(floor(character.pc / pcCharacterMax))) + str("<:MP_Loss_Square:1157462545855168573>" * int(10 - int(floor(character.pc / pcCharacterMax))))

		valueStr = pvCharacter + "\n" + pcCharacter

		if(character == characterTurn):
			embed.add_field(name=str(character) + " - actif", value=valueStr, inline=True)
		else:
			embed.add_field(name=str(character), value=valueStr, inline=True)

	return embed
