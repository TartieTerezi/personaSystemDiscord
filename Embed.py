# -*-coding:utf-8 -*

import discord
from discord.ext import commands
from discord import app_commands

from Element import Element
from Skill import Skill
from Persona import Persona
from Character import Character
from Date import Date

import file

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

def showSkill(skill : Skill):
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
	embed.add_field(name="xp", value=str(persona.xp)+"/"+str(persona.xp), inline=True)
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

def showNewSkill(persona : Persona,newSkill : Skill):
	embed=discord.Embed(title="Nouvelle compétence", description=persona.nom + " a appris la compétence " + newSkill.nom, color=getColorEmbed(persona.element))
	return embed

def getColorEmbed(element):
	rgbColor = Element(element).getColor()
	color = discord.Color.from_rgb(rgbColor[0], rgbColor[1], rgbColor[2])
	return color
