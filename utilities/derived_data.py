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
            if items[4] > a_max:
                a_max = items[4]
            if items[1] > t:
                t = items[1]
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
    compute_base_data()
    compute_v()
    # compute_time()
    print('Done.')
