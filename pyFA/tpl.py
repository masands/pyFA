import sys
from pyFA.OLGA import OLGAFile
from pyFA.OLGAvar import TPLVariable

class TPLFile(OLGAFile):
    '''
    A child class of the OLGAFile object. Handles an OLGA trend (.tpl) files
    '''
    
    def __init__(self, file):
        '''
        Initialise the TPLFile object

        Inputs:    
            file (string): the input file name (including the directory if required), \
            Filename should be provided without any extensions
        
        Output:
            none 
        '''
        file = file + ".tpl"
        OLGAFile.__init__(self, file) # Initialise the parent class
        self.var_list = [] # Holds OLGA variable objects
        self.time_series = [] # Holds the time series
        self._parse_file()

    def _parse_file(self):
        '''
        A method that parses and stores the trend data in an OLGAVariable object 

        Inputs:
            none

        Outputs:
            none
        '''
        # Save the time series
        #time_series = [] # A temp. list to store the time series
        for i in range(len(self.input_file) - self.time_line - 1): # Loop from start of time series to EoF
            line = OLGAFile._get_line_at(self, self.time_line + i + 1)
            self.time_series.append(float(line[0]))
        
        # Get the total number of variables in file
        line = OLGAFile._get_line_at(self, self.catalog_line + 1)
        total_olga_vars = int(line[0]) 
        
       # Save the variable data
        for i in range(total_olga_vars): # Loop through the variable list
            idx = i + 1
            var_line = OLGAFile._get_line_at(self, self.catalog_line + i + 2)
            # Create a new TPL Variable
            oVar = TPLVariable(var_line)
            
            # Get variable data series
            olga_values = []
            for j in range(len(self.input_file) - self.time_line - 1):
                line = OLGAFile._get_line_at(self, self.time_line + j + 1)
                olga_values.append(float(line[idx]))
            
            # Save variable data
            oVar._set_val(olga_values[:])

            #Save variable object in a list
            self.var_list.append(oVar)
     
    def get_values(self, olga_var, olga_var_name = '', olga_var_type = '', olga_var_branch = '', olga_var_pipe = '', olga_var_pipe_nr = ''):
        '''
        A getter method to retrieve variable data

        Inputs:
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The name of the specified OLGA variable.
            olga_var_type(string|None): The type of OLGA variable (section, position, branch etc.),\
            to get the data at. Use None for Global variables.
            olga_var_branch(string|None): The branch at which to get the data at.
            olga_var_pipe(string|None): The pipe at which to get the data at.
            olga_var_pipe_nr(string|None): The pipe section number at which to get the data at.

        Outputs:
            Time Series Data (list): Returns the time data for the OLGA variable
            OLGA Variable Data (list): Returns the OLGA variable data

        Example Usage:
            time_series, OLGA_data = <TPLFile_object>.get_values("TM", "SPOOL-INLET")
            
        '''
        
        for oVar in self.var_list:
            temp_var = oVar._get_val('VARIABLE')
            temp_var_name = oVar._get_val('NAME')
            temp_var_type = oVar._get_val('TYPE')
            temp_var_branch = oVar._get_val('BRANCH')
            temp_var_pipe = oVar._get_val('PIPE')
            temp_var_pipe_nr = oVar._get_val('NR')
            
            if temp_var == olga_var and \
            temp_var_name.find(olga_var_name) != -1 and \
            temp_var_type.find(olga_var_type) != -1 and \
            temp_var_branch.find(olga_var_branch) != -1 and \
            temp_var_pipe.find(olga_var_pipe) != -1 and \
            temp_var_pipe_nr.find(olga_var_pipe_nr) != -1:
                
                return oVar._get_val('VALUES')[:]
            
        else:
            raise Exception('Specified variable not found in file!')
            
    def get_filter(self, olga_var):
        '''
        Used to get the names i.e. positions, branches etc. for a specified TPL variable
        
        Inputs:
            olga_var(string)
        
        Outputs:
            A list containing the names for the specified TPL variable
            
        Example usage:
            var_names = <TPLFile_object>.get_names('TM')
        '''
        
        for oVar in self.var_list:
            temp_var = oVar._get_val('VARIABLE')
            temp_var_name = oVar._get_val('NAME')
            temp_var_type = oVar._get_val('TYPE')
            temp_var_branch = oVar._get_val('BRANCH')
            temp_var_pipe = oVar._get_val('PIPE')
            temp_var_pipe_nr = oVar._get_val('NR')
            
            if temp_var == olga_var:
                print('Variable: ' + temp_var + ', Name: ' + temp_var_name \
                      + ', Variable Type: ' + temp_var_type + ', Branch: ' + \
                      temp_var_branch + ', Pipe: ' + temp_var_pipe + ', NR: ' + \
                      temp_var_pipe_nr)
    
    def get_ave(self, olga_var, olga_var_name, x = 5):
        '''
        Gets the value average of the last x% of points
        
        Inputs:
            x(int): gets value average of last x% of points, default = 5%
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The required OLGA object (position, branch etc.),\
            to get the data at. Use None for Global variables. 
        
        Outputs:
            olga_var_ave(float): Average value
        
        Example usage:
            olga_var_ave = <TPLFile_object>.get_ave('TM', 'SPOOL-INLET', 10)
        '''
        time_series, olga_values = self.get_values(olga_var, olga_var_name)
        
        list_length = int(len(olga_values) - len(olga_values) * (x / 100))
        olga_values_short = olga_values[list_length:]
        olga_var_ave = sum(olga_values_short) / len(olga_values_short)
               
        return olga_var_ave
    
    def get_max(self, olga_var, olga_var_name, x = 5):
        '''
        Gets the maximum value of the laast x% of points
        
        Inputs:
            x(int): gets max of the last x% of points, default = 5%
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The required OLGA object (position, branch etc.),\
            to get the data at. Use None for Global variables. 
        
        Outputs:
            max_time(float): Time at which the maximum value occurs
            olga_var_max(float): Maximum value
        '''
        time_series, olga_values = self.get_values(olga_var, olga_var_name)
        
        list_length = int(len(olga_values) - len(olga_values) * (x / 100))
        olga_values_short = olga_values[list_length:]
        olga_var_max = max(olga_values_short)
        idx = olga_values.index(olga_var_max)
        max_time = time_series[idx]
        
        return max_time, olga_var_max
    
    def get_min(self, olga_var, olga_var_name, x = 5):
        '''
        Gets the minimum value of the laast x% of points
        
        Inputs:
            x(int): gets min of the last x% of points, default = 5%
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The required OLGA object (position, branch etc.),\
            to get the data at. Use None for Global variables. 
        
        Outputs:
            min_time(float): Time at which the minimum value occurs
            olga_var_min(float): Minimum value
        '''
        time_series, olga_values = self.get_values(olga_var, olga_var_name)
        
        list_length = int(len(olga_values) - len(olga_values) * (x / 100))
        olga_values_short = olga_values[list_length:]
        olga_var_min = min(olga_values_short)
        idx = olga_values.index(olga_var_min)
        min_time = time_series[idx]
        
        return min_time, olga_var_min
