from pyFA.tpl import TPLFile

def main():
    olga_file = TPLFile('test_files\Sample')
    print(olga_file.get_max('TM', 'CIMBWI-2-DS-CHOKE'))
    
    
main()
