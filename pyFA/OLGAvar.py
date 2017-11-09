import sys

class OLGAVariable(object):
    '''
    A class object to hold information on an OLGA variable. Has the following child classes:
        TPLVariable
        PPLVariable
    '''
    
    def __init__(self, olga_var):
        '''
        Initialises the object
        
        Inputs:
            olga_var(string): The OLGA variable i.e. PT, TM, QLST etc.
            
        Outputs:
            none
        '''
        
        self.olga_var = olga_var
    
    def _convert_units(self, from_unit, to_unit):
        '''
        '''
        
        pass

class TPLVariable(OLGAVariable):
    '''
    Child class of the OLGAVariable object. Holds information for trend variables
    '''
    
    def __init__(self, var_line):
        '''
        Initialises the object
        
        Inputs:
            var_line (list): A list containing information on the OLGA variable.
        
        Outputs:
            none
        '''
        olga_var = var_line[0]
        OLGAVariable.__init__(self, olga_var) # Initialise the parent class
        
        self.olga_var_data = {'VARIABLE': olga_var, 'NAME': '', 'TYPE': '', 'BRANCH': '', 'PIPE': '', 'NR': '', 'VALUES': []}
               
        self._parse_var(var_line)
        
    def _parse_var(self, var_line):
        '''
        Parses an OLGA variable
        
        Inputs:
            var_line (list): A list containing information on the OLGA Variable
            
        Outputs:
            none
        '''
        
        olga_var_type = var_line[1]
        
        if olga_var_type.find('GLOBAL') != -1:
            self.olga_var_data['TYPE'] = olga_var_type
        elif (olga_var_type.find('SECTION') != -1 or olga_var_type.find('BOUNDARY') != -1):
            branch_name = var_line[3]
            pipe_name = var_line[5]
            pipe_nr = var_line[7]
            self.olga_var_data['TYPE'] = olga_var_type
            self.olga_var_data['BRANCH'] = branch_name
            self.olga_var_data['PIPE'] = pipe_name
            self.olga_var_data['NR'] = pipe_nr
        elif olga_var_type.find('BRANCH') != -1:
            branch_name = var_line[2]
            self.olga_var_data['TYPE'] = olga_var_type
            self.olga_var_data['BRANCH'] = branch_name
        else:
            var_name = var_line[2]
            self.olga_var_data['TYPE'] = olga_var_type
            self.olga_var_data['NAME'] = var_name
            
    def _set_val(self, olga_values):
        '''
        Stores the variable data in the self.OLGA_values list
        
        Inputs:
            olga_values(list)
        Output:
            none
        '''
        
        self.olga_var_data['VALUES'] = olga_values
       
    def _get_val(self, parameter):
        '''
        Used to get OLGA variable data. Returns a copy of the self.OLGA_values list
        
        Inputs:
            parameter(string) = VARIABLE|NAME|TYPE|BRANCH|PIPE|NR|VALUES
        Outputs:
            A copy of the self.OLGA_values list
        '''
        
        return self.olga_var_data[parameter]
    
    def __str__(self):
        '''
        Returns information of the TPL variable
        
        Inputs:
            none
        Outputs:
            string
        '''
              
        return self.olga_var_data['VARIABLE']
              
class PPLVariable(OLGAVariable):
    '''
    Child class of the OLGAVariable object. Holds information for profile variables
    '''
    
    def __init__(self, olga_var):

        OLGAVariable.__init__(self, olga_var) # Initialise the parent class
        self.olga_var_name = '' # Name of the OLGA variable i.e. branch name
        self.olga_values = [] # Holds the OLGA variable data
        self.idx = -1 # Used to for time values

    def _set_name(self, olga_var_name):
        '''
        Sets the name of the OLGA variable i.e. the name of the branch
        
        Inputs:
            olga_var_name(string)
        Outputs:
            none
        '''
        
        self.olga_var_name = olga_var_name

    def _set_val(self, olga_values):
        '''
        Stores the variable data in the self.OLGA_values list
        
        Inputs:
            olga_values(list)
        Output:
            none
        '''
        self.idx = self.idx + 1      
        self.olga_values.insert(self.idx, olga_values)
        
    def _set_unit(self, olga_unit):
        '''
        '''
        
        pass
    
    def _set_desc(self, olga_desc):
        '''
        '''
        
        pass

    def _get_val(self, idx):
        '''
        Used to get OLGA variable data. Returns a copy of the self.OLGA_values list
        
        Inputs:
            idx(int): Index (corresponding to closest time value) at which to get the data
        Outputs:
            A copy of the self.OLGA_values list
        '''
        
        if idx > self.idx:
            idx = self.idx
        
        return self.olga_values[idx][:]
        
    def __str__(self):
        '''
        Returns information of the PPL variable
        
        Inputs:
            none
        Outputs:
            string
        '''
        
        return 'Trend Variable: ' + self.olga_var +  ':' + self.olga_var_name

