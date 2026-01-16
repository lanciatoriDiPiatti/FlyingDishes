import statistics;

def check_flag(data):
    return print("Sostituire con algoritmo di checking dei flag")

def calculate_average(data: list[int]) -> float:
    return sum(data) / len(data)

print (calculate_average([1,2,3,4,5]))


def calculate_pvariance(data: list[float]) -> float:
    return statistics.pvariance(data)

print (calculate_pvariance([1.0,2.0,3.0,4.0,5.0]))

def final_choice(average: list[int], mean: list[float]):
    max_avg = 0
    list_max_avg = []
    index = []
    
    for a in average:
        if a > max_avg:
            max_avg = a
            list_max_avg = [a]
            index = [average.index(a)]
        if a == max_avg:
            list_max_avg.append(a)
            index.append(average.index(a))
    
    if len(list_max_avg) == 1:
        return index[0]
    else:
        min_pv = float('inf')
        choice_index = [] 
        for m in list_max_avg:
            if statistics.pvariance(m) < min_pv:
                min_pv = statistics.pvariance(m),
                choice_index = [list_max_avg.index(m)]
            return "Ha vinto l'elemento" + str(choice_index[0])
                


    

