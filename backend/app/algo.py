import statistics;

def check_flag(data):
    return print("Sostituire con algoritmo di checking dei flag")

def calculate_average(data: list[int]) -> float:
    print (sum(data) / len(data))
    return sum(data) / len(data)

def calculate_pvariance(data: list[float]) -> float:
    print(statistics.pvariance(data))
    return statistics.pvariance(data)

def final_choice(average: list[int], mean: list[float]):
    max_avg = 0
    list_max_avg = []
    index = []
    n1=0

    while n1 < len(average):
        a = average[n1]
        if a > max_avg:
            max_avg = a
            list_max_avg = [a]
            index = [n1]
        if a == max_avg:
            list_max_avg.append(a)
            index.append(n1)
        n1 += 1

    if len(list_max_avg) == 1:
        return index[0]
    else:
        min_pv = float('inf')
        choice_index = []
        n2 = 0 
        while n2 < len(index):
            b = mean[index[n2]]
            if b < min_pv:
                min_pv = b
                choice_index = [index[n2]]
            n2 += 1
        return choice_index[0]