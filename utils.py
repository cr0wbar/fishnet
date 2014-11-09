from re import findall

def deformatSize(size):

    decoder = {'B':1,
            'KB':1024,
            'MB':1024*1024,
            'GB':1024*1024*1024,
            'kB':1024,
            'Bytes':1}
    
    bits = size.split(" ")
    
    if len(bits)!= 2:
        res = findall('([0-9]*\.?[0-9]+)([GKMTB]+)',size)[0]
        bits = res[0] if len(res) == 1 else None #Conversion failed :(
        
    if bits and len(bits)==2:
        for key in decoder:
            if key == bits[1]:
                return int(float(bits[0].replace(',',''))* decoder[key])#It will be more or less correct
    return -1