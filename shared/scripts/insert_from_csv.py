import csv

CSV_FILE = r"C:\Users\paulh\Downloads\Workout Log (Responses) - Form Responses 1.csv"


def main():
    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        # for row in reader:
        #     print(row)

        new_program = None
        sorted_rows = sorted(reader, key=lambda row: row["Date"])
        for row in sorted_rows:
            if program := row["Program Type"] != new_program:
                # insert program
                new_program = program
                print(new_program)

            # insert workout
            if exercise_count := int(row["Exercises"]) != -1:
                for i in range(exercise_count):
                    # insert new blank exercise
                    print(i)


if __name__ == "__main__":
    main()
