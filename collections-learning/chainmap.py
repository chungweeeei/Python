from collections import ChainMap

if __name__ == "__main__":
    
    baseline = {"music": "bach", "art": "rembrandt"}
    adjustments = {"art": "van gogh", "opera": "carmen"}
    
    c = ChainMap(adjustments, baseline)
    
    print(c["art"])