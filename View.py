from dis import disco
import discord
from discord import ui

# classe de base pour les view, a le bouton back de fonctionnelle 
class viewBase(discord.ui.View):
	def __init__(self,character,*args,isBack = True):
		super().__init__()
		self.characterTurn = character
		self.choice = None

		self.addField(*args)

		if(isBack):
			self.add_item(discord.ui.Button(label="Retour", style=discord.ButtonStyle.secondary, emoji="◀️"))

			async def back(interaction):
				if(self.characterTurn.id == interaction.user.id):
					self.choice = -1
					self.stop()
					await interaction.response.defer()

			self.children[int(len(self.children)-1)].callback = back

	def addField(self,*args):
		pass

class viewListObjects(viewBase):
	def __init__(self,characterTurn):
		super().__init__(characterTurn,characterTurn)

	def addField(self,*args):
		self.add_item(SelectListObjects(args[0]))

class SelectListObjects(discord.ui.Select):
	def __init__(self,characterTurn):
		super().__init__()
		self.choice = None
		self.characterTurn = characterTurn	
		options = []

		listItems = characterTurn.inventaire

		for item in listItems.data:
			options.append(discord.SelectOption(label=str(item.nom),value=item.nom))

		super().__init__(placeholder="Quel object selectionner ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = self.values[0]
		self.view.stop()
		await interaction.response.defer()

class viewObject(viewBase):
	def __init__(self,characterTurn,item):
		super().__init__(characterTurn,item)

	def addField(self,*args):
		item = args[0]
		
		self.add_item(discord.ui.Button(label="Utiliser", style=discord.ButtonStyle.green,disabled=not item.is_useable(), emoji="☑️"))
		self.add_item(discord.ui.Button(label="Equiper",style=discord.ButtonStyle.green,disabled= not item.is_equipeable(), emoji="👕"))

		async def use(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 0
				self.stop()
				await interaction.response.defer()

		async def equip(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 1
				self.stop()
				await interaction.response.defer()

		self.children[0].callback = use
		self.children[1].callback = equip

class viewFight(viewBase): # Create a class called viewFight that subclasses discord.ui.View
	def __init__(self,characterTurn):
		super().__init__(characterTurn,characterTurn,isBack = False)
	
	def addField(self,*args):
		characterTurn = args[0]

		self.add_item(discord.ui.Button(label="Attaque", style=discord.ButtonStyle.danger, emoji="⚔️"))
		self.add_item(discord.ui.Button(label="Persona",style=discord.ButtonStyle.blurple,disabled=(characterTurn.persona == None) or (len(characterTurn.persona.skills) == 0) , emoji="🎭"))
		self.add_item(discord.ui.Button(label="Objets", style=discord.ButtonStyle.green,disabled=(len(characterTurn.inventaire.data) == 0),emoji="💊"))
		self.add_item(discord.ui.Button(label="Garde", style=discord.ButtonStyle.secondary, emoji="🛡️"))
		#self.add_item(discord.ui.Button(label="Fuite", style=discord.ButtonStyle.secondary,emoji="↪️"))
		
		async def attaque(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 0
				self.stop()
				await interaction.response.defer()

		async def persona(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 1
				self.stop()
				await interaction.response.defer()

		async def objet(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 2
				self.stop()
				await interaction.response.defer()

		async def garde(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 3
				self.stop()
				await interaction.response.defer()

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
		await interaction.response.defer()

class viewSelectEnnemie(viewBase):
	def __init__(self,listEnnemis,characterTurn):
		super().__init__(characterTurn,listEnnemis)

	def addField(self,*args):
		self.add_item(SelectEnnemie(args[0]))

class SelectSkills(discord.ui.Select):
	def __init__(self,listSkills):
		self.choice = None

		options = []
		for i in range(len(listSkills)):
			skill = listSkills[i]

			if(skill.isUseable()):
				options.append(discord.SelectOption(label=str(skill),value=i,description=skill.getCount()))

		super().__init__(placeholder="Quel technique choisir ?", options=options,min_values=1,max_values=1)


	async def callback(self, interaction: discord.Interaction):
		self.view.choice = int(self.values[0])
		self.view.stop()
		await interaction.response.defer()

class viewSelectSkill(viewBase):
	def __init__(self,listSkills,characterTurn):
		super().__init__(characterTurn,listSkills)

	def addField(self,*args):
		self.add_item(SelectSkills(args[0]))

class viewlistObjectsShop(viewBase):
	def __init__(self,shop,character):
		super().__init__(character,shop,character)

	def addField(self,*args):
		self.add_item(SelectListObjectsShop(args[0],args[1]))

class SelectListObjectsShop(discord.ui.Select):
	def __init__(self,shop,character):
		super().__init__()
		self.choice = None
		options = []

		i = 0
		for oneObject in shop.objects:
			options.append(discord.SelectOption(label=str(oneObject.nom),value=i,description=str(shop.objects[oneObject][0])+"$"))
			i+=1

		super().__init__(placeholder="Quel objet acheter ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = int(self.values[0])
		self.view.stop()
		await interaction.response.defer()

class viewlistObjectsShopSelling(viewBase):
	def __init__(self,shop,character):
		super().__init__(character,shop,character)

	def addField(self,*args):
		self.add_item(SelectListObjectsShopSelling(args[0],args[1]))

class SelectListObjectsShopSelling(discord.ui.Select):
	def __init__(self,shop,character):
		super().__init__()
		self.choice = None
		options = []

		i = 0
		for oneObject in shop.objectsToSell:
			for item in character.inventaire.data:
				if(item.nom == oneObject.nom and character.inventaire.data[item] > 0):
					options.append(discord.SelectOption(label=item.nom,value=i,description=str(shop.objectsToSell[oneObject])+"$"))
					i+=1

		if(i == 0):
			options.append(discord.SelectOption(label="Aucun objet a vendre",value=-1))

		super().__init__(placeholder="Quel objet vendre ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = int(self.values[0])
		self.view.stop()
		await interaction.response.defer()

class SelectNumberObjetct(discord.ui.Select):
	def __init__(self,nbrObjects):
		super().__init__()
		self.choice = None
		options = []

		if(nbrObjects > 10):
			nbrObjects = 10

		for i in range(nbrObjects):
			options.append(discord.SelectOption(label=str(i+1)))

		super().__init__(placeholder="Combien en acheter ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = int(self.values[0])
		self.view.stop()
		await interaction.response.defer()

class viewNumberObjetct(viewBase):
	def __init__(self,nbrObjects,character):
		super().__init__(character,nbrObjects,character)

	def addField(self,*args):
		self.add_item(SelectNumberObjetct(args[0]))

class viewActionsObjects(viewBase):
	def __init__(self,shop,character):
		super().__init__(character,shop)

	def addField(self,*args):
		self.add_item(discord.ui.Button(label="Achat", style=discord.ButtonStyle.secondary, emoji="🛍️"))
		# vente impossible pour le moment
		self.add_item(discord.ui.Button(label="Vente", style=discord.ButtonStyle.secondary, emoji="💰"))
		
		async def purchase(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 1
				self.stop()
				await interaction.response.defer()

		async def selling(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = 2
				self.stop()
				await interaction.response.defer()

		self.children[0].callback = purchase
		self.children[1].callback = selling