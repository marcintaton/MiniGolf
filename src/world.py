from panda3d.core import Point3
from direct.actor.Actor import Actor
from panda3d.core import Filename
from panda3d.core import ConfigVariableSearchPath
import sys,os
from panda3d.core import getModelPath
from panda3d.core import TextureStage
from panda3d.core import Texture

import random

class World:

    trees = []

    def __init__(self, scene, loader):
        self.render = render
        self.loader = loader
        self.mydir = Filename.fromOsSpecific(os.path.abspath(sys.path[0])).getFullpath() + "/../models"
        getModelPath().appendDirectory(self.mydir)
        self.init_models()

    def init_models(self):
        self.trees.append(self.mydir + "/tree1.egg")
        self.trees.append(self.mydir + "/tree2.egg")

    def setup(self):
        self.load_skybox()
        self.load_background()
        self.load_trees()   

    def load_skybox(self):
        skybox = self.loader.loadModel(self.mydir + "/skybox.egg")
        skybox.reparentTo(self.render)
        skybox.setScale(100, 100, 100)
        skybox.setPos(0, 0, 0)
        tex = loader.loadCubeMap(self.mydir + "/tex/skybox_#.png")
        skybox.setTexture(tex, 1)

    def load_background(self):
        enviro = self.loader.loadModel(self.mydir + "/enviro.egg")
        enviro.reparentTo(self.render)
        enviro.setScale(100, 100, 5)
        enviro.setPos(0, 50, -2)
        tex = self.loader.loadTexture(self.mydir + "/tex/grass.png")
        ts = TextureStage('ts')
        enviro.setTexture(ts, tex)
        enviro.setTexScale(ts, 100, 100)
        enviro.setTexOffset(ts, -4, -2)

    def load_trees(self):
        for x in range(-100, 100, 10):
            for z in range(0, 200, 10):
                tree = self.loader.loadModel(random.choice(self.trees))
                tree.reparentTo(self.render)
                tree.setScale(1.2, 1.2, 1.2)
                tree.setPos(random.uniform(x/2, x) , random.uniform(z/2, z), 0)

