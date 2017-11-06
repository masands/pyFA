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

