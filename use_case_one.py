def main():
    import cmath
    import pypyodbc
    import functools
    import operator
    #collect global variables
    num_of_nodes=int(raw_input('enter number of nodes in the feeder: '))
    i_real = float(raw_input('enter the real part of the measured current at substation e.g. 480: '))
    i_imaginary = float(raw_input('enter the imaginary part of the measured current at substation e.g. -160: '))
    i_total = complex(i_real,i_imaginary)
    print "i_total used in this feeder is: ", i_total
    v_real = float(raw_input('enter the real part of the measured voltage at substation e.g. 8002: '))
    v_imaginary = float(raw_input('enter the imaginary part of the measured voltage at substation e.g. 0: '))
    v_source = complex(v_real,v_imaginary)
    print "v_source used in this feeder is: ", v_source
    ansi_nominal = complex(120,0)

    class ConductorsClass():
        def __init__(self):
            self.dict_cond_type={}
            self.dict_cond_leng={}
            self.dict_conductors={}
  
        def collect_cond_type(self):
            """
            return a dictionary that contains the string value of the conductor type
            e.g. '1 AAC', '1 ACSR'
            """
            n = 1
            while n <= num_of_nodes+1:
                var=str(raw_input("the conductor_type of section"+str(n)+" example, 1 AAC : "))
                self.dict_cond_type[n]=var
                n = n+1
            #print "dict_cond_type: ", self.dict_cond_type
            return self.dict_cond_type
      
          #collect conductor lenghth per section
        def collect_cond_leng(self):
            """
            return a dictionary that contains the length of each section
            unit is feet
            """
            n = 1
            while n <= num_of_nodes+1:
                var=float(raw_input("the conductor length of section"+str(n)+" in thousand feet : "))
                self.dict_cond_leng[n]=var
                n = n+1
            #print "dict_cond_leng: ", self.dict_cond_leng
            return self.dict_cond_leng
      
        def get_impedance(self, conductorame):
            """
             return a list of a single tuple in complex number that is the impedance value
             of the corresponding conductor type in per 1000 feet unit
            """
            col1 = 'PosSequenceResistance_PerLUL'
            col2 = 'PosSequenceReactance_PerLUL'
            tabl = 'DevConductors'
            col_id = 'ConductorName'
            pypyodbc.lowercase = False
            conn = pypyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"Dbq=C:\Users\mliu\conductors.accdb;")
            cur = conn.cursor()
            cur.execute ("SELECT %s, %s FROM %s WHERE %s = %r" %(col1, col2, tabl, col_id, conductorame))
            # resist is a list of one tuple
            resist=cur.fetchall()
            #print "resist: ",resist
            real = resist[0][0]
            imag = resist[0][1]
            a=complex(real,imag)
            return a
            cur.close()
            conn.close()
            #resistance=get_impedance('1/4 X 2 CU')
            #resistance=get_impedance(dict_cond_type[2])
            #print "resistance=",resistance
            #print "type is: ",type(resistance)
      
        def build(self):
            """
            return dict_conductors that contains the impedance value for each section
            """
            n=1
            while n <= num_of_nodes+1:
                var1=self.get_impedance(self.dict_cond_type[n])
                var2=self.dict_cond_leng[n]/1000
                var3=var1*var2
                self.dict_conductors[n]=var3
                n = n+1
            return self.dict_conductors
            #print "dict_conductors: ", self.dict_conductors

    class LoadsClass():
        def __init__(self):
            self.dict_laterals={}
            self.dict_impedance_by_loads={}
            self.dict_combined_z_by_lat={}

        def collect_lats(self):
            """
            return a dictionary that contains the number of laterals by node
            """
            n = 1
            while n <= num_of_nodes:
                var = int(raw_input("the number of laterals in node"+str(n)+" : "))
                self.dict_laterals[n]=var
                n = n+1
                if n > num_of_nodes:
                    var = int(raw_input("the number of laterals in last load : "))
                    self.dict_laterals[n]=var
                    break
            #print(self.dict_laterals)
            return self.dict_laterals

        def collect_impedance_by_lat(self):
            """
            return a dictionary that contains the impedance by laterals in complex numbers
            """
            n = 1
            while n <= num_of_nodes:
                lats = self.dict_laterals[n]
                m = 1
                var = []
                while m <= lats:
                    #print "this is node",n,"lat",m
                    real=float(raw_input("real part of the impedance on load"+str(n)+"-lateral"+str(m)+": " ))
                    imaginary=float(raw_input("imaginary part of the impedance for load"+str(n)+"-lateral"+str(m)+": "))
                    var.append(complex(real,imaginary))
                    self.dict_impedance_by_loads[n] = var
                    m = m+1
                n = n+1
                if n > num_of_nodes:
                    lats = self.dict_laterals[n]
                    m =1
                    var = []
                    while m <= lats:
                        real=float(raw_input("real part of the impedance on load"+str(n)+"-lateral"+str(m)+" : " ))
                        imaginary=float(raw_input("imaginary part of the impedance for load"+str(n)+"-lateral"+str(m)+" : "))
                        var.append(complex(real,imaginary))
                        self.dict_impedance_by_loads[n] = var
                        m = m + 1

            #print self.dict_impedance_by_loads
            return self.dict_impedance_by_loads

        def calc_load(self):
            """
            return a dictionary that contains the load value by node, if multiple laterals, use parallel impedance formula
            """
            n = 1
            while n <= num_of_nodes+1:
                var1=self.dict_impedance_by_loads[n]
                if len(var1) == 1:
                    self.dict_combined_z_by_lat[n]=var1[0]
                    #print "node",n,self.dict_combined_z_by_lat
                else:
                    #print "this should be load",n,var1
                    times=functools.reduce(operator.mul, var1, 1)
                    adds=sum(var1)
                    div=times/adds
                    self.dict_combined_z_by_lat[n]=div
                n = n+1
            #print "dict_combined_z_by_lat: ", self.dict_combined_z_by_lat
            return self.dict_combined_z_by_lat
        

    objConductors=ConductorsClass()
    type=objConductors.collect_cond_type()
    leng=objConductors.collect_cond_leng()
    dict_conductors=objConductors.build()
    print "dict_conductors: ",dict_conductors

    objLoads=LoadsClass()
    lats=objLoads.collect_lats()
    lat_impedance=objLoads.collect_impedance_by_lat()
    dict_combined_z_by_lat=objLoads.calc_load()
    print "dict_combined_z_by_lat: ",dict_combined_z_by_lat


    class FeederClass():
        def __init__(self):
            self.v_nodes={}
            self.current_in = i_total
            self.vsource = v_source

        def volt_calc(self):
            #return dictionary with voltage at each node
            n=1
            while n<=num_of_nodes+1:
                #print "The following information corresponds to node: ",n
                conductor_n=dict_conductors[n]
                load_n=dict_combined_z_by_lat[n]
                volt_n=self.vsource-self.current_in*conductor_n
                self.v_nodes[n] = volt_n
                #print "current in: ", self.current_in
                current_out=self.current_in-volt_n/load_n
                #print "current out: ", self.current_out
                n=n+1
                self.current_in=current_out
                #print "Inode in after: ", self.current_in
                self.vsource=volt_n
                #print "vsource after: ",self.vsource

            return self.v_nodes

    objFd=FeederClass()
    dict_volts_pre = objFd.volt_calc()
    print "Voltage at all nodes before PV: ",dict_volts_pre

    class PvFeederClass():
        def __init__(self):
            self.vsource = v_source
            self.dict_pv_nodes = {}
            self.dict_v_nodes_pv = {}

        def collect_pv_generations(self):
            n = 1
            while n <= num_of_nodes+1:
                var = int(raw_input('amount of pv generations in watts in node'+str(n)+' : '))
                self.dict_pv_nodes[n] = var
                n = n + 1
            print self.dict_pv_nodes
            return self.dict_pv_nodes
                

        def calc(self):
            i_pv_total = 0
            for n in self.dict_pv_nodes.keys():
                i = self.dict_pv_nodes[n]/dict_volts_pre[n]
                #print "pv for node: ", n
                i_pv_total = i_pv_total +i
                #print "i_pv_total: ",i_pv_total


            #print "i_pv_total= ",i_pv_total
            self.current_in = i_total - i_pv_total
            n=1
            while n<=num_of_nodes+1:
              print "The following information corresponds to node: ", n
              conductor=dict_conductors[n]
              load=dict_combined_z_by_lat[n]
              print "the vsource is: ",self.vsource
              Vnode=self.vsource-self.current_in*conductor
              self.dict_v_nodes_pv[n] = Vnode
              print "Vnode: ",Vnode
              current_lat=Vnode/load - self.dict_pv_nodes[n]/dict_volts_pre[n]
              current_out=self.current_in - current_lat
              n=n+1
              self.current_in=current_out
              #print "Inode in after: ", self.current_in
              self.vsource=Vnode
              #print "vsource after: ",self.vsource

            return self.dict_v_nodes_pv

    objV=PvFeederClass()
    objV.collect_pv_generations()
    dict_pv_volts=objV.calc()
    print "the volts after PV are", dict_pv_volts

    for k in dict_pv_volts.keys():
        var = dict_pv_volts[k].real
        if var > ansi_nominal.real*1.05 or var < ansi_nominal.real*0.95:
            print "node",k,"is out of range",dict_pv_volts[k]

if __name__ == '__main__':
  main()
