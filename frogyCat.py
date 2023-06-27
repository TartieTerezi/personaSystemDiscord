# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
from discord import app_commands

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
from Item import *

#DATE 
from Date import Date

#Embed
import Embed
#file
import file

import utils

listSkill,listPersonas,listCharacters,date,listItem = file.reset()
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']


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
	await ctx.send(embed=Embed.showDate(date))

@bot.hybrid_command(name="skipday",with_app_command=True,description="passe au jours suivant")
async def _skipday(ctx,daytoskip = 1):
	date.skipDay(daytoskip)
	await ctx.send(embed=Embed.showDate(date))


@bot.hybrid_command(name="skipstep",with_app_command=True,description="passe au jours suivant")
async def _setstep(ctx,steptoskip = 1):
	date.skipStep(steptoskip)
	await ctx.send(embed=Embed.showDate(date))

###### CHARACTER ######

@bot.hybrid_command(name="stat", with_app_command=True, description="Montre vos statistique")
async def _stat(ctx):
	isFind = False

	for oneCharacter in listCharacters:
		if(ctx.author.id == oneCharacter.id):
			isFind = True
			await ctx.send(embed=Embed.showCharacter(oneCharacter))

	if(isFind == False):
		await ctx.send("Vous n'avez pas de character")

@bot.hybrid_command(name="addcharacter", with_app_command=True, description="Ajoute un nouveau character si vous n'en avez pas déjà un.")
async def _addcharacter(ctx,nom,prenom,pv,pc,idAuthor=0):
	if(idAuthor!=0):
		for oneCharacter in listCharacters:
			if(oneCharacter.id == idAuthor):
				await ctx.send("Character déjà existant")
				return

	isFind = False

	for oneCharacter in listCharacters:
		if(oneCharacter.id == ctx.author.id):
			isFind = True

	if(isFind == False):
		newCharacter = Character(ctx.author.id,nom,prenom,None,pv,pc)

		listCharacters.append(newCharacter)
		file.newCharacter(newCharacter)

		await ctx.send("Nouveau character")
	else:
		await ctx.send("Character déjà existant")

###### PERSONA ######

@bot.hybrid_command(name="level", with_app_command=True, description="Montre vos statistique")
async def _level(ctx):
	isFind = False

	for oneCharacter in listCharacters:
		if(ctx.author.id == oneCharacter.id):
			oneCharacter.persona.levelUp()

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
async def _skill(ctx, skill):

	isFind = False
	for oneSkill in listSkill:
		if(oneSkill.nom == skill):
			isFind = True
			await ctx.send(embed=Embed.showSkill(oneSkill))
			break

	if(isFind == False):
		await ctx.send("Aucune attaque trouvé sous le nom de " + str(arg))

@bot.hybrid_command(name="newskill", with_app_command=True, description="Ajoute un nouvelle competence.")
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
		await ctx.send("Aucune attaque trouvé sous le nom de " + str(arg))

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
async def _createchannel(ctx,arg,name,name_category=""):
	if(arg == "channel"):
		guild = ctx.message.guild

		if(name_category == ""):
			await guild.create_text_channel(name)
		else:
			isInCategory = False
			for categorie in ctx.guild.categories:
				if(categorie.name == name_category):
					isInCategory = True
					await categorie.create_text_channel(name)

			if(isInCategory == False):
				await ctx.send("Aucune categorie trouvé sous le nom de "+ str(name))

	elif(arg == "category"):
		await ctx.guild.create_category(name)

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

###### FIGHT ######

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

		isFight = True
		while isFight:
			try:
				embed=discord.Embed(title=str("tour de ")+str(listeTurnCharacter[turn].prenom))
				embed.add_field(name="1️⃣", value="Attaque ", inline=True)
				embed.add_field(name="2️⃣", value="Persona", inline=True)
				embed.add_field(name="3️⃣", value="Objets", inline=True)
				embed.add_field(name="4️⃣", value="Garde", inline=True)
				await mess.edit(embed=embed)

				await utils.setMessageEmotes(mess,emojisFight)

				reaction,user = await bot.wait_for('reaction_add',check=check2)
				#debut du tour, determine qui dois jouer 

				#One Attaque Normal
				#Two Persona
				#Three Items 
				#Four Defense

				isValidEmote = False
				indexValidEmote = 0

				for indexEmote in range(len(emojisFight)):
					if(str(emojisFight[indexEmote]) == str(reaction) and user):
						if(listeTurnCharacter[turn].id == user.id):
							isValidEmote = True
							indexValidEmote = indexEmote

				if(isValidEmote): 
					await mess.clear_reactions()


					if(indexValidEmote==4):
						isFight = False
					else:
						if(indexValidEmote==0):
							listeTurnCharacter[(turn+1)%len(listeTurnCharacter)].pv -= listeTurnCharacter[turn].persona.force
							await mess.edit(content=str(listeTurnCharacter[(turn+1)%len(listeTurnCharacter)].prenom)+" a perdu "+ str(listeTurnCharacter[turn].persona.force) +"pv")				

						elif(indexValidEmote==1):
							pass 
						elif(indexValidEmote==2):
							pass 
						elif(indexValidEmote==3):
							pass  
						await ctx.send(str(indexValidEmote)+ " de "+ listeTurnCharacter[turn].prenom)
						turn = (turn + 1) % len(listeTurnCharacter)

			except asyncio.TimeoutError:
				raise e
			else:
				pass

###### OTHER ######

@bot.command(name="sync")
async def _sync(ctx) :
    fmt = await ctx.bot.tree.sync()
    await ctx.channel.send(f"Synchronisation {len(fmt)} commandes a ce serveur.")
	
bot.run(os.getenv("TOKEN"))