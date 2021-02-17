from panda3d.core import Point3, Vec3
from direct.actor.Actor import Actor
from panda3d.physics import ActorNode, ForceNode
from panda3d.core import Filename
from panda3d.core import ConfigVariableSearchPath
import sys
import os
from panda3d.core import getModelPath
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import TexGenAttrib
from panda3d.core import CollisionPlane, CollisionSphere, CollisionNode, NodePath, CollisionHandlerPusher, CollisionBox
from panda3d.core import Plane
from panda3d.physics import LinearVectorForce, PhysicsCollisionHandler

import random


class World:

    trees = []
    tracks = []
    miscs = []

    def __init__(self, scene, loader, base, notifier):
        self.render = render
        self.loader = loader
        self.base = base
        self.notifier = notifier
        self.mydir = Filename.fromOsSpecific(
            os.path.abspath(sys.path[0])).getFullpath() + "/../models"
        getModelPath().appendDirectory(self.mydir)
        self.init_models()

    def init_models(self):
        self.trees.append(self.mydir + "/tree1.egg")
        self.trees.append(self.mydir + "/tree2.egg")
        self.miscs.append(self.mydir + "/stump.egg")
        self.miscs.append(self.mydir + "/rock.egg")

    def setup(self):
        self.load_skybox()
        self.load_grass()
        self.load_golf_track()
        self.load_golf()
        self.load_container(self.trees, (1.2,1.2,1.2), 0.28, CollisionSphere(0, 0, 0, 3))
        self.load_container(self.miscs, (1, 1, 1), 0.6, CollisionSphere(0, 0, 0, 1))
        self.load_background()

    def load_golf_track(self):
        self.golf_track = self.loader.loadModel(self.mydir + "/golf.egg")
        self.golf_track.reparentTo(self.render)
        self.golf_track.setScale(0.3, 0.3, 0.3)
        self.golf_track.setHpr(90, 0, 0)
        self.golf_track.setPos(0, 10, 0.7)
        tex = self.loader.loadTexture(self.mydir + "/tex/golf.png")
        self.golf_track.setTexture(tex, 1)

    def load_golf(self):
        golf_ball_actor = ActorNode("actor")
        self.golf_ball = self.render.attachNewNode(golf_ball_actor)
        self.golf_ball.node().getPhysicsObject().setMass(100.)
        self.load_collider("ball_collider",CollisionSphere(0, 0, 0, 0.2), self.golf_ball)

        golf_ball_model = loader.loadModel(self.mydir + "/golf_ball.egg")
        tex = self.loader.loadTexture(self.mydir + "/tex/golf_ball.png")
        golf_ball_model.setTexture(tex, 1)
        golf_ball_model.setScale(0.15, 0.15, 0.15)
        golf_ball_model.reparentTo(self.golf_ball)
        self.golf_ball.reparentTo(self.golf_track)
        self.golf_ball.setHpr(0, 0, 0)
        self.golf_ball.setPos(-5.5, 11, 20)

        gravityFN=ForceNode('world-forces')
        gravityFNP=self.golf_ball.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-0.25)
        gravityFN.addForce(gravityForce)

        self.golf_ball.node().getPhysical(0).addLinearForce(gravityForce)

    def load_skybox(self):
        cubeMap = loader.loadCubeMap(self.mydir + "/tex/skybox_#.png")
        self.spaceSkyBox = loader.loadModel(self.mydir + "/skybox.egg")
        self.spaceSkyBox.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.spaceSkyBox.setTexProjector(TextureStage.getDefault(), self.render, self.spaceSkyBox)
        self.spaceSkyBox.setTexPos(TextureStage.getDefault(), 0.44, 0.5, 0.2)
        self.spaceSkyBox.setTexScale(TextureStage.getDefault(), 0.2)
        self.spaceSkyBox.setLightOff()
        self.spaceSkyBox.reparentTo(self.render)
        self.spaceSkyBox.setScale(300)
        self.spaceSkyBox.setPos(-150, 150, 0)
        self.spaceSkyBox.setTexture(cubeMap, 1)

    def load_background(self):
        enviro_actor = ActorNode("enviro")
        self.enviro = self.render.attachNewNode(enviro_actor)
        self.load_collider("enviro_collider", CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))), self.enviro)
        
        enviro_model = self.loader.loadModel(self.mydir + "/enviro.egg")
        enviro_model.reparentTo(self.enviro)
        enviro_model.setScale(100, 100, 5)
        self.enviro.setPos(0, 50, 0.7)
        tex = self.loader.loadTexture(self.mydir + "/tex/grass.png")
        ts = TextureStage('ts')
        self.enviro.setTexture(ts, tex)
        self.enviro.setTexScale(ts, 200, 200)

    def load_trees(self):
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                tree_actor = ActorNode("tree")
                tree = self.render.attachNewNode(tree_actor)                
                tree_model = self.loader.loadModel(random.choice(self.trees))
                tree_model.reparentTo(tree)
                tree.setScale(1.2, 1.2, 1.2)
                tree.setPos(x, z, 0.3)

    def load_grass(self):
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                grass =  self.loader.loadModel(self.mydir + "/grass.egg")
                grass.reparentTo(self.render)
                grass.setScale(1.5, 1.5, 1.5)
                grass.setPos(x, z, 0.7)

    def load_container(self, container, scale, y, sphere): 
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                obj_actor = ActorNode("obj")
                obj = self.render.attachNewNode(obj_actor)                

                obj_model = self.loader.loadModel(random.choice(container))
                obj_model.reparentTo(obj)
                obj.setScale(scale)
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                obj.setPos(x, z, y)

    def load_collider(self, name, collider, obj):
        cnodePath = obj.attachNewNode(CollisionNode(name))
        cnodePath.node().addSolid(collider)
        cnodePath.show()
        pusher = PhysicsCollisionHandler()
        pusher.addCollider(cnodePath, obj)
        self.base.cTrav.addCollider(cnodePath, pusher)
        self.base.physicsMgr.attachPhysicalNode(obj.node())

