import csv


def get_data_from_csv(csv_file):
    with open(csv_file, "r") as csv_file:
        data = []
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data
