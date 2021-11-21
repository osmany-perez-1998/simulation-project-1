import numpy as np

from variables import *

class Repair_Shop:
    def __init__(self,T=480) -> None:
        #Arrivals time limit.
        self.T=T
        # Sellers in paralel
        self.t = 0.0
        self.t_a= self.gen_new_arrival_time()
        self.t_d1=np.inf
        self.t_d2 =np.inf
        
        self.n_a=0
        self.n_d1=0
        self.n_d2=0
        self.SS = [0]
        
        self.a={}
        self.d1={}
        self.d2={}

        self.clients_db={}

        #Technicians in parallel.
        self.rep_queue=[]        
        self.rep_esp_queue=[]

        self.t_dt1=np.inf
        self.t_dt2=np.inf
        self.t_dt3=np.inf
        self.t_dtEsp=np.inf

        self.n_dt1=0
        self.n_dt2=0
        self.n_dt3=0
        self.n_dtEsp=0


        self.dt1_client = 0
        self.dt2_client = 0 
        self.dt3_client = 0
        self.dtEsp_client=0

        self.dt1={}
        self.dt2={}
        self.dt3={}
        self.dtEsp={}

    def min_time(self):
        return min(
            [
               self.t_a,
               self.t_d1,
               self.t_d2,
               self.t_dt1,
               self.t_dt2,
               self.t_dt3,
               self.t_dtEsp
            ]
        )

    def profit(self):
        services={
            1 : 0,
            2 : 350,
            3 : 500,
            4 : 750
        }

        profit = 0
        for client_type in self.clients_db.values():
            profit+= services[client_type]
        return profit
    

    def simulate(self):
        first=True

        while first or self.SS[0] or self.rep_queue or self.rep_esp_queue or self.t_a<=self.T :
            first=False
        #Sellers in parallel-------------------------------------------------
            
            #Arrival out of time
            if (self.min_time()== self.t_a and self.t_a>self.T):
                self.t_a= np.inf
            #Arrivals
            if (self.min_time()==self.t_a and self.t_a<= self.T):
                self.t= self.t_a
                self.n_a+=1
                self.t_a = self.t + self.gen_new_arrival_time()
                self.a[self.n_a] = self.t
                self.clients_db[self.n_a]= self.gen_new_client_type()

                if self.SS[0] == 0:
                    self.SS = [1,self.n_a,0]
                    self.t_d1 = self.t + self.gen_new_seller_departure_time()
                elif self.SS[0]==1 and self.SS[1]!=0 and self.SS[2] == 0:
                    self.SS[0]=2
                    self.SS[2] =self.n_a
                    self.t_d2 = self.t + self.gen_new_seller_departure_time()

                elif self.SS[0]==1 and self.SS[1]==0 and self.SS[2] != 0:
                    self.SS[0]=2
                    self.SS[1] =self.n_a
                    self.t_d1 = self.t + self.gen_new_seller_departure_time()

                elif self.SS[0] > 1 :
                    self.SS[0]+=1
                    self.SS.append(self.n_a)
            
            #Leave Seller1
            if (self.min_time()==self.t_d1 and self.t_d1<= self.T):
                self.t= self.t_d1
                self.n_d1+=1
                self.d1[self.SS[1]]=self.t

                #Add to repair queue---------------------
                if(self.clients_db[self.SS[1]] in [1,2]):
                    self.rep_queue.append(self.SS[1])
                if(self.clients_db[self.SS[1]] == 3):
                    self.rep_esp_queue.append(self.SS[1])
                #----------------------------------------

                #Assign clients to technicians-------------------------------------
                if(len(self.rep_queue) and self.dt1_client ==0):                
                    self.dt1_client= self.rep_queue.pop(0)
                    self.t_dt1 = self.t+ self.gen_new_tec_departure_time()               
                
                if(len(self.rep_queue) and self.dt2_client ==0):                
                    self.dt2_client= self.rep_queue.pop(0)
                    self.t_dt2 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_queue) and self.dt3_client ==0):                
                    self.dt3_client= self.rep_queue.pop(0)
                    self.t_dt3 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_esp_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_esp_departure_time()
                elif (len(self.rep_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_departure_time()
                #------------------------------------------------------------------
                
                if self.SS[0]==1:
                    self.SS =[0]
                    self.t_d1 = np.inf
                if self.SS[0] ==2:
                    self.SS = [1,0,self.SS[2]]
                    self.t_d1 = np.inf
                if self.SS[0]>2:
                    self.SS[0]-=1
                    self.SS[1]= self.SS[3]
                    self.SS.pop(3)     
                    self.t_d1 = self.t + self.gen_new_seller_departure_time()         

            #Leave Seller2
            if (self.min_time()==self.t_d2 and self.t_d2<= self.T):
                self.t= self.t_d2
                self.n_d2+=1
                self.d2[self.SS[2]]=self.t

                #Add to repair queue---------------------
                if(self.clients_db[self.SS[2]] in [1,2]):
                    self.rep_queue.append(self.SS[2])
                if(self.clients_db[self.SS[2]] == 3):
                    self.rep_esp_queue.append(self.SS[2])
                #----------------------------------------

                #Assign clients to technicians-------------------------------------
                if(len(self.rep_queue) and self.dt1_client ==0):                
                    self.dt1_client= self.rep_queue.pop(0)
                    self.t_dt1 = self.t+ self.gen_new_tec_departure_time()               
                
                if(len(self.rep_queue) and self.dt2_client ==0):                
                    self.dt2_client= self.rep_queue.pop(0)
                    self.t_dt2 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_queue) and self.dt3_client ==0):                
                    self.dt3_client= self.rep_queue.pop(0)
                    self.t_dt3 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_esp_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_esp_departure_time()
                elif (len(self.rep_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_departure_time()
                #------------------------------------------------------------------                
                
                if self.SS[0]==1:
                    self.SS =[0]
                    self.t_d2 = np.inf
                if self.SS[0] ==2:
                    self.SS = [1,self.SS[1],0]
                    self.t_d2 = np.inf
                if self.SS[0]>2:
                    self.SS[0]-=1
                    self.SS[2]= self.SS[3]
                    self.SS.pop(3)     
                    self.t_d2 = self.t + self.gen_new_seller_departure_time()   

            #Arrival out of time
            if (self.min_time()== self.t_a and self.t_a>self.T):
                self.t_a= np.inf

            #Close event Seller1 
            if (self.min_time()== self.t_d1 and self.t_a>self.T and self.SS[0]>0):   
                self.t = self.t_d1
                self.n_d1 =+1
                self.d1[self.SS[1]]= self.t    
                
                #Add to repair queue---------------------
                if(self.clients_db[self.SS[1]] in [1,2]):
                    self.rep_queue.append(self.SS[1])
                if(self.clients_db[self.SS[1]] == 3):
                    self.rep_esp_queue.append(self.SS[1])
                #----------------------------------------
                #Assign clients to technicians-------------------------------------
                if(len(self.rep_queue) and self.dt1_client ==0):                
                    self.dt1_client= self.rep_queue.pop(0)
                    self.t_dt1 = self.t+ self.gen_new_tec_departure_time()               
                
                if(len(self.rep_queue) and self.dt2_client ==0):                
                    self.dt2_client= self.rep_queue.pop(0)
                    self.t_dt2 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_queue) and self.dt3_client ==0):                
                    self.dt3_client= self.rep_queue.pop(0)
                    self.t_dt3 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_esp_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_esp_departure_time()
                elif (len(self.rep_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_departure_time()
                #------------------------------------------------------------------      
                
                if self.SS[0]==1:
                    self.SS =[0]
                    self.t_d1 = np.inf
                if self.SS[0] ==2:
                    self.SS = [1,0,self.SS[2]]
                    self.t_d1 = np.inf
                if self.SS[0]>2:
                    self.SS[0]-=1
                    self.SS[1]= self.SS[3]
                    self.SS.pop(3)     
                    self.t_d1 = self.t + self.gen_new_seller_departure_time() 

            #Close event Seller2 
            if (self.min_time()== self.t_d2 and self.t_a>self.T and self.SS[0]>0):   
                self.t = self.t_d2
                self.n_d2 =+1
                
                self.d2[self.SS[2]]= self.t


                
                #Add to repair queue---------------------
                if(self.clients_db[self.SS[2]] in [1,2]):
                    self.rep_queue.append(self.SS[2])
                if(self.clients_db[self.SS[2]] == 3):
                    self.rep_esp_queue.append(self.SS[2])
                #----------------------------------------
                #Assign clients to technicians-------------------------------------
                if(len(self.rep_queue) and self.dt1_client ==0):                
                    self.dt1_client= self.rep_queue.pop(0)
                    self.t_dt1 = self.t+ self.gen_new_tec_departure_time()               
                
                if(len(self.rep_queue) and self.dt2_client ==0):                
                    self.dt2_client= self.rep_queue.pop(0)
                    self.t_dt2 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_queue) and self.dt3_client ==0):                
                    self.dt3_client= self.rep_queue.pop(0)
                    self.t_dt3 = self.t+ self.gen_new_tec_departure_time()
                
                if(len(self.rep_esp_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_esp_departure_time()
                elif (len(self.rep_queue) and self.dtEsp_client ==0):                
                    self.dtEsp_client= self.rep_queue.pop(0)
                    self.t_dtEsp = self.t+ self.gen_new_tec_departure_time()
                #------------------------------------------------------------------
                
                if self.SS[0]==1:
                    self.SS =[0]
                    self.t_d2 = np.inf
                if self.SS[0] ==2:
                    self.SS = [1,self.SS[1],0]
                    self.t_d2 = np.inf
                if self.SS[0]>2:
                    self.SS[0]-=1
                    self.SS[2]= self.SS[3]
                    self.SS.pop(3)     
                    self.t_d2 = self.t + self.gen_new_seller_departure_time() 
        
        
        #-------------------------------------------------------------------------------------------
        
        #Parallel Technicians 

            # Leave technician 1
            if self.min_time() == self.t_dt1 and self.t_dt1<= self.T:
                self.t = self.t_dt1
                self.n_dt1+=1
                self.dt1[self.dt1_client]= self.t
                
                if len(self.rep_queue):
                    self.dt1_client = self.rep_queue.pop(0)
                    self.t_dt1 = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dt1_client = 0
                    self.t_dt1 = np.inf

            # Leave technician 2
            if self.min_time() == self.t_dt2 and self.t_dt2<= self.T:
                self.t = self.t_dt2
                self.n_dt2+=1
                self.dt2[self.dt2_client]= self.t
                
                if len(self.rep_queue):
                    self.dt2_client = self.rep_queue.pop(0)
                    self.t_dt2 = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dt2_client = 0
                    self.t_dt2 = np.inf

            # Leave technician 3
            if self.min_time() == self.t_dt3 and self.t_dt3<= self.T:
                self.t = self.t_dt3
                self.n_dt3+=1
                self.dt3[self.dt3_client]= self.t
                
                if len(self.rep_queue):
                    self.dt3_client = self.rep_queue.pop(0)
                    self.t_dt3 = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dt3_client = 0
                    self.t_dt3 = np.inf

            # Leave specialized technician 
            if self.min_time() == self.t_dtEsp and self.t_dtEsp<= self.T:
                self.t = self.t_dtEsp
                self.n_dtEsp+=1
                self.dtEsp[self.dtEsp_client]= self.t
                
                if len(self.rep_esp_queue):
                    self.dtEsp_client = self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t + self.gen_new_tec_esp_departure_time()
                elif len(self.rep_queue):
                    self.dtEsp_client = self.rep_queue.pop(0)
                    self.t_dtEsp = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dtEsp_client = 0
                    self.t_dtEsp = np.inf

            # Close event technician 1
            if self.min_time() == self.t_dt1 and self.t_a > self.T and self.SS[0]==0 and self.rep_queue :
                self.t = self.t_dt1
                self.n_dt1+=1
                self.dt1[self.dt1_client]= self.t

                if len(self.rep_queue):
                    self.dt1_client = self.rep_queue.pop(0)
                    self.t_dt1 = self.time + self.gen_new_tec_departure_time()
                else:
                    self.dt1_client = 0
                    self.t_dt1 = np.inf

            # Close event technician 2
            if self.min_time() == self.t_dt2 and self.t_a > self.T and self.SS[0]==0 and self.rep_queue :
                self.t = self.t_dt2
                self.n_dt2+=1
                self.dt2[self.dt2_client]= self.t

                if len(self.rep_queue):
                    self.dt2_client = self.rep_queue.pop(0)
                    self.t_dt2 = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dt2_client = 0
                    self.t_dt2 = np.inf
            # Close event technician 3
            if self.min_time() == self.t_dt3 and self.t_a > self.T and self.SS[0]==0 and self.rep_queue :
                self.t = self.t_dt3
                self.n_dt3+=1
                self.dt3[self.dt3_client]= self.t

                if len(self.rep_queue):
                    self.dt3_client = self.rep_queue.pop(0)
                    self.t_dt3 = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dt3_client = 0
                    self.t_dt3 = np.inf

            # Close event especialized technician
            if self.min_time() == self.t_dtEsp and self.t_a > self.T and self.SS[0]==0 and (self.rep_queue or self.rep_esp_queue):
                self.t = self.t_dtEsp
                self.n_dtEsp+=1
                self.dtEsp[self.dtEsp_client]= self.t

                if len(self.rep_esp_queue):
                    self.dtEsp_client = self.rep_esp_queue.pop(0)
                    self.t_dtEsp = self.t + self.gen_new_tec_esp_departure_time()
                elif len(self.rep_queue):
                    self.dtEsp_client = self.rep_queue.pop(0)
                    self.t_dtEsp = self.t + self.gen_new_tec_departure_time()
                else:
                    self.dtEsp_client = 0
                    self.t_dtEsp = np.inf


    def gen_new_client_type(self):        
        u = np.random.uniform(0, 1)
        if u <= 0.45:
            return 1
        if 0.45 < u <= 0.70:
            return 2
        if 0.70 < u <= 0.80:
            return 3
        if 0.80 < u <= 1:
            return 4
            

    def gen_new_arrival_time(self):                                             
        return poisson_distribution(20)
    
    def gen_new_seller_departure_time(self):
        return normal_distribution(5,2)


    def gen_new_tec_departure_time(self):                               
        return exponential_distribution(20)
    
    def gen_new_tec_esp_departure_time(self):                                
        return exponential_distribution(15)



