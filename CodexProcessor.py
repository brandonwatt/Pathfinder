'''
Created on Feb 6, 2018

@author: brandon
'''

import re
import json
import urllib.request
import PathfinderCharacter


class CodexReader(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.charVal = ''
        
        self.charList = []
        
        
    
    def read(self, theURL):
        
        results = []
        
        # Attempt to open and read the link.
        try:
            page = urllib.request.urlopen(theURL)
            pageText = page.read()
            pageString = str(pageText)
            
            
            print(pageString)
            
            self.charVal = pageString
            results = re.findall('<p id=.*?<p id', pageString, re.IGNORECASE)
            #results = re.findall('<p id="savage-mercenary" class="stat-block-title">Savage Mercenary <span class="stat-block-cr">CR 1/2</span></p>', pageString, re.IGNORECASE)
            
            self.charList = results
        except:
            print('Open failed')
 
    def processChar(self, charNum=0):
        #theStr=10, theDex=10, theCon=10, theInt=10, theWis=10, theCha=10, theBA=0,
        #theFullHealth=10, theFortBase=0, theRefBase=0, theWillBase=0, theSize=0
        charDict = {'theName':'', 'theStr': 0, 'theDex': 0, 'theCon': 0,'theInt': 0,'theWis': 0,
                    'theCha': 0,'theBA': 0, 'theFullHealth': 0,'theSize': 0, 'theACTot': 0,
                    'theACTouch': 0, 'theACFlat': 0}
        statList = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
        
        charac = str(self.charList[charNum])
        
        # Name search
        name = re.search('<p id="(.*?)" ', charac, re.IGNORECASE)
        print(name.group(1))
        charDict['theName']= name.group(1)
        
        # Stat search
        for stat in statList:
            statSearch = re.search('>statistics</p>.*?<b>'+stat+'</b> (\d+)', charac, re.IGNORECASE)
            print(stat + ': ' + statSearch.group(1))
            statVal = int(statSearch.group(1))
            charDict['the'+stat]= statVal
        
        
        #print(charDict.keys())
        
        # Base Attack search
        baseAtk = re.search('<b>Base Atk</b> \+(\d+)', charac, re.ASCII)
        print('BA: ' + baseAtk.group(1))
        stat = int(baseAtk.group(1))
        charDict['theBA']= stat
        
        # HP search
        hpSearch = re.search('<b>hp</b> (\d+) ', charac, re.ASCII)
        print('FullHP: ' + hpSearch.group(1))
        hp = int(hpSearch.group(1))
        charDict['theFullHealth']= hp 
        
        # Size search
        size = re.search('<p class="stat-block-1">[CLN]?[GNE]? (\S*) ', charac, re.IGNORECASE)
        print('Size: ' + size.group(1))
        sizeStr = str(size.group(1))
        sizeBonus = self.sizeStrToInt(sizeStr)
        print('Size Bonus: ' + str(sizeBonus))
        charDict['theSize'] = sizeBonus
        
        # Armor Class search
        ACSearch = re.search('<b>AC</b> (\d+), touch (\d+), flat-footed (\d+)', charac, re.ASCII)
        print('ACTot: ' + ACSearch.group(1))
        print('ACTouch: ' + ACSearch.group(2))
        print('ACFlat: ' + ACSearch.group(3))
        ACTot = int(ACSearch.group(1))
        ACTouch = int(ACSearch.group(2))
        ACFlat = int(ACSearch.group(3))
        charDict['theACTot']= ACTot 
        charDict['theACTouch']= ACTouch 
        charDict['theACFlat']= ACFlat
        
        #Save search
        saveSearch = re.search('<b>Fort</b> [+-]?(\d+), <b>Ref</b> [+-]?(\d+), <b>Will</b> [+-]?(\d+)', charac, re.ASCII)
        print('Fort: ' + saveSearch.group(1))
        print('Ref: ' + saveSearch.group(2))
        print('Will: ' + saveSearch.group(3))
        fort = int(saveSearch.group(1))
        ref = int(saveSearch.group(2))
        will = int(saveSearch.group(3))
        charDict['theFortTot']= fort
        charDict['theRefTot']= ref 
        charDict['theWillTot']= will
        
        '''
        newChar = PathfinderCharacter.Charac(theStr=charDict['Str'], theDex=charDict['Dex'], theCon=charDict['Con'],
                                   theInt=charDict['Int'], theWis=charDict['Wis'], theCha=charDict['Cha'], 
                                   theBA=charDict['BA'], theFullHealth=charDict['FullHP'], theSize=charDict['Size'],
                                   theFortTot=charDict['Fort'], theRefTot=charDict['Ref'], theWillTot=charDict['Will'])
        
        '''
        
        #print(charDict.keys())
        newChar = PathfinderCharacter.Charac(**charDict)
        
        return newChar 
         


    def sizeStrToInt(self, sizeStr):
        
        sizeBonus = 0
        
        if sizeStr.lower() == 'small':
            sizeBonus = 1
        elif sizeStr.lower() == 'tiny':
            sizeBonus = 2
        elif sizeStr.lower() == 'diminutive':
            sizeBonus = 4
        elif sizeStr.lower() == 'fine':
            sizeBonus = 8
        elif sizeStr.lower() == 'large':
            sizeBonus = -1
        elif sizeStr.lower() == 'huge':
            sizeBonus = -2
        elif sizeStr.lower() == 'gargantuan':
            sizeBonus = -4
        elif sizeStr.lower() == 'colossal':
            sizeBonus = -8

        return sizeBonus



if __name__ == '__main__':
    url = 'http://paizo.com/pathfinderRPG/prd/npcCodex/core/barbarian.html'
    url2 = 'http://paizo.com/pathfinderRPG/prd/npcCodex/core/fighter.html'
    url3 = 'http://paizo.com/pathfinderRPG/prd/npcCodex/core/cleric.html'
    
    '''theName=dct['myName'], theBA=dct['myBA'],
    theSize=dct['mySize'], theFortTot=dct['myFort'],
    theRefTot=dct['myRef'], theWillTot=dct['myWill'],
    theFullHealth=dct['myFullHealth'],
    theStr=dct['myStats']['Str'],
    theDex=dct['myStats']['Dex'],
    theCon=dct['myStats']['Con'],
    theInt=dct['myStats']['Int'],
    theWis=dct['myStats']['Wis'],
    theCha=dct['myStats']['Cha'] '''
    def as_character(dct):
        if 'myName' in dct:
            return PathfinderCharacter.Charac(**dct)
    
        
        return dct
    
    reader = CodexReader()
    reader.read(url3)
    
    for character in reader.charList:
        print(character)
        print()    
      
      
    someChar = reader.processChar(1)
    
    charJson = someChar.toJSON()
    
    txtDoc = open('characterSample.txt', 'w')
    txtDoc.write(charJson)
    txtDoc.close()
    
    txtDoc = open('characterSample.txt', 'r')
    charTxt = txtDoc.read()
    
    #print(charTxt)
    #dict(charTxt)
    dupChar = json.loads(charTxt)
    print(dupChar)
    
    print(dupChar['myCMD'])
    theChara = as_character(dupChar)
    print(theChara.getCMD())
    print(theChara.myName)
    #dupChar = json.loads(charTxt, object_hook=as_character)
    #print(dupChar)
    #print(dupChar.myStats)
    #print(dupChar.toJSON())
    

    
    