import sys
from pyFA.OLGA import OLGAFile
from pyFA.OLGAvar import PPLVariable

class PPLFile(OLGAFile):
    '''
    A child class of the OLGAFile object. Handles an OLGA profile (.ppl) files
    '''
    
    def __init__(self, file):
        '''
        Initialise the PPLFile object

        Inputs:    
            file (string): the input file name (including the directory if required), \
            Filename should be provided without any extensions
        
        Output:
            none 
        '''
        file = file + ".ppl"
        OLGAFile.__init__(self, file) # Initialise the parent class
        self.var_dict ={} # Holds OLGA variable objects
        self.time_series = [] # Holds the time series
        self._parse_file()
    
    def _parse_file(self):
        '''
        A method that parses and stores the profile data in an OLGAVariable object 

        Inputs:
            none

        Outputs:
            none
        '''
        
        # Get the total number of variables in file
        total_olga_vars = int(OLGAFile._get_line_at(self, self.catalog_line + 1)[0])       
        
        #Save the time series
        for i in range(0, len(self.input_file) - self.time_line - 1, total_olga_vars + 1): # Loop from start of time series to EoF
                line = OLGAFile._get_line_at(self, self.time_line + i + 1)
                self.time_series.append(float(line[0]))
        
        # Save the variable data
        for j in range(total_olga_vars): # Loop through the variable list
            line = OLGAFile._get_line_at(self, self.catalog_line + j + 2)
            olga_var = line[0]
            olga_var_name = line[3]
            
            # Create and save variable data in new data instances
            oVar = PPLVariable(olga_var)
            oVar._set_name(olga_var_name)
            
            #Save variable object in a dictionary
            if olga_var not in self.var_dict:
                self.var_dict[olga_var] = {}
                self.var_dict[olga_var][olga_var_name] = oVar
            else:
                self.var_dict[olga_var][olga_var_name] = oVar
            
            # store the time series
            for i in range(0, len(self.input_file) - self.time_line - 1, total_olga_vars + 1): # Loop from start of time series to EoF
                olga_values = []
                olga_values = OLGAFile._get_line_at(self, self.time_line + i + j + 2)
                oVar._set_val(olga_values[:])
                
    def get_values(self, time, olga_var, olga_var_name):
        '''
        A getter method to retrieve variable data

        Inputs:
            time(float): Time at which to get the variable data
            olga_var(string): The required OLGA variable to get the data from
            olga_var_name(string|None): The required OLGA object (branch),\
            to get the data at.  

        Outputs:
            Time (float): Returns the time at which the data was extracted
            OLGA Variable Data (list): Returns the OLGA variable data

        Example Usage:
            time, OLGA_data = <PPLFile_object>.get_values(3600, "TM", "SPOOL-INLET")
            
        '''
        
        olga_var_name = "'" + olga_var_name + "'"
        
        if olga_var in self.var_dict:
            if olga_var_name in self.var_dict[olga_var]:
                idx = self._bin_search(time)
                olga_values = self.var_dict[olga_var][olga_var_name]._get_val(idx)
                return self.time_series[idx], olga_values
            else:
                raise Exception("Branch: " + olga_var_name + " not found in file")
        else:
            raise Exception("Profile Variable: " + olga_var + " not found in file")    
        

    def _bin_search(self, time):
        '''
        '''
        high = len(self.time_series) - 1
        low = 0
        mid = int((high + low) / 2)

        if time > self.time_series[high]:
            return high
        elif time < self.time_series[low]:
            return low
        
        while True:

            if ((mid == high) or (mid == low)):
                return mid
            elif self.time_series[mid] == time:
                return mid
            elif time < self.time_series[mid]:
                high = mid
                low = low
                mid = int((high + low) / 2)
            elif time > self.time_series[mid]:
                low = mid
                high = high
                mid = int((high + low) / 2)                    
    
    def get_names(self, olga_var):
        '''
        '''
        pass
        