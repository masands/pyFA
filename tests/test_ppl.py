from pyFA.tpl import TPLFile

def main():
    olga_file = PPLFile("../tests/test_files/Sample")
    print(olga_file.get_values(3601, "PT", "PIPELINE"))
    
main()# -*- coding: utf-8 -*-

