import sys
from pyFA.OLGA import OLGAFile
from pyFA.OLGAvar import TPLVariable

class TPLFile(OLGAFile):
    '''
    A child class of the OLGAFile object. Handles an OLGA trend (.tpl) file
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
        self.var_dict ={} # Holds OLGA variable objects
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
            line = OLGAFile._get_line_at(self, self.catalog_line + i + 2)
            olga_var = line[0]
            olga_var_type = line[1]
            
            # Check for 'Global' variables without position, branch etc.
            if olga_var_type.find('GLOBAL') == -1:
                olga_var_name = line[2]
            else:
                olga_var_name = 'None'
                        
            # Get variable data series
            olga_values = []
            for j in range(len(self.input_file) - self.time_line - 1):
                line = OLGAFile._get_line_at(self, self.time_line + j + 1)
                olga_values.append(float(line[idx]))
            
            # Create and save variable data in new data instances
            oVar = TPLVariable(olga_var)
            oVar._set_type(olga_var_type)
            oVar._set_name(olga_var_name)
            oVar._set_val(olga_values[:])

            #Save variable object in a dictionary
            if olga_var not in self.var_dict:
                self.var_dict[olga_var] = {}
                self.var_dict[olga_var][olga_var_name] = oVar
            else:
                self.var_dict[olga_var][olga_var_name] = oVar
     
    def get_values(self, olga_var, olga_var_name):
        '''
        A getter method to retrieve variable data

        Inputs:
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The required OLGA object (position, branch etc.),\
            to get the data at. Use None for Global variables. 

        Outputs:
            Time Series Data (list): Returns the time data for the OLGA variable
            OLGA Variable Data (list): Returns the OLGA variable data

        Example Usage:
            time_series, OLGA_data = <TPLFile_object>.get_values("TM", "SPOOL-INLET")
            
        '''
        if olga_var_name == None:
            olga_var_name = 'None'
        else:
            olga_var_name = "'" + olga_var_name + "'"
        
        if olga_var in self.var_dict:
            if olga_var_name in self.var_dict[olga_var]:
                olga_values = self.var_dict[olga_var][olga_var_name]._get_val()
                return self.time_series[:], olga_values
            else:
                raise Exception("Position: " + olga_var_name + " not found in file")
        else:
            raise Exception("Trend Variable: " + olga_var + " not found in file")

    def get_names(self, olga_var):
        '''
        Used to get the names i.e. positions, branches etc. for a specified TPL variable
        
        Inputs:
            olga_var(string)
        
        Outputs:
            A list containing the names for the specified TPL variable
            
        Example usage:
            var_names = <TPLFile_object>.get_names('TM')
        '''
        var_names = []
        if olga_var in self.var_dict:
            for names in self.var_dict[olga_var]:
                var_names.append(names)
            return var_names
        else:
            raise Exception("Trend Variable: " + olga_var + " not found in file")
    
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
