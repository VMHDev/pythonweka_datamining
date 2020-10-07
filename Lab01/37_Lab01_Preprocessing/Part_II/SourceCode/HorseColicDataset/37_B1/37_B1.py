from sys import argv
import csv
import math


def min_max_normalize(old_value, old_min, old_max, new_min, new_max):
    if (old_max - old_min) > 0:
        return str(round(((old_value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min), 3))
    return '0'


def find_standard_diviation(mean, array):
    length = len(array)
    if length == 1:
        return array[0]
    sum_distance = 0.0
    for value in array:
        sum_distance += 1.0*pow(mean - value, 2)
    varriance = sum_distance/(length - 1)
    standard_diviation = math.sqrt(varriance)

    return standard_diviation


def binning_equal_width(min_value, max_value, quantity, sorted_data):
    bag = []
    bag_item = []
    start = min_value
    if quantity > 0:
        r = int((max_value - min_value) / quantity) + 1
        for value in sorted_data:
            if value <= (start + r - 1):
                bag_item.append(value)
            else:
                bag.append(bag_item)
                bag_item = []
                start = value
                bag_item.append(start)
    last_bag = bag[len(bag) - 1]
    last_value = sorted_data[len(sorted_data) - 1]
    if last_value not in last_bag:
        last_bag.append(last_value)

    return bag


def binning_equal_depth(quantity, sorted_data):
    bag = []
    bag_item = []
    len_data = len(sorted_data)
    if len_data > quantity:
        d = len_data / quantity
        for value in sorted_data:
            bag_item.append(value)
            if len(bag_item) == d:
                bag.append(bag_item)
                bag_item = []
    else:
        bag_item.append(sorted_data)
        bag.append(bag_item)
    return bag


def data_discrete(bag, data):
    for item in bag:
        if data in item:
            return str(item)


def remove_missing_data(data, prop_index):
    new_data = []
    for value in data:
        if value[prop_index].strip() != '':
            new_data.append(value)
    return new_data


def fill_missing_data_numeric(column_data, data, prop_index):
    filter_array = [""]
    numeric_array = [a for a in column_data if a.strip() not in filter_array]
    for index, value in enumerate(numeric_array):
        numeric_array[index] = int(value)
    avg_value = sum(numeric_array) / len(numeric_array)
    for item in data:
        if bool(item[prop_index].strip()):
            continue
        item[prop_index] = str(avg_value)
    return data


def fill_missing_data_string(column_data, data, prop_index):
    filter_array = [""]
    non_empty_array = [a for a in column_data if a.strip() not in filter_array]
    distinct_array = list(set(non_empty_array))
    max_value = find_max_frequency_element(non_empty_array, distinct_array)
    for item in data:
        if bool(item[prop_index].strip()):
            continue
        item[prop_index] = str(max_value)
    return data


def find_max_frequency_element(array, list_element):
    frequency_array = []
    for value in list_element:
        frequency_array.append(array.count(value))
    max_frequency = max(frequency_array)
    index_max = frequency_array.index(max_frequency)
    return list_element[index_max]


def remove_space(data):
    for index, value in enumerate(data):
        data[index] = value.replace(" ", "")
        a = 0
    return data


def write_csv(filename, header, data):
    try:
        writer = csv.writer(open(filename, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header)
        for item in data:
            writer.writerow(item)
        return 1
    except:
        return 0


# convert data column to integer array
def convert_data_column_to_int(data, column_index):
    array = []
    i = 0
    for item in data:
        try:
            array.append(int(item[column_index]))
            i += 1
        except ValueError:
            array = []
            break
    return array


def convert_column_data_to_array(data, column_index):
    array = []
    i = 0
    for item in data:
        array.append(item[column_index])
    return array


def is_numeric_array(array):
    for item in array:
        try:
            int(item)
        except:
            if bool(item.strip()):
                return False
    return True


def is_array_missing_data(array):
    filter_array = [""]
    non_empty_array = [a for a in array if a.strip() not in filter_array]
    return len(non_empty_array) < len(array)


def main(argv):
    filterProperties = argv[4].split(',')
    feature = argv[3]
    input = argv[1]
    output = argv[2]
    if feature == 'c' or feature == 'd':
        bag_quantity = argv[5]
    extension = '.csv'

    if extension not in input:
        input += extension
    if extension not in output:
        output += extension

    with open(input) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
    header = remove_space(data[0])
    del data[0]  # remove header

    filterProperties = remove_space(filterProperties)
    for property in filterProperties:
        if property in header:
            prop_index = header.index(property)
            column_data_int = convert_data_column_to_int(data, prop_index)  # convert data to int
            if len(column_data_int) > 0 and feature != "f" and feature != "e":
                if feature == "a":
                    old_min = min(column_data_int)
                    old_max = max(column_data_int)
                    for item in data:
                        index_item = data.index(item)
                        old_value = column_data_int[index_item]
                        item[prop_index] = min_max_normalize(old_value, old_min, old_max, 0, 1)
                elif feature == "b":
                    mean = sum(column_data_int) / len(column_data_int)
                    standard_deviation = find_standard_diviation(mean, column_data_int)
                    for item in data:
                        index_item = data.index(item)
                        old_value = column_data_int[index_item]
                        item[prop_index] = (old_value - mean) / standard_deviation
                elif feature == "c":
                    min_value = min(column_data_int)
                    max_value = max(column_data_int)
                    sorted_array = column_data_int.copy()
                    sorted_array.sort()
                    bag = binning_equal_width(min_value, max_value, bag_quantity, sorted_array)
                    for item in data:
                        index_item = data.index(item)
                        old_value = column_data_int[index_item]
                        item[prop_index] = data_discrete(bag, old_value)
                elif feature == "d":
                    sorted_array = column_data_int.copy()
                    sorted_array.sort()
                    bag = binning_equal_depth(bag_quantity, sorted_array)
                    for item in data:
                        index_item = data.index(item)
                        old_value = column_data_int[index_item]
                        item[prop_index] = data_discrete(bag, old_value)
            else:
                column_data_str = convert_column_data_to_array(data, prop_index)  # convert column data to str array
                if feature == "e":
                    data = remove_missing_data(data, prop_index)
                    test = 1
                elif feature == "f":
                    if is_array_missing_data(column_data_str):
                        if is_numeric_array(column_data_str):
                            data = fill_missing_data_numeric(column_data_str, data, prop_index)
                        else:
                            data = fill_missing_data_string(column_data_str, data, prop_index)
                else:
                    print("Khong the chuan hoa du lieu ", property)

    write_csv(output, header, data)
    print("Kiem tra file ", output)


if __name__ == "__main__":
    main(argv)
