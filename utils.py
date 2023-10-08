import math
import file

emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

async def deleteMessage(ctx):
	try:
		await ctx.message.delete()
	except Exception as e:
		pass

async def setMessageEmotes(message,listeEmotes):
	for x in range(len(listeEmotes)):
		await message.add_reaction(listeEmotes[x])

def getCharacters(listUsersId,listCharacters):
	Characters = []

	for oneCharacter in listCharacters:
		for oneUser in listUsersId:
			if(oneCharacter.id == oneUser):
				Characters.append(oneCharacter)

	return Characters

def ifIsInArray(array,objectToCompare) -> bool:
	for oneObject in array:
		if(objectToCompare == oneObject):
			return True

	return False

def findCharacterById(listeCharacters,index):
	for oneCharacter in listeCharacters:
		if(index == oneCharacter.id):
			return oneCharacter
	return None

async def getReaction(bot,mess,liste):
	def check(reaction,user):
		return user != mess.author and str(reaction.emoji)

	reaction, user = await bot.wait_for('reaction_add', timeout=10.0,check=check)

	isValidEmote = False
	indexValidEmote = 0

	for indexEmote in range(len(liste)):			
		if(str(emojis[indexEmote]) == str(reaction) and user):
			isValidEmote = True
			indexValidEmote = indexEmote

	return isValidEmote,indexValidEmote

def characterEarnXp(_message,_character,_xp):
	nbrLevelTake = _character.add_xp(int(_xp))
	message = ""
	if(nbrLevelTake != 0):
		message += str(_character.prenom+" gagne "+ str(nbrLevelTake) + " niveau\n")

		if(_character.persona != None):
			message += _character.persona.getNewSkill()

	return message


def listToShow(ctx,listObject,page : int):
	#definition des listes
	listEmojisPage = []
	listObjectPage = []
	nbrObject = 0

	maxPage = int(math.ceil(len(listSkill)/len(emojis))) #nombre max de page
	pageCurrent = int(page) #page actuel 

	if(int(maxPage)<int(pageCurrent)):
		pageCurrent = maxPage

	#gere le systeme de page 
	pageCurrentIndex = pageCurrent - 1
	incrementPageIndex = pageCurrentIndex * 9 
	#si la liste des skill est plus petit que la liste d'emojis 
	if(len(listObject)<len(emojis)):
		nbrObject = len(listObject) #le nombre d'Object affiché sera le nombre d'Object 
	elif(len(listObject)-incrementPageIndex<len(emojis)):
		nbrObject = len(listObject) - incrementPageIndex 
	else:
		nbrObject = len(emojis)

	for indexSkillPage in range(nbrObject):
		listEmojisPage.append(emojis[indexSkillPage])
		listObjectPage.append(listObject[indexSkillPage+incrementPageIndex])

	return listObjectPage,listEmojisPage,pageCurrent,maxPage