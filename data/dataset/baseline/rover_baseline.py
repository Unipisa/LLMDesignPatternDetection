class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
    def move_forward(self, metres: int) -> None:
        self.y += metres
    def move_left(self, metres: int) -> None:
        self.x -= metres
    def move_right(self, metres: int) -> None:
        self.x += metres
    def move_back(self, metres: int) -> None:
        self.y -= metres
