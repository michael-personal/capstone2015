########summary#########
## Done: a function that reads resistence data from accdb DevConductors Table
## Done: a class that calcuates simple voltage drop use resistance from db
## next, write calc outputs to database
## next, compare each cal to ANSI standard and print ones that are out of range
## next, use realistic formulas, each variable needs to be real (from DB)
########revision########
## revision: 0130a, added arguments in function get_resist()
## revision: 0131a, update get_resist() to take conductor name as argument
## do a v drop function with paramers: v-source, impedance * distance, current as arguments
## for get_resist, add a argument to reprsent the conductor type, so can target 
## current will be a function that takes into consideration of PV generation
##assume v at substatio is infinite bus a constant number
def main():
  import cmath
  import pypyodbc

#collect inputs from user
  numberOfNodes = int(raw_input("number of nodes = "))
  section = int(raw_input("the section number ="))
#collect laterals for every section
  laterals={}
  for n in range(1,numberOfNodes):
    lat=int(raw_input("numerOfLaterals in section"+str(n)+'='))
    laterals['sec'+str(n)]=lat
#test collected variables
  print "laterals:", laterals
  print "number of nodes:", numberOfNodes
  print "this section is:", section
                      
  
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
    cur.execute ("SELECT %s, %s FROM %s WHERE ConductorName = %r" %(col1, col2, tabl, conductor_name)) 
    resist=cur.fetchall()
    #print resist
    #print resist[0]
    real = resist[0][0]
    imag = resist[0][1]
    a=complex(real,imag)
    print "the reistance is", a
    return a
    print type(a)
    cur.close()
    conn.close()

  resistance=get_resist('1/4 X 2 CU')
  #print "resistance=",resistance


  class VoltageDrop:
    v_source = cmath.rect(120, 0.5)
    v_dest = complex
    current = cmath.rect(2.0, 0.5)
    impedance = cmath.rect(3.0, 0.5)
    def calcOnce(self, v_source, current):
      v_dest = v_source - current * resistance
      print "v_dest=",v_dest
      #return v_dest
  
    def calcAll(self, v_source, current):
      v_dest = v_source - current * resistance
      print v_dest
      return v_dest
        

  voltObj = VoltageDrop()
  calc1 = voltObj.calcOnce(cmath.rect(120, 0.5), cmath.rect(2.0, 0.5))
  
if __name__ == '__main__':
  main()

