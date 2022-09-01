import re
import subprocess
import os
import shutil

presetPath = ""
configPath = ""

steamUsername = ""
serverInstance = ""

steamWorkshop_Path = r'C:\steamcmd\steamapps\workshop\content\107410'
armaServer_Path = r'C:\steamcmd\steamapps\common\Arma 3 Server'

_updateBATPath = os.path.dirname(__file__)
_updateTXTPath = r'C:\steamcmd'
_startBATPath = os.path.dirname(__file__)
_serverInstancePaths = [r'C:\Users\Administrator\Documents\A3Master',
                        r'C:\Users\Administrator\Documents\A3Events']
_modIDs = []
_fileName = ""

for i in os.listdir(os.path.dirname(__file__)):
    if i.endswith(".html"):
        presetPath_Components = [os.path.dirname(__file__),'\\',i]
        presetPath = "".join(presetPath_Components)
    if i.endswith(".txt"):
        configPath_Components = [os.path.dirname(__file__),'\\',i]
        configPath = "".join(configPath_Components)

with open(configPath, 'r') as f:
    for line in f:
        matchUsername = re.search(r'username=(.*)',line)
        matchInstance = re.search(r'instance=(.*)',line)
        if matchUsername:
            steamUsername = (matchUsername.group(1))
        if matchInstance:
            serverInstance = int(matchInstance.group(1))

with open(presetPath, 'r', encoding='utf8') as f:
    for line in f:
        matchIDs = re.search(r'://steamcommunity.com/sharedfiles/filedetails/\?id=(.*)" data-type="Link">', line)
        matchName = re.search(r'<meta name="arma:PresetName" content="(.*)" />', line)
        if matchIDs:
            _modIDs.append(matchIDs.group(1))
        if matchName:
            _fileName = matchName.group(1)

_fileName_UpdateBAT_Components = ["INSTALL UPDATE ",_fileName,".bat"]
_fileName_UpdateBAT = "".join(_fileName_UpdateBAT_Components)
_fileName_UpdateBAT = _fileName_UpdateBAT.replace(" ", "_")
_fileName_UpdateBAT_Path = "".join([_updateBATPath,'\\',_fileName_UpdateBAT])

_fileName_UpdateTXT_Components = ["install_update_",_fileName,".txt"]
_fileName_UpdateTXT = "".join(_fileName_UpdateTXT_Components)
_fileName_UpdateTXT = _fileName_UpdateTXT.replace(" ", "_")
_fileName_UpdateTXT_Path = "".join([_updateTXTPath,'\\',_fileName_UpdateTXT])

_fileName_StartBAT_Components = ["Start_ArmA_Server_",str(serverInstance),"_",_fileName,".bat"]
_fileName_StartBAT = "".join(_fileName_StartBAT_Components)
_fileName_StartBAT = _fileName_StartBAT.replace(" ","_")
_fileName_StartBAT_Path = "".join([_startBATPath,'\\',_fileName_StartBAT])

_fileContent_UpdateBAT_Components = [r'SET STEAMCMD=C:\steamcmd\steamcmd.exe',
                                     '\n',
                                     r'SET UPDATESCRIPT=C:\steamcmd',
                                     '\\',
                                     _fileName_UpdateTXT,
                                     '\n',
                                     r'start %STEAMCMD% +runscript %UPDATESCRIPT%',
                                     '\n',
                                     'exit']

with open(_fileName_UpdateBAT_Path, 'w') as f:
    f.write("".join(_fileContent_UpdateBAT_Components))

_fileContent_UpdateTXT_Components = ['login ',
                                     steamUsername,
                                     '\n',]

for i in _modIDs:
    _fileContent_UpdateTXT_Components.append('workshop_download_item 107410 ')
    _fileContent_UpdateTXT_Components.append(i)
    _fileContent_UpdateTXT_Components.append('\n')

_fileContent_UpdateTXT_Components.append("quit")

with open(_fileName_UpdateTXT_Path, 'w') as f:
    f.write("".join(_fileContent_UpdateTXT_Components))

_modIDs_forStart = ";".join(_modIDs)

_serverPort = str(int(serverInstance) - 1)

_fileContent_StartBAT_Components = [r'cd "C:\steamcmd\steamapps\common\Arma 3 Server\"',
                                    '\n',
                                    r'START arma3server_x64.exe -profiles="',
                                    _serverInstancePaths[serverInstance-1],
                                    r'" -port=23',
                                    _serverPort,
                                    r'2 -config="',
                                    _serverInstancePaths[serverInstance-1],
                                    r'\CONFIG_server.cfg.txt" -world=empty -mod="',
                                    _modIDs_forStart,
                                    ';"']

with open(_fileName_StartBAT_Path, 'w') as f:
    f.write("".join(_fileContent_StartBAT_Components))

print("subprocess starting...")
subprocess.run("".join([r'C:\steamcmd\steamcmd.exe +runscript ',_fileName_UpdateTXT_Path]))
print("...subprocess ending.")

print("moving files:")
for i in _modIDs:
    _src = "".join([steamWorkshop_Path,'\\',i])
    _dst = "".join([armaServer_Path,'\\',i])
    if os.path.isdir(_dst):
        print("".join([_dst," exists, removing..."]))
        shutil.rmtree(_dst)
        print("...removed.")
    else:
        print("".join([_dst," is not a dir"]))
    print("moving file... "+i)
    shutil.copytree(_src, _dst, dirs_exist_ok=True)
    print("...file moved.")
