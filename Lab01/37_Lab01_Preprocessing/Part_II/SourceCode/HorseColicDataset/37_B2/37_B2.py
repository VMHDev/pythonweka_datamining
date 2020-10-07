from sys import argv
import csv


def get_header(data):
    header = []
    for item in data:
        line_array = item.split('=')
        key = line_array[0]
        if key in header and header.index(key) == 0:
            break
        if key not in header:
            if '?' in key:
                key = key.replace('?', '')
            header.append(key)
    return header


def get_country(data):
    country = []
    country_item = []
    for item in data:
        if '=' not in item:
            print(item)
            continue
        line_array = item.split('=')
        key = line_array[0]
        value = line_array[1]
        if key == 'country':
            value = value.replace('\n', '')
            country_item.append(value)
            country_item.append(data.index(item))
            country.append(country_item)
            country_item = []
    return country


def get_non_country(header, country_data, all_data):
    non_country_data = []
    non_country_item = []
    filtered_property = []
    line_count = 0
    for index_country, item_country in enumerate(country_data):
        filtered_property = []
        if index_country == len(country_data) - 1:
            start_country = country_data[index_country]
            start_index = start_country[1]
            data_index = start_index + 1
            property_count = len(all_data) - int(start_index) - 1
            non_country_item = create_object_array(header, property_count, data_index, all_data)
            non_country_data.append(non_country_item)
            break
        start_country = country_data[index_country]
        end_country = country_data[index_country + 1]
        start_index = start_country[1]
        end_index = end_country[1]
        data_index = start_index + 1
        property_count = end_index - start_index - 1

        non_country_item = create_object_array(header, property_count, data_index, all_data)
        non_country_data.append(non_country_item)

    return non_country_data


def create_object_array(header, property_count, start_index, all_data):
    non_country_item = []
    for header_item in header:
        if header_item == 'country':
            continue
        if start_index == len(all_data) or property_count == 0:
            non_country_item.append('')
            continue
        for i in range(0, property_count):
            field_data = all_data[start_index].split('=')
            key = field_data[0]
            value = field_data[1]
            if key == header_item:
                value = value.replace('\n', '')
                non_country_item.append(value)
                start_index += 1
            else:
                non_country_item.append('')
            break
    return non_country_item


def delete_empty_country(country, non_country):
    country_clone = country.copy()
    non_country_clone = non_country.copy()
    country.clear()
    non_country.clear()
    for non_country_clone_item in non_country_clone:
        if non_country_clone_item.count('') != len(non_country_clone_item):
            index = non_country_clone.index(non_country_clone_item)
            non_country.append(non_country_clone_item)
            country.append(country_clone[index])


def delete_duplicate_country(country, non_country):
    country_clone = country.copy()
    non_country_clone = non_country.copy()
    country.clear()
    non_country.clear()
    for index, non_country_clone_item in enumerate(non_country_clone):
        if non_country_clone_item not in non_country:
            non_country.append(non_country_clone_item)
            country.append(country_clone[index])


def change_mi_to_km(non_country, area_index):
    for index, non_country_item in enumerate(non_country):
        if non_country_item[area_index] != '':
            unit = non_country_item[area_index][-2:]
            if unit == 'mi':
                try:
                    area_mi = non_country_item[area_index][:-2]
                    area_mi = area_mi.replace(',', '.')
                    area_km = float(float(area_mi) / 1000)
                    non_country[index][area_index] = str(area_km) + 'mi'
                except:
                    for c in area_mi:
                        if c.isdigit():
                            area_km = float(float(area_mi) / 1000)
                            non_country[index][area_index] = str(area_km) + 'mi'
                            break
                        area_mi = area_mi.replace(c, '')


def merge_data(country, non_country):
    data = []
    for index, item in enumerate(non_country):
        try:
            data_item = []
            country_id = []
            country_id.append(country[index][0])
            data_item = country_id + item
            data.append(data_item)
        except:
            a=0
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


def main(argv):
    input = argv[1]
    output = '37_B2.csv'
    with open(input, 'r') as file:
        data_text = file.readlines()

    header = get_header(data_text)
    data_value = data_text.copy()  # non-header data
    for index, item in enumerate(header):
        del data_value[0]
    country_data = get_country(data_value)
    non_country_data = get_non_country(header, country_data, data_value)
    delete_empty_country(country_data, non_country_data)
    #delete_duplicate_country(country_data, non_country_data)
    #area_index = header.index('area')
    #change_mi_to_km(non_country_data, area_index - 1)  # in non_country_data no column 'country'
    result_data = merge_data(country_data, non_country_data)
    write_csv(output, header, result_data)
    print("Kiem tra file ", output)


if __name__ == "__main__":
    main(argv)
