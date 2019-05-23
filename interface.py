import speech_recognition as sr
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from REBO import ReboDialog
from bot import BotEngine
from classifier import Classifier
import pyttsx3
import requests
import os
class Interface(QDialog):
	name=""
	def __init__(self):
		super().__init__()
		self.ui=ReboDialog()
		self.ui.setupUi(self)
		
		#setting event handlers 
		self.ui.nextPushButton.clicked.connect(self.saveUserDetails)
		self.ui.clearPushButton.clicked.connect(self.clearDetails)
		self.ui.audioPushButton.clicked.connect(self.convertToText)
		self.ui.sendPushButton.clicked.connect(self.handleUserResponse)
		self.ui.classificationPushButton.clicked.connect(self.handleClassifyButtonClicked)
		self.ui.exitButton.clicked.connect(self.endProgram)
		
		
	#Function to store the details and move to next screen
	def saveUserDetails(self):
		self.name=self.ui.nameLineEdit.text()
		contact=self.ui.contactLineEdit.text()
		email=self.ui.emailLineEdit.text()
		company=self.ui.companyNameLineEdit.text()
		f=open("%s.txt"%contact,"w+")
		str=("Name:- "+self.name+"\nContact:- "+contact+"\nEmail:- "+email+"\nCompany:- "+company+"\n")
		f.write(str)
		self.ui.ReboStack.setCurrentIndex(self.ui.ReboStack.indexOf(self.ui.chatScreen))
		f = open("elicitedRequirements.txt","w")
		f.close()

	#Function to clear text fields	
	def clearDetails(self):
		self.ui.companyNameLineEdit.setText("")
		self.ui.contactLineEdit.setText("")
		self.ui.emailIDLabel.setText("")
		self.ui.nameLineEdit.setText("")
	
	#Function to convert speech to text
	def convertToText(self):
		r = sr.Recognizer()
		mic=sr.Microphone(device_index=0)  
		with mic as source:
			r.adjust_for_ambient_noise(source) 
			audio = r.listen(source)
		self.ui.inputLineEdit.setText(r.recognize_google(audio))
	
	def convertToAudio(self,text):
		engine = pyttsx3.init()
		engine.say(text)
		engine.runAndWait() 		
	
	def handleUserResponse(self):
		userResponse = self.ui.inputLineEdit.text()
		self.ui.inputLineEdit.setText("")
		self.ui.chatTextEdit.append("\nUser : "+userResponse)
		responses = BotEngine.getBotResponse(userResponse)
		for botResponse in responses:
			botResponseText = botResponse['text']
			if botResponseText=='change screen':
				self.changeToDisplayRequirementsScreen()
				break
			#self.convertToAudio(botResponse)
			self.ui.chatTextEdit.append("\nBot : "+botResponseText)
			os.system("say "+ botResponseText);		
			

	def changeToDisplayRequirementsScreen(self):
		# change screen
		self.ui.ReboStack.setCurrentIndex(\
	        self.ui.ReboStack.indexOf(self.ui.elicitedRequirementsScreen))		
		# open requirements file
		f=open("elicitedRequirements.txt","r")
		# display the requirments
		for x in f:
			self.ui.elicitedTextEdit.append("\n"+x)
			
	def handleClassifyButtonClicked(self):
		# change to classified requirements screen
		self.ui.ReboStack.setCurrentIndex(\
	        self.ui.ReboStack.indexOf(self.ui.classifiedRequirementScreen))
		# call classifier
		req=Classifier.classify()
		# display
		splitIndex = req.index("Non-functional Requirements:")
		fi=req.index("FR:")
		ni=req.index("NFR:")
		Fr = req[fi:splitIndex]
		Nfr = req[ni:]
		self.ui.functionalRequirementTextEdit.setText(Fr)
		self.ui.nonFunctionalRequirementsTextEdit.setText(Nfr)
		
	def endProgram(self):
		sys.exit()
		
def main():
	app = QApplication(sys.argv)
	# Create a window and Initialize the user interface 
	window = Interface()
	# Display the window
	window.show()
	# Terminate the program when the window is closed
	sys.exit(app.exec_())

 #Entry point of the program
if __name__=="__main__":
	# Call the main method
	main()