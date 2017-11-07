from pyFA.tpl import TPLFile

def main():
    olga_file = TPLFile('test_files\Sample')
    print(olga_file.get_names('PT'))
    #print(olga_file.get_min("PT", "PIPELINE"))
    
    
main()
