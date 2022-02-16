import csv
import os


def get_data_from_csv(csvfile):
    with open(csvfile, "r") as csv_file:
        data = []
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
        return data


def write_data_to_csv(csvfile, new_data_dict, given_list, data_header):
    given_list.append(new_data_dict)
    with open(csvfile, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for row in given_list:
            csv_writer.writerow(row)


def update_data_in_csv(csvfile, updated_data, given_list, data_header):
    print(given_list)
    print(updated_data)
    for existing_dict in given_list:
        for key, value in existing_dict.items():
            if int(updated_data["id"]) == int(existing_dict["id"]):
                existing_dict[key] = updated_data[key]
    print(given_list)
    with open(csvfile, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for row in given_list:
            csv_writer.writerow(row)
