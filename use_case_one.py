def main():

  import cmath
  import pprintpp
  import pypyodbc
  test = str(raw_input("use sample feeder? enter yes or no: "))
  class AutoVivification(dict):
    #Implementation of Perl's autovivification feature
    def __getitem__(self, item):
      try:
        return dict.__getitem__(self, item)
      except KeyError:
        value = self[item] = type(self)()
        return value

  def get_resist(conductor_name):
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

  if test == 'yes':
    dict_cond_type={}
    dict_cond={1:complex(2.0,2.0),2:complex(3.0,2.0),3:complex(5.0,4.0),4:complex(6.0,4.0),5:complex(10.0,5.0)}
    #dict_load={1:complex(50.0,5.0),2:complex(75.0,3),3:complex(20.0,1.0),4:complex(75.0,3.0),5:complex(50.0,5.0)}
    dict_load = {1: [(50+5j)],2: [(75+3j)],3: [(30+1j), (60+2j)],4: [(75+3j)],5: [(50+5j)]}
    Imain_in=complex(480,-160)
    Vsource=complex(8002,0)

  else:
    dict_cond_type = {}
    dict_cond_leng = {}
    dict_lat = {}
    dict_load = {}
    dict_measure = {}
    dict_load_lat = {}
    dict_cond ={}

    #a node is where current splits to loads at laterals and continue down the feeder
    numberOfNodes = int(raw_input("number of nodes = "))
    #collect conductor type per section
    n = 1
    while n <= numberOfNodes+1:
      var=str(raw_input("the conductor_type of section"+str(n)+"="))
      dict_cond_type[n]=var
      n = n+1
    #test content of dict_cond_type
    pprintpp.pprint(dict_cond_type)
    #collect conductor lenghth per section
    n = 1
    while n <= numberOfNodes+1:
      var=float(raw_input("the conductor lenghth of section"+str(n)+"="))
      dict_cond_leng[n]=var
      n = n+1
    pprintpp.pprint(dict_cond_leng)
    #collect number of laterals per node
    n = 1
    while n <= numberOfNodes+1:
      var = int(raw_input("the number of laterals in node"+str(n)+"= "))
      dict_lat[n]=var
      n = n+1
    #test content of dict_lat
    pprintpp.pprint(dict_lat)
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
        dict_load_lat[n] = var
        m = m+1
      n = n+1
    pprintpp.pprint(dict_load_lat)

  def calc_load(dict_load_lat):
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
