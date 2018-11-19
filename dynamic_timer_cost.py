# Dynamic Programming Python implementation of Coin
# Change problem

import pandas as pd
import ipdb

values, weights, table = [], [], [[]]

def knapsack(i, W):
    global weights, values, table, counter
    if (i < 0):
        # Base case
        return 0
    if (weights[i] > W):
        # Recursion
        table[i][W-1] = knapsack(i - 1, W)
        return table[i][W-1]
    else:
        # Recursion
        table[i][W-1] = max(knapsack(i - 1, W), values[i] + knapsack(i - 1, W - weights[i]))
        return table[i][W-1]


def timer_cost(time, cost, sequence):

    global timers, timer_costs, cost_table

    if time <= 0:
        return cost, sequence
    elif time in cost_table:
        # ipdb.set_trace()
        sequence.extend(cost_table[time][1])
        return cost_table[time][0] + cost, sequence
    elif time in timers.values:
        index = timers[timers == time].index[0]
        cost = cost + timer_costs[index]
        sequence.append(time)
        return cost, sequence
    else:
        min_cost = 99999999
        final_sequence = []

        if any(timers >= time):
            min_index = timers[timers >= time].index[0] + 1
        else:
            min_index = len(timers)

        for i in range(min_index-1, -1, -1):
            new_sequence = list(sequence)
            new_sequence.append(timers[i])

            new_cost, new_sequence = timer_cost(time - timers[i], cost + timer_costs[i], new_sequence)
            if new_cost < min_cost:
                #set new cost and sequence
                min_cost = new_cost
                final_sequence = list(new_sequence)

        return min_cost, final_sequence


def hours_to_days(i):

    return '{0} days, {1} hours'.format(i / 24, i % 24)


if __name__ == '__main__':

    timer_table = pd.read_csv('~/MZ/data/ffxv_timer_costs.csv')

    global timers, timer_costs, cost_table
    timers = timer_table['Hour']
    timer_costs = timer_table['Cost']
    cost_table = dict()
    print_table = pd.DataFrame(columns=['time', 'time (hours', 'cost', 'sequence'])

    MAX_HOURS = 60*24
    for i in xrange(MAX_HOURS):
        cost_table[i] = timer_cost(i, 0, [])
        new_row = [hours_to_days(i), i, cost_table[i][0], cost_table[i][1]]
        print_table.loc[i] = new_row
        print hours_to_days(i), cost_table[i]
