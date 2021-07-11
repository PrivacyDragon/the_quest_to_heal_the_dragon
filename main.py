import re, os, sys, json
################### THE FOLLOWING IS THE DECLARING OF SOME SYSTEM SPECIFIC STUFF ##############################
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
if os.name in 'nt': #For Windows there are two possible Home variables. On Windows7 there are HOMEDRIVE and HOMEPATH, but Windows10 seems to have HOME.
	if os.getenv("HOMEDRIVE") == "None": #If the variable HOMEDRIVE doesn't exist, assume that the HOME variable has to be used.
		HOME = os.environ["HOME"]
	else: #Otherwise, use the HOMEDRIVE and HOMEPATH
		HOME = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
else: #For Linux it is just HOME.
	HOME = os.environ["HOME"]
################### HERE ARE SOME GLOBAL VARIABLES DECLARED ##############################
#First the items that are on the locations are defined.
inventory = []
items_cave1 = []
items_cave2 = []
items_cave3 = []
items_cave4 = ["a wooden star", "a longsword"]
items_cave5 = ["yellow flowers", "blue flowers", "red flowers", "purple flowers", "white flowers"]
items_dragon = []
items_flower = ["a Dracoflorum sylvestris"]
items_grass1 = []
items_grass2 = []
items_grass3 = []
items_house1 = ["a pickaxe", "a letter", "a waterbottle"]
items_house2 = ["a cleaning cloth"]
items_house3 = ["a thermos bag"]
items_path1 = []
items_path2 = []
items_path3 = []
items_path4 = []
items_path5 = []
items_path6 = []
items_path7 = []
items_path8 = []
items_path9 = []
items_shop = []
items_wizard = []
#Then the default current place is defined.
current = "grass1"
value = ""
#Then some global variables are defined for determining whether the player can or cannot go somewhere.
before_path8 = ""
cave3_open = False
cave5_star = False
cave5_active = False
gate_wizard = False
window_clean = False
monster_alive = True
####### THE FOLLOWING VARIABLES ARE FOR DEFINING WHERE THE USER GOES FOR NORTH, EAST, SOUTH AND WEST FOR EACH PLACE. IF ONE OF THE DIRECTIONS IS LEFT OUT, IT IS HANDLED ON IT'S OWN. #######
stat_cave1 = {
	"north":"none",
	"east":"none",
	"south":"cave2",
	"west":"none",
	"back":"cave2"
}
stat_cave2 = {
	"north":"cave1",
	"south":"grass3",
	"west":"none",
	"back":"grass3",
	"quit":"grass3",
	"exit":"grass3"
}
stat_cave3 = {
	"north":"none",
	"east":"none",
	"south":"none",
	"west":"path1",
	"back":"path1",
	"quit":"path1",
	"exit":"path1"
}
stat_cave4 = {
	"north":"none",
	"east":"none",
	"south":"house1",
	"west":"none",
	"back":"house1",
	"quit":"house1",
	"exit":"house1"
}
stat_cave5 = {
	"north":"none",
	"east":"none",
	"south":"none",
	"west":"cave2",
	"back":"cave2"
}
stat_dragon = {
	"north":"none",
	"east":"path6",
	"west":"none"
}
stat_flower = {
	"north":"none",
	"east":"path8",
	"south":"none",
	"west":"none"
}
stat_grass1 = {
	"north":"path1",
	"east":"house1",
	"south":"none",
	"west":"grass2"
}
stat_grass2 = {
	"east":"grass1",
	"south":"none",
	"west":"grass3"
}
stat_grass3 = {
	"north":"cave2",
	"east":"grass2",
	"south":"house2",
	"west":"none"
}
stat_house1 = {
	"north":"cave4",
	"east":"none",
	"south":"none",
	"west":"grass1",
	"back":"grass1",
	"quit":"grass1",
	"exit":"grass1"
}
stat_house2 = {
	"north":"grass3",
	"east":"none",
	"south":"none",
	"west":"none",
	"back":"grass3",
	"quit":"grass3",
	"exit":"grass3"
}
stat_house3 = {
	"north":"none",
	"east":"none",
	"south":"none",
	"west":"path3",
	"back":"path3",
	"quit":"path3",
	"exit":"path3"
}
stat_path1 = {
	"north":"path2",
	"south":"grass1",
}
stat_path2 = {
	"north":"path3",
	"east":"shop",
	"south":"path1",
}
stat_path3 = {
	"north":"path4",
	"east":"house3",
	"south":"path2",
	"west":"none"
}
stat_path4 = {
	"north":"none",
	"east":"none",
	"south":"path3",
}
stat_path5 = {
	"north":"none",
	"east":"path4",
	"south":"path6",
	"west":"none"
}
stat_path6 = {
	"north":"path5",
	"east":"none",
	"south":"none",
	"west":"dragon"
}
stat_path7 = {
	"north":"none",
	"east":"path2",
	"south":"none",
}
stat_path8 = {
	"no stuff is defined here":"skip"
}
stat_path9 = {
	"east":"none",
	"south":"grass2",
	"west":"none"
}
stat_shop = {
	"north":"none",
	"east":"none",
	"south":"none",
	"west":"path2",
	"back":"path2",
	"quit":"path2",
	"exit":"path2"
}
stat_wizard = {
	"north":"none",
	"east":"path1",
	"south":"none",
	"west":"none",
	"back":"path1",
	"quit":"path1",
	"exit":"path1"
}


## THIS FUNCTION IS FOR IF THE USER WANTS TO GO SOMEWHERE WHERE THE FIRE BEGINS. THIS ARE: FROM PATH4 TO PATH5, FROM PATH2 TO PATH7 AND FROM GRASS2 TO PATH9. ##
def die_by_fire(direction, before, after):
	if not "a Fire Amulet" in inventory: #So here I check if the user has the fire amulet.
		print("It is not possible to walk in the fire! are you mad!?")
		return before #The function die_by_fire is called with the result going into 'place', so if nothing is returned, the place is messed up and the game will crash...
	else:
		#In the game the user has to get a magical potion to heal the dragon. This potion is highly explosive. So if the user walks into the fire without having done something to make sure that the potion cannot get hot, the potion will explode. What the user has to do is putting the potion in a thermos bag, but if the user hasn't done that yet but actually *does* have the thermos bag, I am not going to complain.
		if ("A Magical Potion" in inventory or "a magical potion" in inventory)  and "a thermos bag" not in inventory:
			print("You walk to the " + direction + ". You step in the fire, but because of the amulet, it cannot harm you. At the moment the potion for the dragon enters the fire, it gets hot and explodes. You are torn to pieces and you die. You are dead.\n\n Magically, you reincarnate somewhere, though you have lost all your stuff... Probably you can find it where you died.\n\n")
			#If the user dies, the inventory gets dropped at the place where the user was. Because there are two potions, one with caps and one without caps, I first have to check which one the user has. and only put away that one.
			#Of course, if the potion explodes it is fully gone.
			if "A Magical Potion" in inventory:
				inventory.remove("A Magical Potion")
			if "a magical potion" in inventory:
				inventory.remove("a magical potion")
			#And then for every item in the inventory, it is added to the items of the place where the user is, and then removed from the inventory.
			for item in inventory:
				eval("items_" + before + ".append(item)")
				inventory.remove(item)
			eval("items_" + before + ".remove(\"a Fire Amulet\")") #Stupid Python doesn't work how I want it to work, so do this to make sure there don't come problems.
			inventory.append("a Fire Amulet")
			#If the user dies, the main spot to 'respawn' is grass1.
			print(grass1())
			return "grass1"
		#This is the else for if the user does not have the potion without thermos bag in the inventory. Then there isn't a potion to explode, so that is much more boring ;)
		else:
			#To the West of path2 is path7. Yes, this is still about if the user wants to go West.
			print(eval(after + "()"))
			return after

################### THE FOLLOWING TWO FUNCTIONS ARE THE FUNCTIONS WHERE IS CHECKED WHAT SHOULD HAPPEN, DURING THE GAME ##############################
#The static_commands function is always run in the function that checks what to do with the input of the user.
def static_commands(value, items):
	global cave3_open
	global cave5_star
	#This fist part catches the problem that would eist if the user does not specify what should be taken.
	if value.lower() == 'take' or value.lower() == 'pick': #Just 'take' or 'pick' without anything else is not usable.
		print("Please specify what you want to take. Like 'take ITEM'")
		return True
	#The following looks for the item that should be taken and places it in the inventory.
	# --------------------------------------------------------V: This space here makes sure that you don't get to see nothing if you type 'pickaxe'...
	elif re.findall("take", value.lower()) or re.findall("pick ", value.lower()) or (re.findall("harvest", value.lower()) and items == items_cave5):#The harvest is only for the flowers in cave5, I see if the player is in cave5 by looking if items is items_cave5, because items is always the items of the current place, so items_cave5 only for cave5.
		taken = False
		if items == items_cave5: #Cave5 has it's own item picking rule.
			for item in items:
				if re.findall(item, value.lower()):
					print("Taken " + item + "!")
					inventory.append(item)
					taken = True
		else:
			for item in items:
				if re.findall(item.split()[1], value): #I split the item string at the spaces, because the strings are like 'a ....' and I only want to check for the part after 'a'.
					print("Taken " + item + "!")
					inventory.append(item)
					taken = True
					items.remove(item)
		if not taken: #If taken is still False, that means that there isn't taken anything, which means it couldn't be found.
			print("It is not possible to take that, you made a typo or you weren't specific. E.G: \'star\' instead of \'wooden star\'.")
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Here comes the function to check if the user wants to drop an item.
	#First check if the user actually specifies what should be dropped.
	if value.lower() == 'drop': #So if the value is only 'drop' and nothing more, there should come a warning/error.
		print("Please specify what you want to drop. Like 'drop ITEM'. Be sure that you also add the 'a' or 'an' before.")
		return True
	#Then is looked what item should be dropped and drop it if it is in the inventory.
	elif re.findall("drop", value.lower()):
		item = value.split("drop ")[1] #if the user says "drop an item", the value is split to ['','an item']. there index 1 is the item: 'an item'.
		#If the item actually is in the inventory, drop it. Remove it from the inventory and add it to the items of the current place.
		if item in inventory:
			inventory.remove(item)
			eval("items_" + current + ".append(\"" + item + "\")")
		else:
			#If it can't be found, tell that to the user.
			print("That item is not in your iventory, you made a typo or you didn't mention the full item. You should make sure to add the 'a' or 'an' before the item!")
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Then I check if the user wants to inspect something. Actually the only thing that can be inspected is the letter.
	elif re.findall("inspect", value.lower()) or re.findall("look at", value.lower()) or re.findall("read", value.lower()):
		if re.findall("letter", value.lower()): #Though the only inspectable thing is the letter, there still has to be checked if that is what the user wants to inspect
			if "a letter" in inventory: #You know, it is pretty hard to inspect something if you don't have it...  
				print("You inspect the letter and see that it is addressed to the wise wizard. It reads as follows:\nDear wizard, Here are the instructions on how to ask something to the gods. You must get an offer, but it also has to be the right offer. In the Western cave is a hidden room, that has to be opened with a certain machine. In that room, you will find flowers in several colors. Take the white flowers if you want help with healing, take the red flowers if you want help with killing.")
				return True
			elif current != "cave1" and current != "path1": #In cave1 and path1 the other inspect options are defined for itself, so for there, this two lines should be skipped.
				print("You cannot inspect something that you don't have")
				return True
		else:
			return False
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#To be able to complete this game, the user should do something to make sure that the potion doesn't explode. The right way to do this is by putting the potion in a thermos bag, that will keep it cold.
	elif re.findall("potion", value.lower()) and re.findall("thermos bag", value.lower()) and re.findall("in", value.lower()):
		if "a thermos bag" in inventory and ("A Magical Potion" in inventory or "a magical potion" in inventory): #Of course, it is kinda hard to use something if you don't have it, so that should first be checked.  
			print("You do the potion in the thermos bag.")
			inventory.remove("a thermos bag") #The potion will be put in the thermos bag, which creates a new item: 'A potion in a thermos bag'. (or with capitals depending on the potion version). So then the thermos bag is removed.
			if "A Magical Potion" in inventory:
				inventory.remove("A Magical Potion") #Same as for the thermos bag, remove it from the inventory to give the user the item where the potion is in the bag.
				inventory.append("a Potion in a thermos bag") #Which is done here.
			elif "a magical potion" in inventory:
				inventory.remove("a magical potion") #And this is actually exactly the same, but then for the potion without caps.
				inventory.append("a potion in a thermos bag")
		else: #Once again, you can't do something with something that you don't have. If the user doesn't have the thermos bag or the potion, this message will be printed to inform that both are needed.
			print("Cannot do that. You need both the potion and the thermos bag to put the potion in the thermos bag")
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#The next thing that is checked is if the player wants to use something.
	elif re.findall("use", value.lower()):
		if re.findall("waterbottle", value.lower()):
			#In this game the waterbottle is an unnecessary object. You can actually not do anything with it. It shouldn't be made too easy right? :)
			if "a waterbottle" in inventory: #There should be checked if the player actually has a waterbottle to use...
				print("What do you want to do with the water bottle? You cannot extinguish the fire with it, if that was what you were trying to do... It would be very strange if that would be possible...")
				return True
			else:
				print("You cannot use something that you don't have!")
				return True
		
		elif re.findall("pickaxe", value.lower()):
			if current == "path1" and re.findall("cave", value.lower()):
			#The user has to use a pickaxe to be able to crack the rock, to be able to enter cave3. This is the only use for the pickaxe.
				if "a pickaxe" in inventory:
					#Of course, the player should have the pickaxe to be able to use it...
					print("You use your pickaxe to break the big rock in front of the cave.")
					cave3_open = True
					return True
				else:
					print("You cannot use something that you don't have!")
					return True
			else:
				#If the user is not on path1, the user cannot use the pickaxe.
				if current != "path":
					print("You cannot use the pickaxe here")
				else:
					print("What do you want to use the pickaxe for?")
				return True
		elif current == "house2" and re.findall("star", value.lower()):
			if "a wooden star" in inventory: #Again, you can't use something that you don't have...
				print("You put the wooden star in the star-shaped hole of the machine and suddenly you hear something click.")
				cave5_star = True #Set that the star is placed in the hole.
				inventory.remove("a wooden star") #Once the user has placed it in the hole, the star isn't in the inventory anymore. duh.
			else: #If the user does not have the wooden star, an error shows.
				print("You don't have the right thing to put in the hole.")
		else: #Make sure that there is an 'error' if the user wants to use something that can't be used.
			print("You cannot use that.")
			return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Probably the user wants to get the description of the current place again. That is what is checked here. If the user says 'look', the description of the current place is displayed again.
	elif value.lower() == "look":
		print(eval(current + "()"))
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#With '/inventory' or '/i' the user can show the inventory.
	elif value.lower() == "/inventory" or value.lower() == "/i":
		print("Currently you have the following stuff in your inventory: " + ", ".join(inventory)) #Showing the inventory is very easy, by just letting the items in inventory 'joining' the string.
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#With '/help' or '/h' the user can get a small description of how to navigate trough the game.
	elif value.lower() == "/help" or value.lower() == "/h":
		print("Command me what to do. You can give commands like: 'inspect ...' or 'take ...' or 'use ...' etc. and you can say that I should walk somewhere by just saying 'North', 'East', 'South', 'West'.\n Use commands like: /inventory or /i to see your inventory, /help or /h to show help and /exit or /e to exit the game.")
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#And with '/about' the user can get some general information about the game.
	elif value.lower() == "/about":
		print("---------------------------------------------------------------\nThis game was made for CC25 on Cemetech. It was made within one month of time, and actually most of the game was written during the last two weeks.\nWritten in: Python3\nAuthor: Privacy_Dragon\nContact: privacy_dragon@tutanota.com\nTested on: Linux OpenSuse Leap 15.1, Windows7 Home Basic via QEMU\n ---------------------------------------------------------------")
		return True
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def actions(place, value):
	#The first thing that I do here, is defining that I want to use the global variables for 'current', 'cave5_active', 'cave5_star', 'gate_wizard' and 'window_clean'. This is the best possible way that I can think of at the moment.
	global before_path8
	global current
	global cave3_open
	global cave5_active
	global cave5_star
	global gate_wizard
	global monster_alive
	global window_clean
	
	print("\n")#Do this just to make it look better.
	#####WHAT FOLLOWS NOW, IS THE PROCESSING OF THE COMMAND. WHERE THE USER WANTS TO GO OR WHAT THE USER WANTS TO DO. IN GENERAL, THE WHERE TO GO STUFF IS HANDLED IN THE FIRST LINES, BUT FOR SOME DIRECTIONS FOR SOME PLACES IT IS HANDLED LATER ON IT'S OWN. #######
	#First, change 'n', 'e', 's' and 'w' into the right direction.
	if value.lower() == "n":
		value = "north"
	elif value.lower() == "e":
		value = "east"
	elif value.lower() == "s":
		value = "south"
	elif value.lower() == "w":
		value = "west"
	#Every place has a 'stat_PLACE' dictionary, where PLACE is the place. Of course, that can only be used if the command is findable in the dictionary. So first check that.
	if value.lower() in eval("stat_" + current):
		print(eval(eval("stat_" + current + "[\"" + value.lower() + "\"]") + "()")) #Here I am printing the function that is linked to the direction that the user goes. like "stat_grass1["north"]" contains handling going from grass1 to the North. I want to do to execute the function: `eval(stat_grass1["north"] + "()")`. So to make that possible, I should first do eval("stat_" + current + "[\"" + value + "\"]") to get the place, and then eval(THAT + "()") and in a print statement to print the return value.
		place = eval("stat_" + current + "[\"" + value.lower() + "\"]") #And then the place that is there listed in the dictionary is set in variable place. To update the current variable in the end of this 'actions()' function.
	elif eval("static_commands(value, items_" + current + ")"): #Then see if the command that the user gave can be handled in static_commands. It will then be automatically be handled. True is returned if it is handled succesfully. :)
		return
	else:
		value = value.lower()
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		if current == "cave1":
			#In cave1 is a window, that lets you look at the password that is needed to open the gate of the Wizard.
			if re.findall("inspect", value) or re.findall("look", value): #If the user says: 'inspect window' or 'look at window' or something similar, a description should be given.
				if re.findall("window", value):
					if window_clean:#Make sure that the user has cleaned the window
						print("You look closely at the window and you see the following text: 'WizardOfDragons'") #The password of the wizard's gate is "WizardOfDragons'
					else:
						#If the window is not yet cleaned, the description of the dusty window should be given.
						print("You look closely at the window and you see that it is dusty. You cannot see anything trough it.")
				#If the user only says: 'inspect' it is not clear what should be inspected. You can't inspect nothingness! (Well, of course it would be possible and probably quite interesting, but in this game not :P)
				elif len(value.split()) == 1:
					print("You cannot inspect nothingness...")
				#And then at last, if the user doesn't want to inspect the window nor nothingness, just say that it is not possible to inspect whatever the user wants to inspect.
				else:
					print("You cannot inspect that...")
			#There is a dusty window, so that should be cleaned, if the user says something like 'clean (the) window' that is going to happen.
			elif re.findall("clean", value) or re.findall("undust", value) or re.findall("wipe", value):
				if re.findall("window", value):
					if "a cleaning cloth" in inventory: #Check if the user actually has the cleaning cloth to clean the window with...
						print("You clean the window and see that you now actually can look trough it!")
						window_clean = True
					else: #This is printed if the user does NOT have a cleaning cloth. You cannot clean such a dusty window with your bare hands.
						print("What do you want to clean the window with? You need a cleaning cloth for that!")
				elif len(value.split()) == 1:
					#And again, it is not possible to clean nothingness, that is actually really not possible even in real live I assume...
					print("You cannot clean nothingness...")
				else:
					#And again, at last, if the user dosn't want to clean the window nor nothingness, just say that it is not possible to clean whatever the user wants to clean.
					print("You cannot clean that...")
			else:
				#If the command that the user gave is not recognized anywhere, give an error.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "cave2":
			#To the East of cave2 is cave5, but it is only accessible if cave5 is opened.
			if value == "east":
				if cave5_active == True:
					print(cave5())
					place = "cave5"
				else:
					#So if cave5 is not yet opened, it is not possible to go there; That will then be printed.
					print("It is not possible to go there...")
			else:
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "cave3":
			#In cave3 is the altar for the gods. There the flowers can be offered. There are white and red flowers that can be offered, both have slightly difficult effect...
			if re.findall("offer", value):
				#So first is checked if the user wants to offer the white flowers.
				if re.findall("flower", value) and re.findall("white", value):
					if "white flowers" in inventory: #Of course, it is not possible to offer something that you don't have.
						print("You put the white flowers on the altar and suddenly a god appears. \"This is the potion that you want. You should know that you also need something to make sure it will work for the dragon. On the crossing of the monster you should go West to collect a special flower, the Dracoflorum Sylvestris. Then you can go to the dragon. You should give him the flower and the potion and say the following magic sentence: \'Folium cum flore Dracoflori et Medicamentum Magicae, please heal this dragon!\'. Though it is not easy, because the potion is very explosive, so please make sure it doesn't get hot!\"")
						if not "A Magical Potion" in inventory: #Only add the potion if the user doesn't have it.
							inventory.append("A Magical Potion") #NOTE: The potion you get with the white flowers is with caps, the potion from the red flowers is without caps. If you have both at the end, the white one is used by default.
							inventory.remove("white flowers") #Remove the flowers from the inventory, because they have now been used.
					else:
						#If the user does not have the white flowers, there will come a warning.
						print("It is not possible to offer something that I don't have")
				#Then is checked if the user wants to offfer the red flowers.
				elif re.findall("flower", value) and re.findall("red", value):
					if "red flowers" in inventory: #Again, it is not possible to offer something that you don't have.
						print("You put the red flowers on the altar and suddenly a god appears. \"This is the potion that you want. You should know that you also need something to make sure it will work for the dragon. On the crossing of the monster you should go West to collect a special flower, the Dracoflorum Sylvestris. Then you can go to the dragon. You should give him the flower and the potion and say the following magic sentence: \'Folium cum flore Dracoflori et Potio Magicae, please work for this dragon!\'. Though it is not easy, because the potion is very explosive, so please make sure it doesn't get hot!\"")
						if not "a magical potion" in inventory: #Only add the potion if the user doesn't have it.
							inventory.append("a magical potion") #NOTE: The potion you get with the white flowers is with caps, the potion from the red flowers is without caps. If you have both at the end, the white one is used by default.
							inventory.remove("red flowers") #Remove the flowers from the inventory, because they have now been used.
					else:
						#If the user does not have the red flowers, there will come a warning.
						print("It is not possible to offer something that you don't have.")
				else:
					#If there is not specified what to offer or if there is not specified which flowers to offer, this warning will be showed.
					print("Cannot use that. If you think that isn't right, maybe try to be more detailed.")
			else:
				#And at last: if the command that the user gave is not recognized anywhere, give an error.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "dragon":
			#To the South of the dragon is path8.
			if value == "south":
				print(path8())
				place = "path8"
				before_path8 = "dragon" #The variable 'before_path8' is used to make it possible for the user to go back when arriving on path8 and fearing the monster.
			#The main goal in this game is to heal the dragon. So this if-statement checks if the user wants to 'HEAL the DRAGON' or 'USE the POTION'.
			elif (re.findall("heal", value) and ("dragon", value)) or (re.findall("use", value) and re.findall("potion", value)):
				#The dragon can only be healed if the user has the flower and the potion. Because the potion becomes 'a potion in a thermos bag' when you put it in the thermos bag, it should also be checked if that is in the inventory, because the userr might not think about having to get it out of the bag.
				#As you might or might not remember, on lines 329 and 339 I told that the potion with the caps is the correct one, and the one without caps is the bad one. Here that is relevant, because it has influence on what happens.
				if "a Dracoflorum sylvestris" in inventory and ("a Magical Potion" in inventory or "a Potion in a thermos bag" in inventory):
					#If the user has the right one, healing the dragon succeeds! NOTE that the text that the user has to say is somewhat different for the bad potion. Here it is "....et Medicamentum..." for the bad one it is "....et Potio..."
					print("You take the Dracoflorum and the potion and give them both to the dragon. Then you say: \"Folium cum flore Dracoflori et Medicamentum Magicae, please heal this dragon!\". In an instant the dragon looks much better and a minute later, he completely recovered. At this moment the wise wizard appears and he uses his magical powers to let all the fire go away.\n\nCongratulations! You have ended this game successfully!!!")
					#After the user has succesfully healed the dragon, exit the game.
					raise SystemExit
				elif "a Dracoflorum sylvestris" in inventory and ("a magical potion" in inventory or "a potion in a thermos bag" in inventory):
					#If the user has the wrong potion, the dragon will be killed by it. Then the user is very much GAME OVER.. 
					print("You take the Dracoflorum and the potion and give them both to the dragon. Then you say: \"Folium cum flore Dracoflori et Potio Magicae, please work for this dragon!\". In an instant the dragon looks much worse and a minute later, he died. The wizard comes to you and says in a furious voice: \"Why did you kill the dragon!? You used the wrong flowers! Why did you mean to kill him! Traitor! Child of the Devil! Go away!\". Then he casts a very powerful spell and you fall into nothingness. You are locked in the nothingness...\n\nGAME OVER...")
					#If the user is game over, exit the game.
					raise SystemExit
				#But if the user does not have all the items needed, give a warning.
				else:
					print("You cannot heal the dragon, because you don't have everything needed!")
			else:
				#If the command that the user gave is not recognized, this warning is given.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "grass2":
			#To the North of grass2 is path9, but that is on fire.
			if value == "north":
				place = die_by_fire("North", "grass2", "path9")
			else:
				print("Sorry, I don't understand what you want me to do")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "house2":
			#In house2, the wooden star has to be put in the hole to be able to pull the handle.
			if re.findall("star", value) and ((re.findall("hole", value) and re.findall("in", value)) or re.findall("use", value)): #This handles putting the star in the hole.
				if not "a wooden star" in inventory: #Again, you can't use something that you don't have...
					print("You don't have the right thing to put in the hole.")
				else:  #If the user DOES have the star, it can be used.
					print("You put the wooden star in the star-shaped hole of the machine and suddenly you hear something click.")
					cave5_star = True #Set that the star is placed in the hole.
					inventory.remove("a wooden star") #Once the user has placed it in the hole, the star isn't in the inventory anymore. duh.
			#The next thing handles pulling the handle.
			elif (re.findall("use", value) or re.findall("pull", value)) and re.findall("handle", value):
				if cave5_star: #Because the star should be put in the shape before the machine can work, it is checked if that is done.
					print("At the moment you pull the handle, the machine begins to make a lot of rattling noises and it is getting hot. It continues rattling for several minutes before it stops with a loud 'click'.")
					cave5_active = True #Set the variable 'cave5_active' to True, so that cave5 is open.
				else:
					print("You try very hard to pull the handle, but for some reason it seems to be stuck")
			#If the command that the user gave is not recognized anywhere, give an error.
			else:
				print("Sorry, I don't understand what you want me to do")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path1":
			if value == "east":
				if cave3_open: #Check if the user can actually go in the cave, or that there still is that huge rock.
					print(cave3())
					place = "cave3"
				else:
					if "a pickaxe" in inventory: #If the cave is still blocked, but the user has the pickaxe, the destroying of the rock is done 'automatically'.
						print("You use your pickaxe to destroy the huge rock and you enter the cave.\n" + cave3())
						place = "cave3"
						#Set the variable of whether the cave is open to True.
						cave3_open = True
					else:
						#If the user does not have the pickaxe, this is displayed.
						print("The entrance of the cave is closed by a huge rock. You have nothing to destroy it.")
			#To the West of path1 is the home of the wise wizard.
			elif value == "west":
				if gate_wizard: #check if the gate is already opened.
					print(wizard())
					place = "wizard"
				else:
					print("The gate is closed, so it is not possible to go that way...")
			 #If the user says: 'inspect gate' or 'look at port' or something similar, a description should be given.
			elif re.findall("inspect", value) or re.findall("look", value):
				if re.findall("gate", value) or re.findall("port", value):
					print("You look at the big gate. If you look past it, you can see a round home which gives you a strange feeling. Just beside the gate, on your side, is a panel, where you can type something. Above that, you find a symbol of a wand.")
				#If the user just says "inspect", tell that it is not possible to inspect nothingness...
				elif len(value.split()) == 1:
					print("You cannot inspect nothingness...")
				#If the user wants to inspect something else, say that it is not possible to inspect that.
				else:
					print("You cannot inspect that...")
			#The gate to the wizard has to be unlocked before it is possible to go there. So here I check if the user wants to unlock or open the gate.
			elif (re.findall("unlock", value) or re.findall("open", value)) and re.findall("gate", value):
				print("You go to the gate and see the panel where you can enter the password.")
				password = input("\nPlease type the password:")
				#The right password for the gate is "WizardOfDragons". So only if that password is entered, the gate will open.
				if password == "WizardOfDragons":
					print("You enter the password and the gate opens")
					#If the gate is opened is stored in the variable 'gate_wizard'. So if the password is correct, the variable is set True.
					gate_wizard = True
				else:
					#And if the wrong password is entered, then the user will get to see that.
					print("You enter the password and the display shows: WRONG PASSWORD")
			else:
				#And at last, if the command that the user gave is not recognized anywhere, give a warning.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path2":
			#To the West of path2 is path7, but that is on fire.
			if value == "west":
				place = die_by_fire("West", "path2", "path7")
			else:
				#And at last, if the command that the user gave is not recognized anywhere, give a warning.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path4":
			#To the West of path4 is path5. But this path is on fire. It is not possible to walk trough fire without burning under normal circumstances. The wizard will give a fire amulet, so that it is possible to walk trough the fire, but as long as you don't have that, it shouldn't be possible to go into the fire.
			if value == "west":
				place = die_by_fire("West", "path4", "path5")
			else:
				#And at last, if the command that the user gave is not recognized anywhere, give a warning.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path7":
			#To the west of path7 is path8.
			if value == "west":
				print(path8())
				place = "path8"
				before_path8 = "path7" #The variable 'before_path8' is used to make it possible for the user to go back when arriving on path8 and fearing the monster.
			else:
				#If the command that the user gave is not recognized anywhere, give a warning.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path8":
			#On path8 is a monster, there are different things for if the monster is alive and if the monster isn't alive.
			if monster_alive:
				#If the user wants to go to any direction, there will again be said that there is a huge monster on the road. If you think twice, you would probably not continue.
				if value == "north" or value == "east" or value == "south" or value == "west":
					print("There is a huge monster on the road, do you really want to continue?")
					#Let the user choose wheter to continue or not.
					choise = input("Y/N: ")
					if choise.upper() == "Y":
						#If the user has chosen for continue, then it is checked wheter the inventory contains the longsword or not.
						if not "a longsword" in inventory:
							#If the user does not have the sword, (s)he just dies.
							print("You walk past the monster and wish him a good day. The monser isn't really nice though, since he attacks you. you die.\n\nMagically, you reincarnate somewhere, though you have lost all your stuff... Probably you can find it where you died.\n\n")
							#If the user dies, the inventory gets dropped at the place where the user was.
							#for every item in the inventory, it is added to the items of the place where the user is, and then removed from the inventory.
							for item in inventory:
								items_path8.append(item)
								inventory.remove(item)
							#If the user dies, the main spot to 'respawn' is grass1.
							place = "grass1"
							print(grass1())
						else:
							#This is if the user DOES have a longsword.
							#Even though you have a sword, you die.
							print("You walk past the monster and wish him a good day. The monser isn't really nice though, since he attacks you. Fortunately you have a longsword, so you unpack it as fast as you can. But unfortunately, this is not fast enough. You should probably start the attack yourself... You die.\n\nMagically, you reincarnate somewhere, though you have lost all your stuff... Probably you can find it where you died.\n\n")
							#If the user dies, the inventory gets dropped at the place where the user was.
							#for every item in the inventory, it is added to the items of the place where the user is, and then removed from the inventory.
							for item in inventory:
								items_path8.append(item)
								inventory.remove(item)
							#If the user dies, the main spot to 'respawn' is grass1.
							place = "grass1"
							print(grass1())
					else:
						#This is what is displayed if the user does choose to NOT continue.
						print("I am glad that you aren't an idiot.")
				#The user can choose to attack the monster. This is the only way to get it out of the way.
				elif re.findall("attack", value) and re.findall("monster", value):
					#It is only possible to attack the monster if the user has the longsword.
					if "a longsword" in inventory:
						print("You draw your sword and attack the monster. It is a tough fight, but in the end, you just manage to kill the monster.")
						#If the monster is fought, the variable in which is stored whether he is alive or not is set to False.
						monster_alive = False
					else:
						#If the user does not have a longsword, it should be asked if the user really wants to continue to attack the monster.
						print("What do you want to attack the monster with? With words? Are you sure that you want to continue?")
						choise = input("Y/N: ")
						#If the user chooses for continuing, the user dies.
						if choise.upper() == "Y":
							print("You let out a great battle cry and kick the monster as hard as you can. This doesn't do much to the monster and he manages to kill you in less than a second. You die.\n\nMagically, you reincarnate somewhere, though you have lost all your stuff... Probably you can find it where you died.\n\n")
							#If the user dies, the inventory gets dropped at the place where the user was.
							#for every item in the inventory, it is added to the items of the place where the user is, and then removed from the inventory.
							for item in inventory:
								items_path8.append(item)
								inventory.remove(item)
							#If the user dies, the main spot to 'respawn' is grass1.
							place = "grass1"
							print(grass1())
						
						else:
							#This is what is displayed if the user does choose to NOT continue, which is the best option.
							print("I am glad that you aren't an idiot.")
				#You can choose on path8 to go back, then you don't have to walk past the monster.
				elif re.findall("back", value) or re.findall("return", value):
					print(eval(before_path8 + "()"))
					place = before_path8
				else:
					#If the command that the user gave is not recognized, this warning is given.
					print("Sorry, I don't understand what you want me to do.")
			#The following is for when the monster isn't alive anymore.
			else:
				#To the North of path8 is the dragon.
				if value == "north":
					print(dragon())
					place = "dragon"
				#To the East of path8 is path7.
				elif value == "east":
					print(path7())
					place = "path7"
				#To the South of path8 is path9.
				elif value == "south":
					print(path9())
					place = "path9"
				#To the West of path8 is the field where the 'Dracoflorum sylvestris' stands.
				elif value == "west":
					print(flower())
					place = "flower"
				else:
					#If the command that the user gave is not recognized, this warning is given.
					print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "path9":
			#To the North of path9 is path8.
			if value == "north":
				print(path8())
				place = "path8"
				before_path8 = "path9" #The variable 'before_path8' is used to make it possible for the user to go back when arriving on path8 and fearing the monster.
			else:
				#If the command that the user gave is not recognized, this warning is given.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "shop":
			#In the herbal shop stands a man. It is possible to talk to him.
			if re.findall("talk", value) or re.findall("speak", value):
				#If the user wants to talk, the person says what the user has to do to go further on the quest of healing the dragon.
				print("Welcome stranger. I hear you want a medicine to heal the dragon? Sadly I don't have that. A dragon is so much different from humans, our medicines don't work on them. Though not all hope is lost: you can visit the old wise wizard who lives West of the fallen tree. It is possible you need a password to enter. If so, you can find it in the cave to the West. Though I don't know if the window to the password is still clean, you might need to get a cleaning cloth out of one of the houses before you go to the cave.")
			else:
				#If the command that the user gave is not recognized, this warning is given.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		elif current == "wizard":
			#Because there is only the wizard to talk to, if the user says only 'talk' it is clear that the user wants to talk to the wizard.
			if re.findall("talk", value) or re.findall("speak", value):
				#If the user wants to talk, the wizard tells how to probably heal the dragon and gives the Fire Amulet, so that the user can walk trough the fire without being harmed by it.
				print("Welcome, I have been waiting for you. The dragon is having a really hard time because he is very sick. Unfortunately, he has already put part of the trees on fire. I can fix that though, but only after he is healed. I cannot help him, since he seems to have some strange kind of sickness that can't be cured by my magic. But don't be affraid, there might still be one option to cure him; East from here, there is a cave dedicated to the gods. If you can go there and bring the gods an offering, they might be willing to help. I once had a letter with instructions about how to get the right offer, but it got stolen... So you will have to find out yourself or find that letter...\nI will give you one item to help you on your quest. With this Fire Amulet, you will be able to walk trough the fire without getting burned. Good luck!")
				#To make sure that the user doesn't get the amulet twice, firs check if the player already has it.
				if "a Fire Amulet" in inventory:
					return
				#If the user doesn't have it, add the fire amulet to the inventory.
				else:
					inventory.append("a Fire Amulet")
			else:
				#If the command that the user gave is not recognized, this warning is given.
				print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
		else:
			print("Sorry, I don't understand what you want me to do.")
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	
	
	
	#At last, after each turn, the 'current' variable is updated. 'place' is always the new place.
	if place != "none":
		current = place

################### THE FOLLOWING FUNCTIONS ARE THE FUNCTIONS FOR STARTING, SAVING, RESUMING, (ETC.) A GAME ##############################
def start(): #Every time that the game is started, the function 'start' is called.
	option = input("Please type: resume, start or exit\n") #ask if the user wants to start a new game or continue one.
	if (re.findall("resume", option)): #Resuming a game happens in loadGame().
		loadGame()
	elif (re.findall("start", option)): #Starting a game happens in createGame().
		createGame()
	elif (re.findall("exit", option)): #For exiting, just exit the program.
		raise SystemExit
	else:
		#If the user says something else thatn 'resume', 'start', or 'exit', that is not a valid option. then start the function again. I know, this is very awfull. Why do you think I try to make sure that every time the program is aborted it is handled by the program...
		print("ERROR: not a valid option")
		start()

def createGame(): #This is the function that starts a new game.
	print("Some code is setting up the game right now!\n") #First tell the user that everything is being set up.
	try: #Here it is tried to create two new files. One  For the inventory and one for the place where the user is.
		try: #First it should be tried to create a new folder in the .config folder.
			os.mkdir(HOME + "/.config")
			os.mkdir(HOME + "/.config/The-quest-to-heal-the-dragon")
		except:
			print("") #If it goes wrong with creating the folder, it can be that the folder already exists. So don't display anything yet.
		stat = open(HOME + "/.config/The-quest-to-heal-the-dragon/.current", "w") #Then create in the new folder a file .current. Well, open it for writing.
		stat.write("") #And then write nothing it. This is actually more like a test if this works on the OS that the user uses.
		stat.close() #Then close the file.
		invent = open(HOME + "/.config/The-quest-to-heal-the-dragon/.inventory", "w") #And now do exactly the same for the .inventory file.
		invent.write("")
		invent.close()
	except:
		#If something goes wrong, notice the user and tell that a bug report should be made if this keeps happening.
		print("Oh no! something went wrong! If this keeps happening, please report it to privacy_dragon@tutanota.com and mention your Python version and OS.")
		start() #Then Go back to the 'start()' function.
	#You see the following only when you start a new game, so it is placed here in this function.
	print("Oh no! the dragon has a cold!!! Please help!\nAs everyone knows, dragons that have a cold are dangerous, especially here in the woods. Oh please help to make sure the trees don't get on fire!\nDear person, please get the dragon some medicine before it is too late! Maybe the herbal shop has something. You can find it somewhat to the North.\nOH NO!!! Some trees just got on fire, it might be too late! Please help!\n\nI will be your hands and eyes. Just tell me what to do by giving commands. You can give commands like: 'inspect ...' or 'take ...' or 'use ...' etc. and you can make me walk somewhere by just saying 'North', 'East', 'South', 'West'.\n Use commands like: /inventory or /i to see your inventory, /help or /h to show help and /exit or /e to exit the game.\n---\n")
	#Then go to grass1, which is the main start spot.
	print(grass1())
	#And then go to the real game function.
	game()

def saveGame(): #This is the function that saves a game, when you exit.
	global current #Use the global current variable.
	invent = open(HOME + "/.config/The-quest-to-heal-the-dragon/.inventory", "w") #Open the .inventory file.
	curr = open(HOME + "/.config/The-quest-to-heal-the-dragon/.current", "w") #And open the .current file.
	stat = open(HOME + "/.config/The-quest-to-heal-the-dragon/.stat", "w") #And open the .stat file.
	invent.write(json.dumps(inventory)) #Then write to the .inventory file all inventory items.
	curr.write(current) #And write to the .current file the current location.
	stat.write(json.dumps([cave3_open, cave5_star, cave5_active, gate_wizard, window_clean, monster_alive, before_path8])) #Write the variables for defining if something is open/activated, to the .stat file.
	invent.close() #Then close the .inventory file.
	curr.close() #And close the .current file.
	stat.close() #And close the .stat file.

def loadGame(): #This is the function that loads a saved game.
	global before_path8
	global cave3_open
	global cave5_active
	global cave5_star
	global gate_wizard
	global window_clean
	global current #Make sure to use the global 'current' variable.
	global inventory #Make sure to use the global 'inventory' variable.
	print("\nloading...\n") #Let the user know that the game is being loaded.
	try: #I assume that someone has already played once, but because I cannot know for sure, use try - except in case the .inventory and/or .current file does not exist.
		inv = open(HOME + "/.config/The-quest-to-heal-the-dragon/.inventory") #Open the .inventory file.
		curr = open(HOME + "/.config/The-quest-to-heal-the-dragon/.current") #And open the .current file.
		stat = open(HOME + "/.config/The-quest-to-heal-the-dragon/.stat") #And the .stat file.
		current = curr.read() #Put the content of the .current file in variable current and then close the file.
		inventory = json.loads(inv.read()) #Put the content of the .inventory file in the inventory variable and then close the file.
		bools = json.loads(stat.read()) #Put the content of the .stat file in variable bools and then close the file.
		curr.close()
		inv.close()
	except: #If something went wrong, it is almost certain to be that the .inventory and/or .current file doesn't exist.
		print("Whoops, I couldn't find any saved game file :(")
		#Then exit the program.
		raise SystemExit
	#Place the booleans in their right variables.
	cave3_open = bools[0]
	cave5_star = bools[1]
	cave5_active = bools[2]
	gate_wizard = bools[3]
	window_clean = bools[4]
	monster_alive = bools[5]
	before_path8 = bools[6]
	######IN THE FOLLOWING LINES I MAKE SURE THAT ITEMS IN THE INVENTORY ARE NOT ALSO AT THEIR ORIGINAL PLACE, BECAUSE THEY ARE TAKEN #######
	if "a wooden star" in inventory:
		items_cave4.remove("a wooden star")
	if "a longsword" in inventory:
		items_cave4.remove("a longsword")
	if "a pickaxe" in inventory:
		items_house1.remove("a pickaxe")
	if "a letter" in inventory:
		items_house1.remove("a letter")
	if "a waterbottle" in inventory:
		items_house1.remove("a waterbottle")
	if "a cleaning cloth" in inventory:
		items_house2.remove("a cleaning cloth")
	if "a thermos bag" in inventory:
		items_house3.remove("a thermos bag")
	if "a Dracoflorum sylvestris" in inventory:
		items_flower.remove("a Dracoflorum sylvestris")
	#####THEN GET THE CURRENT PLACE IN current, RUN THE DESCRIPTION OF IT AND GO TO THE GAME. ######
	print(eval(current + "()"))
	game()

#The following is the main game function.
def game():
	while True: #Just do the folowing forever.
		value = input() #First get user input.
		if value == "/exit" or value == "/e": #Then, if it is /exit or /e break out of the while loop. 
			break
		actions(current, value) #Otherwise, run the 'actions' functions, which is that big function where most stuff happen.
	clear() #This stuff is only executed after the while loop, so only if the user says /exit or /e. Then first the screen is cleared.
	saveGame() #Then the game is saved.
	print("Exited!") #The user is noticed that the game is exited.
	raise SystemExit #And then exit the game for real.

################### THE FOLLOWING FUNCTIONS ARE THE DESCRIPTIONS OF THE AREAS. ##############################
def grass1():
	if items_grass1 == []:
		return "You are standing on a field that extends West. You can see a forest to the North and a house to the East."
	else:
		return "You are standing on a field that extends West. You can see a forest to the North and a house to the East. You see the following items: " + ", ".join(items_grass1) + "."
def grass2():
	if items_grass2 == []:
		return "You are standing on a large field. In the North you see a wood that is on fire, far away in the East you see a house and in the South you see something that looks much like a building." 
	else:
		return "You are standing on a large field. In the North you see a wood that is on fire, far away in the East you see a house and in the South you see something that looks much like a building. You also see the following items: " + ", ".join(items_grass2) + "."
def grass3():
	if items_grass3 == []:
		return "You are standing at the end of a large field that extends East. In the North, you see some kind of cave and in the South you see a building."
	else:
		return "You are standing at the end of a large field that extends East. In the North, you see some kind of cave and in the South you see a building. You also see the following items: " + ", ".join(items_grass3) + "."

def house1():
	if items_house1 == []:
		return "You are in a house and at the Northern exit you see a path that seems to go to a cave. At the Western exit you see a meadow."
	else:
		return "You are in a house and see the following items: " + ", ".join(items_house1) + ".\nYou see at the Nothern exit a path that seems to go to a cave, at the Western exit you see a meadow."
def house2():
	if items_house2 == []:
		return "You are in a small building and you see some kind of machine. It is very big and heavy. The whole left-side wall is covered with the installation and in front of you, you see a big handle and a star-shaped hole."
	else:
		return "You are in a small building and you see some kind of machine. It is very big and heavy. The whole left-side wall is covered with the installation and in front of you, you see a big handle and a star-shaped hole. you also see: " + ", ".join(items_house2) + "."
def house3():
	if items_house3 == []:
		return "You are in a house with a beautifull table. Furthermore, the marble floor suggests that it is a pretty luxurious house."
	else:
		return "You are in a house with a beautifull table. On that table you see: " + ", ".join(items_house3) + ". Furhtermore, the marble floor suggests that it is a pretty luxurious house."

def cave1():
	if items_cave1 == []:
		return "You are standing at the end of a misty cave and on your left side you see some kind of window."
	else:
		return "You are standing at the end of a misty cave and on your left side you see some kind of window. There also are some items lying on the ground: " + ", ".join(items_cave1) + "."
def cave2():
	if items_cave2 == []:
		if cave5_active == True:
			return "You are standing in a long misty cave. You hear water dripping and some light shines trough small holes. To the East, you see a passage that has opened, leading to another cave. To the North, you see the cave stretching out in the mist."
		else:
			return "You are standing in a long misty cave. You hear water dripping and some light shines trough small holes. To the North, you see the cave stretching out in the mist."
	else:
		if cave5_active == True:
			return "You are standing in a long misty cave. You hear water dripping and some light shines trough small holes. You see the following items: " + ", ".join(items_cave2) + ". On the East side of the cave, you see a passage that has opened, leading to another cave. To the North, you see the cave stretching out in the mist."
		else:
			return "You are standing in a long misty cave. You hear water dripping and some light shines trough small holes. You see the following items: " + ", ".join(items_cave2) + ". To the North, you see the cave stretching out in the mist."
def cave3():
	if items_cave3 == []:
		return "You are standing in a small cave. In front of you, you see an altar for the gods."
	else:
		return "You are standing in a small cave.In front of you, you see an altar for the gods. On the ground you see some items: " + ", ".join(items_cave3) + "."
def cave4():
	if items_cave4 == []:
		return "You are standing in a small cave which looks like once people lived there."
	else:
		return "You are standing in a small cave which looks like once people lived there. You can also see the following items on the ground: " + ", ".join(items_cave4) + "."
def cave5():
	if len(items_cave5) <= 5: #Cave5 has always the flowers, so that can be in a normal description. though if there are more than five items, that means there is more than only the flowers, so that is how I know that then also the items should be showed.
		return "You are standing in a beautiful round cave. A few sun rays shine trough the ceiling, giving a magical feeling. You see five kinds of flowers. Yellow, blue, red, purple and white flowers."
	else:
		return "You are standing in a beautiful round cave.  A few sun rays shine trough the ceiling, giving a magical feeling. You see several stuff. You see: " + ", ".join(items_cave5) + "."

def path1():
	if items_path1 == []:
		return "You are standing on a crossroads in the woods. At the north you can see a fallen tree and at the south you see a meadow. At the East is a cave and at the West is a gate."
	else:
		return "You are standing on a crossroads in the woods. At the north you can see a fallen tree and at the south you see a meadow. At the East is a cave and at the West is a gate. On the ground you see: " + ", ".join(items_path1) + "."
def path2():
	if items_path2 == []:
		return "You are standing on a crossroads in the woods. At the North you see the path continuing. At the NorthEast you see a building. At the East you see a herbal shop and at the South you see a fallen tree and a path. at the west you see a path that continues in fire."
	else:
		return "You are standing on a crossroads in the woods. At the North you see the path continuing. At the NorthEast you see a building. At the East you see a herbal shop and at the South you see a fallen tree and a path. at the west you see a path that continues in fire. On the ground you see: " + ", ".join(items_path2) + "."
def path3():
	if items_path3 == []:
		return "You are standing on a road. You see a large house at the East and to the North the path continues and makes a turn. At the South you see a crossroads."
	else:
		return "You are standing on a road and you see the following items: " + ", ".join(items_path3) + ". You also see a large house at the East and to the North the path continues and makes a turn. At the South you see a crossroads. "
def path4():
	if items_path4 == []:
		return "You are standing on a path. Far to the south you see a building and to the West the path continues in fire."
	else:
		return "You are standing on a path. Far to the south you see a building and to the West the path continues in fire. You also see some items on the ground: " + ", ".join(items_path4) + "."
def path5():
	if items_path5 == []:
		return "You are standing on a path in fiery woods. At the East you see the path leaves the fire, at the South the path continues, seeming to go to the Dragon."
	else:
		return "You are standing on a path in fiery woods. You see some items on the ground: " + ", ".join(items_path5) + ". At the East you see the path leaves the fire, at the South the path continues, seeming to go to the Dragon."
def path6():
	if items_path6 == []:
		return "You are standing on a path amidst the fiery woods. The path extends to the North and West. To the West, you can also see a dragon."
	else:
		return "You are standing on a path amidst the fiery woods. The path extends to the North and West. At the West, you can also see a dragon. Furthermore, you see some items before you: " + ", ".join(items_path6) + "."
def path7():
	if items_path7 == []:
		return "You are standing on a path in the fiery woods. At the East you see the path leaves the fire, but At the West it continues. At the West there seems to be a monster, whereas to the East there seems to be a herbal shop in the distance."
	else:
		return "You are standing on a path in the fiery woods. You see some items: " + ", ".join(items_path7) + ". To the East you see the path leaves the fire, but to the West it continues. At the West there seems to be a monster, whereas to the East there seems to be a herbal shop in the distance."
def path8():
	if monster_alive:
		if items_path8 == []:
			return "You are standing before a crossroads in the fiery woods. There is a big monster on the crossing. At the North, you can go to the dragon. To the East and South there is just another path. To the West is a small field."
		else:
			return "You are standing before a crossroads in the fiery woods. There is a big monster on the crossing. At the North, you can go to the dragon. To the East and South there is just another path. To the West is a small field. You can also see some items on the ground before you: " + ", ".join(items_path8) + "."
	else:
		if items_path8 == []:
			return "You are standing before a crossroads in the fiery woods. At the North you can go to the dragon, to the East and South there is just another path and to the West is a small field."
		else:
			return "You are standing before a crossroads in the fiery woods. At the North you can go to the dragon, to the East and South there is just another path and to the West is a small field. On the ground before you, there are some items: " + ", ".join(items_path8) + "."
def path9():
	if items_path9 == []:
		return "You are standing on a path and the trees around you are all aflame. At the North you see a crossroads with a monster on it and At the South you see a meadow where isn't fire yet."
	else:
		return "You are standing on a path and the trees around you are all aflame. At the North you see a crossroads with a monster on it and At the South you see a meadow where isn't fire yet. You can also see some stuff: " + ", ".join(items_path9) + "."

def wizard():
	if items_wizard == []:
		return "You are standing in the round house of the old wise wizard. You see the wizard sitting on a chair."
	else:
		return "You are standing in the round house of the old wise wizard. You see the wizard sitting on a chair. You also see some items: " + ", ".join(items_wizard) + "."

def shop():
	if items_shop == []:
		return "You are standing in a small herbal shop. You see a friendly person before you."
	else:
		return "You are standing in a small herbal shop. You see a friendly person before you. You also see something lying on the floor: " + ", ".join(items_shop) + "."

def dragon():
	if items_dragon == []:
		return "You are standing in the woods. There is fire all around you. at a clearing before you there is a sick-looking dragon. The path continues to the East and South."
	else:
		return "You are standing in the woods. There is fire all around you. at a clearing before you there is a sick-looking dragon. The path continues to the East and South. You can also see: " + ", ".join(items_dragon) + "before you."

def flower():
	if items_flower == []:
		return "You are standing on a small field with magical green grass."
	else:
		return "You are standing on a small field with magical green grass. On the field you see: " + ", ".join(items_flower) + "."

def none():
	return "It is not possible to go there..."

################### THE FOLLOWING IS A CHECK OF COMMANDLINE ARGUMENTS AND THE 'MAIN' FUNCTION. ##############################
if len(sys.argv) >= 2: #If there are commandline arguments given, the sys.argv should be 2 or more.
	if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "help": #When the commandline arguments '--help', '-h' or 'help' are given, this small description is given.
		print("---------------------------------------------------------------\nThis game was made for CC25 on Cemetech. It was made within one month of time, and actually most of the game was written during the last two weeks.\nWritten in: Python3\nAuthor: Privacy_Dragon\nContact: privacy_dragon@tutanota.com\nTested on: Linux OpenSuse Leap 15.1, Windows7 Home Basic via QEMU\n ---------------------------------------------------------------\nIn this game you have to cure a dragon that has caught a cold. To do this, you will have to go to people, find clues and collect items.\nI really hope that everyone enjoys playing this game!!\n")
		raise SystemExit #To be able to let the program only output that description, after that the program is exited.
	else: #If there are other commandline arguments given, notice that it is an unknown option and exit the program.
		print("ERROR: unknown commandline option")
		raise SystemExit

#And here we have the 'main' function.
if __name__ == "__main__":
	try:
		clear() #First clear the screen, then say welcome and then start.
		print("Welcome to the game!\n")
		start()
	#If the user uses ^C, handle it the same as /e or /exit.
	except KeyboardInterrupt:
		clear()
		saveGame()
		print("Exited!")
		raise SystemExit
	except SystemExit: #I have to do this because otherwise it gets messed up if I raise SystemExit from within the game... Stupid Python
		raise SystemExit
	"""except:
		clear()
		saveGame()
		print("Oh no! An error occured!")
		raise SystemExit
 """
