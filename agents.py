import random

from map import Room


class Agent:
    # Note Return of action() is a string that the testing program
    # can use to determine the points for the agent.
    # Actions are:
    # MOVE
    # SUCK_SUCCESS
    # SUCK_FAILURE
    # SUCK_POINTLESS
    # NO_ACTION

    def __init__(
        self,
        position=(-1, -1),
        random=False,
        murphy=False,
        sensor_failure=10,
        suck_failure=25,
    ):
        self.__position = position  # Starting position
        self.__random = random  # Bool if the agent is random or reflex
        self.sensor_failure = 0  # Percentage of sensor failure
        self.suck_failure = 0  # Percentage of suck failure

        # If Murphy's Law is enabled, set the sensor and suck failure rates
        # Default is 10% and 25% respectively
        if murphy:
            self.sensor_failure = sensor_failure
            self.suck_failure = suck_failure

    def __del__(self):
        self.__position = None
        self.__random = None
        self.__murphy_percentage = None

    def __str__(self):
        return "󰭆"

    @property
    def random(self):
        return self.__random

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    def move(self):
        if self.random:
            return self.random_move()
        else:
            return self.reflex_move()

    def detect_dirt(self, room: Room) -> bool:
        failure_roll = random.randint(1, 100)

        if failure_roll <= self.sensor_failure:
            return not room.dirty

        return room.dirty

    def suck(self, room: Room):
        failure_roll = random.randint(1, 100)
        was_dirty = room.dirty

        if failure_roll <= self.suck_failure:
            room.make_dirty()
            return "SUCK_FAILURE"

        room.clean()
        if was_dirty:
            return "SUCK_SUCCESS"
        return "SUCK_POINTLESS"

    def reflex_move(self):
        # D R D
        # R U D
        # U L L
        match self.__position:
            case (0, 0):
                self.down()
            case (0, 1):
                self.right()
            case (0, 2):
                self.up()
            case (1, 0):
                self.right()
            case (1, 1):
                self.up()
            case (1, 2):
                self.left()
            case (2, 0):
                self.down()
            case (2, 1):
                self.down()
            case (2, 2):
                self.left()
        return "MOVE"

    def random_move(self):
        changed_position = False
        while not changed_position:
            move = random.randint(0, 3)
            # Make sure the movement is possible.
            # Hard coded since this is tied to a 3x3 grid
            match move:
                case 0:
                    if self.__position[1] < 2:
                        self.down()
                        changed_position = True
                case 1:
                    if self.__position[1] > 0:
                        self.up()
                        changed_position = True
                case 2:
                    if self.__position[0] > 0:
                        self.left()
                        changed_position = True
                case 3:
                    if self.__position[0] < 2:
                        self.right()
                        changed_position = True
        return "MOVE"

    def down(self):
        self.__position = (self.__position[0], self.__position[1] + 1)

    def up(self):
        self.__position = (self.__position[0], self.__position[1] - 1)

    def left(self):
        self.__position = (self.__position[0] - 1, self.__position[1])

    def right(self):
        self.__position = (self.__position[0] + 1, self.__position[1])

    def action(self, room: Room):
        if self.random:
            return self.random_action(room)
        return self.reflex_action(room)

    def reflex_action(self, room: Room):
        if self.detect_dirt(room):
            return self.suck(room)
        return self.move()

    def random_action(self, room: Room):
        action = random.randint(1, 6)

        if action <= 4:
            return self.move()
        elif action == 5:
            return self.suck(room)
        else:
            return "NO_ACTION"
