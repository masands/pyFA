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
                line = OLGAFile._get_line_at(self, self.time_line + i + 1)
                self.time_series.append(float(line[0]))
        
                olga_values = []
                olga_values = OLGAFile._get_line_at(self, self.time_line + i + j + 2)
                oVar._set_val(olga_values[:])
                
        
def main():
    olga_file = PPLFile("../tests/test_files/Sample")
    print(olga_file.var_dict['Q2']["'PIPELINE'"]._get_val(0))
    
main()