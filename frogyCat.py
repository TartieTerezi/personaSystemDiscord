# -*-coding:utf-8 -*

from curses import halfdelay
from pickle import FALSE
from tkinter import CHAR
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

import random

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

from Lieu import Lieu

#DATE 
from Date import Date

#Embed
import Embed
#file
import file

import utils

listSkill,listPersonas,listCharacters,date,listItem = file.reset()
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
		#print(message)
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

@bot.hybrid_command(name="addcharacter", with_app_command=True, description="Ajoute un nouveau character si vous n'en avez pas déjà un.")
async def _addcharacter(ctx,nom,prenom,pv,pc,idauthor=0):
	if(idAuthor!=0):
		character = findCharacterById(listCharacters,idAuthor)
		if(character != None):
			await ctx.send("Character déjà existant")
			return

	character = findCharacterById(listCharacters,ctx.author.id)

	if(character == None):
		newCharacter = Character(ctx.author.id,nom,prenom,None,pv,pc)

		listCharacters.append(newCharacter)
		file.newCharacter(newCharacter)

		await ctx.send("Nouveau character")
	else:
		await ctx.send("Character déjà existant")

###### PERSONA ######

@bot.hybrid_command(name="level", with_app_command=True, description="level up vos person")
async def _level(ctx):
	character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		character.persona.levelUp()
		await ctx.send(embed=Embed.showPersonaLevelUp(character.persona))
	else:
		await ctx.send("aucun character trouvé")

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

###### LIEU ######

@bot.hybrid_command(name="createchannel",with_app_command=True,description="Creer un channel avec son nom")
async def _createchannel(ctx,arg,name,description_lieu,name_category=""):
	if(arg == "category"):
		await ctx.guild.create_category(name)
	elif(arg == "channel"):
		channel = None
		guild = ctx.message.guild

		if(name_category == ""):
			channel = await guild.create_text_channel(name)
		else:
			isInCategory = False
			for categorie in ctx.guild.categories:
				if(categorie.name == name_category):
					isInCategory = True
					channel = await categorie.create_text_channel(name)

			if(isInCategory == False):
				channel = await ctx.send("Aucune categorie trouvé sous le nom de "+ str(name))
				return

		nouveauLieu = Lieu(channel,description_lieu,False)
		await nouveauLieu.sendMessage(nouveauLieu.description)
		listLieu.append(nouveauLieu)
		listLieu.objects.append(listItem[0])

@bot.hybrid_command(name="startdonjon",with_app_command=True,description="Entre dans un donjon.")
async def _startdonjon(ctx):
	global groupe

	category = await ctx.guild.create_category("Donjon")

	progressBar = await startprogressbar(ctx,7)

	newLieu = Lieu(category)

	await newLieu.newPiece("Premiere pièce","```ansi\n Salle blanche vide, une [2;40m[2;37mporte blanche [0m[2;40m[0ms'y trouve  ainsi qu'une trappe.\n```")
	await newLieu.newPiece("Deuxieme pièce","```ansi\n Une deuxieme pièce blanche sans trait particulier, outre deux porte, une [2;40m[2;37mporte blanche [0m[2;40m[0m et une [2;35mporte rose[0m.\n```")
	await addprogressbar(progressBar,7,1)
	await newLieu.newPiece("Troisième pièce","```ansi\n [0;2mEncore une pièce blanche avec deux portes, une [0;35mporte rose[0m et une [0;31mporte rouge[0m.[0m. \n```")
	
	await newLieu.newPiece("Quatrieme pièce","```ansi\n [0;2mEncore une pièce blanche avec trois portes, une [0;34mporte bleu [0met une [0;31mporte rouge[0m, ainsi qu'une [0;32m[0;32mporte verte[0m[0;32m[0m.[0m.\n```")
	await addprogressbar(progressBar,7,2)
	
	await newLieu.newPiece("Pipi Room","```ansi\n [0;2mdes toilette pour ses besoin primordiaux, une [0;32mporte verte[0m permet de retourner en arrière.[0m \n```")
	await newLieu.newPiece("Zone de fin","```ansi\n Cette zone est probablement la fin, il s'y trouve juste la [2;34mporte bleu [0mpour revenir en arrière.\n```")
	
	await addprogressbar(progressBar,7,3)

	await newLieu.newPiece("Sous sol","```ansi\n Salle blanche vide, Seul une trappe se trouve ici.\n```")

	newLieu.pieces[0].links([newLieu.pieces[1],newLieu.pieces[6]],["Porte blanche","Trappe"])

	await addprogressbar(progressBar,7,4)

	newLieu.pieces[1].links([newLieu.pieces[0],newLieu.pieces[2]],["Porte blanche","Porte rose"])
	newLieu.pieces[2].links([newLieu.pieces[1],newLieu.pieces[3]],["Porte rose","Porte rouge"])

	await addprogressbar(progressBar,7,5)

	newLieu.pieces[3].links([newLieu.pieces[2],newLieu.pieces[4],newLieu.pieces[5]],["Porte rouge","Porte verte","Porte bleu"])
	newLieu.pieces[4].link(newLieu.pieces[3],["Porte verte"])

	await addprogressbar(progressBar,7,6)

	newLieu.pieces[5].link(newLieu.pieces[3],["Porte bleu"])
	newLieu.pieces[6].link(newLieu.pieces[0],["Trappe"])

	await addprogressbar(progressBar,7,7)

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

				return

		await currentPiece.inautorize(user)
		await currentPiece.nextRooms[0].autorize(user)
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
			for nextRoom in currentPiece.nextRooms:
				if(nextRoom.channel.name == select.values[0]):
					await interaction.response.defer()

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

		select = discord.ui.Select(placeholder="Prochaine destination : ",options=options)
		select.callback = my_callback
		view = discord.ui.View()
		view.add_item(select)

		await ctx.send(view=view)
			
@bot.hybrid_command(name="suppr",with_app_command=True,description="supprime les channel et la catgeorie lie.")
async def _suppr(ctx):
	if(ctx.author.id != 996365971130425385):
		await ctx.author.send("Mon reuf, tu essaies de faire quoi ?")
		await ctx.message.delete()
		return

	categorie = ctx.channel.category
	listChannels = categorie.channels

	for channel in listChannels:
		await channel.delete()

	await categorie.delete()

###### ITEM ######

@bot.hybrid_command(name="take",with_app_command=True,description="Prendre un objet s'il est proche")
async def _take(ctx,objettotake):
	#for unLieu in listLieu:
	#	if(ctx.message)

	for item in listItem:
		if(item.nom == objettotake):

			for oneCharacter in listCharacters:
				if(ctx.author.id == oneCharacter.id):

					isFind = True

					oneCharacter.add_item(item)
					await ctx.send("vous rammassez l'objet "+ str(item.nom))
					return

	await ctx.send("Ce objet est introuvable")

@bot.hybrid_command(name="inventaire",with_app_command=True,description="Montre votre inventaire")
async def _inventaire(ctx):
	for oneCharacter in listCharacters:
		if(ctx.author.id == oneCharacter.id):

			for oneItem in oneCharacter.inventaire:
				await ctx.send(str(oneItem.nom) + " x" + str(oneCharacter.inventaire[oneItem]))

###### GROUPE ######

@bot.hybrid_command(name="creategroupe",with_app_command=True, description="Cree un groupe d'autres personnes de rejoindre")
async def _creategroupe(ctx,name):
	global groupe 
	groupe = Groupe(name,findCharacterById(listCharacters,ctx.author.id))

	await ctx.send("Groupe cree sous le nom de "+name)

@bot.hybrid_command(name="startgroupe",with_app_command=True, description="Cree un groupe d'autres personnes de rejoindre")
async def _startgroupe(ctx):

	if(groupe == None):
		await ctx.send("aucun groupe existant")
		return

	if(groupe.leader.id != ctx.author.id):
		await ctx.send("Vous n'etes pas le leader du groupe")
		return

	messGroupe = await ctx.send("Attente des membres du groupe...")
	await messGroupe.add_reaction('👋')

	isFinish = False

	while(isFinish == False):
		def check(reaction,user):
			return user != ctx.author

		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)
		except asyncio.TimeoutError:
			await messGroupe.edit(content="fin de selection des membres")
			await messGroupe.add_reaction('🕐')
			isFinish = True
		else:
			character = findCharacterById(listCharacters,user.id)
			if(character != None):
				haveRejoind = groupe.addPlayer(character)
				if(haveRejoind):
					await ctx.send(character.nom + " a rejoint le groupe")

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

###### FIGHT ######

@bot.hybrid_command(name="startfightmob",with_app_command=True, description="Initie un combat contre un mob")
async def _startfightmob(ctx):
	pass


@bot.hybrid_command(name="startfight",with_app_command=True, description="Initie un combat")
async def _startfight(ctx):
	mess = await ctx.send("Attente de l'adversaire...")
	await mess.add_reaction('🆚')

	def check(reaction,user):
		return user != ctx.author

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)
	except asyncio.TimeoutError:
		await mess.edit(content="Aucun adversaire trouvé")
		await mess.add_reaction('🕐')
	else:
		charactersToFight = []
		idUsers = [ctx.author.id,user.id]

		for oneCharacter in listCharacters:
			for oneUser in idUsers:
				if(oneCharacter.id == oneUser):
					charactersToFight.append(oneCharacter)

		await mess.edit(content=str(charactersToFight[0].nom + " " + charactersToFight[0].prenom)+" VS " + str(charactersToFight[1].nom + " "+ charactersToFight[1].prenom))
		await mess.clear_reactions()
		
		emojisFight = ['1️⃣','2️⃣','3️⃣','4️⃣','🛑']
		def check2(reaction,user):
			return user and str(reaction.emoji)
		
		turn = 0 #permet de choisir le tour du joueurs

		#determine qui dois jouer 
		listeTurnCharacter = []
		
		while len(charactersToFight)>0:
			tempCharacter = charactersToFight[0]
			for oneCharaceter in charactersToFight:
				if(tempCharacter.persona.agilite<oneCharacter.persona.agilite):
					tempCharacter = oneCharacter

			charactersToFight.remove(tempCharacter)
			listeTurnCharacter.append(tempCharacter)

		await mess.edit(embed=Embed.showFight(listeTurnCharacter[turn]))
		isFight = True
		while isFight:
			try:
				await utils.setMessageEmotes(mess,emojisFight)

				reaction,user = await bot.wait_for('reaction_add',check=check2)
				#debut du tour, determine qui dois jouer 

				#One Attaque Normal
				#Two Persona
				#Three Items 
				#Four Defense

				isValidEmote = False
				indexValidEmote = 0
				characterTurn = listeTurnCharacter[turn] # recupère le joueur qui joue pour ce tour
				characterTarget = listeTurnCharacter[(turn+1)%len(listeTurnCharacter)] # recupère le joueur va subir les degats ( a changer )

				for indexEmote in range(len(emojisFight)):
					if(str(emojisFight[indexEmote]) == str(reaction) and user):
						if(characterTurn.id == user.id):
							isValidEmote = True
							indexValidEmote = indexEmote

				if(isValidEmote): 
					await mess.clear_reactions()


					if(indexValidEmote==4):
						isFight = False
					else:
						if(indexValidEmote==0):
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
										#embded avec les informations de l'attaque 
										skill = listSkillPage[indexValidEmote]

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
							if(listeTurnCharacter[i].pv <= 0):
								isFight = False
								listeTurnCharacter[i].pv = 1
								await ctx.send(str(listeTurnCharacter[i].nom)+" a perdu le combat")


						if(isFight):
							# prochain tour
							#await ctx.send(str(indexValidEmote)+ " de "+ listeTurnCharacter[turn].prenom)
							turn = (turn + 1) % len(listeTurnCharacter)
							mess = await ctx.send(embed=Embed.showFight(listeTurnCharacter[turn]))

			except asyncio.TimeoutError:
				raise e
			else:
				pass

@bot.hybrid_command(name="progressbar",with_app_command=True, description="test d'une progress bar")
async def _progressbar(ctx, number : int = 10):

	progress_bar = await ctx.send("🟩"+("⬜"*number))

	for i in range(number):
		await progress_bar.edit(content = str(("🟩"*i)+"🟩"+("⬜"*int((number-i-1)))))

async def startprogressbar(ctx,number : int):
	progress_bar = await ctx.send("🟩"+("⬜"*(number-1)))

	return progress_bar

async def addprogressbar(progress_bar,number,step):
	await progress_bar.edit(content = str(("🟩"*step)+"🟩"+("⬜"*int((number-step)))))

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