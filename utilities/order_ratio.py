#!/usr/bin/python3
import datetime
from tqdm import tqdm
import json
from math import sin, cos, radians, sqrt, asin, pow

EARTH_REDIUS = 6378.137

order2derived = {}
order2ratio = {}
order2turnNum = {}


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
    with open('../data/order2detail_sample.json', 'r', encoding='utf-8') as json_file:
        order2detail = json.load(json_file)
    # output_file1 = open('../data_bak/didi_derived.csv', 'w', encoding='utf8')

    for order in tqdm(order2detail.keys()):
        past_time = 0
        detail = list(map(int, order2detail[order].keys()))
        dis = 0
        if len(detail) == 1:
            continue
        for time in sorted(detail):
            time = str(time)
            if past_time:
                x = distance(order2detail[order][past_time][0], order2detail[order][past_time][1], order2detail[order][time][0], order2detail[order][time][1])
                dis += x
                if order not in order2derived.keys():
                    order2derived[order] = [[int(past_time), int(time), x]]
                else:
                    order2derived[order].append([int(past_time), int(time), x])
            past_time = time
        derived_data = order2derived[order]
        past_time = []
        order2ratio[order] = [[dis, -2]]
        dis = 0
        for time in sorted(detail): 
            time = str(time)
            if len(past_time)>=3:
                #compute the ratio 
                i = len(past_time)-1
                x2 = distance(order2detail[order][past_time[i]][0], order2detail[order][past_time[i]][1], order2detail[order][past_time[i-2]][0], order2detail[order][past_time[i-2]][1])
                x0 = derived_data[i-1][2]
                x1 = derived_data[i-2][2]
                if x2 != 0 and x0 != 0 and x1 != 0:
                    r = (x0+x1)/x2
                    # 余弦定理求theta
                    theta = (x1*x1+x0*x0-x2*x2)/(2*x1*x0)
                    if order not in order2ratio.keys():
                        order2ratio[order] = [[r, theta]]
                    else:
                        order2ratio[order].append([r, theta])
            past_time.append(time)
    print('Saving data...')
    # with open('../data/didi_derived.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(order2derived, json_file, ensure_ascii=False)
    with open('../data/order2ratio.json', 'w', encoding='utf-8') as json_file:
        json.dump(order2ratio, json_file, ensure_ascii=False)
    print('saving finished')

def compute_turn_times(threshold):
    with open('../data/order2ratio.json', 'r', encoding='utf-8') as json_file:
        order2ratio = json.load(json_file)
    for order in tqdm(order2ratio.keys()):
        turnNum = 0
        for time in order2ratio[order]:
            if(time[1] == -2): continue
            if(time[1]>-0.9 and time[1]<-0.7):
                turnNum += 1
        order2turnNum[order] = turnNum/order2ratio[order][0][0]
    print('start saving')
    with open('../data/order2turnNum.json', 'w', encoding='utf-8') as json_file:
        json.dump(order2turnNum, json_file, ensure_ascii=False)
    print('finish saving')

if __name__ == '__main__':
    compute_base_data()    
    compute_turn_times(-0.9)
    print('Done.')
