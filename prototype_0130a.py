########summary#########
## Done: a function that reads resistence data from accdb DevConductors Table
## Done: a class that iterates all resistence and calcuates voltage drop
## next, write calc outputs to database
## next, compare each cal to ANSI standard and print ones that are out of range
## next, use realistic formulas, each variable needs to be real (from DB)
########revision########
## revision: 0130a, added arguments in function get_resist() 

def main():
  import cmath
  import pypyodbc
  
  def get_resist(colm, tabl):
    pypyodbc.lowercase = False
    conn = pypyodbc.connect(
	r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
	r"Dbq=C:\Users\mliu\conductors.accdb;")
    cur = conn.cursor()
    cur.execute ("SELECT %s FROM %s" %(colm, tabl))
    resistance_list=cur.fetchall()
    return resistance_list
    cur.close()
    conn.close()

  list_z=get_resist('PosSequenceResistance_PerLUL', 'DevConductors')


  class VoltageDrop:
    v_source = cmath.rect(120, 0.5)
    v_dest = complex
    current = cmath.rect(2.0, 0.5)
    impedance = cmath.rect(3.0, 0.5)
    def calcOnce(self, v_source, current, impedance):
      v_dest = v_source - current * impedance
      print v_dest
      return v_dest
      #print v_dest
    def calcAll(self, v_source, current, impedance):
      for d in list_z:
        v_dest = v_source - current * (impedance*d[0])
        print v_dest
        

  voltObj = VoltageDrop()
  calc1 = voltObj.calcOnce(cmath.rect(120, 0.5), cmath.rect(2.0, 0.5), cmath.rect(3.0, 0.5))
  calc_all = voltObj.calcAll(cmath.rect(120, 0.5), cmath.rect(2.0, 0.5), cmath.rect(3.0, 0.5))
  
  
if __name__ == '__main__':
  main()

