from blick import BlickLoader
import pandas


b = BlickLoader()

#Evaluating single strings of phones

score = b.assessWord(“T EH1 S T”) #Probable string in ARPABET format
print(score)
