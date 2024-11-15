class Wolf:
    def __init__(self, movement):
        self.x = 0.0
        self.y = 0.0
        self.movement = movement

    def distance_squared(self, sheep):
        return (self.x - sheep.x) ** 2 + (self.y - sheep.y) ** 2

    def move(self, herd):
        closest_sheep = None
        closest_distance = float('inf')

        for sheep in herd:
            if sheep is not None:
                distance = self.distance_squared(sheep)
                if distance < closest_distance:
                    closest_sheep = sheep
                    closest_distance = distance

        if closest_sheep is not None:
            if closest_distance ** 0.5 <= self.movement:
                herd[herd.index(closest_sheep)] = None
                self.x, self.y = closest_sheep.get_position()
            else:
                dx = closest_sheep.x - self.x
                dy = closest_sheep.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                self.x += self.movement * dx / distance
                self.y += self.movement * dy / distance

    def get_position(self):
        return self.x, self.y