from subprocess import Popen, PIPE, STDOUT
from sklearn.externals import joblib

class DefacementClassifier():

	def __init__(self):
		self.clfSVM = joblib.load('ai/models/svm.pkl')
		self.clfPA = joblib.load('ai/models/passive_aggressive.pkl')
		self.scaler = joblib.load('ai/scalers/standard_scaler.pkl')

	def isDefaced(self, path):
		features = self.getFeatures(path)
		transformed = self.scaler.transform([features])
		labelSVM = self.clfSVM.predict(transformed)[0]
		labelPA = self.clfPA.predict(transformed)[0]
		return labelSVM or labelPA

	def getFeatures(self, path):
		p = Popen(['java', '-jar', './lire_extract.jar', '-p', path], stdout=PIPE, stderr=STDOUT)
		f = [l for l in p.stdout]
		print f
		if len(f) != 1:
			raise Exception('LIRE failure')
		f = f[0].replace('\n', '')
		return [float(x) for x in f.split(' ')]

	def train(self, path, isDefaced):
		features = self.getFeatures(path)
		label = 1 if isDefaced else 0
		self.clfPA.partial_fit([features], [label])
		joblib.dump(self.clfPA, 'ai/models/passive_aggressive.pkl')