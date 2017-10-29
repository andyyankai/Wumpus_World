# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
import copy
class MyAI ( Agent ):

	def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		self.curr = {"loc" : [1, 1], "d" : 0, "wall" : ["W", "S"], "state" : []}
		self.face = "E"
		self.path = [{"loc" : [1, 1], "d" : 0, "wall" : ["W", "S"], "state" : []}]
		self.gold = False
		self.breeze = False
		self.stench = False
		self.glitter = False
		self.back = False
		self.tabu = []

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

	def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		if glitter:
			self.gold = True
			self.back = True
			return Agent.Action.GRAB
		if self.curr["loc"] == [1, 1] and self.back == True:
			return Agent.Action.CLIMB
		if (stench or breeze) and self.curr["loc"] == [1, 1]:
			return Agent.Action.CLIMB
		if stench or breeze or self.back == True:
			self.back = True
			return self.backHome()
		if not stench and not breeze and not glitter and not bump:
			self.updateCurr()
			self.path.append(copy.deepcopy(self.curr))
			return Agent.Action.FORWARD
		if bump:
			self.updateFaceL()
			return Agent.Action.TURN_LEFT


        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
	def updateCurr( self ):
		if self.face == "E":
			self.curr["loc"][1] += 1
		elif self.face == "W":
			self.curr["loc"][1] -= 1
		elif self.face == "N":
			self.curr["loc"][0] += 1
		elif self.face == "S":
			self.curr["loc"][0] -= 1
		self.curr["d"] = self.curr["loc"][0] + self.curr["loc"][1]
	
	def updateFaceL( self ):
		if self.face == "E":
			self.face = "N"
		elif self.face == "W":
			self.face = "S"
		elif self.face == "N":
			self.face = "W"
		elif self.face == "S":
			self.face = "E"
			
	def updateFaceR( self ):
		if self.face == "E":
			self.face = "S"
		elif self.face == "W":
			self.face = "N"
		elif self.face == "N":
			self.face = "E"
		elif self.face == "S":
			self.face = "W"

	def backHome( self ):
		print(self.face)
		for node in self.path:
			if node["d"] < self.curr["d"]:
				if self.face == "E":
					print("loli1")
					if node["loc"][1] == self.curr["loc"][1] + 1 and node["loc"][0] == self.curr["loc"][0]:
						self.path.remove(self.curr)
						self.updateCurr()
						return Agent.Action.FORWARD
					elif node["loc"][1] == self.curr["loc"][1] -1 and node["loc"][0] == self.curr["loc"][0]:
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] + 1:
						self.updateFaceR()
						return Agent.Action.TURN_RIGHT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] - 1:
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					
				elif self.face == "W":
					print("loli2")
					if node["loc"][1] == self.curr["loc"][1] - 1 and node["loc"][0] == self.curr["loc"][0]:
						print("1")
						self.path.remove(self.curr)
						self.updateCurr()
						return Agent.Action.FORWARD
					elif node["loc"][1] == self.curr["loc"][1] + 1 and node["loc"][0] == self.curr["loc"][0]:
						print("2")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] + 1:
						print("3")
						self.updateFaceR()
						return Agent.Action.TURN_RIGHT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] - 1:
						print("4")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
				elif self.face == "N":
					print("loli3")
					if node["loc"][1] == self.curr["loc"][1] + 1 and node["loc"][0] == self.curr["loc"][0]:
						print("1")
						self.updateFaceR()
						return Agent.Action.TURN_RIGHT
					elif node["loc"][1] == self.curr["loc"][1] -1 and node["loc"][0] == self.curr["loc"][0]:
						print("2")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] + 1:
						print("3")
						self.path.remove(self.curr)
						self.updateCurr()
						return Agent.Action.FORWARD
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] - 1:
						print("4")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
				elif self.face == "S":
					print("loli4")
					if node["loc"][1] == self.curr["loc"][1] + 1 and node["loc"][0] == self.curr["loc"][0]:
						print("1")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					elif node["loc"][1] == self.curr["loc"][1] -1 and node["loc"][0] == self.curr["loc"][0]:
						print("2")
						self.updateFaceR()
						return Agent.Action.TURN_RIGHT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] + 1:
						print("3")
						self.updateFaceL()
						return Agent.Action.TURN_LEFT
					elif node["loc"][1] == self.curr["loc"][1] and node["loc"][0] == self.curr["loc"][0] - 1:
						print("4")
						self.path.remove(self.curr)
						self.updateCurr()
						return Agent.Action.FORWARD
		
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
