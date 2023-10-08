import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

import utils
import sys
import asyncio
import random

import Embed
import View

sys.path.append('metier')
from Element import Element
from Skill import Skill
from Persona import Persona
from Ennemy import Ennemy
from Character import Character
from Groupe import Groupe
from Dao import Dao

ennemis = []
skillShadow = [Skill.byBdd(1),Skill.byBdd(9)]
ennemis.append(Ennemy("Ombre",25 , 5,None , 5, 5, 8, 3, 2, 5, []))

def sortSpeedCharacter(charactersToFight):
	listTurn = []
	# determine qui dois jouer en premier 
	while len(charactersToFight)>0:
		tempCharacter = charactersToFight[0]
		for oneCharacter in charactersToFight:
			if(tempCharacter.getAgilite()<oneCharacter.getAgilite()):
				tempCharacter = oneCharacter

		charactersToFight.remove(tempCharacter)
		listTurn.append(tempCharacter)

	return listTurn

async def fight(ctx,listCharacters,user : discord.User = None,groupe = None):
	turn = 0 # permet de choisir le tour du joueurs
	xp = 0 # xp qui sera gagné a la fin du combat
	
	listeTurnCharacter = [] # liste des joueurs 
	
	allie = [] #  liste des allies du combat
	ennemi = [] # liste des ennemis du combat

	charactersToFight = [] # liste des personnages qui se battrons ( allie comme ennemi )
	

	if(groupe!=None):
		character = utils.findCharacterById(listCharacters,ctx.author.id)
		if(groupe.searchPlayer(character)):
			allie = groupe.getPlayersId()
		else:
			allie = [ctx.author.id]
	else:
		allie = [ctx.author.id]
	
	charactersToFight = utils.getCharacters(allie,listCharacters)
	allie = utils.getCharacters(allie,listCharacters)
	
	# conditions si le combat ne se fait pas
	if(user == None):
		for i in range(len(ennemis)):
			ennemi.append(ennemis[i])
			charactersToFight.append(ennemis[i])
	else:
		if(user.id == ctx.author.id):
			await ctx.send("on tente pas un combat contre soi meme ~")
			return

		ennemi = getCharacters([user.id],listCharacters)

		if(ennemi == None):
			await ctx.send("Character non existant pour ce utilisateur -")
			return

		charactersToFight.append(ennemi[0])

	for i in range(len(charactersToFight)):
		if(isinstance(charactersToFight[i], Character)):
			if(charactersToFight[i].isFight):
				await ctx.send( charactersToFight[i].prenom +" deja en combat")
				return

	listeTurnCharacter = sortSpeedCharacter(charactersToFight)

	for i in range(len(listeTurnCharacter)):
		if(isinstance(listeTurnCharacter[i], Character)):
			listeTurnCharacter[i].isFight = True

	mess = await ctx.send(" - ")
	isFight = True
	while isFight:
		try:
			characterTurn = listeTurnCharacter[turn] #  recupère le joueur qui joue pour ce tour
			# characterTarget = listeTurnCharacter[(turn+1)%len(listeTurnCharacter)] #  recupère le joueur va subir les degats ( a changer )
			characterTarget = None

			# regarde si c'est le tour d'un ennemis
			if(isinstance(characterTurn, Ennemy)):
				# choisis le personnge a	toucher 
				characterTarget = random.choice(allie)
				
				# choisis aléatoirement l'action

				# 0 attaque normale
				#  au dela selectionne un skill
				choice = random.randint(0,len(characterTurn.skills))

				if(choice == 0):
					damage = characterTarget.takeDamage(characterTurn.attack())
					await mess.edit(content=str(characterTurn.getName()+" lance son attaque. \n```diff\n- [ "+characterTarget.getName()+" perd "+str(damage)+" PV ]\n```"),view=None)
				else:
					skill = characterTurn.skills[choice-1]
					damage = characterTurn.attackSkill(skill)

					# differencie si c'est un skill physique ou non
					if(skill.element.nom == "PHYSIQUE"):
						cout = int(characterTurn.maxPv * skill.cout / 100)
						characterTurn.pv -= cout		
						damage = characterTarget.takeDamage(damage,skill)
										
					else:
						characterTurn.pc -= skill.cout
						damage = characterTarget.takeDamage(damage,skill)	
					
					await ctx.channel.send(content=str("```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+skill.nom+" ]\n```\n```diff\n- [ "+characterTarget.getName()+" perd "+str(damage)+" PV a cause de "+skill.nom+" ]\n```"),view=None)		
					
				nextTurn = False
					

				# ici qu'on gère les tours du joueur
			else:
				nextTurn = True
				while nextTurn: 
					choiceAction = None
					view = View.viewFight(characterTurn)

					if(utils.ifIsInArray(allie,characterTurn)):
						await mess.edit(content=None,embed=Embed.showFight(listeTurnCharacter[turn],allie,ennemi),view=view)
					else:
						await mess.edit(content=None,embed=Embed.showFight(listeTurnCharacter[turn],ennemi,allie),view=view)

					await view.wait() 
					choiceAction = view.choice
					
					if(choiceAction==4):
						isFight = False

					if(choiceAction==0):
						characterTarget = None

						# choisis le personnge a	toucher 
						if(utils.ifIsInArray(allie,characterTurn)):
							if(len(ennemi)==1):
								characterTarget = ennemi[0]
							else:
								view = View.viewSelectEnnemie(ennemi,characterTurn)
								await mess.edit(view=view)
								await view.wait() 
								if(view.choice != -1):
									characterTarget = ennemi[view.choice]
						else:
							if(len(allie)==1):
								characterTarget = allie[0]
							else:
								view = View.viewSelectEnnemie(allie,characterTurn)
								await mess.edit(view=view)
								await view.wait() 
								if(view.choice != -1):
									characterTarget = allie[view.choice]

						await mess.edit(view=None)

						damage = characterTarget.takeDamage(characterTurn.attack())
						nextTurn = False

						await mess.edit(content=str("```diff\n- [ "+characterTarget.getName()+" perd "+str(damage)+" PV ]\n```"),embed=None,view=None)

					elif(choiceAction==1):
						# choisis le skill
						skill = None
						skillIsValid = True
						selectIsValid = False

						view = None

						while skillIsValid:
							view = View.viewSelectSkill(characterTurn.persona.skills,characterTurn)

							await mess.edit(view=view)
							await view.wait() 

							if(view.choice != -1):
								skill = characterTurn.persona.skills[view.choice]

								# check si l'attaque est possible
								if(skill.element.nom == "PHYSIQUE"):
									cout = int(characterTurn.maxPv * skill.cout / 100)

									if(characterTurn.pv - cout > 0):
										selectIsValid = True
									else:
										await mess.edit("Pas assez de Pv pour lancer "+ str(skill.nom))
								else:
									if(characterTurn.pc - skill.cout >= 0):
										selectIsValid = True
									else:
										await mess.edit("Pas assez de pc pour lancer "+ str(skill.nom))
							else:
								skillIsValid = False

							while selectIsValid:
								# choisis le personnge a	toucher 
								characterTarget = None
					
								if(utils.ifIsInArray(allie,characterTurn)):
									if(len(ennemi)==1):
										characterTarget = ennemi[0]
									else:
										view = View.viewSelectEnnemie(ennemi,characterTurn)
										await mess.edit(content="",view=view)
										await view.wait() 
					
										if(view.choice != -1):
											characterTarget = ennemi[view.choice]
										else:
											selectIsValid = False
								else:
									if(len(allie)==1):
										characterTarget = allie[0]
									else:
										view = View.viewSelectEnnemie(allie,characterTurn)
										await mess.edit(content="",view=view)
										await view.wait() 
					
										if(view.choice != -1):
											characterTarget = allie[view.choice]
										else:
											selectIsValid = False

								if(characterTarget != None):
									# embded avec les informations de l'attaque 
									damage = characterTurn.attackSkill(skill)
									skillIsValid = False
									selectIsValid = False

									# differencie si c'est un skill physique ou non
									if(skill.element.nom == "PHYSIQUE"):
										cout = int(characterTurn.maxPv * skill.cout / 100)
										characterTurn.pv -= cout		
										nextTurn = False
										damage = characterTarget.takeDamage(damage,skill)
									else:
										characterTurn.pc -= skill.cout
										nextTurn = False
										damage = characterTarget.takeDamage(damage,skill)	
									
									await mess.edit(content=str("```diff\n  [ "+characterTurn.getName()+" lance l'attaque "+skill.nom+" ]\n```\n```diff\n- [ "+characterTarget.getName()+" perd "+str(damage)+" PV a cause de "+skill.nom+" ]\n```"),embed=None,view=None)

					elif(choiceAction==2):
						item = None
						itemIsValid = True
						selectIsValid = False

						while itemIsValid:
							view = View.viewListObjects(characterTurn)
							await mess.edit(embed=Embed.showObjects(characterTurn.inventaire),view=view)
							await view.wait() 

							if(view.choice != -1):
								item = characterTurn.getItemByName(view.choice)
								selectIsValid = True

							else:
								itemIsValid = False

							while selectIsValid:
								view = View.viewObject(characterTurn,item)
								await mess.edit(embed=Embed.showObject(item),view=view)

								await view.wait() 

								if(view.choice != -1):
									nextTurn = False
									selectIsValid = False
									itemIsValid = False

									if(view.choice == 0):
										item.use(characterTurn)
										characterTurn.deleteItem()
										await mess.edit(content=str(characterTurn.nom + " utilise " + item.nom),embed=None,view=None)
									if(view.choice == 1):
										item.equip(characterTurn)
										characterTurn.deleteItem()
										await mess.edit(content=str(characterTurn.nom + " equipe la " + item.nom),embed=None,view=None)

								else:
									selectIsValid = False
 
					elif(choiceAction==3):
						characterTurn.isProtect = True
						nextTurn = False
						await mess.edit(content=str(characterTurn.prenom)+ " se met sur ses gardes.",embed=None,view=None)

			# fin du tour, applique les effets des  statut
			if(turn+1 == len(listeTurnCharacter)):

				listeTurnCharacter = sortSpeedCharacter(listeTurnCharacter)

				for i in range(len(ennemi)):
					message = ennemi[i].updateStatutEffect()

					if(message != None):
						await ctx.channel.send(message)

			# a la fin du tour, regarde si les joueurs sont toujours en vie
			i = len(listeTurnCharacter) -1
			while i != -1:
				oneCharacter = listeTurnCharacter[i]

				if(isinstance(oneCharacter, Character)):
					if(oneCharacter.pv <= 0):
						oneCharacter.pv = 1

						oneCharacter.isFight = False
						listeTurnCharacter.remove(oneCharacter)
						allie.remove(oneCharacter)
						await ctx.channel.send(str(oneCharacter.nom)+" est tombe K.O")
				else:
					if(oneCharacter.pv <= 0):
						oneCharacter.pv = oneCharacter.maxPv

						# ajoute l'exp gagné , formule provisoire
						xp += oneCharacter.getXp() * ((oneCharacter.level+2) / (allie[0].level +2))
						ennemi.remove(oneCharacter)
						listeTurnCharacter.remove(oneCharacter)
						await ctx.channel.send(str(oneCharacter.nom)+" a perdu le combat")
				i-=1
												
			if(len(allie) <= 0):
				await ctx.send("combat perdu")

				for i in range(len(ennemi)):
					if(isinstance(ennemi[i], Character)):
						oneEnnemi.isFight = False


				isFight = False

			if(len(ennemi) <= 0):
				# # calcule de l'exp gagné
				# création d'une formule qui vous calcule l'exp gagné en fonction des ennemis battus  en fonction de leur niveau 
				message = "```Combat gagne\nVous remportez "+str(int(xp))+" points d'experience\n\n"

				for i in range(len(allie)):
					allie[i].isFight = False				

				for i in range(len(allie)):
					message += utils.characterEarnXp(message,allie[i],xp)

				message += "```"
				await ctx.channel.send(message)

				isFight = False

			if(isFight):
				#  prochain tour
				# await ctx.send(str(indexValidEmote)+ " de "+ listeTurnCharacter[turn].prenom)
				turn = (turn + 1) % len(listeTurnCharacter)

				mess = await ctx.channel.send(" - ")

		except asyncio.TimeoutError:
			raise e
		else:
			pass
	pass