import simpy
import random

# Simulation Parameters
INITIAL_INVENTORY = 60
DEMAND_SIZES = [1, 2, 3, 4]
DEMAND_PROBABILITIES = [0.167, 0.500, 0.833, 1.000]
MEAN_INTERDEMAND_TIME = 0.10
DELIVERY_LAG_RANGE = (0.50, 1.00)
SIMULATION_LENGTH = 120
ORDER_POLICIES = [(20, 40), (20, 60), (20, 80), (20, 100), (40, 60), (40, 80), (40, 100), (60, 80), (60, 100)]
K = 32.0
i = 3.0
h = 1.0
pi = 5.0

def demand_generator():
    r = random.random()
    for i, prob in enumerate(DEMAND_PROBABILITIES):
        if r < prob:
            return DEMAND_SIZES[i]
    return DEMAND_SIZES[-1]

def inventory_system(env, policy, results):
    s, S = policy
    inventory = INITIAL_INVENTORY
    total_cost, ordering_cost, holding_cost, shortage_cost = 0, 0, 0, 0
    
    while env.now < SIMULATION_LENGTH:
        demand = demand_generator()
        if inventory >= demand:
            inventory -= demand
        else:
            shortage_cost += (demand - inventory) * pi
            inventory = 0
        
        holding_cost += inventory * h
        if inventory <= s:
            order_quantity = S - inventory
            ordering_cost += K + i * order_quantity
            delivery_time = random.uniform(*DELIVERY_LAG_RANGE)
            yield env.timeout(delivery_time)
            inventory += order_quantity
        
        yield env.timeout(random.expovariate(1.0 / MEAN_INTERDEMAND_TIME))
    
    total_cost = ordering_cost + holding_cost + shortage_cost
    results.append((policy, total_cost, ordering_cost, holding_cost, shortage_cost))

def main():
    random.seed(42)
    env = simpy.Environment()
    results = []
    
    for policy in ORDER_POLICIES:
        env.process(inventory_system(env, policy, results))
    env.run()
    
    print("Single-product inventory system")
    print(f"Initial inventory level                      {INITIAL_INVENTORY} items")
    print(f"Number of demand sizes                        {len(DEMAND_SIZES)}")
    print("Distribution function of demand sizes    ", "   ".join(f"{p:.3f}" for p in DEMAND_PROBABILITIES))
    print(f"Mean interdemand time                      {MEAN_INTERDEMAND_TIME:.2f} months")
    print(f"Delivery lag range                         {DELIVERY_LAG_RANGE[0]:.2f} to      {DELIVERY_LAG_RANGE[1]:.2f} months")
    print(f"Length of the simulation                    {SIMULATION_LENGTH} months")
    print(f"K = {K}   i = {i}   h = {h}   pi = {pi}")
    print(f"Number of policies                            {len(ORDER_POLICIES)}")
    print("                  Average        Average        Average        Average")
    print("   Policy       total cost    ordering cost  holding cost   shortage cost")
    for policy, total, order, hold, short in results:
        print(f" {policy}         {total:.2f}          {order:.2f}          {hold:.2f}          {short:.2f}")

if __name__ == "__main__":
    main()
