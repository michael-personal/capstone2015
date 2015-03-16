"""
capstone_team_10
"""
#import sys
import numpy as np
import cmath
import math
import xlwt
import pypyodbc
class Node(object):
    '''Node represents a physical node of the feeder.
    attributes:
    Voltage - Voltage of node
    Connection - list of Load objects attached to the node
    loadsum - the addition of the inverse impedances of all Load objects
    attached
    name - the Node number
    equation - the mathmatical representation of Node derived from
    kirchoffs current law.'''

    def __init__(self, number):
        self.connections = list()
        self.loadsum = 0.0
        self.name = str(number)
        self.equation = list()
        self.voltage = 0

    def get_connections(self, load_list):
        '''module iterates through load_list and creates a list
        containing all Load objects connected to Node. A Load is considered
        connected to Node if either load.vin or load.vout is the Node
        '''
        self.connections = [item for item in load_list \
        if item.vin == self or item.vout == self]
        print "self.connections: ", self.connections

    def getloadsum(self):
        ''' module retreives the sum of the inverse imdedances connected to Node'''
        inversedata = [1.0/ item.impedance for item in self.connections]
        self.loadsum = sum(inversedata)
        print "self.loadsum", self.loadsum

    def get_equation(self, node_dict):
        '''Module accepts dictionary of all Nodes and sets the attribute
        ".equation" for the selected Node. '''
        equ_list = list()
        equ_list.append((self.name, self.loadsum))
        print "equ_listbegin: ", "node: ", self.name, equ_list
        for load in self.connections:
            if load.vout != node_dict[0]:
                if load.vin != self:
                    equ_list.append((load.vin.name, (-1.0 / load.impedance)))
                else:
                    equ_list.append((load.vout.name, (-1.0 / load.impedance)))
            else:
                pass
        print "equ_list_mid:", equ_list
        for i in range(len(node_dict)-2):
            self.equation.append(0)
        for i in equ_list:
            x , y = i
            if x != 'sub':
                self.equation[(int(x)-1)] = y
        print "end, self.equation:", self.equation

class Load(object):
    '''Object represents a physical load or impedance of the feeder
    Attributes:
    Voltage in - Node object on substation side of load
    Voltage out - Node object on the opposite side of sub station
    impedance - impedance of load
    current - current passing through the Load
    power - power consumed by load'''

    def __init__(self, impedance, vin, vout):
        '''vin and vout are Node objects, impedance is a complex number'''
        self.impedance = impedance
        self.vin = vin
        self.vout = vout
        self.current = complex
        self.power = complex 

    def get_info(self):
        '''Module assignes the .impedance and .power attributes'''
        self.current = (self.vin.voltage - self.vout.voltage) \
         / self.impedance
        self.power = (self.current**2) * (self.impedance)

def get_nodes(file):
    '''function reads a text file that describes the feeder to be
    evaluated. A Node Object is created for each node of the feeder'''
    node_dict = dict()
    feeder = open('/Users/mliu5715k/Downloads/'+file, 'r')
    for line in feeder:
        if 'Number of Nodes' in line:
            numberofnodes = int(line.split(':')[-1])
            for i in range(numberofnodes+1):
                node_dict[i] = Node(i)
        elif 'Substation Voltage' in line:
            node_dict['sub'] = Node('sub')
            node_dict['sub'].voltage = complex(line.split(':')[-1])
        elif 'Load to first Node' in line:
            impedance = line.split(':')[-1]
            node_dict['sub'].impedance = complex(impedance.split(',')[0])
        else:
            pass
    feeder.close()
    print "node_dict: ", node_dict
    return node_dict

def get_loads(file, node_dict):
    '''function reads feeder txt file and Node_dict and creates Load objects
    for each load of the feeder. For conductors, it gets impedance data from accdb'''
    x = list()
    feeder = open('/Users/mliu5715k/Downloads/'+file, 'r')
    for line in feeder:
        if 'Load:' in line:
            info = line.split(':')[-1]
            data = info.split(',')
            if len(data) == 3:
                x.append(Load(complex(data[0]), node_dict[int(data[1].strip())], node_dict[int(data[2].strip())]))
            elif len(data) ==4:
                col1 = 'PosSequenceresistance_PerLUL'
                col2 = 'PosSequenceReactance_PerLUL'
                tabl = 'DevConductors'
                conductor_name = str(data[0])
                print "conductorname: ", conductor_name
                pypyodbc.lowercase = False
                conn = pypyodbc.connect(
                r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                r"Dbq=C:\Users\mliu\conductors.accdb;")
                cur = conn.cursor()
                cur.execute ("SELECT %s, %s FROM %s WHERE ConductorName = %r" %(col1, col2, tabl, conductor_name))
                # impd is a list of one tuple
                impd=cur.fetchall()
                print "impd: ",impd
                real = impd[0][0]
                imag = impd[0][1]
                a=complex(real,imag)*float(data[1])
                print "a:", a
                x.append(Load(a,node_dict[int(data[2].strip())], node_dict[int(data[3].strip())]))
                print "x_4: ",x
                cur.close()
                conn.close()

            else:
                print "hey your feeder load data is incorrect, check number of fields"
        elif 'Load to first Node' in line:
            info = line.split(':')[-1]
            data = info.split(',')
            x.append(Load(complex(data[0]), node_dict[data[1]], node_dict[int(data[2].strip())]))
        else:
            pass
    feeder.close()
    print "x: ",x
    return x

    

def get_array(file, node_dict):
    '''function creates a 1 by X array where X is the number of Node
    objects. The numbers are determined by the Sub station voltage and
    the PV current added.'''
    x = list()
    for i in range(len(node_dict)-2): #creates an array of zeros
        x.append(0)
    x[0] = node_dict['sub'].voltage / node_dict['sub'].impedance
    feeder = open('/Users/mliu5715k/Downloads/'+file, 'r')
    for line in feeder: #replaces a zero with PV value if needed
        if 'PV on Node' in line:
            data = line.split(':')[-1]
            data = data.split(',')
            if data[0] == '1':
                x[0] = x[0] + complex(data[1])
            else:
                x[int(data[0])-1] = complex(data[1])
        else:
            pass
    feeder.close()
    return x

def build_equations(file, node_dict):
    '''function builds matrix array from each Node objects .equation attribute
    then returns an array of Node voltages'''
    equation_list = list()
    for i in range(len(node_dict)-2):
        equation_list.append(node_dict[i+1].equation)
    print "build_equations_equation_list", equation_list
    test = get_array(file, node_dict)
    a = np.array(equation_list)
    b = np.array(test)
    x = np.linalg.solve(a,b)
    return x

def get_voltage(node_dict, voltages):
    '''function converts array of voltages and assignes the .voltage attribute
    to each Node object'''
    x = voltages.tolist()
    for i in range((len(node_dict)-2)):
        node_dict[i+1].voltage = x[i]

def get_results(node_dict, load_list, file, excelname):
    '''Function writes results to excel spreadsheet'''
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'Node')
    sheet1.write(0, 1, 'Voltage')
    sheet1.write(0, 2, 'Angle')
    
    for i, node in enumerate(node_dict):
        sheet1.write(i+1, 0, node_dict[node].name)
        sheet1.write(i+1, 1, cmath.polar(node_dict[node].voltage)[0])
        sheet1.write(i+1, 2, math.degrees(cmath.polar(node_dict[node].voltage)[1]))

    feeder = open('/Users/mliu5715k/Downloads/'+file, 'r')
    for line in feeder:
        if 'Number of Nodes' in line:
            x = int(line.split(':')[-1]) + 5
        else:
            pass
    feeder.close()
    sheet1.write(x, 0, 'Load')
    sheet1.write(x, 1, 'Current')
    sheet1.write(x, 2, 'Angle')
    sheet1.write(x, 3, 'Power')
    sheet1.write(x, 4, 'Angle')
    for i, load in enumerate(load_list):
        load.get_info()
        sheet1.write(i+x+1, 0, load.vin.name+load.vout.name)
        sheet1.write(i+x+1, 1, cmath.polar(load.current)[0])
        sheet1.write(i+x+1, 2, math.degrees(cmath.polar(load.current)[1]))
        sheet1.write(i+x+1, 3, cmath.polar(load.power)[0])
        sheet1.write(i+x+1, 4, math.degrees(cmath.polar(load.power)[1]))

        
    book.save(excelname)

def main():
    file = raw_input('Please enter the file for the feeder: ')
    name = raw_input('please enter the name for the results file: ')
    excelname = name+'.xls'
    node_dict = get_nodes(file)
    print "node_dict_dictionary: ", node_dict
    load_list = get_loads(file, node_dict)
    print "load_list: ", load_list
    for k in node_dict:
        x = node_dict[k]
        print "node_dict[k]: ", x
        x.get_connections(load_list)
        x.getloadsum()
        x.get_equation(node_dict)
    voltages = build_equations(file, node_dict)
    get_voltage(node_dict, voltages)
    get_results(node_dict, load_list, file, excelname)

    return 0

if __name__ == '__main__':
    main()
