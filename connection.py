import csv
import data_manager


def get_data_from_csv(csvfile):
    with open(csvfile, "r") as csv_file:
        data = []
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
        return data


def write_data_to_csv(csvfile, given_list, data_header):
    with open(csvfile, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for row in given_list:
            csv_writer.writerow(row)


def update_data_in_csv(csvfile, updated_data, given_list, data_header):
    for existing_dict in given_list:
        for key, value in existing_dict.items():
            if int(updated_data["id"]) == int(existing_dict["id"]):
                existing_dict[key] = updated_data[key]
    write_data_to_csv(csvfile, given_list, data_header)


def delete_from_csv(csv_file, given_id, given_list, header):
    new_list = []
    for data_dict in given_list:
        if int(data_dict["id"]) != given_id:
            new_list.append(data_dict)
    write_data_to_csv(csv_file, new_list, header)
    return new_list

#
# def delete_from_question_csv(csv_file, question_id, given_list):
#     with open(csv_file, "w") as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=data_manager.QUESTION_HEADER)
#         csv_writer.writeheader()
#         for data_dict in given_list:
#             if int(data_dict["id"]) != question_id:
#                 csv_writer.writerow(data_dict)
#         return given_list


def delete_from_answer_csv(question_id):
    answers = get_data_from_csv(data_manager.answer_file_path)
    with open(data_manager.answer_file_path, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_manager.ANSWER_HEADER)
        csv_writer.writeheader()
        for answer in answers:
            if int(answer["question_id"]) != question_id:
                csv_writer.writerow(answer)
        return answers
