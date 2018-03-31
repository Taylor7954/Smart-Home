import goslate

def main():
    with open("insertHere", 'r') as f:
        xml_to_trans = f.read()
    gs = goslate.Goslate()
    gs.translate(xml_to_trans)

    if __name__ == '__main__': 
        main()

    ##This code needs to have goslate installed in order to work
    ##To install use cmd pip install goslate