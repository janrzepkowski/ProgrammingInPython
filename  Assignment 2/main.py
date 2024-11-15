from wolf import Wolf
from sheep import Sheep


def main():
    max_rounds = 50
    num_sheep = 15
    limit = 10.0
    sheep_movement = 0.5
    wolf_movement = 1.0

    wolf = Wolf(wolf_movement)
    herd = [Sheep(sheep_movement, limit) for _ in range(num_sheep)]

    for round_no in range(1, max_rounds + 1):
        print(f"Round {round_no}")

        for sheep in herd:
            if sheep is not None:
                sheep.move()

        wolf.move(herd)

        wolf_pos = wolf.get_position()
        alive_sheep = sum(1 for sheep in herd if sheep is not None)
        print(f"Wolf position: ({wolf_pos[0]:.3f}, {wolf_pos[1]:.3f})")
        print(f"Number of alive sheep: {alive_sheep}")

        if alive_sheep == 0:
            print("All sheep have been eaten.")
            break


if __name__ == "__main__":
    main()