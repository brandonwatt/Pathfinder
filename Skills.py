'''
Created on Jan 29, 2018

@author: brandon
'''
import PathfinderCharacter

class Skill(object):
    '''
    classdocs
    '''


    def __init__(self, theName='', theAbility='Int', classSkill=False, theAbiMod=0, theRank=0,
                 theMisc=0, theTotBonus=None, theOrigSkill = None):
        '''
        Constructor
        '''
        # Copy Constructor, runs if given another Skill object.
        if theOrigSkill != None:
            self.myName = theOrigSkill.myName
            self.myAbility = theOrigSkill.myAbility
            self.isClassSkill = theOrigSkill.isClassSkill
            self.myAbiMod = theOrigSkill.myAbiMod
            self.myRank = theOrigSkill.myRank
            self.myMisc = theOrigSkill.myMisc
        
        # Normal Constructor
        else:
            self.myName = theName
            self.myAbility = theAbility
            self.isClassSkill = classSkill
            self.myAbiMod = theAbiMod
            self.myRank = theRank
            self.myMisc = theMisc
        
        self.myTotBonus = self.calcBonus(theTotBonus)
        
    def calcBonus(self, theTotal=None):
        
        if theTotal == None:
            classBonus = 0
        
            if self.isClassSkill and self.myRank > 0:
                classBonus = 3
        
            return self.myAbiMod + self.myRank + self.myMisc + classBonus
            
        else:
            self.myTotBonus = theTotal
    
    # Get methods
    
    def getName(self):
        return self.myName
    
    def getAbility(self):
        return self.myAbility
    
    def getAbiMod(self):
        return self.myAbiMod
    
    def getRank(self):
        return self.myRank
    
    def getMisc(self):
        return self.myMisc
    
    def getTotal(self):
        return self.myTotBonus
    
    # Set Methods
    
    def setName(self, theName):
        self.myName = theName
    
    def setAbility(self, theAbility):
        self.myAbility = theAbility
    
    def setAbiMod(self, theAbiMod):
        self.myAbiMod = theAbiMod
        self.calcBonus()
    
    def setRank(self, theRank):
        self.myRank = theRank
        self.calcBonus()
    
    def setMisc(self, theMisc):
        self.myMisc = theMisc
        self.calcBonus()
    
    def valueString(self):
        rankStr = ''
        
        if self.isClassSkill and self.myRank > 0:
            rankStr = ' + 3'
        
        return '('+self.getAbility()+') '+str(self.getAbiMod())+' + '+str(self.getRank())+' + '+str(self.getMisc())+rankStr+' = ' + str(self.getTotal())
    
    def __lt__(self, otherSkill):
        return self.getName() < otherSkill.getName()
    
    def __str__(self):
        
        rankStr = ''
        
        if self.isClassSkill and self.myRank > 0:
            rankStr = ' + 3'
        
        return self.getName()+': (' + self.getAbility() + ') '+str(self.getAbiMod())+' + '+str(self.getRank())+' + '+str(self.getMisc())+rankStr+' = ' + str(self.getTotal()) 
        

class SkillList(object):
    '''
    classdocs
    '''


    def __init__(self, theCharacter = None, theOrigList = None):
        '''
        Constructor
        '''
        self.mySkillNameDic = {'Con':[],
                               'Cha':['Bluff','Diplomacy','Disguise','Handle Animal','Intimidate',
                                      'Perform1','Perform2', 'Use Magic Device'],
                               'Dex':['Acrobatics', 'Disable Device', 'Escape Artist', 'Fly',
                                      'Ride', 'Sleight of Hand', 'Stealth'],
                               'Int':['Appraise', 'Craft1','Craft2', 'Craft3','Knowledge (Arcana)',
                                      'Knowledge (Dungeoneering)','Knowledge (Engineering)',
                                      'Knowledge (Geography)','Knowledge (History)',
                                      'Knowledge (Local)', 'Knowledge (Nature)',
                                      'Knowledge (Nobility)','Knowledge (Planes)',
                                      'Knowledge (Religion)','Linguistics', 'Spellcraft'], 
                               'Str':['Climb','Swim'],
                               'Wis':['Heal', 'Perception', 'Profession1','Profession2',
                                      'Sense Motive', 'Survival'] 
                                }
        if theOrigList == None:   
            self.mySkillDic = {}
            self.buildSkillDic()
            
            if theCharacter != None:
                self.setAbiMods(theCharacter)
        else:
            self.mySkillDic = {}
            self.copySkillDic(theOrigList)
        
    
    def copySkillDic(self, theOrigDic):
        
        for abi in self.mySkillNameDic.keys():
            self.mySkillDic[abi] = []
            for num in range(0,len(theOrigDic.mySkillDic[abi])):
                ability = Skill(theOrigSkill=theOrigDic.mySkillDic[abi][num])
                self.mySkillDic[abi].append(ability)
    
    
    def buildSkillDic(self):
        for abi in self.mySkillNameDic.keys():
            self.mySkillDic[abi] = []
            for name in self.mySkillNameDic[abi]:
                ability = Skill(theName=name, theAbility=abi)
                self.mySkillDic[abi].append(ability)
                
            
    def setAbiMods(self, theCharacter):
        for abi in self.mySkillDic.keys():
            self.abiUpdate(abi, theCharacter.getStatMod(abi))
    
    
    def abiUpdate(self, theAbility, theMod):
        for name in self.mySkillDic[theAbility]:
            name.setAbiMod(theMod)

            
    def __str__(self):
        
        stringList = ''
        
        for abi in self.mySkillDic.keys():
            for skillNames in self.mySkillDic[abi]:
                stringList += str(skillNames) + '\n'
            #print(stringList)
        
        return stringList
        
if __name__ == '__main__':
    test = SkillList()
    
    test.buildSkillDic()
    #print(test.mySkillDic)
    for abi in test.mySkillDic.keys():
        for name in test.mySkillDic[abi]:
            print(name)
    
    #print(test.mySkills)
    
    testSkill = Skill(theName='Test', theAbility='Dex', theAbiMod=2, theMisc=1, theRank=2,
                      classSkill=True) 
    
    print(testSkill.myTotBonus)
    print(testSkill)
    
    copySkill = Skill(theOrigSkill=testSkill)
    print(copySkill.myTotBonus)
    print(copySkill)
    print(copySkill.valueString())   
    
    
    newCharacter = PathfinderCharacter.Charac()
    skillDicCopy = SkillList(theOrigList=newCharacter.mySkills)
    
    print(newCharacter.mySkills)
    skillDicCopy.mySkillDic['Str'][1].setRank(3)
    print(newCharacter.mySkills)
    print(skillDicCopy) 
    
    print(isinstance(skillDicCopy.mySkillDic['Str'][1], Skill))
    print(copySkill != None)            