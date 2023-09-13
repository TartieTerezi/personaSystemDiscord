
# LIEU 


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


