import random


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

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def dirt_piles(self):
        dirt = 0
        for row in self.rooms:
            for room in row:
                if room.dirty:
                    dirt += 1
        return dirt

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
