def create_list_with_given_average(n,avg):

    average = n * avg

    test1 = int(average/(n/2)/2)

    n1 = int(average-test1/2)
    n2 = int(average+test1/2)
    avg_pkt_ia_time = [n1, n2]

    current_add = test1

    while len(avg_pkt_ia_time) < n:
        avg_pkt_ia_time.append(n1 - current_add)
        avg_pkt_ia_time.append(n2 + current_add)
        current_add += test1

    avg_pkt_ia_time.sort()
    return avg_pkt_ia_time
