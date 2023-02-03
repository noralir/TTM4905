import simpy

def packetgenerator(env):
    i = 0
    while True:
        yield env.timeout(np.random.exponential(1/lambda_arrival)) 
        env.process(packet(env, i))
        i += 1

def packet(env, number):
    t_generated = env.now
    size = np.random.exponential(1/lambda_size)

    with buffer.request() as req:
        yield req
        t_processing_start = env.now
        yield env.timeout(size / buffer_capacity * 10**6)
        t_processing_end = env.now 

    # Calculate data
    t_buffer = t_processing_start - t_generated
    t_processing = t_processing_end - t_processing_start

    # Save data
    packets += 1
    waiting_time += t_buffer
    processing_time += t_processing
    sojourn_time += t_buffer + t_processing

    # Printing
    writer.writerow([number, t_generated, t_buffer, t_processing])
    #print(f"{number}\t{t_generated}\t{t_processing}\t{t_buffer}")




def generic_simulator(
        avg_pkt_ia_time_µs, dist_type_pkt_ia_time, 
        avg_pkt_len_bits, variance_pkt_len_bits, dist_type_pkt_len,
        capacity_bps,
        filename):
    
    

    
        

    env = simpy.Environment()
    buffer = simpy.Resource(env)
    
    return