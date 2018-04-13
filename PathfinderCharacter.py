'''
Created on Jan 28, 2018

@author: brandon
'''

import Skills
import json
from TemporaryModifier import TempDict

class Charac(object):
    '''
    classdocs
    '''


    def __init__(self, theName='Tabor', theStr=10, theDex=10, theCon=10, theInt=10, theWis=10,
                 theCha=10, theBA=0, theFullHealth=10, theFortBase=0, theRefBase=0,
                 theWillBase=0, theSize=0, theFortTot=None, theRefTot=None, theWillTot=None,
                 theArmorB=0, theShieldB=0, theACTot=None, theACTouch=None, theACFlat=None,
                 theOrigChar=None):
        '''
        Constructor
        '''
        if theOrigChar == None:
            self.myName = theName
            
            self.myStats = {'Str': theStr, 'Dex': theDex, 'Con': theCon,
                             'Int': theInt, 'Wis': theWis, 'Cha': theCha}
            self.myStatMods = {'Str': self.calcMod(theStr), 'Dex': self.calcMod(theDex),
                               'Con': self.calcMod(theCon), 'Int': self.calcMod(theInt), 
                               'Wis': self.calcMod(theWis), 'Cha': self.calcMod(theCha)}
            
            self.mySize = theSize
            
            self.myBA = theBA
            
            self.myFortBase = theFortBase
            self.myRefBase = theRefBase
            self.myWillBase = theWillBase
            
            self.setSaves(theFortTot, theRefTot, theWillTot)
            
            self.myFullHealth = theFullHealth
            
            
            self.myAC = ArmorClass(theArmor=theArmorB, theShield=theShieldB, theSize=self.mySize,
                                   theTotal=theACTot, theTouch=theACTouch, theFlat=theACFlat)
             
            self.mySkills = Skills.SkillList(self)
            
            
            self.myNotes = TempDict()
        
        else:
            self.copyConstructor(theOrigChar)
            
        self.myCurrentHealth = self.myFullHealth
        self.myCMB = self.myBA + self.myStatMods['Str'] - self.mySize
        self.myCMD = self.myBA + self.myStatMods['Str'] + self.myStatMods['Dex'] - self.mySize + 10
        self.myMeleeAtk = self.myBA + self.myStatMods['Str'] + self.mySize
        self.myRangeAtk = self.myBA + self.myStatMods['Dex'] + self.mySize
       
    def copyConstructor(self, theOrig):
        
        self.myName = theOrig.myName
        
        self.myStats = dict(theOrig.myStats)
        self.myStatMods = dict(theOrig.myStatMods)
        
        self.mySize = theOrig.mySize
        
        self.myBA = theOrig.myBA
        
        self.myFortBase = theOrig.myFortBase
        self.myRefBase = theOrig.myRefBase
        self.myWillBase = theOrig.myWillBase
        
        self.setSaves(theOrig.myFortTot, theOrig.myRefTot, theOrig.myWillTot)
        
        self.myFullHealth = theOrig.myFullHealth
        
        self.myAC = ArmorClass(theOrigAC=theOrig.myAC)
        
        self.mySkills = Skills.SkillList(theOrigList=theOrig.mySkills)
        
        # To Do: Check and ensure deep copying.
        self.myNotes = TempDict(theOrig.myNotes)
    
    def setSaves(self, theFortTot=None, theRefTot=None, theWillTot=None):
        if theFortTot == None:
            self.myFort = self.myFortBase + self.myStatMods['Con']
        else:
            self.myFort = theFortTot
        
        if theRefTot == None:
            self.myRef = self.myRefBase + self.myStatMods['Dex']
        else:
            self.myRef = theRefTot
        
        if theWillTot == None:
            self.myWill = self.myWillBase + self.myStatMods['Wis']
        else:
            self.myWill = theWillTot
      
    # Get methods
    
    def getStat(self, stat='Dex'):
        return self.myStats[stat]
    
    def getStatMod(self, stat='Dex'):
        return self.myStatMods[stat]
    
    def getFort(self):
        return self.myFort
    
    def getRef(self):
        return self.myRef
    
    def getWill(self):
        return self.myWill
    
    def getBA(self):
        return self.myBA
    
    def getCMB(self):
        return self.myCMB
    
    def getCMD(self):
        return self.myCMD
    
    def getFullHealth(self):
        return self.myFullHealth
    
    def getCurrentHealth(self):
        return self.myCurrentHealth
    
    # Set methods
    
    def setStat(self, stat, newVal):
        self.myStats[stat] = newVal
        self.myStatMods[stat] = self.calcMod(newVal)
        self.updateStat(stat)
    
    def setBaseFort(self, theFortBase=0):
        self.myFort = theFortBase + self.myCon
    
    def setBaseRef(self, theRefBase=0):
        self.myRefBase = theRefBase
        self.myRef = theRefBase + self.myDex
    
    def setBaseWill(self, theWillBase=0):
        self.myWillBase = theWillBase
        self.myWill = theWillBase + self.myWis
        
    def setCMB(self, theBA= 0, theDex=0, theStr=0, theSize=0):
        self.myCMB = theBA + theDex + theStr + theSize
    
    def setCMD(self, theBA= 0, theDex=0, theStr=0, theSize=0):
        self.myCMB = theBA + theDex + theStr + theSize + 10
    
    def setCurrentHealth(self, theHealth):
        self.myCurrentHealth = theHealth
        
    def damage(self, theDmg):
        self.myCurrentHealth -= theDmg
        
        if self.myCurrentHealth == 0:
            self.addNote('Staggered', 'Limited to only one main action per round.')
        # If a character is dropped below 0 hp, they go unconscious and start bleeding out.
        elif self.myCurrentHealth < 0:
            self.addNote('Unconscious', 'Is unconscious.')
            self.addNote('Bleeding out', 'Is bleeding out. Loses 1 HP per round till stabilized.')
            
        elif self.myCurrentHealth <= (-1*self.getStat('Con')):
            self.addNote('Dead', 'This Creature/Character is dead.')
    
    # The character has received some amount of healing so the hp will increase by the
    # given amount, a character cannot be healed past maximum.   
    def healing(self, theHeal):
        if self.myCurrentHealth <= 0:
            try:
                self.removeNote('Bleeding out')
            except:
                print("Wasn't bleeding out?")
        
        elif self.myCurrentHealth == 0:
            try:
                self.removeNote('Staggered')
            except:
                print("Wasn't staggered.")
        
        
        # If the heal would put the characters hp above their full health.
        if theHeal + self.myCurrentHealth > self.myFullHealth:
            self.myCurrentHealth = self.myFullHealth
        # If the heal doesn't put the character above their full health.
        else:
            self.myCurrentHealth += theHeal
            
           
        if self.myCurrentHealth == 0:
            self.addNote('Staggered', 'Limited to only one main action per round.')
            
    
    # Modifiers
    # Modifiers are assumed to be positive and such effects that decrease an ability should
    # be entered as negative.
    
    # Adds a modifier to a characters Fortitude Save.
    def addFortMod(self, theFortMod=0):
        self.myFort += theFortMod
    
    # Adds a modifier to a characters Reflex Save.
    def addRefMod(self, theRefMod=0):
        self.myRef += theRefMod
    
    # Adds a modifier to a characters Will Save.
    def addWillMod(self, theWillMod=0):
        self.myWill += theWillMod
    
    # Adds a modifier to a characters Melee Attack Bonus.
    def addMeleeAtkMod(self, theAtkMod):
        self.myMeleeAtk += theAtkMod
    
    # Adds a modifier to a characters Ranged Attack Bonus.    
    def addRangeAtkMod(self, theAtkMod):
        self.myRangeAtk += theAtkMod
    
    # Adds a modifier to a characters Melee and Ranged Attack Bonuses.    
    def addAtkMod(self, theAtkMod):
        self.addMeleeAtkMod(theAtkMod)
        self.addRangeAtkMod(theAtkMod)
        
    
    # Update methods
    
    # Updates a characters Fortitude Save.
    def updateFort(self):
        self.myFort = self.myFortBase + self.myStatMods['Con']
    
    # Updates a characters Reflex Save.
    def updateRef(self):
        self.myRef = self.myRefBase + self.myStatMods['Dex']
        
    # Updates a characters Will Save.
    def updateWill(self):
        self.myRef = self.myRefBase + self.myStatMods['Wis']
    
    # Updates a characters Combat Maneuver Bonus.
    def updateCMB(self):
        self.myCMB = self.myBA + self.myStatMods['Str'] + self.mySize
    
    # Updates a characters Combat Maneuver Defense. 
    def updateCMD(self):
        self.myCMB = self.myBA + self.myStatMods['Dex'] + self.myStatMods['Str'] + self.mySize + 10
    
    # Updates a characters standard melee attack bonus.
    def updateMeleeAtk(self):
        self.myMeleeAtk = self.myBA + self.myStatMods['Str']
    
    # Updates a characters standard ranged attack bonus.   
    def updateRangeAtk(self):
        self.myRangeAtk = self.myBA + self.myStatMods['Dex']
    
    # Used to update all abilities and skills relate to a given state.
    def updateStat(self, stat='Dex'):
        if stat == 'Dex':
            self.updateCMD()
            self.updateRef()
            self.mySkills.abiUpdate('Dex', self.getStatMod('Dex'))
        elif stat == 'Str':
            self.updateCMB()
            self.updateCMD()
            self.mySkills.abiUpdate('Str', self.getStatMod('Str'))
        elif stat == 'Con':
            self.updateFort()
        elif stat == 'Int':
            self.mySkills.abiUpdate('Int', self.getStatMod('Int'))
        elif stat == 'Wis':
            self.updateWill()
            self.mySkills.abiUpdate('Wis', self.getStatMod('Wis'))
        else:
            self.mySkills.abiUpdate('Cha', self.getStatMod('Cha'))
                
    
    # Adds a note to the note dictionary.
    # Notes should be used for identifying and describing temporary modifiers applied to 
    # characters. 
    def addNote(self, theNote= 'No note', theDesc='None'):
        self.myNotes[theNote] = theDesc
    
    # Removes a note with the given title from the note dictionary
    def removeNote(self, theNote):
        self.myNotes.pop(theNote)
    
    # Calculates the modifier of a given stat and returns it.
    # A modifier is equal to a (stats value - 10) / 2 rounded down.
    def calcMod(self, value=10):
        return (value-10) // 2


    def toJSON(self):
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys=True, indent=4)

# Defines the Armor Class of a character.
# AC is used to define how difficult a character is to hit.
class ArmorClass(object):
    
    # AC constructor. Can take in information from multiple individual sources or from a 
    # set of total sources.
    def __init__(self, theArmor=0, theDex=0, theSize=0, theShield=0, theNatArmor=0, theDefl=0,
                 theAddi=0, theTouch=None, theFlat=None, theTotal=None, theOrigAC=None):
        
        if theOrigAC == None:
            self.myArmor = theArmor
            self.myDexMod = theDex
            self.mySize = theSize
            self.myShield = theShield
            self.myNatArm = theNatArmor
            self.myDefl = theDefl
            self.myMisc = theAddi
        
        else:
            self.myArmor = theOrigAC.myArmor
            self.myDexMod = theOrigAC.myDex
            self.mySize = theOrigAC.mySize
            self.myShield = theOrigAC.myShield
            self.myNatArm = theOrigAC.myNatArmor
            self.myDefl = theOrigAC.myDefl
            self.myMisc = theOrigAC.myAddi
            
        self.setTotFlTou(theTotal, theTouch, theFlat)
    
    # Sets the Armor AC value and updates the appropriate AC types.
    def setArmor(self, theArmor):
        self.myArmor = theArmor
        self.calcTotal()
        self.calcFlat()
    
    # Sets the Dexterity AC value and updates the appropriate AC types.
    def setDexMod(self, theMod):
        self.myDexMod = theMod
        self.calcTotal()
        self.calcTouch()

    # Sets the Size AC value and updates the appropriate AC types.
    def setSize(self, theMod):
        self.myDexMod = theMod
        self.calcTotal()
        self.calcTouch()
        self.calcFlat()
        
    # Sets the Shield AC value and updates the appropriate AC types.
    def setShield(self, theMod):
        self.myDexMod = theMod
        self.calcTotal()
        self.calcFlat()
    
    # Sets the Natural Armor AC value and updates the appropriate AC types.
    def setNatArm(self, theMod):
        self.myNatArm = theMod
        self.calcTotal()
        self.calcFlat()
        
    # Sets the Deflection AC value and updates the appropriate ACs.
    def setDefl(self, theDefl):
        self.myDefl = theDefl
        self.calcTotal()
        self.calcTouch()
        self.calcFlat()
    
    # Sets the Misc. AC value and updates the appropriate AC types.    
    def setMisc(self, theMisc):
        self.myMisc = theMisc
        self.calcTotal()
        self.calcTouch()
        self.calcFlat()
            
    # Sets the total AC to the given value.
    def setTotal(self, theTotal):
        self.myTotal = theTotal
        
    # Sets the touch AC to the given value.
    def setTouch(self, theTouch):
        self.myTouch = theTouch
    
    # Sets the flat footed AC to the given value.
    def setFlat(self, theFlat):
        self.myFlatFoot = theFlat
    
    # Checks to see if total, touch and flat footed AC were given or if the AC modifiers of
    # individual items were given.
    def setTotFlTou(self, theTotal=None, theTouch=None, theFlat=None):
        if theTotal == None:
            self.myTotal = self.calcTotal()
        else:
            self.myTotal = theTotal
        
        if theTouch == None:
            self.myTouch = self.calcTouch()
        else:
            self.myTouch = theTouch
        
        if theFlat == None:
            self.myFlatFoot = self.calcFlat()
        else:
            self.myFlatFoot = theFlat    
    
    # Sums up the armor from all sources and updates the AC total.
    def calcTotal(self):
        armor = self.myArmor + self.myShield + self.myNatArm + self.myDefl
        evasion = self.myDexMod + self.mySize   + self.myMisc
        self.myTotal = armor + evasion    
    
    # Sums up the effects that apply to touch armor class and updates the touch total.
    def calcTouch(self):
        self.myTouch = self.myDexMod + self.mySize + self.myDefl + self.myMisc
    
    # Sums up the items/effects that apply to flat footed AC, and updates the Flat footed total.    
    def calcFlat(self):
        armor = self.myArmor + self.myShield + self.myNatArm
        self.myFlatFoot =  armor + self.mySize +  self.myDefl + self.myMisc     
    
    
class AttackAndDamage(object):
    
    def __init__(self, theMeleeAtk, theRangedAtk, theMeleeDmg, theRangedDmg, theStr, theDex,
                 theBA, theWeaponFinesse=False):
        self.myMeleeAtk = self.calcMeleeAtk(theMeleeAtk, theBA, theStr, theDex, theWeaponFinesse)
        self.myRangedAtk = self.calcRangedAtk(theRangedAtk, theBA, theDex)
        self.myMeleeDmg = theMeleeDmg
        self.myRangedDmg = theRangedDmg
        
    def calcMeleeAtk(self, theAtkTotal, theBA, theStr, theDex, theWeaponFinesse):
        meleeAtk = 0
        
        if theAtkTotal == None:
            if theWeaponFinesse:
                meleeAtk = theBA + theDex
            else:
                meleeAtk = theBA + theStr
        else:
            meleeAtk = theAtkTotal
            
        return meleeAtk
    
    def calcRangedAtk(self, theAtkTotal, theBA, theDex):
        rangedAtk = 0
        
        if theAtkTotal == None:
            rangedAtk = theBA + theDex
        else:
            rangedAtk = theAtkTotal
        
        return rangedAtk
    
if __name__ == '__main__':
    basic = Charac(theStr=15)
    
    basic.setStat('Dex', 12)
    
    print(basic.myStatMods['Dex'])
    print(basic.myStatMods['Str'])
    print(basic.myStatMods['Con'])
    
    print(basic.calcMod(basic.getStat('Dex')))
    print(basic.calcMod(basic.getStat('Str')))
    
    print(basic.getStat('Str'))
    print(basic.getStat('Dex'))
    print(basic.mySkills)
    
    print(basic.__dict__)
    
    print(basic.toJSON())
    
    
    copyDic = dict(basic.myStats)
    copyDic['Dex'] = 18
    print(basic.myStats)
    print(copyDic)
    print(copyDic)
    
    