from panda3d.core import Point3, Vec3
from direct.actor.Actor import Actor
from panda3d.physics import ActorNode, ForceNode
from panda3d.core import Filename
from panda3d.core import ConfigVariableSearchPath
from panda3d.core import getModelPath
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import TexGenAttrib
from panda3d.core import CollisionPlane, CollisionSphere, CollisionNode, NodePath, CollisionHandlerPusher, CollisionBox
from panda3d.core import Plane
from panda3d.physics import LinearVectorForce, PhysicsCollisionHandler

import random
import sys
import os

class World:

    trees = []
    tracks = []
    miscs = []

    def __init__(self, scene, loader, base, notifier):
        self.render = render
        self.loader = loader
        self.base = base
        self.notifier = notifier
        
        self.models_dir = Filename.fromOsSpecific(
            os.path.abspath(sys.path[0])).getFullpath() + "/../models"
        getModelPath().appendDirectory(self.models_dir)
        self.colliders_dir = Filename.fromOsSpecific(
        os.path.abspath(sys.path[0])).getFullpath() + "/../colliders"
        getModelPath().appendDirectory(self.colliders_dir)
        self.init_models()

    def init_models(self):
        self.trees.append(self.models_dir + "/tree1.egg")
        self.trees.append(self.models_dir + "/tree2.egg")
        self.miscs.append(self.models_dir + "/stump.egg")
        self.miscs.append(self.models_dir + "/rock.egg")

    def setup(self):
        self.load_skybox()
        self.load_grass()
        self.load_golf_track()
        self.load_golf()
        self.load_container(self.trees, (2.5,2.5,2.5), 0.28, CollisionSphere(0, 0, 0, 3))
        self.load_container(self.miscs, (1.4, 1.4, 1.4), 0.6, CollisionSphere(0, 0, 0, 1))
        self.load_background()

    def load_golf_track(self):
        golf_track_actor = ActorNode("golf_track")
        self.golf_track = self.render.attachNewNode(golf_track_actor)
        self.base.physicsMgr.attachPhysicalNode(self.golf_track.node())

        golf_track_model = self.loader.loadModel(self.models_dir + "/golf_track.egg")
        golf_track_model.reparentTo(self.golf_track)
        tex = self.loader.loadTexture(self.models_dir + "/tex/golf_track.png")
        golf_track_model.setTexture(tex, 1)

        golf_track_collider = self.loader.loadModel(self.colliders_dir + "/golf_track.egg")
        golf_track_collider.flattenLight()
        golf_track_collider.reparentTo(self.golf_track)
        collisionNode = golf_track_collider.find("**/+CollisionNode")

        hole_actor = ActorNode("hole")
        hole = self.render.attachNewNode(hole_actor) 
        self.load_collider("hole", CollisionSphere(0, 0, 0, 1.5), Vec3(0,0,0), hole, False)               
        hole_model = loader.loadModel(self.models_dir + "/golf_ball.egg")
        hole_model.reparentTo(hole)
        hole.setPos(-19.5, -10.5, -1.2)
        hole.reparentTo(self.golf_track)

        self.golf_track.setScale(0.8, 0.5, 0.5)
        self.golf_track.setHpr(90, 0, 0)
        self.golf_track.setPos(-5.5, 10, 0.9)

    def load_golf(self):
        golf_ball_actor = ActorNode("golf_ball")
        self.golf_ball = self.render.attachNewNode(golf_ball_actor)
        self.golf_ball.node().getPhysicsObject().setMass(5)
        self.base.physicsMgr.attachPhysicalNode(self.golf_ball.node())
        self.load_collider("golf_ball", CollisionSphere(0, 0, 0, 0.2), Vec3(0,0,0), self.golf_ball, True)

        golf_ball_model = loader.loadModel(self.models_dir + "/golf_ball.egg")
        tex = self.loader.loadTexture(self.models_dir + "/tex/golf_ball.png")
        golf_ball_model.setTexture(tex, 1)
        golf_ball_model.setScale(0.2, 0.2, 0.2)
        golf_ball_model.reparentTo(self.golf_ball)
        self.golf_ball.setHpr(0, 0, 0)
        self.golf_ball.setPos(3, 19, 15)

        self.camera_container = NodePath("CameraContainer")
        self.camera_container.reparentTo(self.golf_ball)
        self.camera_container.setHpr(0, 0, 0)
        self.camera_container.setPos(0, 0, 0)

        gravityFN=ForceNode('world-forces')
        gravityFNP=self.golf_ball.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-7)
        gravityFN.addForce(gravityForce)

        self.golf_ball.node().getPhysical(0).addLinearForce(gravityForce)

    def load_skybox(self):
        cubeMap = loader.loadCubeMap(self.models_dir + "/tex/skybox_#.png")
        self.spaceSkyBox = loader.loadModel(self.models_dir + "/skybox.egg")
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
        enviro_actor = ActorNode("floor")
        self.enviro = self.render.attachNewNode(enviro_actor)
        self.enviro.node().getPhysicsObject().setMass(1000)
        self.base.physicsMgr.attachPhysicalNode(self.enviro.node())
        self.load_collider("floor", CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))), Vec3(0,0,0), self.enviro, False)

        enviro_model = self.loader.loadModel(self.models_dir + "/enviro.egg")
        enviro_model.reparentTo(self.enviro)
        enviro_model.setScale(100, 100, 5)
        self.enviro.setPos(0, 50, 0.7)
        tex = self.loader.loadTexture(self.models_dir + "/tex/grass.png")
        ts = TextureStage('ts')
        self.enviro.setTexture(ts, tex)
        self.enviro.setTexScale(ts, 200, 200)

    def load_grass(self):
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                grass =  self.loader.loadModel(self.models_dir + "/grass.egg")
                grass.reparentTo(self.render)
                grass.setScale(1.5, 1.5, 1.5)
                grass.setPos(x, z, 0.7)

    def load_container(self, container, scale, y, sphere): 
        for x in range(-200, 200, random.randint(8, 12)):
            for z in range(-200, 200, random.randint(8, 12)):
                x = random.uniform(x - 10, x + 10)
                z = random.uniform(z - 10, z + 10)
                if not (x > -25 and x < 25 and z < 25 and z > -25):
                    obj_actor = ActorNode("obj")
                    obj = self.render.attachNewNode(obj_actor) 
                    self.load_collider("misc", sphere, Vec3(0,0,0), obj, False)               
                    obj_model = self.loader.loadModel(random.choice(container))
                    obj_model.reparentTo(obj)
                    obj.setScale(scale)
                    obj.setPos(x, z, y)

    def load_collider(self, name, collider, rot, obj, flag):
        cnodePath = obj.attachNewNode(CollisionNode(name))
        cnodePath.setHpr(rot)
        cnodePath.node().addSolid(collider)
        self.notifier.addCollider(cnodePath, obj)
        if(flag):
            self.base.cTrav.addCollider(cnodePath, self.notifier)


