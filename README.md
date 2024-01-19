# gse_creator_Npp
Create basic GSE macros using wowhead and GSE's raw editor feature within Notepad++

 If you are playing world of warcraft and use the Gnome Sequencer Enhanced (GSE) addon
 you might want to create your own macro. This might be interesting for you.

 You fill out a JSON file containing:
 
  buffs_outfight -> Cast these buffs when you are outfight, eg DuDu: Mark of the wild
  
  opener         -> Cast these spells before the rota
  
  rota           -> Rotation, is repeated 2 times
  
  on_cooldown    -> Always use when ready
  
 and run the python script inside Notepad++.

 It will create a file. The contents of this file can be used for the raw editor.

 Needs Notepad++ / Windows
 Tested with Notepad 8.6.2 and the PythonScript plugin
 Used the rotation from wowhead.com and their suggested talents

 Installation / Windows
   Download Notepad++
   Install PythonScript Plugin
   Copy gse_creator_Npp.py "<Notepad++Portable>\App\Notepad++64\plugins\PythonScript\scripts"
   Copy substGSE.txt       "<Notepad++Portable>\App\Notepad++64\plugins\PythonScript\scripts"

lousy, 2024
