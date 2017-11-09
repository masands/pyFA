from pyFA.tpl import TPLFile

def main():
    olga_file = TPLFile('test_files\Sample')
    #print(olga_file.var_list[5].olga_var_data)
   # print(olga_file.get_min("PT", "PIPELINE"))
#    print(olga_file.get_values(olga_var = 'PT', olga_var_type = 'SECTION', olga_var_branch = 'PIPELINE', olga_var_pipe = 'PIPE-1', olga_var_pipe_nr = '1'))
    #print(olga_file.get_values(olga_var = 'VOLGBL', olga_var_type = 'GLOBAL'))

    
main()
