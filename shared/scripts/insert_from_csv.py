import csv

CSV_FILE = r"/Users/pharbulak/Downloads/Workout Log.csv"


def main():
    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        new_program = None
        sorted_rows = sorted(reader, key=lambda row: row["Date"])
        for row in sorted_rows:
            program = row.get("Program Type")
            if not program:
                raise ValueError(f"Program is required: {row}")

            if program != new_program:
                # insert program
                new_program = program
                print(new_program)

            # insert workout
            exercises = row.get("Exercises")
            if not exercises:
                raise ValueError(f"Exercises is required: {row}")

            exercise_count = int(exercises)
            print(exercise_count)
            # if exercise_count != -1:
            #     for i in range(exercise_count):
            #         # insert new blank exercise
            #         print(i)


if __name__ == "__main__":
    main()
