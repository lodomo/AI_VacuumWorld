import random
import time


def main():
    agent = ReflexAgent()
    map = Map(3, 3, 3)
    agent.set_position(map.random_position())
    map.spread_dirt()
    max_steps = 100

    while not map.all_clean():
        clear_screen()
        map.print(agent)
        agent.action(map.get_room(agent.position))
        time.sleep(0.5)
        max_steps -= 1
        if max_steps == 0:
            print("Max steps reached")
            break

    if map.all_clean():
        clear_screen()
        map.print(agent)
        print("All clean!")

    return


def clear_screen():
    print("\033[H\033[J")


class Room:
    def __init__(self):
        self.__dirty = False

    @property
    def dirty(self):
        return self.__dirty

    def __str__(self):
        if self.__dirty:
            return ""
        else:
            return " "

    def clean(self):
        self.__dirty = False

    def make_dirty(self):
        self.__dirty = True


class Map:
    def __init__(self, width, height, dirty_rooms):
        self.width = width
        self.height = height
        self.rooms = [[Room() for _ in range(width)] for _ in range(height)]
        self.dirty_rooms = dirty_rooms

    def get_room(self, position):
        return self.rooms[position[1]][position[0]]

    def spread_dirt(self):
        current_dirt = 0
        while current_dirt < self.dirty_rooms:
            pos = self.random_position()
            if not self.rooms[pos[1]][pos[0]].dirty:
                self.rooms[pos[1]][pos[0]].make_dirty()
                current_dirt += 1

    def random_position(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return (x, y)

    def all_clean(self):
        for row in self.rooms:
            for room in row:
                if room.dirty:
                    return False
        return True

    def print_empty(self, width=3, chars=3):
        print("█", end="")
        for i in range(width):
            for j in range(chars):
                print("█", end="")
            print("█", end="")
        print("█", end="")
        print("█", end="")
        print()

    def print(self, agent=None):
        self.print_empty()

        for x in range(self.width):
            for y in range(self.height):
                print("█", end="")
                if agent and agent.position == (x, y):
                    print(f"{agent}", end="")
                else:
                    print(" ", end="")
                print(f"{self.rooms[y][x]} ", end="█")
            print()
            self.print_empty()


class ReflexAgent:
    # This agent will only work for a 3x3 room
    # It will not clean space 0,0 if it does not start there.
    def __init__(self, position=(-1, -1)):
        self.__position = position

    def __str__(self):
        return "󰭆"

    @property
    def position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def action(self, room):
        if room.dirty:
            self.suck(room)
        else:
            self.move()

    def move(self):
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

    def down(self):
        self.__position = (self.__position[0], self.__position[1] + 1)

    def up(self):
        self.__position = (self.__position[0], self.__position[1] - 1)

    def left(self):
        self.__position = (self.__position[0] - 1, self.__position[1])

    def right(self):
        self.__position = (self.__position[0] + 1, self.__position[1])

    def suck(self, room):
        if room.dirty:
            room.clean()


if __name__ == "__main__":
    main()
