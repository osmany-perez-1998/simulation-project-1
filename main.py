from proyecto import *

def main():
    
    print("\n \n \n Welcome to Happy Computing. \n \n \n")

    sim_cond= False
    

    while not sim_cond:
        try:
            simulations = int(input("Number of Simulations: "))
            sim_cond = True
        except:
            print("Simulations must be an integer. \n")

    time_cond= False

    while not time_cond:
        try:
            time = float(input("Time in hours of a workday: "))
            time_cond = True
            time*=60
        except:
            print("Time must be a number. \n")

    print()
    

    total_profit=0
    clients_count=0
    
    time_after=0
    overtime_count=0


    for i in range(simulations):
        shop = Repair_Shop(time)
        shop.simulate()
        total_profit+= shop.profit()
        clients_count+= len(shop.clients_db)
        if shop.t -time >0:
            time_after+= (shop.t-time) 
            overtime_count+=1
        
        print("Simulation Progress: ",i+1," completed.", end='\r')

    average_profit = total_profit /simulations
    average_clients_count = clients_count /simulations
    average_time_after = time_after/overtime_count if overtime_count else 0

    print()
    print("Mean profit after ",time/60 , " hours:", average_profit)
    print("Mean clients served: " ,average_clients_count)
    print("Mean overtime: ",average_time_after," minutes. \n \n")

    

main()