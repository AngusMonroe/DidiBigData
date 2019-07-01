#!/usr/bin/python3

from tqdm import tqdm

file = open('../data/didi.csv', 'r', encoding='utf8')

empty_num = 0
out_of_range_num = 0
mapping_conflict_num = 0
order2driver = {}


def save_map(dic, file_path):
    f = open(file_path, 'w', encoding='utf8')
    for key in dic.keys():
        f.write(key + ', ' + dic[key] + '\n')
    f.close()
    print('Map already saved in ' + file_path)

lines = file.readlines()
print('Found ' + str(len(lines)) + ' lines in the file.')

for line in tqdm(lines):
    items = line[:-1].split(',')
    if len(items) == 6:
        for item in items:
            if not item:
                empty_num += 1

        if float(items[4]) < 108.921859 or float(items[4]) > 109.009348 or \
           float(items[5]) < 34.204946 or float(items[5]) > 34.279936:
            out_of_range_num += 1

        if items[2] in order2driver.keys():
            if order2driver[items[2]] != items[1]:
                mapping_conflict_num += 1
        else:
            order2driver[items[2]] = items[1]

    else:
        empty_num += 1


if not empty_num:
    print('[Data Integrity Check] No null field in the data set.')
else:
    print('[Data Integrity Check] There is(are) ' + str(empty_num) + ' null field(s) in the data set.')
if not out_of_range_num:
    print('[Longitude and Latitude out of range Check] No field out of range in the data set.')
else:
    print('[Longitude and Latitude out of range Check] There is(are) ' + str(empty_num) + ' field(s) out of range in the data set.')
if not mapping_conflict_num:
    print('[ID Mapping Conflict Check] No ID mapping conflict in the data set.')
else:
    print('[ID Mapping Conflict Check] There is(are) ' + str(mapping_conflict_num) + ' ID mapping conflict(s) in the data set.')

save_map(order2driver, '../data/order2driver.csv')
