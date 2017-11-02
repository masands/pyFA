import sys

class OLGAFile(object):
    '''
    A class object to read and process an OLGA v7 or higher trend (.tpl) or profile (.ppl) data files
    Has the following child classes:
        TPLFile
        PPLFile
    '''
    
    def __init__(self, file):
        '''
        Initialises the OLGAFile object
        
        Inputs:    
            file (string): the input file name (including the directory if required), \ 
            plus extension (.tpl or .ppl)
        
        Output:
            none
        '''
        self.file = file
        self.input_file = []
        self.total_lines = -1
        self.current_line = -1
        self.catalog_line = -1
        self.time_line = -1
        self._read_file()

    def _read_file(self):
        '''
        Reads the file into a list for further processing
        
        Inputs:
            none
            
        Outputs:
            none
        '''
        try:
            file = open(self.file, 'r')
            for line in file:
                self.total_lines += 1
                line = line.split()
                self.input_file.append(line) 
                if line[0].find('CATALOG') != -1:
                    self.catalog_line = self.total_lines
                elif line[0].find('TIME') != -1:
                    self.time_line = self.total_lines
        except Exception as e:
             print(str(e))
             sys.exit(0)
        else:
             file.close()
    
    def _get_next_line(self):
        '''
        Gets the next item from the self.input_file list based on the current, \
        value of the self.current_line
        
        Inputs:
            none
            
        Outputs:
            A list at the current line (or None type if, \
            current line is outside the scope of the file)
        '''
        self.current_line += 1
        
        if self.current_line <= self.total_lines:
            return self.input_file[self.current_line]
        else:
            return None
    
    def _get_line_at(self, line_number):
        '''
        Gets the value of the item at the specified line_number
        
        Inputs:
            line_number (integer): the line number from which to get the required values
            
        Outputs:
            A list at the specified line (or None type if the specified, \
            line is outside the scope of the file)
        '''
        if line_number <= self.total_lines:
            return self.input_file[line_number]
        else:
            return None
    
    def _reset(self):
        '''
        Resets the self.current_line variable to -1
        
        Inputs:
            none
        Outputs:
            none
        '''
        self.current_line = -1
    
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
            self.time_series.append(line[0])
        
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
                olga_values.append(line[idx])
            
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
        
        Outputs:
            float: average
        
        Example usage:
            olga_var_ave = <TPLFile_object>.get_ave('TM', 'SPOOL-INLET', 10)
        '''
        pass
    
    def get_max(self, olga_var, olga_var_name, x = 5):
        '''
        '''
        pass
    
    def get_min(self, olga_var, olga_var_name, x = 5):
        '''
        '''
        pass
    
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
    def __init__(self, olga_var):
        '''
        Initialises the object
        
        Inputs:
            olga_var(string): The OLGA variable i.e. PT, TM, QLST etc.
        
        Outputs:
            none
        '''
        OLGAVariable.__init__(self, olga_var) # Initialise the parent class
        self.olga_var_type = '' # Type of variable i.e. Position or Branch
        self.olga_var_name = ''# Name of the OLGA variable i.e. position or branch name
        self.olga_values = [] # Holds the OLGA variable data
    
    def _set_type(self, olga_var_type):
        '''
        Sets type of OLGA variable i.e. Position or Branch
        
        Inputs:
            olga_var_type(string)
        
        Outputs:
            none
        '''
        self.olga_var_type = olga_var_type

    def _set_name(self, olga_var_name):
        '''
        Sets the name of the OLGA variable i.e. the name of the position or branch
        
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
        self.olga_values = olga_values
    
    def _set_unit(self, olga_unit):
        '''
        '''
        pass
    
    def _set_desc(self, olga_desc):
        '''
        '''
        pass
    
    def _get_val(self):
        '''
        Used to get OLGA variable data. Returns a copy of the self.OLGA_values list
        
        Inputs:
            none
        Outputs:
            A copy of the self.OLGA_values list
        '''
        return self.olga_values[:]
    
    def __str__(self):
        '''
        Returns information of the TPL variable
        
        Inputs:
            none
        Outputs:
            string
        '''
        return 'Trend Variable: ' + self.olga_var +  ':' + self.olga_var_type + ':' + self.olga_var_name
          
