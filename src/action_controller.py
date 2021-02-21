from panda3d.physics import LinearVectorForce
from panda3d.physics import ForceNode
from panda3d.physics import Physical 
from panda3d.core import Point3, Vec3
from math import sin, cos, radians
from numpy import sign

class BallState:

    ready = "ready"
    moving = "moving"
    in_hole = "in_hole"


class ActionController:

    def __init__(self, ball, camera, camera_data) -> None:
        self.golf_ball = ball
        self.camera = camera
        self.camera_data = camera_data
        self.current_pos = self.golf_ball.getPos()
        self.camera_pitch_range = [-15, 15]
        self.counter = 0

        self.ball_state = BallState.moving
        self.ball_last_position = self.golf_ball.getPos()
        self.firepower = 0
        self.max_firepower = 15
        self.force_constant = 100

        self.ballFN = ForceNode('ball_force')
        self.ballFNP = self.golf_ball.attachNewNode(self.ballFN)
        self.force = LinearVectorForce(Vec3(0, 0, 0))

    def update(self, input_table):
    
        self.process_rotation(
                input_table['left'], input_table['right'], input_table['up'], input_table['down'])
        
        if self.ball_state == BallState.ready:
            self.process_fire(input_table['fire'])

        
        if self.ball_state != BallState.in_hole and self.ball_last_position == self.golf_ball.getPos():
            self.ball_state = BallState.ready
        elif self.ball_state != BallState.in_hole and self.ball_last_position != self.golf_ball.getPos():
            self.ball_state = BallState.moving

        self.ball_last_position = self.golf_ball.getPos()


    def process_rotation(self, left, right, up, down):
        heading_rotation_direction = left - right

        self.camera_data.pivot_object.setH(
            self.camera_data.pivot_object.getH() + heading_rotation_direction)

        pitch_rotation_direction = up - down

        new_pitch_value = max(self.camera_pitch_range[0], min(
            self.camera_data.pivot_object.getP() + pitch_rotation_direction, self.camera_pitch_range[1]))

        self.camera_data.pivot_object.setP(new_pitch_value)

    def process_fire(self, fire):

        if fire == 0 and self.firepower == 0:
            self.golf_ball.node().getPhysical(0).removeLinearForce(self.force)
            self.force = LinearVectorForce(0, 0, 0)
        elif fire == 0 and self.firepower != 0:
            self.current_pos = self.golf_ball.getPos()
            self.fire_ball()
        elif fire == 1:
            self.firepower += globalClock.getDt()
            self.firepower = max(0, min(self.firepower, self.max_firepower))

    def fire_ball(self):

        ###        
        self.counter += 1

        angle = radians(self.camera_data.pivot_object.getH())

        x = -sin(angle) * self.firepower * self.force_constant
        y = cos(angle) * self.firepower * self.force_constant

        self.force = LinearVectorForce(Vec3(x, y, 0))       


        ###

        self.ballFN.addForce(self.force)
        self.golf_ball.node().getPhysical(0).addLinearForce(self.force)


        self.firepower = 0

    # TODO: reset position @marcin
    def reset_pos(self):
        self.golf_ball.node().getPhysical(0).removeLinearForce(self.force)
        self.golf_ball.setPos(self.current_pos + Point3(0,0,5))
        ball_last_position = self.current_pos + Point3(0,0,5)

    def bounce(self, normal):
        print("bounce")

    def win(self):
        print("won in " + str(self.counter) + "hits")

