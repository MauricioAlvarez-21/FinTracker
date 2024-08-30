import numpy as np
def ComputeMarkovProbability(hist:list, num_days = 3, target_growth_rate = 0.02):
    growth_array = list()
    for i in range(-1*len(hist), -1):
        growth_array.append((hist[i+1]/hist[i])-1)
    last_closing_rate = growth_array[-1]
    total_recount = 0
    succes_cases = 0
    tragedy_cases = 0
    for rate_index in range(len(growth_array)-num_days):
        if (last_closing_rate - 0.005) < growth_array[rate_index] and growth_array[rate_index] < last_closing_rate + 0.005:
            total_recount += 1
            final_growth_rate = 1
            for i in range(num_days):
                final_growth_rate = final_growth_rate*(growth_array[rate_index+i]+1)
            if (final_growth_rate -1 >= target_growth_rate):
                succes_cases +=1
            if (final_growth_rate -1 < 0):
                tragedy_cases+=1
    if (total_recount ==0):
        return "Growth like this has not been seen before"
    return [succes_cases/total_recount, tragedy_cases/total_recount]
