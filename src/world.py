from panda3d.core import Point3, Vec3
from direct.actor.Actor import Actor
from panda3d.core import Filename
from panda3d.core import ConfigVariableSearchPath
import sys
import os
from panda3d.core import getModelPath
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import TexGenAttrib
from panda3d.core import CollisionPlane, CollisionSphere, CollisionNode
from panda3d.core import Plane

import random


class World:

    trees = []
    tracks = []

    def __init__(self, scene, loader):
        self.render = render
        self.loader = loader
        self.mydir = Filename.fromOsSpecific(
            os.path.abspath(sys.path[0])).getFullpath() + "/../models"
        getModelPath().appendDirectory(self.mydir)
        self.init_models()

    def init_models(self):
        self.trees.append(self.mydir + "/tree1.egg")
        self.trees.append(self.mydir + "/tree2.egg")

    def setup(self):
        self.load_skybox()
        self.load_background()
        self.load_golf()
        self.load_trees()

    def load_golf(self):
        self.golf_ball = self.loader.loadModel(self.mydir + "/golf.egg")
        self.golf_ball.reparentTo(self.render)
        self.golf_ball.setScale(0.3, 0.3, 0.3)
        self.golf_ball.setHpr(90, 0, 0)
        self.golf_ball.setPos(0, 10, 0)
        tex = self.loader.loadTexture(self.mydir + "/tex/golf.png")
        self.golf_ball.setTexture(tex, 1)

        self.dummy_golf_ball = self.render.attachNewNode("DummyGolf")
        self.dummy_golf_ball.reparentTo(self.golf_ball)
        self.dummy_golf_ball.setHpr(0, 0, 0)
        self.dummy_golf_ball.setPos(0, 0, 0)

    def load_skybox(self):
        cubeMap = loader.loadCubeMap(self.mydir + "/tex/skybox_#.png")
        spaceSkyBox = loader.loadModel('models/box.egg')
        spaceSkyBox.reparentTo(self.render)
        spaceSkyBox.setScale(300)
        spaceSkyBox.setPos(-150, 150, 0)
        spaceSkyBox.setTexture(cubeMap, 1)

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

        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        cnodePath = enviro.attachNewNode(CollisionNode('cnode'))
        cnodePath.node().addSolid(plane)

    def load_trees(self):
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                tree = self.loader.loadModel(random.choice(self.trees))
                tree.reparentTo(self.render)
                tree.setScale(1.2, 1.2, 1.2)
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                tree.setPos(x, z, 0)
                sphere = CollisionSphere(0, 0, 0, 3)
                cnodePath = tree.attachNewNode(CollisionNode('cnode'))
                cnodePath.node().addSolid(sphere)
