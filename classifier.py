import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import pickle

class Classifier:
	def train(): 
		# name of file containing the requirements samples
		file_name = 'requirementsDataset.csv' 
		# read the excel file
		dataset = pd.read_csv(file_name)
		target_names = ['Functional','Non-functional']
		data = dataset.Requirements
		target = dataset.Classification
		target = target.replace(to_replace = ['Non-functional','Functional'],value = [1,0])
		train_data,test_data,train_target,test_target = train_test_split(data,target,test_size=0.2,random_state=42)
		text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
		text_clf.fit(train_data, train_target)  
		predicted = text_clf.predict(test_data)
		print(np.mean(predicted == test_target))    
		print(metrics.classification_report(test_target, predicted,target_names=target_names))
		print(metrics.confusion_matrix(test_target, predicted))
		# save the model to disk
		modelFileName = 'model.sav'
		pickle.dump(text_clf, open(modelFileName, 'wb'))

	def classify():
		requirementsListFile = 'elicitedRequirements.txt' 
		target_names = ['Functional','Non-functional']
		modelFileName = 'model.sav'  
		text_clf = pickle.load(open(modelFileName, 'rb'))
		with open(requirementsListFile) as file:
			data = [line.strip() for line in file]
		predicted = text_clf.predict(data)
		fr="Functional Requirements:\n"
		nfr="Non-functional Requirements:\n"
		for req, category in zip(data, predicted):
			if category==0:
				fr = fr +"FR:"+ req + "\n"
			else:
				nfr = nfr +"NFR:" + req + "\n"
		classifiedRequirementsList =  fr + nfr
		classifiedRequirementsListFile = open("ClassifiedRequirements.txt","w")
		classifiedRequirementsListFile.write(classifiedRequirementsList)
		classifiedRequirementsListFile.close()
		return classifiedRequirementsList
