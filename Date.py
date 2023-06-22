
nbrJourByMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
MounthName = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
DayName = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
stepDay = ["Matin","Midi","Après-midi","Soir","Nuit"]

class Date(object):
	"""docstring for Date"""
	def __init__(self, jour,nameJour,mois,annee,step = 0):
		if(mois>len(nbrJourByMonth)):
			mois = len(nbrJourByMonth)
		self.mois = mois

		if(jour>nbrJourByMonth[self.mois-1]):
			jour = nbrJourByMonth[self.mois-1]

		self.jour = jour

		self.jourName = nameJour

		self.annee = annee

		if(step>len(stepDay)):
			self.step = len(stepDay)
		else:
			self.step = step

		print(self)

	def __str__(self):
		return f"(jour={self.jour}-{self.getJour()},Etape={self.getStep()},mois={self.getMois()},annee={self.annee})"

	def nextDay(self,step = 0):
		self.nextDayName(step+1)
		if(self.jour>=nbrJourByMonth[self.mois-1]):
			if(self.mois>=len(nbrJourByMonth)):
				self.annee += 1
				self.mois = 1
			else:
				self.mois+=1
			self.jour = 1
		else:
			self.jour += 1
		self.step = step

	def setDay(self,jour):
		if(jour>=nbrJourByMonth[self.mois-1]):
			self.jour = nbrJourByMonth[self.mois-1]
			self.jour = 1
		else:
			self.jour = jour
		self.step = 0

	def setMonth(self,mois):
		if(mois>=len(nbrJourByMonth)):
			self.mois = len(nbrJourByMonth)
		else:
			self.mois = mois
		self.step = 0

	def setYear(self,annee):
		self.annee = annee
		self.step = 0

	def skipDay(self,numberDay,step = 0):
		for day in range(numberDay):
			self.nextDay(step)

	def skipStep(self,step = 1):
		if(self.step+step>=len(stepDay)):
			self.step += step

			numberDay = int(self.step / len(stepDay))
			self.step -= numberDay * len(stepDay)

			#self.step += self.step % len(stepDay)
			self.skipDay(numberDay,self.step)
		else:
			self.step += step

	def getNumberDayByYear(self):
		days = 0
		for i in range(len(nbrJourByMonth)):
			days += nbrJourByMonth[i]
		return days

	def getMois(self):
		return MounthName[self.mois-1]

	def getStep(self):
		return stepDay[self.step]

	def getJour(self):
		return DayName[self.jourName-1]

	def nextDayName(self,step = 1):
		if(self.jourName + step > len(DayName)):
			self.jourName = (self.jourName + step) % (len(DayName))
		else:
			self.jourName += step