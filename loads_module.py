import functools
import operator
nodes=int(raw_input('enter number of nodes in the feeder: '))

class Loads():
    def __init__(self):
        self.dict_laterals={}
        self.dict_impedance_by_loads={}
        self.dict_total_impedance_by_lat={}

    def collect_lats(self, number_of_nodes):
        """
        return a dictionary that contains the number of laterals by node
        """
        n = 1
        while n <= number_of_nodes:
            var = int(raw_input("the number of laterals in node"+str(n)+"= "))
            self.dict_laterals[n]=var
            n = n+1
            if n > number_of_nodes:
                var = int(raw_input("the number of laterals in last load = "))
                self.dict_laterals[n]=var
                break
        #print(self.dict_laterals)
        return self.dict_laterals

    def collect_impedance_by_lat(self, number_of_nodes):
        """
        return a dictionary that contains the impedance by laterals in complex numbers
        """
        n = 1
        while n <= number_of_nodes:
            lats = self.dict_laterals[n]
            m = 1
            var = []
            while m <= lats:
                real=float(raw_input("real part of the impedance on load"+str(n)+"-lateral"+str(m)+": " ))
                imaginary=float(raw_input("imaginary part of the impedance for load"+str(n)+"-lateral"+str(m)+": "))
                var.append(complex(real,imaginary))
                self.dict_impedance_by_loads[n] = var
                m = m+1
            n = n+1
            if n > number_of_nodes:
                lats = self.dict_laterals[n]
                m =1
                while m <= lats:
                    real=float(raw_input("real part of the impedance on load"+str(n)+"-lateral"+str(m)+": " ))
                    imaginary=float(raw_input("imaginary part of the impedance for load"+str(n)+"-lateral"+str(m)+": "))
                    var.append(complex(real,imaginary))
                    self.dict_impedance_by_loads[n] = var
                    m = m + 1
                break


        #print self.dict_impedance_by_loads
        return self.dict_impedance_by_loads

    def calc_load(self, number_of_nodes):
        """
        return a dictionary that contains the load value by node, if multiple laterals, use parallel impedance formula
        """
        n = 1
        while n <= number_of_nodes+1:
            var1=self.dict_impedance_by_loads[n]
            times=functools.reduce(operator.mul, var1, 1)
            adds=sum(var1)
            div=times/adds
            self.dict_total_impedance_by_lat[n]=div
            n = n+1
        #print "dict_total_impedance_by_lat: ", self.dict_total_impedance_by_lat
        return self.dict_total_impedance_by_lat


loads=Loads()
lats=loads.collect_lats(nodes)
lat_impedance=loads.collect_impedance_by_lat(nodes)
total_impedance_by_lat=loads.calc_load(nodes)
print "dict_total_impedance_by_lat: ",total_impedance_by_lat

