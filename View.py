from dis import disco
import discord
from discord import ui

class viewListObjects(discord.ui.View):
	def __init__(self,characterTurn):
		super().__init__()
		self.characterTurn = characterTurn
		self.add_item(SelectListObjects(characterTurn))
		self.add_item(discord.ui.Button(label="Retour", style=discord.ButtonStyle.secondary, emoji="◀️"))

		async def back(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = -1
				self.stop()
				await interaction.response.defer()

		self.children[1].callback = back

class SelectListObjects(discord.ui.Select):
	def __init__(self,characterTurn):
		super().__init__()
		self.choice = None
		self.characterTurn = characterTurn	
		options = []

		listItems = characterTurn.inventaire

		for item in listItems:
			options.append(discord.SelectOption(label=str(item.nom),value=item.nom))

		super().__init__(placeholder="Quel object selectionner ?", options=options,min_values=1,max_values=1)

	async def callback(self, interaction: discord.Interaction):
		self.view.choice = self.values[0]
		self.view.stop()
		await interaction.response.defer()


class viewObject(discord.ui.View):
	def __init__(self,characterTurn,item):
		super().__init__()
		self.choice = None
		self.characterTurn = characterTurn	

		self.add_item(discord.ui.Button(label="Utiliser", style=discord.ButtonStyle.green,disabled=not item.is_useable(), emoji="☑️"))
		self.add_item(discord.ui.Button(label="Equiper",style=discord.ButtonStyle.green,disabled= not item.is_equipeable(), emoji="👕"))

		self.add_item(discord.ui.Button(label="Retour", style=discord.ButtonStyle.secondary, emoji="◀️"))

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

		async def back(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = -1
				self.stop()
				await interaction.response.defer()

		self.children[0].callback = use
		self.children[1].callback = equip
		self.children[2].callback = back

class viewFight(discord.ui.View): # Create a class called viewFight that subclasses discord.ui.View
	def __init__(self,characterTurn):
		super().__init__()
		self.add_item(discord.ui.Button(label="Attaque", style=discord.ButtonStyle.danger, emoji="⚔️"))

		self.add_item(discord.ui.Button(label="Persona",style=discord.ButtonStyle.blurple,disabled=(characterTurn.persona == None) or (len(characterTurn.persona.skills) == 0) , emoji="🎭"))

		self.add_item(discord.ui.Button(label="Objets", style=discord.ButtonStyle.green,disabled=(len(characterTurn.inventaire) == 0),emoji="💊"))
		self.add_item(discord.ui.Button(label="Garde", style=discord.ButtonStyle.secondary, emoji="🛡️"))
		#self.add_item(discord.ui.Button(label="Fuite", style=discord.ButtonStyle.secondary,emoji="↪️"))
		self.choice = None
		self.characterTurn = characterTurn		

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

class viewSelectEnnemie(discord.ui.View):
	def __init__(self,listEnnemis,characterTurn):
		super().__init__()
		self.characterTurn = characterTurn
		self.add_item(SelectEnnemie(listEnnemis))
		self.add_item(discord.ui.Button(label="Retour", style=discord.ButtonStyle.secondary, emoji="◀️"))

		async def back(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = -1
				self.stop()
				await interaction.response.defer()

		self.children[1].callback = back

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

class viewSelectSkill(discord.ui.View):
	def __init__(self,listSkills,characterTurn):
		super().__init__()
		self.characterTurn = characterTurn
		self.add_item(SelectSkills(listSkills))
		self.add_item(discord.ui.Button(label="Retour", style=discord.ButtonStyle.secondary, emoji="◀️"))

		async def back(interaction):
			if(self.characterTurn.id == interaction.user.id):
				self.choice = -1
				self.stop()
				await interaction.response.defer()

		self.children[1].callback = back