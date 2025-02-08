import simpy 
import random

# Simulation Parameters
RANDOM_SEED = 42
MEAN_INTERARRIVAL_TIME = 1.0  # Average time between arrivals (minutes)
MEAN_SERVICE_TIME = 0.5       # Average service time (minutes)
NUM_CUSTOMERS = 1000          # Total number of customers

def customer(env, name, server, wait_times):
    """Customer process."""
    arrival_time = env.now
    with server.request() as request:
        yield request  # Wait for server
        wait_times.append(env.now - arrival_time)
        service_time = random.expovariate(1.0 / MEAN_SERVICE_TIME)
        yield env.timeout(service_time)  # Service time

def setup(env, server, wait_times):
    """Generate customers at exponential intervals."""
    for i in range(NUM_CUSTOMERS):
        env.process(customer(env, f'Customer {i+1}', server, wait_times))
        interarrival_time = random.expovariate(1.0 / MEAN_INTERARRIVAL_TIME)
        yield env.timeout(interarrival_time)

def main():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)
    wait_times = []
    
    env.process(setup(env, server, wait_times))
    env.run()
    
    # Calculate performance metrics
    avg_delay_queue = sum(wait_times) / len(wait_times)
    avg_num_queue = avg_delay_queue / MEAN_INTERARRIVAL_TIME
    server_utilization = (sum(wait_times) + NUM_CUSTOMERS * MEAN_SERVICE_TIME) / env.now
    
    print(f"Mean interarrival time      {MEAN_INTERARRIVAL_TIME:.3f} minutes")
    print(f"Mean service time           {MEAN_SERVICE_TIME:.3f} minutes")
    print(f"Number of customers          {NUM_CUSTOMERS}")
    print(f"Average delay in queue      {avg_delay_queue:.3f} minutes")
    print(f"Average number in queue     {avg_num_queue:.3f}")
    print(f"Server utilization          {server_utilization:.3f}")
    print(f"Time simulation ended    {env.now:.3f} minutes")

if __name__ == "__main__":
    main()
