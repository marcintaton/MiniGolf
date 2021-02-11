from panda3d.core import Point3
from direct.actor.Actor import Actor
from panda3d.core import Filename
from panda3d.core import ConfigVariableSearchPath
import sys,os
from panda3d.core import getModelPath
import random

class World:

    trees = []

    def __init__(self, scene, loader):
        self.render = render
        self.loader = loader
        self.mydir = Filename.fromOsSpecific(os.path.abspath(sys.path[0])).getFullpath()
        getModelPath().appendDirectory(self.mydir + "/models")
        self.init_models()

    def init_models(self):
        self.trees.append(self.mydir + "/models/tree1.egg")
        self.trees.append(self.mydir + "/models/tree2.egg")

    def setup(self):
        self.load_background()
        self.load_trees()   

    def load_background(self):
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(5, 5, 5)
        self.scene.setPos(-8, 42, 0)

    def load_trees(self):
        self.scene = self.loader.loadModel(random.choice(self.trees))
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.45, 0.45, 0.45)
        self.scene.setHpr(0, 90, 0)
        self.scene.setPos(0, 0, 0)

