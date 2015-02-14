def main():
  #uses three dictionaries to collect and store data from users
  #dict_conductors will have conductor type and length for each section
  #dict_laterals will have number of lateral per node
  #dict_measures will have the current measurement from the section it's taken

    import pprintpp
    class AutoVivification(dict):
      #Implementation of perl's autovivification feature
        def __getitem__(self, item):
            try:
                return dict.__getitem__(self, item)
            except KeyError:
                value = self[item] = type(self)()
                return value

    dict_conductors = AutoVivification()
    dict_laterals = AutoVivification()
    dict_measures = AutoVivification()

    numberOfNodes = int(raw_input("number of nodes = "))
  #collect conductor info per section
    n=1
    while n < numberOfNodes:
       sec='sec'+str(n)
       key1='con_type'
       key2='con_length'
       var1=str(raw_input("the conductor_type of section"+str(n)+"="))
       var2=str(raw_input("the conductor_length of section"+str(n)+"="))
       #print sec,var1,var2
       dict_conductors[sec][key1]=var1
       dict_conductors[sec][key2]=var2
       n=n+1
    pprintpp.pprint(dict_conductors)
    #print dict_conductors['sec1']['con_length']
  #collect number of lateras per node
    n=1
    while n <= numberOfNodes:
       node='node'+str(n)
       key1='numberOfLaterals'
       var1=str(raw_input("the number of lateral in node"+str(n)+"="))
       #print sec,var1,var2
       dict_laterals[node][key1]=var1
       n=n+1
    pprintpp.pprint(dict_laterals)
    #print dict_conductors['sec1']['numberOfLaterals']

    theSection = int(raw_input("enter the measurement section number only e.g. 3"))
    sec='sec'+str(theSection)
    key1='measured_current'
    var1=float(raw_input("the measured current from meter="))
    dict_measures[sec][key1]=var1
    pprintpp.pprint(dict_measures)

    

if __name__ == '__main__':
    main()
    