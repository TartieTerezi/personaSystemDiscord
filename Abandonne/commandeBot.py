@bot.hybrid_command(name="level", with_app_command=True, description="level up")
async def _level(ctx):
	character = findCharacterById(listCharacters,ctx.author.id)

	if(character != None):
		character.persona.levelUp()
		await ctx.send(embed=Embed.showPersonaLevelUp(character.persona))
	else:
		await ctx.send("aucun character trouvé")


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
		idUsers = [ctx.author.id,user.id]
		charactersToFight = getCharacters(idUsers,listCharacters)

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
			for oneCharacter in charactersToFight:
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


# LIEU 

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


@bot.hybrid_command(name="passe",with_app_command=False,description="passe dans une autre salle.")
async def _passenextpiece(ctx,nextchannel : discord.TextChannel = None):

	#recherche le channel dans lequel le joueur ecrit
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

	if(nextchannel != None):
		for nextRoom in currentPiece.nextRooms:
			if(nextRoom.channel.jump_url == nextchannel.jump_url):

				for beforePiece in currentPiece.nextRooms:
					await beforePiece.inautorize(user)

				await ctx.message.delete()
				await ctx.send(character.prenom + " se deplace.")

				await currentPiece.inautorize(user)
				await nextRoom.autorize(user)

				await nextRoom.channel.send(character.prenom + " arrive ici.")

				return

		await ctx.send("Ce n'est pas un endroit valide pour se déplacer")
	else:
		if(len(currentPiece.nextRooms)==1):
			await currentPiece.inautorize(user)
			await currentPiece.nextRooms[0].autorize(user)
		elif(len(currentPiece.nextRooms)==0):
			await ctx.send("impossible d'aller autre part.")
		else:
			await ctx.send("Il y à plusieurs endroit ou se déplacer, veuillez selectionner votre destination.")

@bot.hybrid_command(name="listchannel",with_app_command=True,description="Liste les channels du serveur")
async def _listchannel(ctx):
	text_channel_list = []
	for channel in ctx.guild.text_channels:
		print(channel.position)

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


#persona 

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


@bot.hybrid_command(name="newskill", with_app_command=True, description="crée une nouvelle competence.")
async def _newSkill(ctx,nom : str,element : int,description : str,cout : int,puissance : int,precision : int):
	newSkillToAdd = Skill(nom,element,description,cout,puissance,precision)
	listSkill.append(newSkillToAdd)
	file.newSkill(newSkillToAdd)

@bot.hybrid_command(name="addskill", with_app_command=True, description="Ajoute un nouvelle competence a ta persona.")
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


#(item)

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


# OTHER 

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


