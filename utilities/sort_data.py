#!/usr/bin/python3

from tqdm import tqdm
import json

dates = []
date2driver = {}
driver2order = {}
order2detail = {}

input_file = open('../data/didi.csv', 'r', encoding='utf8')
output_file = open('../data/didi_sorted.csv', 'w', encoding='utf8')

print('Loading data...')
for line in tqdm(input_file.readlines()):
    items = line.split(',')

    if items[0] not in dates:
        dates.append(items[0])

    if items[0] not in date2driver.keys():
        date2driver[items[0]] = [items[1]]
    elif items[1] not in date2driver[items[0]]:
        date2driver[items[0]].append(items[1])

    if items[1] not in driver2order.keys():
        driver2order[items[1]] = [items[2]]
    elif items[2] not in driver2order[items[1]]:
        driver2order[items[1]].append(items[2])

    if items[2] not in order2detail.keys():
        detail = {items[3]: [items[4], items[5]]}
        order2detail[items[2]] = detail
    elif items[3] not in order2detail[items[2]].keys():
        order2detail[items[2]][items[3]] = [items[4], items[5]]


def save_json(dic, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(dic, json_file, ensure_ascii=False)

save_json(date2driver, '../data/date2driver.json')
save_json(driver2order, '../data/driver2order.json')
save_json(order2detail, '../data/order2detail.json')

print('Sorting...')
for date in tqdm(dates):
    for driver in date2driver[date]:
        for order in driver2order[driver]:
            detail = list(map(int, order2detail[order].keys()))
            for time in sorted(detail):
                output_file.write(date + ', ' + driver + ', ' + order + ', ' + str(time) + ', ' + order2detail[order][str(time)][0] + ', ' + order2detail[order][str(time)][1] + '\n')

input_file.close()
output_file.close()
