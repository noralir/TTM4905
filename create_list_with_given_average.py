def create_list_with_given_average(n,avg):
    average = n * avg
    increment_number = int(average/(n/2)/2)

    n1 = int(average-increment_number/2)
    n2 = int(average+increment_number/2)
    avg_pkt_ia_time = [n1, n2]

    current_add = increment_number

    while len(avg_pkt_ia_time) < n:
        avg_pkt_ia_time.append(n1 - current_add)
        avg_pkt_ia_time.append(n2 + current_add)
        current_add += increment_number

    avg_pkt_ia_time.sort()
    return avg_pkt_ia_time
