from panda3d.core import Point3


class CameraData:

    def __init__(self, pivot) -> None:
        self.starting_position = Point3(0, -30, 5)
        self.position = self.starting_position
        self.pivot_object = pivot
