import pygame
import json
import time

# Class for moving entity, including player, referee and ball
class entity:

	def __init__(self, img):
		self.image = pygame.image.load(img)
		self.pos=[0,0]
		self.jersey_number = 0

	# Method mooving entity
	def move(self,x,y):
		self.pos = [x,y]

	# Method setting picture if there is one
	def jersey(self, im):
		self.jersey_number = im

	# Method getting position
	def getPos(self):
		return (self.pos[0], self.pos[1])

	# Method getting picture
	def getIMG(self):
		return self.image

	# Method getting jersey number
	def getJS(self):
		return self.jersey_number
		

# Class managing the match
class windows:

	def __init__(self, file):

		# Intialisation of pygame
		pygame.init()

		self.loadData(file)

		# Create Screen
		self.screen = pygame.display.set_mode((1256,711))

		# Background
		self.background = pygame.image.load('field.png')

		# Title and Icon
		pygame.display.set_caption("Field")
		pygame.display.set_icon(pygame.image.load('logo.jpg'))

		# Player
		self.playerHome = [entity('p_home.png') for k in range(11)]
		self.playerAway = [entity('p_away.png') for k in range(11)]

		# Referee
		self.playerReferee = [entity('p_referee.png') for k in range(3)]

		#Ball
		self.playerBall = entity('p_ball.png')
		self.comptBallOut=0

		# Score
		self.score = [[ pygame.image.load("n_"+str(i)+".png") for i in range(10)] for k in range(4)]

		# Number
		jerseyNumber = [1,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,23,99]
		self.jerseyHome =[[k,pygame.image.load('p_'+str(k)+'.png')] for k in jerseyNumber]
		self.jerseyAway = self.jerseyHome[:]

		# Different text for occupation and possission statistics
		self.posImg = [pygame.font.SysFont('chalkduster.ttf', 40).render('Occupation', True, (69,72,77))]
		self.posImg += [pygame.font.SysFont('chalkduster.ttf', 40).render('['+str(k)+'0m, '+str(k-3)+'0m]', True, (69,72,77)) for k in range(9,0,-3)]

		self.possession =  [pygame.font.SysFont('chalkduster.ttf', 40).render('Possession', True, (69,72,77)) ]
		self.possession += [pygame.font.SysFont('chalkduster.ttf', 40).render('50%', True, (255,242,0))]
		self.possession += [pygame.font.SysFont('chalkduster.ttf', 40).render('50%', True, (63,72,204))]

		self.percent = [pygame.font.SysFont('chalkduster.ttf', 40).render('0%', True, k) for k in [(63,72,204) for i in range(3)]+[(255,242,0) for i in range(3)]]

		self.sumBallPossession = 0
		self.poss = [0,0,0,0,0,0]

		# Variable for managing ball out of the field 
		self.ballAway = 0
		self.ballHome = 0

	# Method to load json file
	def loadData(self, file):
		#'match.json'
		with open(file) as f:
  			self.data = json.load(f)

  	# Method to display players
	def playerDisplay(self):

		self.moveTeam()

		# Display all players and referees
		for player in self.playerHome+self.playerAway+self.playerReferee:
			self.screen.blit(player.getIMG(),player.getPos())

			# If there is a jersay (players), display it
			if player.getJS():
				self.screen.blit(player.getJS(), player.getPos())


	# Method mooving all players and referee
	def moveTeam(self):

		# Home Team		
		k=0
		for player in self.data[self.comptTime]["home_team"]:
			self.playerHome[k].move(456+ int(8.33*player["position"][0]),  356+ int(10*player["position"][1]))
			self.playerHome[k].jersey( self.searchForJersey(player["jersey_number"]) )
			k+=1

		# Away Team
		k=0
		for player in self.data[self.comptTime]["away_team"]:
			self.playerAway[k].move(456+ int(8.33*player["position"][0]),   356+ int(10*player["position"][1]))
			self.playerAway[k].jersey( self.searchForJersey(player["jersey_number"],home=False) )
			k+=1

		# Referees
		k=0
		# You can display more referee by changing [...[0]] to self.data[self.comptTime]["referees"]
		for referee in [self.data[self.comptTime]["referees"][0]]:
			if referee["position"]!= None:
				self.playerReferee[k].move(456+int(8.33*referee["position"][0]),  356+int(10*referee["position"][1]))
				k+=1

	# Method mooving and displaying ball
	def updateBall(self):
		if self.data[self.comptTime]["ball"]["position"]!=None:
			self.comptBallOut = 0
			self.playerBall.move(456+int(8.33*self.data[self.comptTime]["ball"]["position"][0]),  356+int(10*self.data[self.comptTime]["ball"]["position"][1]))	        
		
		elif self.comptBallOut<5:
			self.comptBallOut+=1

		self.screen.blit(self.playerBall.getIMG(),self.playerBall.getPos())

	# Method getting jersey number if there is one
	def searchForJersey(self,num, home=True):
		for k in range(len(self.jerseyHome)):
			if self.jerseyHome[k][0] == num:
				if home:
					return self.jerseyHome[k][1]
				else:
					return self.jerseyAway[k][1]
		return 0

	# Method getting utc_time to sec
	def convertTime(self, a):
		a = a//1000
		return(self.secToScore(a))

	# Method getting time in sec to time in min + sec
	def secToScore(self, a):
		minutes = str(a//60)
		if a//60<1:
			minutes = "00"
		elif a//60<10:
			minutes = "0" + minutes
		a = str(a%60)
		if int(a)<10:
			return(minutes+"0"+a)

		return(minutes + a)

	# Method displaying time
	def displayTime(self, a):
		a = self.secToScore(a)
		for i in range(4):
			self.screen.blit(self.score[i][int(a[i])],(926+80*i,20))

	# Method getting 
	def temps(self):
		a = str(time.time())
		b=a[0]+a[1]+a[2]+a[3]+a[4]+a[5]+a[6]+a[7]+a[8]+a[9]
		i=0
		for i in range(11,14):
			if i<len(a):
				b+=a[i]
			else:
				b+="0"
		return int(b)

	# Method to Tempo
	def tempo(self,timePrev,timeAft,timeUtcPrev):
		while(timeAft - timePrev > self.temps() - timeUtcPrev):
			a=None

	# Method closing window
	def stillRunning(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False

	# Method updating pocession and occupation
	def updatePossession(self):

		# Processing away_team occupation
		if self.data[self.comptTime]["ball"]["team"]=="away_team":
			self.ballAway+=1
			if self.data[self.comptTime]["ball"]["position"]!=None:
				#self.posAwayCamp+=1
				if 456+8.33*self.data[self.comptTime]["ball"]["position"][0]>600:
					self.poss[0]+=1
				#self.posAwayAdv+=1
				elif 456+8.33*self.data[self.comptTime]["ball"]["position"][0]>300:
					self.poss[1]+=1 
				#self.posAwaySurf+=1
				else:
					self.poss[2]+=1 

				for k in range(3):
					self.percent[k]  = pygame.font.SysFont('chalkduster.ttf', 40).render( str(int(round((( self.poss[k]/  sum(self.poss[:3]))*100),0)))+"%", True, (63,72,204))
			

		# Processing home_team occupation
		elif self.data[self.comptTime]["ball"]["team"]=="home_team":
			self.ballHome+=1
			if self.data[self.comptTime]["ball"]["position"]!=None:
				if 456+8.33*self.data[self.comptTime]["ball"]["position"][0]<300:
					self.poss[3]+=1 #self.posHomeCamp+=1
				elif 456+8.33*self.data[self.comptTime]["ball"]["position"][0]<600:
					self.poss[4]+=1 #self.posHomeAdv+=1
				else:
					self.poss[5]+=1  #self.posHomeSurf+=1			

				for k in range(3):
					self.percent[3+k]=pygame.font.SysFont('chalkduster.ttf', 40).render( str(int(round((( self.poss[3+k]/sum(self.poss[3:]))*100),0)))+"%", True, (255,242,0))

		# Processing possession
		if self.ballHome+self.ballAway!=0 and self.sumBallPossession != self.ballHome+self.ballAway:
			self.sumBallPossession = self.ballHome+self.ballAway
			self.possession[1] = pygame.font.SysFont('chalkduster.ttf', 40).render(str(int(round(((self.ballHome)/(self.ballHome+self.ballAway))*100,0)))+"%", True, (255,242,0))
			self.possession[2] = pygame.font.SysFont('chalkduster.ttf', 40).render(str(int(round(((self.ballAway)/(self.ballHome+self.ballAway))*100,0)))+"%", True, (63,72,204))

	# Method displaying pocession and occupation
	def displayPossession(self):

		self.updatePossession()

		self.screen.blit(self.posImg[0], (926, 180))

		for k in range(3):
			self.screen.blit(self.percent[k],(1180,220+40*k))
			self.screen.blit(self.percent[3+k],(1100,220+40*k))

			self.screen.blit(self.posImg[1+k], (926, 220+40*k))

		self.screen.blit(self.possession[0], (926, 120))
		self.screen.blit(self.possession[1], (1100, 120))
		self.screen.blit(self.possession[2], (1180, 120))

	# Method running match
	def runMatch(self):

		self.run = True

		dateUtcPrev=self.temps()

		compt = 0
		second=0
		
		self.comptTime=1;
		self.timeStart = self.data[0]["utc_time"]

		dataTimePrev = self.timeStart

		while self.run:

			self.stillRunning()

			# Start turn time
			dataUtcPrev= self.temps()

			self.screen.fill((58,157,35))
			# Backgroung Image
			self.screen.blit(self.background,(0,0))

			timePrev=self.convertTime(self.data[self.comptTime]["utc_time"]-self.timeStart)
			self.comptTime+=1
			timeAft=self.convertTime(self.data[self.comptTime]["utc_time"]-self.timeStart)

			self.tempo(dataTimePrev,self.data[self.comptTime]["utc_time"],dataUtcPrev)
			dataTimePrev = self.data[self.comptTime]["utc_time"]
			dataUtcPrev= self.temps()

			if timePrev!=timeAft:
				second+=1

			self.displayTime(second)

			self.displayPossession()

		    # Diplay players & ball
			self.playerDisplay()
			self.updateBall()

			pygame.display.update()
