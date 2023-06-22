# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import math
import os

from dotenv import load_dotenv
load_dotenv()

#PERSONA,ELEMENT,SKILL
from Element import Element
from Skill import Skill
from Persona import Persona
from Character import Character

#DATE 
from Date import Date

#Embed
import Embed
#file
import file


listSkill,listPersonas,listCharacters,date = file.reset()


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

@bot.hybrid_command(name="date",with_app_command=True,description="Donne la date du jour")
async def _date(ctx):
	await ctx.send(embed=Embed.showDate(date))

@bot.hybrid_command(name="skipday",with_app_command=True,description="passe au jours suivant")
async def _skipday(ctx,daytoskip = 1):
	date.skipDay(daytoskip)

@bot.hybrid_command(name="skipstep",with_app_command=True,description="passe au jours suivant")
async def _setstep(ctx,steptoskip = 1):
	date.skipStep(steptoskip)

@bot.hybrid_command(name="reset", with_app_command=True, description="Regarde la competence selectionné")
async def _reset(ctx):
	global listSkill
	global listPersonas
	global listCharacters
	global date

	listSkill,listPersonas,listCharacters,date = file.reset()
	await ctx.send("Update de tout les elements")

# Listener commande
@bot.hybrid_command(name="stat", with_app_command=True, description="Montre vos statistique")
async def _stat(ctx):
	isFind = False

	for oneCharacter in listCharacters:
		if(ctx.author.id == oneCharacter.id):
			isFind = True
			await ctx.send(embed=Embed.showCharacter(oneCharacter))

	if(isFind == False):
		await ctx.send("Vous n'avez pas de character")

@bot.hybrid_command(name="level", with_app_command=True, description="Montre vos statistique")
async def _level(ctx):
	isFind = False

	for oneCharacter in listCharacters:
		if(ctx.author.id == oneCharacter.id):
			oneCharacter.persona.levelUp()

@bot.command(name="sync")
async def _sync(ctx) :
    fmt = await ctx.bot.tree.sync()
    await ctx.channel.send(f"Synchronisation {len(fmt)} commandes a ce serveur.")

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

@bot.hybrid_command(name="addcharacter", with_app_command=True, description="Ajoute un nouveau character si vous n'en avez pas déjà un.")
async def _addcharacter(ctx,nom,prenom,pv,pc):	
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

@bot.hybrid_command(name="newskill", with_app_command=True, description="Ajoute un nouvelle competence.")
async def _newSkill(ctx,nom : str,element : int,description : str,cout : int,puissance : int,precision : int,is_healing : bool):
	newSkillToAdd = Skill(nom,element,description,cout,puissance,precision,is_healing)
	listSkill.append(newSkillToAdd)
	file.newSkill(newSkillToAdd)


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
				for indexEmote in range(len(emojisFight)):
					await mess.add_reaction(emojisFight[indexEmote])

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
						isValidEmote = True
						indexValidEmote = indexEmote

				if(isValidEmote): 
					await ctx.send(str(indexValidEmote)+ " de "+ listeTurnCharacter[turn].prenom)
					turn = (turn + 1) % len(listeTurnCharacter)

					await mess.clear_reactions()

					print(indexValidEmote)
					if(indexValidEmote==0):
						pass 
					elif(indexValidEmote==1):
						pass 
					elif(indexValidEmote==2):
						pass 
					elif(indexValidEmote==3):
						pass 
					elif(indexValidEmote==4):
						isFight = False 

			except asyncio.TimeoutError:
				raise e
			else:
				pass

@bot.hybrid_command(name="skilllist",with_app_command=True, description="Liste des comperences")
async def _skillList(ctx,page : int = 1):
	#definition des listes
	listEmojisPage = [] 
	listSkillPage = []
	nbrSkill = 0

	maxPage = int(math.ceil(len(listSkill)/len(emojis))) #nombre max de page
	pageCurrent = int(page) #page actuel 

	if(int(maxPage)<int(pageCurrent)):
		pageCurrent = maxPage

	#gere le systeme de page 
	pageCurrentIndex = pageCurrent - 1
	incrementPageIndex = pageCurrentIndex * 9 

	#si la liste des skill est plus petit que la liste d'emojis 
	if(len(listSkill)<len(emojis)):
		nbrSkill = len(listSkill) #le nombre de skill affiché sera le nombre de skill 
	elif(len(listSkill)-incrementPageIndex<len(emojis)):
		nbrSkill = len(listSkill) - incrementPageIndex 
	else:
		nbrSkill = len(emojis)

	for indexSkillPage in range(nbrSkill):
		listEmojisPage.append(emojis[indexSkillPage])
		listSkillPage.append(listSkill[indexSkillPage+incrementPageIndex])

	embed=discord.Embed(title="Liste des compétences "+ str(pageCurrent) +"/"+ str(maxPage))
	for oneSkill in listSkillPage:
		embed.add_field(name=oneSkill.nom,value=oneSkill.getCount(), inline=True)
	mess = await ctx.send(embed=embed)

	for indexEmote in range(len(listEmojisPage)):
		await mess.add_reaction(listEmojisPage[indexEmote])

	def check(reaction,user):
		return user != mess.author and str(reaction.emoji)

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)

		isValidEmote = False
		indexValidEmote = 0

		for indexEmote in range(len(listSkillPage)):			
			if(str(emojis[indexEmote]) == str(reaction) and user):
				isValidEmote = True
				indexValidEmote = indexEmote

		if(isValidEmote):
			#embded avec les informations de l'attaque 
			skill = listSkill[indexValidEmote+incrementPageIndex]
			await ctx.send(embed=Embed.showSkill(skill))

	except asyncio.TimeoutError:
		await mess.add_reaction('🕐')
	else:
		await mess.delete()

@bot.hybrid_command(name="personalist",with_app_command=True, description="Liste des comperences")
async def _personalist(ctx,page : int = 1):

	#definition des listes
	listEmojisPage = [] 
	listPersonaPage = []
	nbrPersona = 0

	maxPage = int(math.ceil(len(listPersonas)/len(emojis))) #nombre max de page
	pageCurrent = int(page) #page actuel 

	if(int(maxPage)<int(pageCurrent)):
		pageCurrent = maxPage

	#gere le systeme de page 
	pageCurrentIndex = pageCurrent - 1
	incrementPageIndex = pageCurrentIndex * 9 

	#si la liste des skill est plus petit que la liste d'emojis 
	if(len(listPersonas)<len(emojis)):
		nbrPersona = len(listPersonas) #le nombre de skill affiché sera le nombre de skill 
	elif(len(listPersonas)-incrementPageIndex<len(emojis)):
		nbrPersona = len(listPersonas) - incrementPageIndex 
	else:
		nbrPersona = len(emojis)

	for indexPersonaPage in range(nbrPersona):
		listEmojisPage.append(emojis[indexPersonaPage])
		listPersonaPage.append(listPersonas[indexPersonaPage+incrementPageIndex])

	embed=discord.Embed(title="Liste des personas "+ str(pageCurrent) +"/"+ str(maxPage))

	for onePersona in listPersonaPage:
		embed.add_field(name="",value=onePersona.nom, inline=True)
	mess = await ctx.send(embed=embed)

	for indexEmote in range(len(listEmojisPage)):
		await mess.add_reaction(listEmojisPage[indexEmote])

	def check(reaction,user):
		return user != mess.author and str(reaction.emoji)

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)

		isValidEmote = False
		indexValidEmote = 0

		for indexEmote in range(len(listPersonaPage)):			
			if(str(emojis[indexEmote]) == str(reaction) and user):
				isValidEmote = True
				indexValidEmote = indexEmote

		if(isValidEmote):
			#embded avec les informations de la persona 
			persona = listPersonas[indexValidEmote+incrementPageIndex]
			await ctx.send(embed=Embed.showPersona(persona))

	except asyncio.TimeoutError:
		await mess.add_reaction('🕐')
	else:
		await mess.delete()

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

async def deleteMessage(ctx):
	try:
		await ctx.message.delete()
	except Exception as e:
		pass
		
bot.run(os.getenv("TOKEN"))