import json
import csv
from wolf import Wolf
from sheep import Sheep


def main():
    max_rounds = 50
    num_sheep = 15
    limit = 10.0
    sheep_movement = 0.5
    wolf_movement = 1.0

    wolf = Wolf(wolf_movement)
    herd = [Sheep(sheep_movement, limit, index) for index in range(num_sheep)]

    rounds_data = []
    alive_sheep_data = []

    for round_no in range(1, max_rounds + 1):
        print(f"Round {round_no}")

        for sheep in herd:
            if sheep is not None:
                sheep.move()

        target_sheep_index = wolf.move(herd)
        wolf_pos = wolf.get_position()
        sheep_pos = [sheep.get_position() if sheep is not None else None for sheep in herd]

        alive_sheep = sum(1 for sheep in herd if sheep is not None)
        print(f"Wolf position: ({wolf_pos[0]:.3f}, {wolf_pos[1]:.3f})")
        print(f"Number of alive sheep: {alive_sheep}")

        if target_sheep_index is not None and herd[target_sheep_index] is None:
            print(f"The sheep number: {target_sheep_index} has been eaten")
        else:
            print(f"The wolf is chasing sheep number: {target_sheep_index}")

        if alive_sheep == 0:
            print("All sheep have been eaten.")
            break

        round_data = {
            "round_no": round_no,
            "wolf_pos": list(wolf_pos),
            "sheep_pos": sheep_pos,
        }
        rounds_data.append(round_data)
        alive_sheep_data.append([round_no, alive_sheep])

        print()

    with open("pos.json", "w") as json_file:
        json.dump(rounds_data, json_file, indent=4)

    with open("alive.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["round_no", "alive_sheep"])
        writer.writerows(alive_sheep_data)


if __name__ == "__main__":
    main()