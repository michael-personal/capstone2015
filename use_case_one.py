def main():

  import cmath
  import pypyodbc
  #dict_cond_type={1: '1 AAC', 2: '1 ACSR', 3: '1 AL-CN UG', 4 : '1 AAC', 5: '1 AAC'}
  test = str(raw_input("use sample feeder? enter yes or no: "))
  if test == 'yes':
    dict_cond_type = {1: '1 AAC', 2: '1ACSR', 3: '1 AL-CN UG'}
    dict_cond_leng = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500} 
    dict_cond={1:complex(2.0,2.0),2:complex(3.0,2.0),3:complex(5.0,4.0),4:complex(6.0,4.0),5:complex(10.0,5.0)}
    #dict_load={1:complex(50.0,5.0),2:complex(75.0,3),3:complex(20.0,1.0),4:complex(75.0,3.0),5:complex(50.0,5.0)}
    dict_loads_by_lat = {1: [(50+5j)],2: [(75+3j)],3: [(30+1j), (60+2j)],4: [(75+3j)],5: [(50+5j)]}
    dict_lat = {1:1, 2:1, 3: 2, 4: 1, 5:1}
    Imain_in=complex(480,-160)
    Vsource=complex(8002,0)

  else:
    dict_cond_type = {} #conductor type by node
    dict_cond_leng = {} #conductor length by section
    dict_cond ={} #conductor impedance by section
    dict_lat = {} #number of laterals by node
    dict_load = {} #load impedance by nodes/loads
    dict_measure = {} #measurments by node
    dict_loads_by_lat = {} #impedance by laterals, node1-lat1, node1-lat2, etc

    #a node is where current splits to loads at laterals and continue down the feeder
    numberOfNodes = int(raw_input("number of nodes = "))
    #collect conductor type per section
    n = 1
    while n <= numberOfNodes+1:
      var=str(raw_input("the conductor_type of section"+str(n)+"="))
      dict_cond_type[n]=var
      n = n+1
    print "dict_cond_type: ",dict_cond_type
    
    #collect conductor lenghth per section
    n = 1
    while n <= numberOfNodes+1:
      var=float(raw_input("the conductor lenghth of section"+str(n)+"="))
      dict_cond_leng[n]=var
      n = n+1
    print "dict_cond_leng: ",dict_cond_leng

    def get_impedance(conductor_name):
    col1 = 'PosSequenceResistance_PerLUL'
    col2 = 'PosSequenceReactance_PerLUL'
    tabl = 'DevConductors'
    col_id = 'ConductorName'
    pypyodbc.lowercase = False
    conn = pypyodbc.connect(
  r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
  r"Dbq=C:\Users\mliu\conductors.accdb;")
    cur = conn.cursor()
    cur.execute ("SELECT %s, %s FROM %s WHERE %s = %r" %(col1, col2, tabl, col_id, conductor_name))
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
  resistance=get_impedance(dict_cond_type[2])
  print "resistance=",resistance
  print "type is: ",type(resistance)

    #build dict_cond from dict_cond_type and dict_cond_length
    n=1
    while n <= numberOfNodes+1:
      var1=get_impedance(dict_cond_type[n])
      var2=dict_cond_leng[n]
      var3=var1*var2
      dict_cond[n]=var3
      n = n+1
    print dict_cond

    #collect number of laterals per node into dict_lat{}
    n = 1
    while n <= numberOfNodes+1:
      var = int(raw_input("the number of laterals in node"+str(n)+"= "))
      dict_lat[n]=var
      n = n+1
    #print(dict_lat)
    
    #collect load info per node
    n = 1
    while n <= numberOfNodes+1:
      lats = dict_lat[n]
      m = 1
      var = []
      while m <= lats:
        real=float(raw_input("real part of the impedance on node"+str(n)+"lateral"+str(m)+": " ))
        imagin=float(raw_input("imagin part of the impedance for node"+str(n)+"lateral"+str(m)+": "))
        var.append(complex(real,imagin))
        dict_loads_by_lat[n] = var
        m = m+1
      n = n+1
    print(dict_loads_by_lat)

  def calc_load(dict_loads_by_lat):
    #return dict_load_by_node

    return dict_load

  def db_lookup(dict_cond_type):
    #input=conductor type, return= dict_impedance_by_conductor type
    dict_imped = {}
    return dict_imped



  def calc_conductors(dict_imped,dict_cond_leng):
    #input = the two dictionaries, return = conduction impedance dict by section
    return dict_cond



  
  class Feeder():
    #to represeant a distribution Feeder by sections
    #basic logic, voltage at substation is a constant, v0
    #total current is known by measurment, i0
    #impedance on section1, z1
    #load on node1,lateral1, l1
    #vdorp on section1, vd1= i0*z1
    #voltage at node1, vn1=v0-vd1
    #current to load1, i1l=vn1/l1
    #current to next node, i1n=i0-i1l
    
    def node_voltage(self,node,Imain_in=complex(480,-160),Vsource=complex(8002,0)):
      self.node=node
      n=1
      while n<=self.node:
        print "The following information corresponds to node: ",n
        Conductor_n=dict_cond[n]
        Load_n=dict_load[n]
        print "Inode in: ",Imain_in
        print "Conductor impedance: ", Conductor_n
        print "Load impedance: ", Load_n
        print "Vsource: ",Vsource
        Vdrop=Imain_in*Conductor_n
        print "Vdrop for section ",n,":", Vdrop
        Vnode=Vsource-Vdrop
        print "Vnode: ",Vnode
        Iload=Vnode/Load_n
        print "Iload: ",Iload
        Imain_out=Imain_in-Iload
        print "Inode out: ", Imain_out
        n=n+1
        Imain_in=Imain_out
        print "Inode in after: ", Imain_in
        Vsource=Vnode
        print "Vsource after: ",Vsource
        
  
      return Vnode 
  
  
  testobj=Feeder()
  
  voltageobj = testobj.node_voltage(5)
  print "Volatage at last node: ",voltageobj

if __name__ == '__main__':
  main()
