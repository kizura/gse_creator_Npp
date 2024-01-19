# This Python file uses the following encoding: utf-8
#
# Reads a .rota File (JSON format) as input
# and creates a gse "raw editor" file
# tested with GSE 3.1.30
#
# 2024-01-19: https://www.wowhead.com/guide/classes/hunter/beast-mastery/rotation-cooldowns-pve-dps
#
#
# Installation / Windows
#   Download Notepad++
#   Install PythonScript Plugin
#   Copy gse_creator_Npp.py "<Notepad++Portable>\App\Notepad++64\plugins\PythonScript\scripts"
#   Copy substGSE.txt       "<Notepad++Portable>\App\Notepad++64\plugins\PythonScript\scripts"
#
# Usage:
#   Create your .rota file -- see hunter_bm_mt_lousy_wh.json
#   Call Plugins/PythonScript/Scripts/gse_creator_Npp
# Debug:
#   If you want to see debug/error messages: Plugins/PythonScript/ShowConsole
#
#
# buffs_outfight -> Cast these buffs when you are outfight, eg DuDu: Mark of the wild
# opener         -> Cast these spells before the rota
# rota           -> Rotation, is repeated 2 times
# on_cooldown    -> Always use when ready
import json
import sys;
import os;
import io;
from datetime import datetime


BUFFS_OUTFIGHT = "buffs_outfight"
OPENER="opener"         
ROTA="rota"
ON_COOLDOWN="on_cooldown"

GLOBcountKeypress=0
GLOBtextKeypress=""

def translateSpellsInFile(pFileGSE):
    """Replaces the (english) spells with the word found in the file

       Uses the file "substGSE.txt"

       @param pFileGSE -- Path + filename of the GSE Macro file,
                          or the file with the names to be replaced
       @return String with replaced spells
    """
    spellsDeutsch = ""
    cwd = os.getcwd()
    print( "CWD: " + cwd)
    with open(pFileGSE) as substGSE:
        for substGSEl in substGSE:
            #print("Text: " + substGSEl )
            origContent = substGSEl
            with open( cwd + '\\plugins\\PythonScript\\scripts\\substGSE.txt') as f:
                istSchonUebersetzt = "NEIN"
                for l in f:
                    s = l.split(",")
                    if s[0].startswith("#") == True:
                        continue
                    if len(s) != 2:
                        continue
                    if s[1][-1:] in '\n\r':
                        s[1] = trimcr(s[1][:-1])
                    s[1] = s[1].strip()
                    #print(s[0] + " / " + s[1] + " // " + substGSEl)
                    substGSEl = substGSEl.replace(s[0], s[1])
            if substGSEl == origContent:
                if "/cast" in substGSEl and istSchonUebersetzt == "NEIN":
                    print("WARNUNG - Unbekannter Spell: " + substGSEl )
            #print(substGSEl )
            spellsDeutsch += substGSEl
        return spellsDeutsch

def translateSpellsInString(pStringGSE):
    """Replaces the (english) spells with the word found in the file

       Uses the file "substGSE.txt"

       Falls ein Spell nicht übesetzt werden konnte, dann wird eine Warnung ausgegeben

       @param pStringGSE -- GSE Raw Editor String mit den zu ersetzenden Spells
                            Getrennt durch LF
       @return String mit den übersetzten Spells
    """
    spellsDeutsch = ""
    cwd = os.getcwd()
    print( "CWD: " + cwd)
    for substGSEl in pStringGSE.splitlines():
        #print("Text: " + substGSEl )
        origContent = substGSEl
        with io.open(cwd + '\\plugins\\PythonScript\\scripts\\substGSE.txt', "r", encoding="utf-8") as f:
            istSchonUebersetzt = "NEIN"
            for l in f:
                s = l.split(",")
                if s[0].startswith("#") == True:
                    continue
                if len(s) != 2:
                    continue

                if s[1][-1:] in '\n\r':
                    s[1] = trimcr(s[1][:-1])
                s[1] = s[1].strip()
                #print(s[0] + " / " + s[1] + " // " + substGSEl)
                substGSEl = substGSEl.replace(s[0], s[1])
                # Falls der Spruch schon auf deutsch ist, dann findet
                # keine Ersetzung statt - dieses "if" überprüft dies
                if s[1] in substGSEl:
                    istSchonUebersetzt = "JA"
        if substGSEl == origContent:
            if "/cast" in substGSEl and istSchonUebersetzt == "NEIN":
                print("WARNUNG - Unbekannter Spell: " + substGSEl )
        #print(substGSEl )
        spellsDeutsch += substGSEl +"\n"
    return spellsDeutsch

# CR (carriage return) entfernen
def trimcr(str):
        if str == '':
                return ''
        if str[-1:] in '\n\r':
                return trimcr(str[:-1])
        else:
                return str
#
# Indent
#
def indent(anz):
    retVal = ""
    for x in range(anz):
        retVal += "    "
    return retVal

def addKeyPress(castCondition, wowSpell):
    """Creates a text like this:
          /cast Frostwyrm's Fury
       Or - if castCondition is specified - eg:
         /cast [noharm,nocombat] Marc of the wild

       @param castCondition - eg "[noharm,nocombat]" or simply "" if not wanted
       @param wowSpell - Spell text, eg "Frostwyrm's Fury"
              Take care, if you have eg an english client and you use spanish spells this will not work
    """
    global GLOBtextKeypress
    global GLOBcountKeypress
    #if len(GLOBtextKeypress) != 0:
    #    GLOBtextKeypress = GLOBtextKeypress + ",\n"
    GLOBcountKeypress = GLOBcountKeypress + 1
    lAddSpell = indent(3) + "["+ str(GLOBcountKeypress) +"] = \"/cast "+ castCondition +" "+ wowSpell +"\""
    GLOBtextKeypress = GLOBtextKeypress + lAddSpell

    return lAddSpell

def createBuffsOutfight(jsBuffsOutfight):
    print (">>createBuffsOutfight")
    txtCreateBuffsOutfight = ""
    if len(jsBuffsOutfight) == 0:
        return ""
    for x in jsBuffsOutfight:
        x = x.strip()
        if len(x) != 0:
            if len(txtCreateBuffsOutfight) != 0:
                txtCreateBuffsOutfight += ",\n"
            txtCreateBuffsOutfight += addKeyPress( "[noharm,nocombat]", x)
    return txtCreateBuffsOutfight
#
#
# @param 
def createOnCooldown(jsCdSpells):
    print (">>createBuffsOutfight")
    print("createBuffsOutfight: " + str(jsCdSpells)) 
    txtCreateOnCooldown = ""
    if (jsCdSpells) == 0:
        return ""
    for x in jsCdSpells:
        x = x.strip()
        if len(x) != 0:
            if len(txtCreateOnCooldown) != 0:
                txtCreateOnCooldown += ",\n"
            txtCreateOnCooldown += addKeyPress( "[nochanneling]", x)
    return txtCreateOnCooldown

def createOpener(blkNum, jsOpenerSpells):
    retVal=[]
    txtOpenerSpells = ""
    cntRota = 1
    for x in jsOpenerSpells:
        x = x.strip()
        if len(x) != 0:
            if len(txtOpenerSpells) != 0:
                txtOpenerSpells += ",\n"
            txtOpenerSpells += createGseActionNoKeyPress(cntRota, 2, x)
            cntRota+=1

    retVal.append(cntRota)
    retVal.append( ( indent(1) + "[\"Actions\"] = {\n"
        + txtOpenerSpells + ",\n"
        #+ indent(3) + "[\"Type\"] = \"Action\"\n"
        ) )
    return retVal

#
# Spells used as opener - before rota
#
def createOpenerBulk(blkNum, jsOpenerSpells):
    print (">>createOpenerBulk")
    txtOpenerSpells = ""
    if len(jsOpenerSpells) == 0:
        return ""
    cntOpen = 1
    if len(GLOBtextKeypress) !=0:
        cntOpen = 2
        txtOpenerSpells = indent(3) + "[1] = \"~~KeyPress~~\""
    for x in jsOpenerSpells:
        x = x.strip()
        if len(x) != 0:
            if len(txtOpenerSpells) != 0:
                txtOpenerSpells += ",\n"
            txtOpenerSpells += indent(3) + "["+str(cntOpen)+"] = \"/cast [nochanneling] " + x +"\""
        cntOpen = cntOpen + 1
    txtOpenerSpells = (
          indent(1) + "[\"Actions\"] = {\n"
        + indent(2) +"["+str(blkNum)+"] = {\n" + txtOpenerSpells + ",\n"
        + indent(3) + "[\"Type\"] = \"Action\"\n" 
        + indent(2) + "},\n")
    return txtOpenerSpells

def createGseAction(actCounter, srcindent, actSpell):
    locCounter = 1
    return (
          indent(srcindent)   + "[" + str(actCounter) + "] = {\n"
        + indent(srcindent+2) + "[" + str(locCounter) + "] = \"~~KeyPress~~\",\n"
        + indent(srcindent+2) + "[" + str(locCounter+1) + "] = \"/cast [nochanneling] " +actSpell+ "\",\n"
        + indent(srcindent+2) + "[\"Type\"] = \"Action\"\n"
        + indent(srcindent) + "}"
    )
def createGseActionNoKeyPress(actCounter, srcindent, actSpell):
    locCounter = 1
    return (
          indent(srcindent)   + "[" + str(actCounter) + "] = {\n"
        + indent(srcindent+2) + "[" + str(locCounter) + "] = \"/cast [nochanneling] " +actSpell+ "\",\n"
        + indent(srcindent+2) + "[\"Type\"] = \"Action\"\n"
        + indent(srcindent) + "}"
    )

def createRota(blkNum, jsSpellRota):
    """ blkNum      - Block number for GSE
        jsSpellRota - Array with spells
    """
    txtSpellRotas = ""
    cntRota = 1
    for x in jsSpellRota:
        x = x.strip()
        if len(x) != 0:
            if len(txtSpellRotas) != 0:
                txtSpellRotas += ",\n"
            txtSpellRotas += createGseAction(cntRota, 3, x)
            cntRota+=1

    return (
          indent(2) + "["+str(blkNum)+"] = {\n"
        + txtSpellRotas + ",\n"
        + indent(3) + "[\"Repeat\"] = 2,\n"
        + indent(3) + "[\"Type\"] = \"Loop\",\n"
        + indent(3) + "[\"StepFunction\"] = \"Sequential\"\n"
        + indent(2) + "},\n"
        )

def getInbuiltVariablesString():
    return (
    indent(1) + "[\"InbuiltVariables\"] = {\n"
    + indent(2) + "[\"Trinket1\"] = true,\n"
    + indent(2) + "[\"Trinket2\"] = true\n"
    + indent(1) + "}"
    )

def createVariables(jsBuffsOutfight, jsCdSpells):
    """ Creates the variable section with 'KeyPress'
       It will contains these spells:
       - OnCooldown
       - Buffs outfight
    """
    lBuffsOutfight = createBuffsOutfight(jsonCompleteRota[BUFFS_OUTFIGHT])
    lOnCooldown    = createOnCooldown(jsonCompleteRota[ON_COOLDOWN])
    if len(lOnCooldown) != 0:
        if len(lBuffsOutfight) != 0:
            lBuffsOutfight += ",\n"
    return (
        "{\n"
         + indent(1) + "[\"Variables\"] = {\n" 
         + indent(2) + "[\"KeyPress\"] = {\n" + lBuffsOutfight + lOnCooldown +"\n"
         + indent(2) + "}\n"
         + indent(1) + "},")

def createGseRawEditor(jsonCompleteRota):
    """Return the raw string for the GSE editor

       String is complete - just replace all your editor content with it
    """
    lVariables     = createVariables(jsonCompleteRota[BUFFS_OUTFIGHT], jsonCompleteRota[ON_COOLDOWN])
    #lOpener        = createOpener(1, jsonCompleteRota[OPENER])
    retOpener       =  createOpener(1, jsonCompleteRota[OPENER])
    lOpener = retOpener[1]
    blkNum  = retOpener[0]
    lCompleteRota  = createRota(blkNum, jsonCompleteRota[ROTA])
    #print (">>createGseRawEditor")
    #print("GSE:")
    #print(lVariables)
    #print(lOpener)
    #print(lCompleteRota)
    #print(getInbuiltVariablesString())
    #print("}")
    return lVariables + "\n" + lOpener + "\n" + lCompleteRota + "\n" + indent(1) + "},\n" + getInbuiltVariablesString() + "\n" + "}"
#
# Programm -- For Notepad++ with PythonScript plugin
#

# Copy complete editor contents to string
completeRota = editor.getText()
completeRota = completeRota.decode('utf8')
print( completeRota )
# json -> python
jsonCompleteRota = json.loads(completeRota)
gseRawEditorTxt = createGseRawEditor(jsonCompleteRota)
print ("gseRawEditorTxt>>>" + gseRawEditorTxt)
# if you want to translate the spells to a different language
#  -> Texts are defined in substGSE.txt
# set useReplace = 1
useReplace = 0
if useReplace != 0:
    gseRawEditorTxtDe = translateSpellsInString(gseRawEditorTxt)
    print ("gseRawEditorTxtDe>>>" + gseRawEditorTxtDe)
else:
    gseRawEditorTxtDe = gseRawEditorTxt
# New Editor window -> transfer content
ergName = str( os.getenv('HOME') ) + "_gseCreator_" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".json"
gseRawEditorDe = io.open(ergName, "w", encoding="utf-8")
gseRawEditorDe.write(gseRawEditorTxtDe)
gseRawEditorDe.close()
notepad.open(ergName)
#neuesDok = editor.createDocument()
#neuesDok.addText(gseRawEditorTxtDe)
#print ("GSE RawEditor file: " + os.path.basename("./" + fileRota + "_de.gse"))

# lousyplayer, 2023-10-03
