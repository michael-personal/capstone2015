#demonstrate db access, this function returns the conductor impedance in complex number
#the argument is the conductor type in string value

def main():
  import cmath
  import pypyodbc
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

  #resistance=get_resist('1/4 X 2 CU')
  #print "resistance=",resistance
  #print "type is: ",type(resistance)
if __name__ == '__main__':
  main()

