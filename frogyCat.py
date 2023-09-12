# -*-coding:utf-8 -*

from curses import halfdelay
from pickle import FALSE
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

###### DATE ######

@bot.hybrid_command(name="date",with_app_command=True,description="Donne la date du jour")
async def _date(ctx):
	await ctx.send(Embed.showDate(date))

@bot.hybrid_command(name="skipday",with_app_command=True,description="passe au jours suivant")
async def _skipday(ctx,daytoskip = 1):
	date.skipDay(daytoskip)
	await ctx.send(Embed.showDate(date))

@bot.hybrid_command(name="skipstep",with_app_command=True,description="passe au jours suivant")
async def _setstep(ctx,steptoskip = 1):
	date.skipStep(steptoskip)
	await ctx.send(Embed.showDate(date))

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

@bot.hybrid_command(name="personalist",with_app_command=True, description="Liste des personas")
async def _personalist(ctx,page : int = 1):
	listPersonaPage,listEmojisPage,pageCurrent,maxPage = utils.listToShow(ctx,listPersonas,page)

	embed=discord.Embed(title="Liste des personas "+ str(pageCurrent) +"/"+ str(maxPage))

	for onePersona in listPersonaPage:
		embed.add_field(name="",value=onePersona.nom, inline=True)
	mess = await ctx.send(embed=embed)

	await utils.setMessageEmotes(mess,listEmojisPage)

	try:
		isValidEmote,indexValidEmote = await utils.getReaction(bot,mess,listPersonaPage)

		if(isValidEmote):
			#embded avec les informations de la persona 
			persona = listPersonaPage[indexValidEmote]
			await ctx.send(embed=Embed.showPersona(persona))

	except asyncio.TimeoutError:
		await mess.add_reaction('🕐')
	else:
		await mess.delete()

###### SKILL ######

@bot.hybrid_command(name="skill", with_app_command=True, description="Regarde la competence selectionné")
async def _skill(ctx, skill_name):
	skill = findSkillByName(listSkill,skill_name)

	if(skill != None):
		await ctx.send(embed=Embed.showSkill(skill))
	else:
		await ctx.send("Aucune attaque trouvé sous le nom de " + str(skill_name))

@bot.hybrid_command(name="newskill", with_app_command=True, description="crée une nouvelle competence.")
async def _newSkill(ctx,nom : str,element : int,description : str,cout : int,puissance : int,precision : int,is_healing : bool):
	newSkillToAdd = Skill(nom,element,description,cout,puissance,precision,is_healing)
	listSkill.append(newSkillToAdd)
	file.newSkill(newSkillToAdd)

@bot.hybrid_command(name="addskill", with_app_command=True, description="Ajoute un nouvelle competence a ton persona.")
async def _addskill(ctx,nom):
	isFind = False

	for oneSkill in listSkill:
		if(oneSkill.nom == nom):
			isFind = True

			isAlreadyLearned = False
			for skillAlreadyLearn in persona.skills:
				if(skillAlreadyLearn.nom == oneSkill.nom):
					isAlreadyLearned = True

			if(isAlreadyLearned == False):
				persona.skills.append(oneSkill)
				await ctx.send(embed=Embed.showNewSkill(persona,oneSkill))
			else:
				await ctx.send("Attaque "+ oneSkill.nom + " déjà apprise")

			break

	if(isFind == False):
		await ctx.send("Aucune attaque trouvé sous le nom de " + str(nom))

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

@bot.hybrid_command(name="listchannel",with_app_command=True,description="Liste les channels du serveur")
async def _listchannel(ctx):
	text_channel_list = []
	for channel in ctx.guild.text_channels:
		print(channel.position)

###### ITEM ######

@bot.hybrid_command(name="itemlist",with_app_command=True, description="Liste des objets")
async def _itemlist(ctx,page : int = 1):
	listItemsPage,listEmojisPage,pageCurrent,maxPage = utils.listToShow(ctx,listItem,page)

	embed=discord.Embed(title="Liste des Items "+ str(pageCurrent) +"/"+ str(maxPage))

	for oneItem in listItemsPage:
		embed.add_field(name="",value=oneItem.nom, inline=True)
	mess = await ctx.send(embed=embed)

	await utils.setMessageEmotes(mess,listEmojisPage)

	try:
		isValidEmote,indexValidEmote = await utils.getReaction(bot,mess,listItemsPage)

		if(isValidEmote):
			#embded avec les informations de la persona 
			item = listItemsPage[indexValidEmote]
			embed=discord.Embed(title=item.nom, description=item.info)
			await ctx.send(embed=embed)

	except asyncio.TimeoutError:
		await mess.add_reaction('🕐')
	else:
		await mess.delete()

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

###### DIALOGUE #####

@bot.hybrid_command(name="dialogue",with_app_command=True, description="Dialogue")
async def _dialogue(ctx,arg):
	embed=discord.Embed(color=0xe81162)

	if(len(arg)>1024):
		await ctx.send("impossible d'envoyer un message aussi long")
	else:
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1118247026635853958/1119009981119856640/tartie_base.png")
		#embed.set_image(url="https://cdn.discordapp.com/attachments/1093990697717215292/1113807915128717413/image.png")
		for oneCharacter in listCharacters:
			if(ctx.author.id == oneCharacter.id):
				embed.add_field(name=oneCharacter.nom +" "+ oneCharacter.prenom, value=str(arg), inline=False)
		await ctx.send(embed=embed)

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

							await ctx.send(content=str(characterTarget.prenom)+" a perdu "+ str(damage) +"pv")				
							await ctx.send(content="pv actuel de "+str(characterTarget.prenom) + " : "+ str(characterTarget.pv) + "/"+ str(characterTarget.maxPv))

						elif(indexValidEmote==1):
							nextStepSkill = False
							while(nextStepSkill == False):
								listSkillPage,listEmojisPage,pageCurrent,maxPage = utils.listToShow(ctx,characterTurn.persona.skills,1)
								embed=discord.Embed(title="Liste des compétences " +str(pageCurrent) +"/"+ str(maxPage))
							
								for oneSkill in listSkillPage:
									embed.add_field(name=oneSkill.nom,value=oneSkill.getCount(), inline=True)
							
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
										
												await ctx.send(content=str(characterTarget.prenom)+" a perdu "+ str(damage) +"pv")				
												await ctx.send(content="pv actuel de "+str(characterTarget.prenom) + " : "+ str(characterTarget.pv) + "/"+ str(characterTarget.maxPv))
											else:
												await ctx.send("Pas assez de Pv pour lancer "+ str(skill.nom))
										else:
											if(characterTurn.pc - skill.cout >= 0):
												nextStepSkill = True
												characterTurn.pc -= skill.cout

												damage = characterTarget.takeDamage(damage,skill)
										
												await ctx.send(content=str(characterTarget.prenom)+" a perdu "+ str(damage) +"pv")				
												await ctx.send(content="pv actuel de "+str(characterTarget.prenom) + " : "+ str(characterTarget.pv) + "/"+ str(characterTarget.maxPv))
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

@bot.command(name="button")
async def _button(ctx):
	view = discord.ui.View()
	button = discord.ui.Button(label="click me")
	textInput = discord.ui.TextInput(
		style=discord.TextStyle.short,
		label="Poids",
		required=True,
		placeholder=""
	)
	view.add_item(button)

	await ctx.send(view=view)

class FeedbackModal(discord.ui.Modal,title="Création de personnage"):
	prenom = discord.ui.TextInput(
		style=discord.TextStyle.short,
		label="prenom",
		required=True,
		placeholder=""
	)

	nom = discord.ui.TextInput(
		style=discord.TextStyle.short,
		label="nom",
		required=True,
		placeholder=""
	)

	async def on_submit(self,interaction: discord.Interaction):
		user = interaction.user

		for categorie in interaction.guild.categories:
			if(categorie.name == "fiches"):
				channel = await categorie.create_text_channel(str(self.nom)+" "+str(self.prenom))
				newCharacter = Character(user.id,str(self.nom),str(self.prenom))
				file.newCharacter(newCharacter)
				listCharacters.append(newCharacter)
					
				await channel.set_permissions(user, read_messages=True,send_messages=True)
					
					

	async def on_error(self,interaction: discord.Interaction,error):
		print(error)
		pass

@bot.hybrid_command(name="testmondal",with_app_command=True, description="modal")
async def _testmondal(ctx):
	if(findCharacterById(listCharacters,ctx.author.id) != None):
		await ctx.author.send("Tu as déjà un personnage >:D")
		return
	
	feedback_modal = FeedbackModal()
	feedback_modal.user = ctx.author
	await ctx.interaction.response.send_modal(feedback_modal)

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