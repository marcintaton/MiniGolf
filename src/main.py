from panda3d.core import loadPrcFileData
from pandac.PandaModules import *

from mini_golf import MiniGolf


ConfigVariableString("window-title", "MiniGolf").setValue("Client")
ConfigVariableString(
    "win-size", "500 400").setValue(str(900) + " " + str(900))
loadPrcFileData('', 'win-fixed-size 1')
game = MiniGolf()
game.run()
