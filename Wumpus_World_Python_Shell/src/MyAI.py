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

class MyAI ( Agent ):

	def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		self.curr = {"loc" : [1, 1], "d" : 0, "wall" : ["W", "S"], "state" : []}
		self.face = "E"
		self.path = []
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
		self.path.append(self.curr)
		if (stench or breeze) and self.curr == [1, 1]:
			return Agent.Action.CLIMB
		if glitter:
			self.gold = True
			return Agent.Action.GRAB
		if not stench and not breeze and not glitter and not bump:
			self.curr = [1, 1]
			return Agent.Action.FORWARD
		if bump:
			return Agent.Action.TURN_LEFT

		#if self.curr == [1, 1]:
		#	return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
	def updateCurr( self ):
		if self.face = "E":
			self.curr["loc"][1] += 1
		elif self.face = "W":
			self.curr["loc"][1] -= 1
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
