import pypyodbc
number=int(raw_input('enter number of nodes in the feeder: '))

class Conductors():
  def __init__(self):
      self.dict_cond_type={}
      self.dict_cond_leng={}
      self.dict_cond={}

  def collect_cond_type(self, number_of_nodes=None):
      """
      return a dictionary that contains the string value of the conductor type
      e.g. '1 AAC', '1 ACSR'
      """
      n = 1
      while n <= number_of_nodes+1:
          var=str(raw_input("the conductor_type of section"+str(n)+"="))
          self.dict_cond_type[n]=var
          n = n+1
      print "dict_cond_type: ", self.dict_cond_type
      return self.dict_cond_type

    #collect conductor lenghth per section
  def collect_cond_leng(self, number_of_nodes):
      """
      return a dictionary that contains the length of each section
      unit is feet
      """
      n = 1
      while n <= number_of_nodes+1:
          var=float(raw_input("the conductor length of section"+str(n)+"="))
          self.dict_cond_leng[n]=var
          n = n+1
      print "dict_cond_leng: ", self.dict_cond_leng
      return self.dict_cond_leng

  def get_impedance(self, conductor_name):
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
      cur.execute ("SELECT %s, %s FROM %s WHERE %s = %r" %(col1, col2, tabl, col_id, conductor_name))
      # resist is a list of one tuple
      resist=cur.fetchall()
      print "resist: ",resist
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

  def build(self, number_of_nodes):
      """
      return dict_cond that contains the impedance value for each section
      """
      n=1
      while n <= number_of_nodes+1:
          var1=self.get_impedance(self.dict_cond_type[n])
          var2=self.dict_cond_leng[n]/1000
          var3=var1*var2
          self.dict_cond[n]=var3
          n = n+1
      return self.dict_cond
      print "dict_cond: ", self.dict_cond

conductors=Conductors()
type=conductors.collect_cond_type(number)
leng=conductors.collect_cond_leng(number)
dict_cond=conductors.build(number)
print dict_cond

