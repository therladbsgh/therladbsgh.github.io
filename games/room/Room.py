#
# Room.py
# Project Room
#
# Copyright (c) rladbsgh. All rights reserved.
#

import os, sys

#Creates character/player object. Intended for separate characters for seperate saves, but not yet added.
class char(object):
	
	rooms = {}
	
	#Location of said player.
	location = ""
	
	#Inventory shows item name, amount of item, and description of item, respectively.
	inventory = {}
	
	inNewRoom = 0

#Creates a generic room class to make all other rooms with.
class room(object):
	name = ""
	desc = ""
	npc = []
	#Contains the items within said room. I may change this into a dictionary later instead of a list, who knows
	items = []
	#The user input is stored in this variable.
	input = ""
	#If this is 3, then the input the user made is invalid.
	input_invalid = 0
	#Items that are examinable.
	xItems = {}
	#The directions you can make in the game.
	directions = {
		"west" : "",
		"east" : "",
		"north" : "",
		"south" : "",
		"northwest" : "",
		"northeast" : "",
		"southwest" : "",
		"southeast" : "",
		"up" : "",
		"down" : "",
		"in" : "",
		"out" : ""
	}
	
	directions_alias = {
		"w" : "west",
		"e" : "east",
		"n" : "north",
		"s" : "south",
		"nw" : "northwest",
		"ne" : "northeast",
		"sw" : "southwest",
		"se" : "southeast",
		"u" : "up",
		"d" : "down"
	}
	
	#Sets the something of the room.
	def __init__(self):
		pass
	
	#Prints the room name, description, and items in room.
	def seeroom(self):
		print self.name
		print self.desc
		if len(self.items) > 0:
			print "The following items are in this room:"
			for each in self.items:
				print each
	
	#Takes a user input, checks if the input matches with anything, or if the input is invalid.
	def roominput(self,char):
		try:
			tempinput = raw_input("> ")
		except EOFError:
			print "Invalid input."
			return

		self.input = tempinput.lower().split()
		if len(self.input) == 0:
			print "Invalid input."
			return

		self.defaultChecks(char)
		self.directionalChecks(char)
		self.additionalChecks(char)
		self.npcChecks(char)
		self.checkForInvalidInput()

	#All the commands that are in every room (Help, examine, etc.)
	def defaultChecks(self,char):
		if self.input[0] in ['h','help','manual','?','about']:
			print "<<The Zen of The Game>>"
			print "<<By Anonymous>>"
			print ""
			print "You can LOOK or SEE a given room."
			print "You can also EXAMINE stuff, including yourSELF."
			print "You can TAKE items in a room or DROP them."
			print "You can check your INVENTORY as well."
			print "You can move in any direction, N/S/E/W/NE/NW/SE/SW/UP/DOWN/IN/OUT."
			print "You can also do some interesting actions in some rooms, who knows?"
			print "You can ask for HELP if you need it."
			print "If all else fails, you can DIE."
		
		elif self.input[0] in ['examine','x']:
			#Checks if the input has two words, "examine" and some examinable object.
			if len(self.input) == 1:
				print "You need to specify what item to examine."
			elif len(self.input) > 2:
				print "You can only specify one item at a time."
			else:
				#Checks if the item is in the xItems attribute
				if self.input[1].lower() in self.xItems.keys():
					print self.xItems[self.input[1].lower()]
				#Checks if the item is within the inventory (those can be examined too)
				elif self.input[1].lower() in char.inventory.keys():
					if char.inventory[self.input[1]][0] > 0:
						print char.inventory[self.input[1]][1]
					#Checks if the item is an item lying in the room (those can be examined too)
					elif self.input[1].lower() in self.items:
						print char.inventory[self.input[1]][1]
					else:
						print "I don't know what item that is."
				elif self.input[1].lower() in [each_npc.name.lower() for each_npc in self.npc]:
					print each_npc.desc
				elif self.input[1].lower() == "self":
					print "You are Adolph blaine charles david earl frederick gerald hubert irvin john kenneth lloyd martin nero oliver paul quincy randolph sherman thomas uncas victor william xerxes yancy zeus Wolfe schlegelstein hausenberger dorffvoraltern waren gewissenhaft schaferswessen schafewaren wohlgepflege und sorgfaltigkeit beschutzen von angreifen durch ihrraubgierigfeinde welche voraltern zwolftausend jahres vorandieerscheinen wander ersteer dem enschderraumschiff gebrauchlicht als sein ursprung von kraftgestart sein lange fahrt hinzwischen sternartigraum auf der suchenach diestern welche gehabt bewohnbar planeten kreise drehen sich und wohin der neurasse von verstandigmen schlichkeit konnte fortplanzen und sicher freuen anlebens langlich freude und ruhe mit nicht ein furcht vor angreifen von anderer intelligent geschopfs von hinzwischen sternartigraum, Senior. You just woke up."
				else:
					print "I don't know what item that is."
					
		elif self.input[0] in ['see','look']:
			return self.seeroom()
	
		elif self.input[0] in ['save']:
			#print "This is a work in progress."
			#return
			if len(self.input) < 2:
				print "You must supply a save name."
			elif len(self.input) == 2:
				f = open(self.input[1],'w')
				f.write(char.location + "\n")
				for items in char.inventory.keys():
					f.write(str(char.inventory[items][0]) + "\n")
				f.close()
				print "Saved."
		
		elif self.input[0] in ['load']:
			#print "This is a work in progress."
			#return
			if len(self.input) < 2:
				print "You must supply a save name."
				return
			elif len(self.input) > 2:
				print "A save file cannot have spaces on its name."
				return

			try:
				f = open(self.input[1],'r')
			except:
				print "The save file does not exist, or you have typed an improper save name."
				return
			test = []
			#try:
			for line in f:
				moddedLine = line[:-1]
				test.append(moddedLine)
			char.location = str(test[0])
			somenumber = 0
			for itemtype in char.inventory:
				char.inventory[itemtype][0] = int(test[somenumber + 1])
				somenumber += 1
			somenumber = None
			test = None
			print "Loaded."
			print ""
			self.seeroom()
			return
			#except:
			#	print "The save file either does not exist, or is corrupted."
			#	return
			f.close()
			
		elif self.input[0] in ['die','suicide']:
			print "You are dead. Not big surprise."
			sys.exit()
		
		#For each item in the game, if a player has at least 1 of it, then the item will be printed in the inventory, along with the number.
		elif self.input[0] in ['i','inventory','inv']:
			print "Inventory:"
			for each in char.inventory:
				if char.inventory[each][0] >= 1:
					print str(char.inventory[each][0]) + " " + each
		
		elif self.input[0] in ['get','take']:
			try:
				if self.input[1].lower() in ["the","that","this"]:
					del self.input[1]
			except:
				pass
				
			#Checks if there are two words: the "get" and an item that can be picked up.
			if len(self.input) == 1:
				print "You need to specify which item to pick up."
			elif len(self.input) > 2:
				print "You can only specify one item at a time."
			else:
				if self.input[1].lower() in self.items:
					char.inventory[self.input[1]][0] += 1
					self.items.remove(self.input[1])
					print "Taken."
				elif self.input[1].lower() in ["all"]:
					if len(self.items) > 0:
						for each in self.items:
							char.inventory[each][0] += 1
							self.items.remove(each)
						print "Taken."
					else:
						print "There are no more items to pick up."
				else:
					print "This item does not exist in this room."
		
		elif self.input[0] in ['drop','discard','trash']:
			#Checks if there are two words: the "drop" and an item that can be picked up.
			try:
				if self.input[1].lower() in ["the","that","this"]:
					del self.input[1]
			except:
				pass

			if len(self.input) == 1:
				print "You need to specify which item to discard."
			elif len(self.input) > 2:
				print "You can only specify one item at a time."
			else:
				if self.input[1].lower() in char.inventory:
					if char.inventory[self.input[1].lower()][0] >= 1:
						char.inventory[self.input[1]][0] -= 1
						self.items.append(self.input[1])
						print "Discarded."
					else:
						print "You don't have this item."
				elif self.input[1].lower() in ["all"]:
					garbage = 0
					for each in char.inventory.keys():
						if char.inventory[each][0] >= 1:
							char.inventory[each][0] -= 1
							self.items.append(each)
							garbage += 1
					if garbage == 0:
						print "You have nothing to drop, idiot."
					else:
						print "Dropped all."
				else:
					print "You don't have this item."
		
		#If the input does not match anything in this function then the input_invalid attribute gets a +1.
		else:
			self.input_invalid += 1
	
	def directionalChecks(self,char):
		
		for aliases in self.directions_alias.keys():
			if self.input[0] == aliases:
				self.input[0] = self.directions_alias[aliases]
		
		for directions in self.directions_alias.values():
			if self.input[0] == directions:
				if directions not in self.directions:
					print "You can't go that way."
					self.input_invalid -= 1
				else:
					char.location = self.directions[directions]
					char.inNewRoom = 1
					self.input_invalid -= 1

		self.input_invalid += 1
	
	def npcChecks(self, char):
		if len(self.input) == 3:
			if self.input[0] in ["talk","speak","converse"] and self.input[1] in ["to","with"]:
				if self.input[2] not in [each_npc.name.lower() for each_npc in self.npc]:
					print "There is nobody named that here."
				else:
					print each_npc.idleMessage()
			else:
				self.input_invalid += 1
		
		elif len(self.input) == 4:
			if self.input[0] in ["show","give"] and self.input[2] in ["to"]:
				if self.input[3] not in [each_npc.name.lower() for each_npc in self.npc]:
					print "There is nobody named that here."
				else:
					if self.input[1] in char.inventory.keys() and char.inventory[self.input[1]][0] > 0:
						print each_npc.showMessage()
					else:
						print "You need to have the item to show it to the person."
			elif self.input[0] in ["ask","tell"] and self.input[2] in ["about"]:
				if self.input[1] not in [each_npc.name.lower() for each_npc in self.npc]:
					print "There is nobody named that here."
				else:
					print each_npc.tellMessage()
			else:
				self.input_invalid += 1
		else:
			self.input_invalid += 1
	
	#This is in case a room has its own exclusive checks/commands. Since this is a generic room, it doesn't have any.
	def additionalChecks(self, char):
		if 0 is 0:
			self.input_invalid += 1
	
	#If input_invalid does not match any of the above 3 functions and has input_invalid as 3, then the input is invalid.
	def checkForInvalidInput(self):
		if self.input_invalid < 4:
			self.input_invalid = 0
			input = ""
		elif self.input_invalid >= 4:
			print "Invalid input."
			self.input_invalid = 0
			input = ""

class npc(object):
	location = ""
	desc = ""
	
	def __init__(self,name):
		self.name = name
	
	def idleMessage(self):
		pass
		
	def showMessage(self):
		pass
	
	def tellMessage(self):
		pass

#NPC IMPLEMENTATION------------------------------------------------------------------------------------------------
class testnpcs(npc):
	location = "Room 101"
	desc = "This is an invisible test bot. How did you find him? You can talk to him, if you want."
	
	def idleMessage(self):
		if char1.inventory["money"][0] > 0:
			return "<Test> Hello. You have money."
		else:
			return "<Test> Hello. You don't have money."
	
	def showMessage(self):
		return "<Test> Yay."
	
	def tellMessage(self):
		return "<Test> I am not going to tell you anything."
		
testnpc = testnpcs("Test")

	

#ROOM IMPLEMENTATION------------------------------------------------------------------------------------------------
#See how rooms are made. It is the easiest thing in the world now.

#ROOM 101
class room101(room):
	name = "[Room 101]"
	desc = "You have no idea how or why you are here. There is a path to the NORTH."
	items = ["money","toothpick"]
	npc = [testnpc]
	directions = {
		"north" : "Room 102"
	}

Room101 = room101()

#ROOM 102
class room102(room):
	name = "[Room 102]"
	desc = "There is a path to the south and north."
	npc = []
	directions = {
		"south" : "Room 101"
	}

Room102 = room102()

#MAIN IMPLEMENTATION-----------------------------------------------------------------------------------------------
class Main(char):
	
	rooms = {
		1 : Room101,
		2 : Room102
	}

	#Location of said player.
	location = "Room 101"

	#Inventory shows item name, amount of item, and description of item, respectively.
	inventory = {
		"money" : [0,"It seems to be a one dollar bill. Of course, in this period of time, it's quite worthless."],
		"toothpick" : [0,"It is a toothpick."]
	}

char1 = Main()

#EXECUTION---------------------------------------------------------------------------------------------------------
#Actual execution of the code.

char1.inNewRoom = 1

#Loops continuously and checks where the person is, and gives the corresponding functions.
while 0 is 0:
	if char1.location == "Room 101":
		if char1.inNewRoom is 1:
			Room101.seeroom()
			char1.inNewRoom = 0
		Room101.roominput(char1)
		
	if char1.location == "Room 102":
		if char1.inNewRoom is 1:
			Room102.seeroom()
			char1.inNewRoom = 0
		Room102.roominput(char1)
		
		