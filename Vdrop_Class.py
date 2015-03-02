import cmath
dict_testcond={1:complex(2.0,2.0),2:complex(3.0,2.0),3:complex(5.0,4.0),4:complex(6.0,4.0),5:complex(10.0,5.0)}
dict_testload={1:complex(50.0,5.0),2:complex(75.0,3),3:complex(20.0,1.0),4:complex(75.0,3.0),5:complex(50.0,5.0)}
current_in=complex(480,-160)
vsource=complex(8002,0)
dict_pv_nodes={1:500,2:0,3:0,4:200,5:0} #power in watts
class FeederClass():
  #to represeant a distribution FeederClass by sections, basic logic, voltage at substation is a constant, v0, total current is known by measurment, i0, impedance on section1, z1
  #load on node1,lateral1, l1 #vdorp on section1, vd1= i0*z1 #voltage at node1, vn1=v0-vd1 #current to load1, i1l=vn1/l1 #current to next node, i1n=i0-i1l

  def __init__(self, num_of_nodes=5,current_in=complex(480,-160),vsource=complex(8002,0)):
    self.v_nodes={}
    self.num_of_nodes = num_of_nodes
    self.current_in = current_in
    self.vsource = vsource
    self.v_nodes
  
  def volt_calc(self):
    '''
    return dictionary with voltage at each node
    '''
    n=1
    while n<=self.num_of_nodes:
      print "The following information corresponds to node: ",n
      Conductor_n=dict_testcond[n]
      Load_n=dict_testload[n]
      #print "Inode in: ",current_in
      #print "Conductor impedance: ", Conductor_n
      #print "Load impedance: ", Load_n
      #print "vsource: ",self.vsource
      #Vdrop=self.current_in*Conductor_n
      #print "Vdrop for section ",n,":", Vdrop
      Vnode=self.vsource-self.current_in*Conductor_n
      self.v_nodes[n] = Vnode
      print "Vnode: ",Vnode
      #Iload=Vnode/Load_n
      #print "Iload: ",Iload
      current_out=self.current_in-Vnode/Load_n
      #print "Inode out: ", current_out
      n=n+1
      self.current_in=current_out
      #print "Inode in after: ", self.current_in
      self.vsource=Vnode
      #print "vsource after: ",self.vsource
      

    return self.v_nodes

V=FeederClass()
dict_volts_pre = V.volt_calc()
print "Volatage at all nodes: ",dict_volts_pre