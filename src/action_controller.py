class BallState:

    ready = "ready"
    moving = "moving"
    in_hole = "in_hole"


class ActionController:

    def __init__(self, ball, camera, camera_data) -> None:
        self.golf_ball = ball
        self.camera = camera
        self.camera_data = camera_data

        self.camera_pitch_range = [-15, 15]

        self.ball_state = BallState.ready
        self.firepower = 0
        self.max_firepower = 3

    def process_inputs(self, input_table):

        if self.ball_state == BallState.ready:
            self.process_rotation(
                input_table['left'], input_table['right'], input_table['up'], input_table['down'])
        self.process_fire(input_table['fire'])

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
            return
        elif fire == 0 and self.firepower != 0:
            self.fire_ball()
        elif fire == 1:
            self.firepower += globalClock.getDt()

    def fire_ball(self):

        self.firepower = max(0, min(self.firepower, self.max_firepower))
        print(self.firepower)
        self.firepower = 0
