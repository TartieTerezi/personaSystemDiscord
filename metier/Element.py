from enum import Enum 

class Element(Enum):
	"""docstring for Element"""
	PHYSIQUE = 1
	FIRE = 2
	ICE = 3
	ELECTRICITY = 4
	WIND = 5
	PSYCHOKINESIS = 6
	NUCLEAR = 7
	BLESS = 8
	CURSE = 9
	ALMIGHTY = 10

	def getColor(self):
		color = [0,0,0]

		if(self == Element.ELECTRICITY):
			color = [252, 253, 91]
		elif(self == Element.PHYSIQUE):
			color = [255,168,59]
		elif(self == Element.FIRE):
			color = [255,74,39]
		elif(self == Element.ICE):
			color = [0,172,247]
		elif(self == Element.WIND):
			color = [0,232,83]
		elif(self == Element.PSYCHOKINESIS):
			color = [255,140,243]
		elif(self == Element.NUCLEAR):
			color = [0,244,250]
		elif(self == Element.BLESS):
			color = [254,253,187]
		elif(self == Element.CURSE):
			color = [247,6,58]
		elif(self == Element.CURSE):
			color = [213,213,213]
		else:
			color = [0,0,0]
		
		return color