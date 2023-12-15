import re

def formatName(name):
    """
    Formats the name passed to the function by removing everything
    except alphabets and whitespaces. Also captilises the string.

    Args:
        name (string): This is a name string as defined in the 
        assignment description, a single or multi word string.

    Returns:
        list: a list of strings where each strings are the words
        in the name
    """
    # Remove non-letter characters
    regexPattern = re.compile("[^a-zA-Z\s]+")
    cleanedName = regexPattern.sub("", name)

    # Convert the cleaned name to uppercase and 
    # split each words in the name into a list.
    capitalisedName = cleanedName.upper()
    words = capitalisedName.split()

    return words


def computeScores(wordList, alphabetScores):
    """
    Calculates the score of a supplied name based on the rules
    laid out in the assignment document. 

    Args:
        wordList (list): a list of strings which together make up 
        the name
        alphabetScores (dictionary): a dictionary containing the 
        scores of each letter.

    Returns:
        tuple: contains two lists. First one is a list of characters 
        which contains all the alphabets of the name in order. Second 
        one is a list of integers which contains all the scores of the 
        alphabets in the first list, in order. 
    """
    #lists containing the characters and scores respectively
    charList = []
    scoreList = []
    
    for word in wordList: 
        for index, char in enumerate(word):
            # first loop iterates through each word. Inner loop iterates through
            # each character in the word appending the character to the charList 
            # and appending its corresponding score in the scoreList.                  
            if index == 0:
                # first letter in the word gets a score of 0
                scoreList.append(0)
                charList.append(char)                             
            elif index == len(word) - 1:
                # last letter in the word gets either 20 or 5 
                if char == 'E':
                    scoreList.append(20)
                    charList.append(char)  
                else:
                    scoreList.append(5)
                    charList.append(char)                                
            else:
                # the words in between gets a score with its positional value
                # added to its corresponding value in the dictionary
                if index < 3:
                    scoreList.append(index + alphabetScores[char])
                    charList.append(char)    
                else:
                    scoreList.append(3 + alphabetScores[char])
                    charList.append(char)
    return charList, scoreList      
        

class NameAbbreviation:
    """
    Holds each name, its corresponding abbreviations,  
    the abbreviation(s) with the lowest score and 
    a reference to the dictionary holding the scores.
    
    Implements methods that adds an abbreviation and chooses
    the final abbreviation.
    """
    def __init__(self, name, abbreviationScoreDict):
        """
        instantiates a NameAbbreviation object.

        Args:
            name (string): a name string 
            abbreviationScoreDict (dict): dictionary containing all 
            the abbreviations and their scores.
        """
        self.name = name
        self.abbreviationList = []
        self.chosenAbbreviation = ''
        self.abbreviationScoreDict = abbreviationScoreDict
        
    def addAbbreviation(self, abbreviation, score):
        """
        Adds a newly generated abbreviation to the object and 
        adds its score to the abbreviationScoreDict.
        
        Args:
            abbreviation (string): three character string 
            holding the abbreviation
            score (int): score of the corresponding abbreviation
        """
        if abbreviation in self.abbreviationScoreDict.keys():    
            # chech if the abbreviation exists in the abbreviationScoreDict
            # If it does, check if it is because its been used for this word or
            # some other word. 
            if abbreviation in self.abbreviationList:
                # abbreviation is used for the same word. Compare the current abbreviation's
                # score with existing score to find the lowest score and update it
                # in the abbreviationScoreDict.
                oldScore = self.abbreviationScoreDict[abbreviation]
                if oldScore > score:
                    self.abbreviationScoreDict[abbreviation] = score
            else:
                # abbreviation is used for some other word. To denote the 
                # the abbreviation should not be used for any word, set its value
                # to -1 in the abbreviationScoreDict. This signifies an invalid
                # score and will be ignored by the getChosenAbbreviation(). The 
                # abbreviation is still maintained in the object for the time being.
                self.abbreviationList.append(abbreviation)
                self.abbreviationScoreDict[abbreviation] = -1
        else:
            # This is a new abbreviation, add it to the object and
            # add its score in the abbreviationScoreDict
            self.abbreviationList.append(abbreviation)
            self.abbreviationScoreDict[abbreviation] = score
        
    def getChosenAbbreviation(self):
        """
        Finds the abbreviation(s) associated with the 
        name having the lowest score and updates the 
        attribute chosenAbbreviation with that abbreviation.
             
        Returns:
            string: a three character abbreviation for the 
            name in the object with the lowest score. If no 
            valid abbreviation exist, it is an empty string.
        """
        # create a temporary dictionary containing only this 
        # name's abbreviations. All the invalid abbreviations
        # (abbreviations which are shared by multiple names)
        # with the value -1 are filtered out.
        abbreviationScores = {k:v for (k,v) in self.abbreviationScoreDict.items() if k in self.abbreviationList and v != -1}
        if abbreviationScores == {}:
            # No valid abbreviations, set an empty string
            self.chosenAbbreviation = ''
        else:
            # Sort the items of the temporary dictionary and 
            # find the abbreviation with the lowest score. 
            # There can be multiple abbreviations with the same
            # score.       
            sortedList = sorted(abbreviationScores.items(), key=lambda keyValuePair:keyValuePair[1])
            self.chosenAbbreviation = sortedList[0][0]
            valueList = list(abbreviationScores.values())
            lowestValue = sortedList[0][1]
            instanceCount = valueList.count(lowestValue)
            # count the number of occurence of the abbreviation
            # with the lowest value and if there are more than
            # one with the same score, add them all to the 
            # chosenAbbreviation attribute each separated by
            # spaces
            for index in range(instanceCount-1):
                self.chosenAbbreviation += " "
                self.chosenAbbreviation += sortedList[index+1][0]

        return self.chosenAbbreviation
 

def abbreviateNames():
    """
    Reads a file containing a set of names and produces 
    abbreviations for them. Names are expected to be at 
    least three letter long. The output which consits of
    the names and their corresponding abbreviations are
    written to a file.
    """
    
    # Get the file name and read the names into a list 
    inputFile = input("Enter the name of the text file: ")
    try:
        with open(inputFile, 'r') as file:
            rawNameList = file.read().split("\n")  
    except FileNotFoundError:
        print(f"Error: File '{inputFile}' could not be found")
        return
    
    abbreviationScoreDict = {}
    nameAbbreviaitonList = []
    alphabetScores = {'A': 25, 'B': 8, 'C': 8, 'D': 9, 'E': 35, 'F': 7, 'G': 9, 'H': 7, 'I': 25, 'J': 3,
                   'K': 6, 'L': 15, 'M': 8, 'N': 15, 'O': 20, 'P': 8, 'Q': 1, 'R': 15, 'S': 15, 'T': 15,
                   'U': 20, 'V': 7, 'W': 7, 'X': 3, 'Y': 7, 'Z': 1}

    for rawName in rawNameList:
        # for each name in the list of names read from the file,
        # calculate the abbreviation, its score and store them in 
        # a NameAbbreviation object. First the name is formatted 
        # and score for each character is computed.
        name = formatName(rawName)
        charList, scoreList = computeScores(name, alphabetScores)
        
        if len(charList) < 3:
            # Not enough words in the name to make a three letter 
            # abbreviation
            continue
        
        # Instatiate a NameAbbreviation object to store a name and
        # its abbreviations
        nameAbbreviation = NameAbbreviation(rawName, abbreviationScoreDict)
        
        # The first word of the abbreviation is always the first
        # letter of the name. Store the first letter and its score 
        # in a variable and remove them from the list before passing
        # them to the loop.
        score = scoreList[0]
        firstChar = charList[0]
        scoreList = scoreList[1:]
        charList = charList[1:]
        for index, char in enumerate(charList):
            # in this loop, the character that forms the second
            # letter in the abbreviation is selected
            if index == len(charList) - 1:
                # break out if we reach the last character.
                # all the possible abbreviations have been 
                # found at this point
                break
            
            # add the second letter and its score 
            abbreviation = firstChar + char
            score = scoreList[index]
            # slice the charList and scoreList to only include
            # the elements from the second letter (exclusive) 
            # before passing them to the loop
            loopCharList = charList[index + 1:]
            loopScoreList = scoreList[index + 1:]
            for loopIndex, loopChar in enumerate(loopCharList):
                # this loop adds the third letter and its score, finally creating
                # tne three letter abbreviation and invokes addAbbreviation() to add 
                # the abbreviation and the score to the nameAbbreviation object.              
                threeCharAbbreviation =  abbreviation + loopChar
                threeCharScore = score + loopScoreList[loopIndex]
                nameAbbreviation.addAbbreviation(threeCharAbbreviation, threeCharScore)
                
        # add each nameAbbreviation object to a list 
        nameAbbreviaitonList.append(nameAbbreviation)

    # create the output file name in the required format
    outputFile = "tom_" + inputFile[:-4] + "_abbrevs.txt"
    with open(outputFile, "w") as file:
        for nameAbbreviation in nameAbbreviaitonList:
            # write each name and its abbreviation to the output file             
            file.write(nameAbbreviation.name + "\n" + nameAbbreviation.getChosenAbbreviation() + "\n")            

            
def main():
    abbreviateNames()
    
    
if __name__ == "__main__":
    main()
