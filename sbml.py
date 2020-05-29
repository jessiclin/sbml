import Parser as parser 
import sys 

def main():
    if (len(sys.argv) != 2) :
        print("Incorrect Input")      
    try: 
        # Read in text file 
        f = open(sys.argv[1],"r+")
        contents = f.read()
        parser.parseAll(contents)
        f.close()
    except Exception as e: 
        print(e)
            
if __name__ == "__main__":
    main()
