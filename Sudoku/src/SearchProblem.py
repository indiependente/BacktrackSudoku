class SearchProblem:
	def exhaustiveSearch(self):
		for s in self.enumerateSI():
			if self.isAdmissible(s):
				return s
		return None

	def BackTrack(self,Empty=None):
		currentEmpty = self.computeNextEmpty(Empty)
		if self.verbose:
			print("Calling BackTrack on")
			print(self)
			print("with next empty in "+str(currentEmpty))
		if currentEmpty==None:
			return self.isAdmissible()

		for gamma in self.Gamma(currentEmpty):
			self.setNextEmpty(currentEmpty,gamma)
			if self.verbose:
				print("Trying to set "+str(gamma)+" in "+str(currentEmpty))
			if not self.isNotExtendible():
				if self.verbose:
					print("It seems ok\n")
				if self.BackTrack(currentEmpty):
					return True
			if self.verbose:
				print("It is not ok\n")
		if self.verbose:
			print("Finished all alternatives in "+str(currentEmpty))
		self.setNextEmpty(currentEmpty,self.emptySymbol)
		return False
