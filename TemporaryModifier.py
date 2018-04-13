'''
Created on Jan 29, 2018

@author: brandon
'''

class TempDict(object):
    
    def __init__(self, theOrigDict = None):
        
        if theOrigDict == None:
            self.myDict = {}
        else:
            self.myDict = dict(theOrigDict)
            
    def addMod(self, mod):
        temp = TempModifier(theMod=mod)
        self.myDict[temp.myTitle] = temp
    
    
    def removeMods(self, modList):
        for mod in modList:
            self.myDict.pop(mod)
    
    def endOfRound(self):
        
        toBeRemovedList = []
        
        for mod in self.myDict.keys():
            temp = self.myDict[mod]
            temp.myDuration -= 1
        
            if temp.myDuration == 0:
                toBeRemovedList.append(temp.myTitle)
        
        self.removeMods(toBeRemovedList)

class TempModifier(object):
    '''
    classdocs
    '''

    def __init__(self, theDuration=-1, theTitle ='', theDesc = '', theOrigMod=None):
        '''
        Constructor
        '''
        if theOrigMod == None:
            self.myDuration = theDuration
        
            self.myTitle = theTitle
            self.myDesc = theDesc
            
        else:
            self.myDuration = theOrigMod.myDuration
            self.myTitle = theOrigMod.myTitle
            self.myDesc = theOrigMod.myDesc
    
    # Changes the duration of the modifier for a number of rounds given.
    # The duration will increase if the value is positive and decrease if it is negative.
    def changeDuration(self, theChange):
        self.myDuration += theChange
    
    # Returns a string version of the modifier.
    # The string will have the following format:
    # Title: Description
    # Duration: X
    def __str__(self):
        tempString = self.myTitle + ': ' + self.myDesc + '/nDuration: ' + str(self.myDuration)
        return tempString

    
        
if __name__ == '__main__':
    sickened = TempModifier(1, 'sickened','-2 to attack and ability mods')
    fatigued = TempModifier(2, 'fatigued','-2 to attack and ability mods')
    haste = TempModifier(2, 'haste','double move speed and one additional attack')
    
    adict = {sickened.myTitle:sickened, fatigued.myTitle:fatigued, 
             haste.myTitle:haste}
    
    testDict = TempDict(adict)
    
    
    testDict.endOfRound()
    testDict.endOfRound()
    testDict.endOfRound()
    
    print(str(testDict))