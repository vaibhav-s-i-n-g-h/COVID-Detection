import sys 
from test import  concatenate

if __name__ == "__main__":
    
    print (concatenate(sys.argv[1],sys.argv[2]))
    print(concatenate(sys.argv[2],sys.argv[1]))