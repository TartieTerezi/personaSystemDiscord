# -*-coding:utf-8 -*

from ast import Num
from curses import halfdelay
from dis import disco
from pickle import FALSE
from re import L
from tkinter import CHAR
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

import random
import sqlite3

import asyncio
import math
import os
import sys

from dotenv import load_dotenv
load_dotenv()


sys.path.append('metier')

#PERSONA,ELEMENT,SKILL
from Element import Element
from Skill import Skill
from Persona import Persona
from Character import Character
from Groupe import Groupe
from Item import *
from Button import Button
from Mechanism import Mechanism
from ProgressBar import ProgressBar
from Dao import Dao

from Lieu import Lieu

#DATE 
from Date import Date

#Embed
import Embed
#file
import file

import utils

listPersonas,listCharacters,date,listItem = file.reset()
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
listLieu = []
groupe = None

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = commands.Bot(command_prefix="$",intents=discord.Intents.all())

# Listerner quand le bot s'allume 
@bot.event
async def on_ready():
	guild_count = 0

	for guild in bot.guilds:
		print(f"- {guild.id} ( nom : {guild.name})")
		guild_count += 1

	print("FrogyCat est dans " + str(guild_count) + " serveurs.")

# Listener quand on envoie un message
@bot.event
async def on_message(message):
	if(message.author.bot == False):
		#print(message.content)
		await bot.process_commands(message)

###### RESET ######

@bot.hybrid_command(name="reset", with_app_command=True, description="Regarde la competence selectionné")
async def _reset(ctx):
	global listSkill
	global listPersonas
	global listCharacters
	global date
	global listItem

	listSkill,listPersonas,listCharacters,date,listItem = file.reset()
	await ctx.send("Update de tout les elements")

###### CHARACTER ######

@bot.hybrid_command(name="stat", with_app_command=True, description="Montre vos statistique")
async def _stat(ctx,user: discord.User = None):
	character = None

	if(user != None):
		character = findCharacterById(listCharacters,user.id)
	else:
		character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		await ctx.send(embed=Embed.showCharacter(character))
	else:
		await ctx.send("aucun character trouvé")

###### PERSONA ######

@bot.hybrid_command(name="statpersona",with_app_command=True, description="montre les stats de votre persona")
async def _statpersona(ctx,user: discord.User = None):
	character = None

	if(user != None):
		character = findCharacterById(listCharacters,user.id)
	else:
		character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		await ctx.send(embed=Embed.showPersona(character.persona))
	else:
		await ctx.send("Aucune persona trouvé.")

@bot.hybrid_command(name="level", with_app_command=True, description="level up")
async def _level(ctx,user: discord.User = None):
	character = None

	if(user != None):
		character = findCharacterById(listCharacters,user.id)
	else:
		character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		character.levelUp()
		character.persona.levelUp()
		await ctx.send(embed=Embed.showPersonaLevelUp(character.persona))
	else:
		await ctx.send("aucun character trouvé")

@bot.hybrid_command(name="xp", with_app_command=True, description="level up")
async def _xp(ctx,xp : int = 0, user: discord.User = None):
	character = None

	if(user != None):
		character = findCharacterById(listCharacters,user.id)
	else:
		character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		character.add_xp(xp)
	else:
		await ctx.send("aucun character trouvé")

###### SKILL ######

@bot.hybrid_command(name="skill", with_app_command=True, description="Regarde la competence selectionné")
async def _skill(ctx, skill_name):
	skill = findSkillByName(listSkill,skill_name)

	if(skill != None):
		await ctx.send(embed=Embed.showSkill(skill))
	else:
		await ctx.send("Aucune attaque trouvé sous le nom de " + str(skill_name))

@bot.hybrid_command(name="skilllist",with_app_command=True, description="Liste des competences")
async def _skillList(ctx,page : int = 1):	
	listSkillPage,listEmojisPage,pageCurrent,maxPage = utils.listToShow(ctx,listSkill,page)

	embed=discord.Embed(title="Liste des compétences " +str(pageCurrent) +"/"+ str(maxPage))
	for oneSkill in listSkillPage:
		embed.add_field(name=oneSkill.nom,value=oneSkill.getCount(), inline=True)
	mess = await ctx.send(embed=embed)

	await utils.setMessageEmotes(mess,listEmojisPage)

	def check(reaction,user):
		return user != mess.author and str(reaction.emoji)

	try:
		isValidEmote,indexValidEmote = await utils.getReaction(bot,mess,listSkillPage)

		if(isValidEmote):
			#embded avec les informations de l'attaque 
			skill = listSkillPage[indexValidEmote]
			await ctx.send(embed=Embed.showSkill(skill))

	except asyncio.TimeoutError:
		await mess.add_reaction('🕐')
	else:
		await mess.delete()

###### PROGRESS BAR ######

@bot.hybrid_command(name="progressbar",with_app_command=True, description="test d'une progress bar / limite de 15")
async def _progressbar(ctx, number : int = 10, first_emote = "🟩", second_emote = "⬜"):
	if(number > 15):
		number = 15

	progress_bar = ProgressBar(ctx,number,first_emote,second_emote)

	while(not await progress_bar.add()):
		pass

	del progress_bar

###### LIEU ######

@bot.hybrid_command(name="startdonjon",with_app_command=True,description="Entre dans un donjon.")
async def _startdonjon(ctx):
	global groupe

	category = await ctx.guild.create_category("Donjon -  RDC")

	newLieu = Lieu(category)

	await newLieu.category.set_permissions(ctx.guild.roles[0],read_messages=False)

	await newLieu.newPiece("Premiere pièce","```ansi\n Salle blanche vide, une [2;40m[2;37mporte blanche [0m[2;40m[0ms'y trouve  ainsi qu'une trappe.\n```")
	await newLieu.newPiece("Deuxieme pièce","```ansi\n Une deuxieme pièce blanche sans trait particulier, outre deux porte, une [2;40m[2;37mporte blanche [0m[2;40m[0m et une [2;35mporte rose[0m.\n```")
	await newLieu.newPiece("Troisième pièce","```ansi\n [0;2mEncore une pièce blanche avec deux portes, une [0;35mporte rose[0m et une [0;31mporte rouge[0m.[0m. \n```")
	await newLieu.newPiece("Quatrieme pièce","```ansi\n [0;2mEncore une pièce blanche avec trois portes, une [0;34mporte bleu [0met une [0;31mporte rouge[0m, ainsi qu'une [0;32m[0;32mporte verte[0m[0;32m[0m.[0m.\n```")
	await newLieu.newPiece("Pipi Room","```ansi\n [0;2mdes toilette pour ses besoin primordiaux, une [0;32mporte verte[0m permet de retourner en arrière.[0m \n```")
	await newLieu.newPiece("Zone de fin","```ansi\n Cette zone est probablement la fin, il s'y trouve juste la [2;34mporte bleu [0mpour revenir en arrière.\n```")
	await newLieu.newPiece("Sous-sol-1","```ansi\n Salle blanche avec un petit interrupteur autrement seul une trappe se trouve ici.\n```")
	await newLieu.newPiece("Sous-sol-2","```ansi\n Salle blanche avec un petit interrupteur autrement seul une trappe se trouve ici.\n```")


	newLieu.pieces[0].links([newLieu.pieces[1],newLieu.pieces[6]],["Porte blanche","Trappe"])
	newLieu.pieces[1].links([newLieu.pieces[0],newLieu.pieces[2]],["Porte blanche","Porte rose"])
	newLieu.pieces[2].links([newLieu.pieces[1],newLieu.pieces[3]],["Porte rose","Porte rouge"])
	newLieu.pieces[3].links([newLieu.pieces[2],newLieu.pieces[4],newLieu.pieces[5],newLieu.pieces[7]],["Porte rouge","Porte verte","Porte bleu","Trappe"])
	newLieu.pieces[4].link(newLieu.pieces[3],["Porte verte"])
	newLieu.pieces[5].link(newLieu.pieces[3],["Porte bleu"])
	newLieu.pieces[6].link(newLieu.pieces[0],["Trappe"])
	newLieu.pieces[7].link(newLieu.pieces[3],["Trappe"])

	mecanismFirstDoor = Mechanism(0,"mecha_0")
	mecanismSecondDoor = Mechanism(1,"mecha_1")

	newLieu.pieces[0].lockedByMechanism.append(mecanismFirstDoor) #"gestion des mechanism"
	newLieu.pieces[0].lockedByMechanism.append(None)

	buttonSwich = Button(0,"bouton",mechanism=[mecanismFirstDoor])
	newLieu.pieces[6].objects.append(buttonSwich)

	if(groupe!=None):
		character = findCharacterById(listCharacters,ctx.author.id)
		if(groupe.searchPlayer(character)):
			for joueur in groupe.joueurs:
				userPlayer = bot.get_user(joueur.id)
				await newLieu.pieces[0].autorize(userPlayer)

	else:
		await newLieu.pieces[0].autorize(ctx.author)

	global listLieu
	listLieu.append(newLieu)

@bot.hybrid_command(name="joindonjon",with_app_command=True,description="Rejoins le donjon.")
async def _joindonjon(ctx):
	if(len(listLieu) > 0):
		await listLieu[0].pieces[0].autorize(ctx.author)

@bot.hybrid_command(name="use",with_app_command=True,description="utilise un objet dans la salle.")
async def _use(ctx,objectname):
	global listLieu
	channel = ctx.channel
	user = ctx.author
	character = findCharacterById(listCharacters,user.id)
	currentPiece = None

	for piece in listLieu[0].pieces:
		if(piece.channel == channel):
			currentPiece = piece

	if(character == None):
		await ctx.send("Tu n'es pas un joueur :c")
		return

	if(currentPiece == None):
		await ctx.send("Ce n'est pas un channel rp.")
		return

	for oneObject in currentPiece.objects:
		if(oneObject.nom == objectname):
			oneObject.use()

			await ctx.send(oneObject.nom+ " est utilisé")
			return

	await ctx.send("Aucun objet trouvé sous le nom de "+ str(objectname)+ " dans la salle.")

@bot.hybrid_command(name="passe",with_app_command=True,description="passe dans une autre salle.")
async def _passenextpiece(ctx):
	global listLieu
	global groupe
	channel = ctx.channel
	user = ctx.author
	character = findCharacterById(listCharacters,user.id)
	currentPiece = None

	for piece in listLieu[0].pieces:
		if(piece.channel == channel):
			currentPiece = piece

	if(character == None):
		await ctx.send("Tu n'es pas un joueur :c")
		return

	if(currentPiece == None):
		await ctx.send("Ce n'est pas un channel rp.")
		return

	if(len(currentPiece.nextRooms)==1):
		if(groupe != None):
			character = findCharacterById(listCharacters,user.id)
			if(groupe.searchPlayer(character)):
				for joueur in groupe.joueurs:
					userPlayer = bot.get_user(joueur.id)
					await currentPiece.inautorize(userPlayer)
					await currentPiece.nextRooms[0].autorize(userPlayer)

					
				await ctx.channel.send(groupe.nom + " se deplacent.")
				await ctx.message.delete()
				await currentPiece.nextRooms[0].channel.send(groupe.nom + " arrivent ici.")
				return

		await currentPiece.inautorize(user)
		await currentPiece.nextRooms[0].autorize(user)

		await ctx.channel.send(character.prenom + " se deplace.")
		await ctx.message.delete()
		await currentPiece.nextRooms[0].channel.send(character.prenom + " arrive ici.")
	elif(len(currentPiece.nextRooms)==0):
		await ctx.send("impossible d'aller autre part.")
	else:
		options = []

		for i in range(len(currentPiece.nextRooms)):
			nameRoom = ""
			if(currentPiece.nextRooms[i].isAlreadyVisited(user)):
				nameRoom = currentPiece.nextRooms[i].channel.name
			else:
				nameRoom = "???"

			options.append(discord.SelectOption(label=nameRoom,value=currentPiece.nextRooms[i].channel.name,emoji="✨",description=currentPiece.descriptionsNextRooms[i]))


		async def my_callback(interaction):
			a = 0
			for nextRoom in currentPiece.nextRooms:
				if(nextRoom.channel.name == select.values[0]):
					await interaction.response.defer()

					#gestion des méchanismes
					#for i in range(len(nextRoom.lockedByMechanism)):
					#	if(nextRoom.lockedByMechanism[i].isActive == False):
					#		await interaction.followup.edit_message(interaction.message.id,content=str("Impossible de se déplacer,"+nextRoom.descriptionsNextRooms[a]+" est bloqué."), view=None)
					#		return          

					if(nextRoom.lockedByMechanism[a] != None):
						if(nextRoom.lockedByMechanism[a].isActive == False):
								await interaction.followup.edit_message(interaction.message.id,content=str("Impossible de se déplacer,"+nextRoom.descriptionsNextRooms[a]+" est bloqué."), view=None)
								return

					character = findCharacterById(listCharacters,user.id)

					#gestion du groupe
					if(groupe != None):
						
						if(groupe.searchPlayer(character)):
							for joueur in groupe.joueurs:

								userPlayer = bot.get_user(joueur.id)
								await currentPiece.inautorize(userPlayer)
								await nextRoom.autorize(userPlayer)

							await interaction.followup.edit_message(interaction.message.id,content=groupe.nom + " se deplace.", view=None)

							await ctx.message.delete()

							await nextRoom.channel.send(groupe.nom + " arrive ici.")
						else:
							await interaction.followup.edit_message(interaction.message.id,content=character.prenom + " se deplace.", view=None)
							await currentPiece.inautorize(user)
							await nextRoom.autorize(user)
							
							await ctx.message.delete()

							await nextRoom.channel.send(character.prenom + " arrive ici.")
					else:
						await interaction.followup.edit_message(interaction.message.id,content=character.prenom + " se deplace.", view=None)
						await currentPiece.inautorize(user)
						await nextRoom.autorize(user)
						await ctx.message.delete()

						await nextRoom.channel.send(character.prenom + " arrive ici.")

					return
				a+=1

		select = discord.ui.Select(placeholder="Prochaine destination : ",options=options)
		select.callback = my_callback
		view = discord.ui.View()
		view.add_item(select)

		await ctx.send(view=view)

async def protecCommandeAdmin(ctx):
	if(ctx.author.id != 996365971130425385):
		await ctx.author.send("Mon reuf, tu essaies de faire quoi ?")
		await ctx.message.delete()
		return False
	else:
		return True

@bot.hybrid_command(name="suppr",with_app_command=True,description="supprime les channel et la catgeorie lie.")
async def _suppr(ctx):
	if(await protecCommandeAdmin(ctx) == False):
		return
	
	categorie = ctx.channel.category
	listChannels = categorie.channels

	for channel in listChannels:
		await channel.delete()

	await categorie.delete()

###### GROUPE ######

@bot.hybrid_command(name="creategroupe",with_app_command=True, description="Cree un groupe et vous place en leader")
async def _creategroupe(ctx,name):
	global groupe 
	groupe = Groupe(name,findCharacterById(listCharacters,ctx.author.id))

	await ctx.send("Groupe cree sous le nom de "+name)

@bot.hybrid_command(name="startgroupe",with_app_command=True, description="Permet a d'autres personnes de rejoindre")
async def _startgroupe(ctx):

	if(groupe == None):
		await ctx.send("aucun groupe existant")
		return

	if(groupe.leader.id != ctx.author.id):
		await ctx.send("Vous n'etes pas le leader du groupe")
		return

	messGroupe = await ctx.send("Attente des membres du groupe...",embed=Embed.showGroupe(groupe))
	await messGroupe.add_reaction('👋')

	isFinish = False

	while(isFinish == False):
		def check(reaction,user):
			return user != ctx.author

		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)
		except asyncio.TimeoutError:
			await messGroupe.edit(content="fin de selection des membres",embed=Embed.showGroupe(groupe))
			await messGroupe.add_reaction('🕐')
			isFinish = True
		else:
			character = findCharacterById(listCharacters,user.id)
			if(character != None):
				haveRejoind = groupe.addPlayer(character)
				if(haveRejoind):
					#await ctx.send(character.nom + " a rejoint le groupe")
					await messGroupe.edit(content="Attente des membres du groupe...",embed=Embed.showGroupe(groupe))

					if(len(groupe.joueurs) >= 4):
						isFinish = True
						await ctx.send("Groupe complet")
				else:

					await ctx.send("Vous ne pouvez pas rejoindre le groupe")
			else:
				pass

@bot.hybrid_command(name="statgroupe",with_app_command=True, description="Affiche les infos du groupe")
async def _statgroupe(ctx):
	if(groupe == None):
		await ctx.send("aucun groupe existant")
		return

	await ctx.send(embed=Embed.showGroupe(groupe))

@bot.hybrid_command(name="quitgroupe",with_app_command=True, description="Quitte le groupe")
async def _quitgroupe(ctx):
	if(groupe == None):
		await ctx.send("aucun groupe existant")
		return

	if(groupe.leader.id == ctx.author.id):
		await ctx.send("Vous etes le leader du groupe")
		return

	player = findCharacterById(listCharacters,ctx.author.id)

	if(player == None):
		await ctx.send("Pas un joueur valide")
		return

	if(groupe.removePlayer(player)):
		await ctx.send(str(player) + " quitte le groupe") 


@bot.hybrid_command(name="tag",with_app_command=True, description="quitte le groupe")
async def _tag(ctx, user : discord.Member):
	if(groupe == None):
		await ctx.send("aucun groupe existant")
		return

	if(groupe.leader.id == ctx.author.id):
		if(not groupe.tag(findCharacterById(listCharacters,user.id))):
			await ctx.send("Personnage pas dans le groupe")
	else:
		await ctx.send("Vous n'etes pas le leader du groupe")
		return

###### FIGHT ######

def getCharacters(listUsersId,listCharacters):
	Characters = []

	for oneCharacter in listCharacters:
		for oneUser in listUsersId:
			if(oneCharacter.id == oneUser):
				Characters.append(oneCharacter)

	return Characters

class viewFight(discord.ui.View): # Create a class called viewFight that subclasses discord.ui.View
	def __init__(self,characterTurn):
		super().__init__()
		self.add_item(discord.ui.Button(label="Attaque", style=discord.ButtonStyle.danger, emoji="⚔️"))
		self.add_item(discord.ui.Button(label="Persona", style=discord.ButtonStyle.blurple, emoji="🎭"))
		self.add_item(discord.ui.Button(label="Objets", style=discord.ButtonStyle.green,emoji="💊"))
		self.add_item(discord.ui.Button(label="Garde", style=discord.ButtonStyle.secondary, emoji="🛡️"))
		#self.add_item(discord.ui.Button(label="Fuite", style=discord.ButtonStyle.secondary,emoji="↪️"))
		self.choice = None
		self.characterTurn = characterTurn

		async def attaque(interaction):
			if(self.characterTurn.id == interaction.user.id):
				await interaction.response.send_message("Attaque")
				self.choice = 0
				self.stop()

		async def persona(interaction):
			if(self.characterTurn.id == interaction.user.id):
				await interaction.response.send_message("persona")
				self.choice = 1
				self.stop()

		async def objet(interaction):
			if(self.characterTurn.id == interaction.user.id):
				await interaction.response.send_message("objet")
				self.choice = 2
				self.stop()

		async def garde(interaction):
			if(self.characterTurn.id == interaction.user.id):
				await interaction.response.send_message("garde")
				self.choice = 3
				self.stop()

		self.children[0].callback = attaque
		self.children[1].callback = persona
		self.children[2].callback = objet
		self.children[3].callback = garde

class SelectEnnemie(discord.ui.Select):
	def __init__(self,listEnnemis):
		self.choice = None
		options = []

		for i in range(len(listEnnemis)):
			ennemi = listEnnemis[i]
			
			options.append(discord.SelectOption(label=str(ennemi),value=i))

		super().__init__(placeholder="Qui attaquer ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = int(self.values[0])
		self.view.stop()

class viewSelectEnnemie(discord.ui.View):
	def __init__(self,listEnnemis,characterTurn):
		super().__init__()
		self.characterTurn = characterTurn
		self.add_item(SelectEnnemie(listEnnemis))

@bot.hybrid_command(name="startfightmob",with_app_command=True, description="Initie un combat contre un mob")
async def _startfightmob(ctx):

	idUsers = [ctx.author.id]
	charactersToFight = []
		
	turn = 0 #permet de choisir le tour du joueurs

	#determine qui dois jouer 
	listeTurnCharacter = []
	
	allie = []
	allie = getCharacters(idUsers,listCharacters)

	ennemi = []
	ennemi.append(listCharacters[3])
	ennemi.append(listCharacters[5])

	for i in range(len(ennemi)):
		charactersToFight.append(ennemi[i])

	for i in range(len(allie)):
		charactersToFight.append(allie[i])

	while len(charactersToFight)>0:
		tempCharacter = charactersToFight[0]
		for oneCharacter in charactersToFight:
			if(tempCharacter.persona.agilite<oneCharacter.persona.agilite):
				tempCharacter = oneCharacter

		charactersToFight.remove(tempCharacter)
		listeTurnCharacter.append(tempCharacter)


		#ajoute les emojis en fonction du nombre d'ennemis
		characterTargetemotes = []
			
		for emoteIndex in range(len(ennemi)):
			characterTargetemotes.append(emojis[emoteIndex])		

	isFight = True
	while isFight:
		try:
			characterTurn = listeTurnCharacter[turn] # recupère le joueur qui joue pour ce tour
			#characterTarget = listeTurnCharacter[(turn+1)%len(listeTurnCharacter)] # recupère le joueur va subir les degats ( a changer )

			#regarde si c'est le tour d'un ennemis
			turnEnnemi = False

			for oneCharacter in ennemi:
				if(characterTurn == oneCharacter):
					turnEnnemi = True

			if(turnEnnemi):
				await ctx.send("tour de l'ennemi " + characterTurn.nom)
				pass
				#ici qu'on gère les tours du joueur
			else:
				view = viewFight(characterTurn)
				mess = await ctx.send(embed=Embed.showFight(listeTurnCharacter[turn],allie,ennemi),view=view)

				await view.wait() 

				indexValidEmote = view.choice
				isValidEmote = True

				if(isValidEmote): 
					if(indexValidEmote==4):
						isFight = False
					else:
						if(indexValidEmote==0):
							isValidEmote = False
							characterTarget = None

							#choisis le personnge a	toucher 
							if(len(ennemi)==1):
								isValidEmote = True
								characterTarget = ennemi[0]
							else:

								view = viewSelectEnnemie(ennemi,characterTurn)

								messChoiceEnnemi = await ctx.send(embed=Embed.showListEnnemis(ennemi),view=view)

								await view.wait() 

								if(view.choice != None):
									isValidEmote = True
									characterTarget = ennemi[view.choice]

								#characterTarget = ennemi[indexEmote]

							if(isValidEmote):
								print(characterTarget)
								damage = characterTurn.attack()

								damage = characterTarget.takeDamage(damage)
							
								await ctx.send(content=str("```diff\n- [ "+characterTarget.prenom+" perd "+str(damage)+" PV ]\n```"))

								#await ctx.send(content=str(characterTurn.prenom)+" a infligé "+ str(damage) +" dommage "+ str(characterTarget.prenom))				

						elif(indexValidEmote==1):
							nextStepSkill = False
							while(nextStepSkill == False):
								listSkillPage,listEmojisPage,pageCurrent,maxPage = utils.listToShow(ctx,characterTurn.persona.skills,1)
								embed=discord.Embed(title="Liste des compétences")
							
								for i in range(len(listSkillPage)):
									embed.add_field(name=str(i+1) +" " + listSkillPage[i].nom,value=listSkillPage[i].getCount(), inline=True)
							
								messSkills = await ctx.send(embed=embed)
								await utils.setMessageEmotes(messSkills,listEmojisPage)
							
								isValidEmote = False
								indexValidEmote = 0


								while(isValidEmote == False):
									reaction,user = await bot.wait_for('reaction_add',check=check2)
							
									for indexEmote in range(len(listEmojisPage)):
										if(str(listEmojisPage[indexEmote]) == str(reaction) and user):
											if(characterTurn.id == user.id):
												isValidEmote = True
												indexValidEmote = indexEmote

									if(isValidEmote):
										skill = listSkillPage[indexValidEmote]

										#choisis le personnge a	toucher 
										if(len(ennemi)==1):
											isValidEmote = True
											characterTarget = ennemi[0]
										else:
											messChoiceEnnemi = await ctx.send(embed=Embed.showListEnnemis(ennemi))
											await utils.setMessageEmotes(messChoiceEnnemi,characterTargetemotes)

											reaction,user = await bot.wait_for('reaction_add',check=check2)
							
											isValidEmote = False

											for indexEmote in range(len(characterTargetemotes)):
												if(str(characterTargetemotes[indexEmote]) == str(reaction) and user):
													if(characterTurn.id == user.id):
														isValidEmote = True
														indexValidEmote = indexEmote

														characterTarget = ennemi[indexEmote]

											
														
										if(isValidEmote):
											#embded avec les informations de l'attaque 
											

											damage = characterTurn.attackSkill(skill)

											#differencie si c'est un skill physique ou non
											if(skill.element == Element.PHYSIQUE):
												cout = int(characterTurn.maxPv * skill.cout / 100)

												if(characterTurn.pv - cout >= 0):
													nextStepSkill = True
													characterTurn.pv -= cout

													damage = characterTarget.takeDamage(damage,skill)
										
													await ctx.send(content=str("```diff\n  [ "+characterTurn.prenom+" lance l'attaque "+skill.nom+" ]\n```"))
													await ctx.send(content=str("```diff\n- [ "+characterTarget.prenom+" perdu "+str(damage)+" PV a cause de "+skill.nom+" ]\n```"))
												else:
													await ctx.send("Pas assez de Pv pour lancer "+ str(skill.nom))
											else:
												if(characterTurn.pc - skill.cout >= 0):
													nextStepSkill = True
													characterTurn.pc -= skill.cout

													damage = characterTarget.takeDamage(damage,skill)
										
													await ctx.send(content=str("```diff\n  [ "+characterTurn.prenom+" lance l'attaque "+skill.nom+" ]\n```"))
													await ctx.send(content=str("```diff\n- [ "+characterTarget.prenom+" perdu "+str(damage)+" PV a cause de "+skill.nom+" ]\n```"))
												else:
													await ctx.send("Pas assez de pc pour lancer "+ str(skill.nom))

						elif(indexValidEmote==2):
							pass 
						elif(indexValidEmote==3):
							characterTurn.isProtect = True
							await ctx.send(content=str(characterTurn.prenom)+ " se met sur ses gardes.")


			#a la fin du tour, regarde si les joueurs sont toujours en vie		
			for i in range(len(listeTurnCharacter)):
				nbrCaracrs = len(listeTurnCharacter) - i - 1
				if(listeTurnCharacter[nbrCaracrs].pv <= 0):
					listeTurnCharacter[nbrCaracrs].pv = 1
					await ctx.send(str(listeTurnCharacter[nbrCaracrs].nom)+" a perdu le combat")

					for x in range(len(ennemi)):
						nbrEnnemi = len(ennemi) - x - 1

						if(listeTurnCharacter[nbrCaracrs] == ennemi[nbrEnnemi]):

							listeTurnCharacter.pop(nbrCaracrs)
							ennemi.pop(nbrEnnemi)
							characterTargetemotes.pop(-1)
							break
							

			if(len(ennemi) <= 0):
				isFight = False

			if(isFight):
				# prochain tour
				#await ctx.send(str(indexValidEmote)+ " de "+ listeTurnCharacter[turn].prenom)
				turn = (turn + 1) % len(listeTurnCharacter)

		except asyncio.TimeoutError:
			raise e
		else:
			pass

	pass

###### ONYX ######

def Roll(nb,jet):
	score = []
	for i in range(nb):
		score.append(random.randint(1,jet))
	return score

def reussite(chiffre,nb_max):
	taux = int((nb_max * 5) / 100) - 1 #calcule le taux critique

	if chiffre == nb_max:
		return "\n**Échec Parfait** ! Aïe, coup dur."
	elif chiffre == 1:
		return "\n**Réussite Parfaite** ! GG WP !"
	elif chiffre >= (nb_max - taux):
		return "\nÉchec **Critique**. Ça picote un peu."
	elif chiffre <= (1 + taux):
		return "\nRéussite **Critique**. Bien joué !"
	else:
		return ""

@bot.hybrid_command(name="roll", with_app_command=True,description="Lancer de dé(s)")
async def _roll(ctx,nb_dice = 1,nb_max = 100):
	score_final = Roll(int(nb_dice),int(nb_max))
	message = f'Résultat des jets de {ctx.author.mention} : {score_final}'
	
	if int(nb_dice) == 1 and nb_max>=20:
		message += reussite(score_final[0],nb_max)

	message += "``` ```"
	await ctx.send(message)

###### THREADS ######

@bot.event
async def on_thread_create(thread):
	mj = discord.utils.get(thread.parent.guild.roles,name="MJ")
	spectacteur = discord.utils.get(thread.parent.guild.roles, name="Spectateur")

	pingThreads = await thread.send(mj.mention+ " " + spectacteur.mention)
	await pingThreads.delete()

##### NOUVEAU MEMBRE ####

@bot.event 
async def on_member_join(member):
	result = Dao.getOneDataBdd("SELECT * FROM RoleLinkUser where id = ?",[member.id])

	memberRole = None 

	if(result == None):
		memberRole = await member.guild.create_role(name=str(member))
		Dao.insert("INSERT INTO RoleLinkUser VALUES (?,?)",[member.id,memberRole.id])
		await memberRole.edit(position=(len(member.guild.roles)-3))
	else:
		memberRole = discord.utils.get(member.guild.roles,id=result[1])

	if(memberRole != None):
		await member.add_roles(memberRole)

@bot.event 
async def on_member_remove(member):
	pass

@bot.hybrid_command(name="setcolor", with_app_command=True,description="Change la couleur de ton role")
async def _setcolor(ctx, red : int,green : int, blue : int, user : discord.Member = None):
	color = discord.Color.from_rgb(red,green,blue)

	memberRole = None 
	result = None

	if(user == None):
		user = ctx.author
	else:
		if(await protecCommandeAdmin(ctx) == False):
			return
	
	result = Dao.getOneDataBdd("SELECT * FROM RoleLinkUser where id = ?",[user.id])

	if(result == None):
		print("pas de pupuce trouvé")
		memberRole = await ctx.author.guild.create_role(name=str(user))
		Dao.insert("INSERT INTO RoleLinkUser VALUES (?,?)",[user.id,memberRole.id])
		await user.add_roles(memberRole)
		await memberRole.edit(position=(len(ctx.guild.roles)-3))
	else:
		memberRole = discord.utils.get(ctx.author.guild.roles,id=result[1])
	
	await memberRole.edit(colour = color)

@bot.hybrid_command(name="setname", with_app_command=True,description="Change le nom de ton role")
async def _setcolor(ctx, nom : str,user : discord.Member = None):
	memberRole = None 
	result = None

	if(user == None):
		user = ctx.author
	else:
		if(await protecCommandeAdmin(ctx) == False):
			return

	result = Dao.getOneDataBdd("SELECT * FROM RoleLinkUser where id = ?",[user.id])

	if(result == None):
		memberRole = await ctx.author.guild.create_role(name=str(user))
		Dao.insert("INSERT INTO RoleLinkUser VALUES (?,?)",[user.id,memberRole.id])
		await user.add_roles(memberRole)
		await memberRole.edit(position=(len(ctx.guild.roles)-3))
	else:
		memberRole = discord.utils.get(user.guild.roles,id=result[1])
	
	await memberRole.edit(name = nom)

###### OTHER ######

@bot.command(name="sync")
async def _sync(ctx):
    fmt = await ctx.bot.tree.sync()
    await ctx.channel.send(f"Synchronisation {len(fmt)} commandes a ce serveur.")

def findSkillByName(listeSkills,nameSkill):
	for oneSkill in listeSkills:
		if(oneSkill.nom == nameSkill):
			return oneSkill
	return None

def findCharacterById(listeCharacters,index):
	for oneCharacter in listCharacters:
		if(index == oneCharacter.id):
			return oneCharacter
	return None

bot.run(os.getenv("TOKEN"))