from random import random, choice

class Sheep:
    def __init__(self, movement, limit):
        self.x = random.uniform(-limit, limit)
        self.y = random.uniform(-limit, limit)
        self.movement = movement

    def move(self):
        direction = choice(['north', 'south', 'east', 'west'])
        if direction == 'north':
            self.y += self.movement
        elif direction == 'south':
            self.y -= self.movement
        elif direction == 'east':
            self.x += self.movement
        elif direction == 'west':
            self.x -= self.movement

    def get_position(self):
        return self.x, self.y