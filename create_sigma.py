def create_sigma(avg_pkt_len_bits, dist_type_pkt_len):
    sigma = []
    for i in range(len(avg_pkt_len_bits)):
        length = avg_pkt_len_bits[i]
        typ = dist_type_pkt_len[i]
        value=0
        if typ == "M":
            value = 1/((1/length)**2)
        elif typ == "D":
            value = 0
        elif typ == "G_uniform":
            value = (1/12)*((2*length)**2)
        sigma.append(value)
    return sigma