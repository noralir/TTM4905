def create_list_with_given_average(n,avg,type="lambda"):

    if type=="lambda":
        average = n * avg
        increment_number = avg
        n1 = int(average-increment_number/2)
        n2 = int(average+increment_number/2)
        avg_pkt_ia_time = [n1, n2]
        current_add = increment_number
        while len(avg_pkt_ia_time) < n:
            avg_pkt_ia_time.append(n1 - current_add)
            avg_pkt_ia_time.append(n2 + current_add)
            current_add += increment_number
        avg_pkt_ia_time.sort()

    elif type=="mu":
        average = avg
        start = average-4.5
        list1 = [int(start+i) for i in range(10)]
        if n == 10:
            avg_pkt_ia_time = list1
        elif n == 100:
            avg_pkt_ia_time = list1*10
        elif n == 1000:
            avg_pkt_ia_time = list1*100
        else:
            return False
    

    
    return avg_pkt_ia_time
