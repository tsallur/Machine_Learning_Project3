#Thomas Sallurday
#Professor Hodges
# CPSC 6430
# 10/26/2020
import math as np

def cleanUp(text): #function that removes unecessary characters from email subject lines
    text = text.lower()
    text = text.strip()
    for letters in text:
        if letters in """[]!.,"-!—@;':#$%^&*()+/?""":
            text = text.replace(letters," ")
    return text
def organize(words,identifier,counted): #puts email subject words into a dictionary
#and counts how many times the subject word appears in SPAM and HAM emails
    for val in words:
        if(val in counted):
            if(identifier == 1):
                counted[val][1] = counted[val][1] + 1
            else:
                counted[val][0] = counted[val][0] + 1
        else:
            if(identifier == 1):
                counted[val] = [0,1]
            else:
                counted[val] = [1,0]
    return counted
def makePercentList(k,theCount,spams,hams): #changes the counts of HAM and SPAM into %'s
# also smooths out the values
    for key in theCount:
        theCount[key][0] = (theCount[key][0] + k) / (2 * k + hams)
        theCount[key][1] = (theCount[key][1] + k) / (2 * k + spams)
    return theCount

k = 1 #k-value for smoothing
spamCounter = 0
hamCounter = 0
str1 = input("Please enter the filename of the spam-ham file: ")
trainData = open(str1,'r',encoding = 'unicode-escape')
line = trainData.readline()
counted = dict()

while(line != ""): # while loop organizes data into dictionaries
    identifier = int (line[0])
    if(identifier == 1):
        spamCounter = spamCounter + 1
    else:
        hamCounter = hamCounter + 1
    line = cleanUp(line)
    words = line.split()
    
    words = set(words)
    counted = organize(words,identifier,counted)
    line = trainData.readline()
trainData.close()
vocab = makePercentList(k,counted,spamCounter,hamCounter) # makes percentages list
str1 = input("Please enter the filename of the stop-words file: ")
stopWords = open(str1,'r',encoding = 'unicode-escape')
line = stopWords.readline()
myList = list()
while(line != ""): #makes list of stopWords
    line = line.strip('\n')
    for val in vocab.keys():
        if(line == val):
            myList.append(val)
    line = stopWords.readline()
stopWords.close()     
for val in myList:
    vocab.pop(val) #deletes keys that are in myList

str1 = input("Please enter the filename of the Spam-Ham test file: ")
testFile = open(str1,'r',encoding = 'unicode-escape')
line = testFile.readline()

spamCounter2 = 0
hamCounter2 = 0
percentageOfSpam = spamCounter / (spamCounter + hamCounter)
percentageOfHam = hamCounter / (spamCounter + hamCounter)
hamProb = 0
spamProb = 0
truePositive = 0
trueNegative = 0
falsePositive = 0
falseNegative = 0
while(line != ""):
    identifier = int(line[0])
    line = cleanUp(line)
    words = line.split()
    for val in words:
        for key in vocab.keys():
            if(val == key):
                hamProb = hamProb + np.log(vocab[key][0])
                spamProb = spamProb + np.log(vocab[key][1])
            else:
                 hamProb = hamProb + np.log(( 1 - vocab[key][0]))
                 spamProb = spamProb + np.log((1 - vocab[key][1]))
    if(identifier == 1):
        spamCounter2 = spamCounter2 + 1
    else:
        hamCounter2 = hamCounter2 + 1
    top = 1
    hamProb = np.exp(hamProb)
    spamProb = np.exp(spamProb)
    bottom1 = np.log(hamProb * percentageOfHam)
    bottom2 = np.log(spamProb * percentageOfSpam)
    bottom3 =  1 + (np.exp(bottom1 - bottom2))
    answer = top / bottom3
    line = testFile.readline()
    hamProb = 0
    spamProb = 0
    if(answer >= 0.5 and identifier == 1):
        truePositive = truePositive + 1
    elif(answer >= 0.5 and identifier == 0):
        falsePositive = falsePositive + 1
    elif(answer < 0.5 and identifier == 0):
        trueNegative = trueNegative + 1
    elif(answer < 0.5 and identifier == 1):
        falseNegative = falseNegative + 1
    
                
testFile.close()
accuracy = (truePositive + trueNegative) / (truePositive + trueNegative + falsePositive + falseNegative)
precision = truePositive/ (truePositive + falsePositive)
recall = truePositive / (truePositive + falseNegative)
F1 = 2 * (1 / ((1/precision) + (1/recall)))



print("Number of Spam emails in test file: " + str(spamCounter2))
print("Number of Ham emails in test file: " +str(hamCounter2))
print("Number of true positives: " + str(truePositive))
print("Number of false positives: " + str(falsePositive))
print("Number of true negatives: " + str(trueNegative))
print("Number of false negatives: " +str(falseNegative))
print("Accuracy = " + str(accuracy))
print("Precision = " + str(precision))
print("Recall = " +str(recall))
print("F1 value: " + str(F1))
