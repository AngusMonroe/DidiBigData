#!/usr/bin/python3
import datetime
from tqdm import tqdm
import json
from math import sin, cos, radians, sqrt, asin, pow

EARTH_REDIUS = 6378.137

order2derived = {}


def distance(lng1, lat1, lng2, lat2):
    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)

    radLat1 = radians(lat1)
    radLat2 = radians(lat2)
    a = radLat1 - radLat2
    b = radians(lng1) - radians(lng2)
    s = 2 * asin(sqrt(pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s


def compute_base_data():
    with open('../data/order2detail.json', 'r', encoding='utf-8') as json_file:
        order2detail = json.load(json_file)
    # output_file1 = open('../data_bak/didi_derived.csv', 'w', encoding='utf8')

    for order in tqdm(order2detail.keys()):
        past_time = 0
        detail = order2detail[order]
        if len(detail.keys()) == 1:
            continue
        for time in detail.keys():
            if past_time:
                x = distance(detail[past_time][0], detail[past_time][1][:-1], detail[time][0], detail[time][1][:-1])
                v = x / (int(time) - int(past_time))
                if order not in order2derived.keys():
                    order2derived[order] = [[int(past_time), int(time), x, v]]
                else:
                    order2derived[order].append([int(past_time), int(time), x, v])
            past_time = time
        derived_data = order2derived[order]
        for i in range(len(derived_data)):
            if i == 0 or i == 1:
                if i == 0:
                    order2derived[order][i].append(-1.0)
                continue
            a = (derived_data[i][3] + derived_data[i - 1][3] + derived_data[i - 2][3]) / abs(derived_data[i][1] - derived_data[i - 2][0])
            order2derived[order][i - 1].append(a)
            if i == len(derived_data) - 1:
                order2derived[order][i].append(-1.0)

    print('Saving data...')
    with open('../data/didi_derived.json', 'w', encoding='utf-8') as json_file:
        json.dump(order2derived, json_file, ensure_ascii=False)
    # for order in order2derived.keys():
    #     line = order
    #     for item in order2derived[order]:
    #         line += ', ' + str(item)
    #     line += '\n'
    #     output_file1.write(line)

    # output_file1.close()


# def compute_statistics_data():
#     order2statistics = {}
#     with open('../data_bak/order2detail.json', 'r', encoding='utf-8') as json_file1:
#         order2derived = json.load(json_file1)
#     with open('../data_bak/driver2order.json', 'r', encoding='utf-8') as json_file2:
#         driver2order = json.load(json_file2)
#     output_file2 = open('../data/order_statistics.csv', 'w', encoding='utf8')
#     output_file3 = open('../data/driver_statistics.csv', 'w', encoding='utf8')
#
#     for order in order2derived.keys():
#         v_count = 0.0
#         a_count = 0.0
#         # v_sum = 0.0
#         a_sum = 0.0
#         for items in order2derived[order]:
#             if items[3] > 60 / 3.6:
#                 v_count += 1
#             if items[4] > 7:
#                 a_count += 1
#             # v_sum += items[3]
#             # if items[4] >= 0:
#             #     a_sum += items[4]
#         v_ave = abs(order2derived[order][-1][3] - order2derived[order][0][3]) / (order2derived[order][-1][1] - order2derived[order][0][0])
#         a_ave = abs(order2derived[order][-2][4] - order2derived[order][1][4]) / (order2derived[order][-2][1] - order2derived[order][1][0])
#         line = str(v_count) + ', ' + str(a_count) + ', ' + str() + ', ' + str(a_sum/(len(order2derived[order]) - 2)) + '\n'
#         output_file2.write(line)
#
#     for driver in driver2order.keys():
#         v_count = 0.0
#         a_count = 0.0
#         v_sum = 0.0
#         a_sum = 0.0
#         for order in driver2order[driver]:
#             for items in order2derived[order]:
#                 if items[3] > 60 / 3.6:
#                     v_count += 1
#                 if items[4] > 7:
#                     a_count += 1
#                 v_sum += items[3]
#                 if items[4] >= 0:
#                     a_sum += items[4]
#
#
#
#     output_file2.close()

def compute_v():
    with open('../data/didi_derived.json', 'r', encoding='utf-8') as json_file1:
        order2derived = json.load(json_file1)
    output_file2 = open('../data/order_v.csv', 'w', encoding='utf8')

    for order in tqdm(order2derived.keys()):
        t0 = order2derived[order][0][0]
        t = order2derived[order][0][0]
        v_max = 0.0
        a_max = 0.0
        x_sum = 0.0
        for items in order2derived[order]:
            items = list(map(float, items))
            x_sum += items[2]
            if items[3] > v_max:
                v_max = items[3]
            if len(items) >= 5 and items[4] > a_max:
                a_max = items[4]
            if items[1] > t:
                t = items[1]
        if t == t0:
            continue
        v_ave = x_sum / (t - t0)
        output_file2.write(order + ', ' + str(v_max) + ', ' + str(a_max) + ', ' + str(v_ave) + '\n')
    output_file2.close()


def compute_time():

    input_file = open('../data/didi_sorted.csv', 'r', encoding='utf8')
    output_file = open('../data/order_time.csv', 'w', encoding='utf8')

    t0 = 0
    t = 0
    x0 = 0
    y0 = 0
    xt = 0
    yt = 0
    order = ''
    for line in tqdm(input_file.readlines()):
        items = line[:-1].split(',')

        if not order:
            t0 = datetime.datetime.fromtimestamp(int(items[3]))
            x0 = items[4]
            y0 = items[5]
        elif items[2] != order:
            t = datetime.datetime.fromtimestamp(int(items[3]))
            xt = items[4]
            yt = items[5]
            output_file.write(order + ', ' + str(t0) + ', ' + x0 + ', ' + y0 + ', ' + str(t) + ', ' + xt + ', ' + yt + '\n')
        order = items[2]
    input_file.close()
    output_file.close()


if __name__ == '__main__':
    print('Derive start')
    # compute_base_data()
    compute_v()
    # compute_time()
    print('Done.')
