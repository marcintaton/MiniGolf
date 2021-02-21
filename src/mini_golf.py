from direct.task.Task import TaskManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from direct.task.TaskManagerGlobal import taskMgr
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties
from panda3d.core import GraphicsWindow
from panda3d.core import ClockObject
from panda3d.core import AmbientLight, VBase4, DirectionalLight
from panda3d.core import NodePath, CollisionTraverser, CollisionHandlerEvent
from panda3d.physics import PhysicsCollisionHandler
from direct.actor.Actor import Actor
from panda3d.core import Point3
from math import pi, sin, cos
from action_controller import ActionController
from camera_data import CameraData
import math

from world import World

import sys


class MiniGolf(ShowBase):

    Instance = None

    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.base.cTrav = CollisionTraverser()
        self.notifier = PhysicsCollisionHandler()
        self.task_manager = TaskManager()
        self.game_loop_running = False
        self.ui_text = "Kappa123"

        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(60)
        #
        if MiniGolf.Instance is None:
            MiniGolf.Instance = self
        #
        self.run_setup()

    def run(self):
        self.game_loop_running = True
        self.game_loop()

    def handle_events(self):
        self.handle_mouse()

    def handle_mouse(self):
        if self.base.mouseWatcherNode.hasMouse():
            self.setInputValue(
                "mouse_x", self.base.mouseWatcherNode.getMouseX())
            self.setInputValue(
                "mouse_y", self.base.mouseWatcherNode.getMouseY())

    def game_loop(self):

        while self.game_loop_running:

            angle = self.camera_data.pivot_object.getH()
            self.sample_text.setText("angle: " +
                                     str("{:.2f}".format(
                                         angle)) + "\n" +
                                     "radian: " +
                                     str("{:.2f}".format(
                                         math.radians(angle))) +"\n" +
                                        "x: " +
                                     str("{:.2f}".format(
                                         -math.sin(math.radians(angle)))) +"\n" +
                                        "y: " +
                                     str("{:.2f}".format(
                                         math.cos(math.radians(angle)))) +"\n" +
                                         "firepower: " +
                                    str("{:.2f}".format(
                                         self.action_controller.firepower)) +"\n" +
                                        "Ball state: " +
                                    self.action_controller.ball_state +"\n"
                                          )

            self.handle_events()

            ###

            self.action_controller.update(self.player_input)
            ###

            self.task_manager.step()

    # temp setup method, for pretty much everything
    # refactor and remove later
    def run_setup(self):
        # mouse stuff
        self.base.disableMouse()

        wp = WindowProperties()
        # wp.setCursorHidden(True)
        wp.setMouseMode(WindowProperties.M_confined)
        self.base.win.requestProperties(wp)

        # gui
        self.sample_text = OnscreenText(text="0", parent=self.base.a2dTopLeft, pos=(0.07, -.06 * 0 - 0.1),
                                        fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05, mayChange=1)

        # player input
        self.player_input = {"mouse_x": 0, "mouse_y": 0,
                             "left": 0, "right": 0, "up": 0, "down": 0, "fire": 0}
        self.accept("escape", sys.exit)  # Escape quits

        self.accept("arrow_left",     self.setInputValue, ["left", 1])
        self.accept("arrow_left-up",  self.setInputValue, ["left", 0])
        self.accept("arrow_right",    self.setInputValue, ["right", 1])
        self.accept("arrow_right-up", self.setInputValue, ["right", 0])
        self.accept("arrow_up",       self.setInputValue, ["up", 1])
        self.accept("arrow_up-up",    self.setInputValue, ["up", 0])
        self.accept("arrow_down",       self.setInputValue, ["down", 1])
        self.accept("arrow_down-up",    self.setInputValue, ["down", 0])
        self.accept("mouse1",          self.setInputValue, ["fire", 1])
        self.accept("mouse1-up",          self.setInputValue, ["fire", 0])

        directionalLight = DirectionalLight('directionalLight')
        directionalLightNP = self.render.attachNewNode(directionalLight)
        directionalLightNP.setHpr(0, -60, 0)

        self.render.setLight(directionalLightNP)
        self.render.set_shader_auto()
        self.base.enableParticles() 

        self.base.cTrav.showCollisions(render)
        self.notifier.addInPattern("%fn-in-%in")
        self.notifier.addOutPattern("%fn-out-%in")
        self.accept("golf_ball-in-floor", self.onCollisionStart)
        self.accept("golf_ball-in-Cube.001", self.onBounceStart)
        self.accept("golf_ball-in-hole", self.onGolfInHole)

        self.world = World(self.render, self.loader, self.base, self.notifier)
        self.world.setup()

        self.camera_data = CameraData(self.world.camera_container)
        self.camera.setPos(self.camera_data.position)

        self.camera.reparent_to(self.camera_data.pivot_object)

        self.action_controller = ActionController(
        self.world.golf_ball, self.camera, self.camera_data)

    def setInputValue(self, input, val):
        self.player_input[input] = val

    def onCollisionStart(self, entry):
        self.action_controller.reset_pos()

    def onGolfInHole(self, entry):
        self.action_controller.win()

    def onBounceStart(self, entry):
        self.action_controller.bounce(entry.getContactNormal(entry.getIntoNodePath()))

