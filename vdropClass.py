import cmath
dict_testcond={1:complex(2.0,2.0),2:complex(3.0,2.0),3:complex(5.0,4.0),4:complex(6.0,4.0),5:complex(10.0,5.0)}
dict_testload={1:complex(50.0,5.0),2:complex(75.0,3),3:complex(20.0,1.0),4:complex(75.0,3.0),5:complex(50.0,5.0)}
Imain_in=complex(480,-160)
Vsource=complex(8002,0)

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
    Conductor_n=dict_testcond[n]
    Load_n=dict_testload[n]
    while n<=self.node:
      print "Imainin: ",Imain_in
      print "Conductor: ", Conductor_n
      print "Load: ", Load_n
      print "Vsource: ",Vsource
      Vdrop=Imain_in*Conductor_n
      Vnode=Vsource-Vdrop
      print "Vnode: ",Vnode
      Iload=Vnode/Load_n
      Imain_out=Imain_in-Iload
      print "Imain_out: ", Imain_out
      n=n+1
      Imain_in=Imain_out
      print "Imain_in after: ", Imain_in
      Vsource=Vnode
      print "Vsource after: ",Vsource
      print "Imain_in: ",Imain_in


    return Vnode 





testobj=Feeder()

voltageobj = testobj.node_voltage(5)
print "volatage at node 5: ",voltageobj
    
     



