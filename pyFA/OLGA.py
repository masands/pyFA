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