#AI class
class AI:


	def __init__(self,puzzle,style):
		self.activepuzzle = puzzle
		self.style = style


	def breath_first(self):
		pass
	def depth_first(self):
		pass

	def Astar(self):
		pass
	


	def solution_finder(self,style,step):

		if self.activepuzzle.is_goal_match():
			return	"goal"
		elif self.activepuzzle.closedstate():
			return  "closed"
		else :
			if style == "Breadth First":
				self.breath_first()
			elif style == "Depth First":
				self.depth_first()
			else:
				self.Astar()
			

	def ai_run(self):
		pass


