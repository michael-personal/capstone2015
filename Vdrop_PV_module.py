import cmath
dict_testcond={1:complex(2.0,2.0),2:complex(3.0,2.0),3:complex(5.0,4.0),4:complex(6.0,4.0),5:complex(10.0,5.0)}
dict_testload={1:complex(50.0,5.0),2:complex(75.0,3),3:complex(20.0,1.0),4:complex(75.0,3.0),5:complex(50.0,5.0)}
current_in=complex(480,-160)
vsource=complex(8002,0)
dict_pv_nodes={1:500,2:0,3:0,4:200,5:0} #power in watts
dict_volts_pre={1: (6722-640j), 2: (5409.493069306931-934.2693069306931j), 3: (3551.4769156148845-1447.3556574826812j), 4: (2782.1215982071626-1633.9202285201072j), 5: (2040.438033729386-1824.4836692164665j)}
num_of_nodes=5
v_nodes={}

class FeederPvClass():
  def __init__(self,current_in,vsource):
    self.current_in = current_in
    self.vsource=vsource
    
  def calc(self):
    '''
    input=dict_pv_nodes, output=imain after pv currents injection
    '''
    pv_total = 0
    for n in dict_pv_nodes.keys():
      i = dict_pv_nodes[n]/dict_volts_pre[n]
      pv_total = pv_total +1

    print "pv_total= ",pv_total

    self.current_in = self.current_in - pv_total

    n=1
    while n<=num_of_nodes:
      print "The following information corresponds to node: ", n
      conductor=dict_testcond[n]
      load=dict_testload[n]
      #print "Inode in: ",current_in
      #print "Conductor impedance: ", conductor
      #print "Load impedance: ", load
      #print "vsource: ",self.vsource
      #Vdrop=self.current_in*conductor
      #print "Vdrop for section ",n,":", Vdrop
      Vnode=self.vsource-self.current_in*conductor
      v_nodes[n] = Vnode
      print "Vnode: ",Vnode
      #Iload=Vnode/load
      #print "Iload: ",Iload
      current_lat=Vnode/load - dict_pv_nodes[n]/dict_volts_pre[n]
      current_out=current_in - current_lat
      #print "Inode out: ", current_out
      n=n+1
      self.current_in=current_out
      #print "Inode in after: ", self.current_in
      self.vsource=Vnode
      #print "vsource after: ",self.vsource
  

    return v_nodes

  def ansi(self):
    pass

V=FeederPvClass(current_in,vsource)
dict_pv_volts=V.calc()
print "the new volts are", dict_pv_volts