def parse_ftin2in(str):
    # str =input("enter ft in")
    feet, inches = str.split(' ') 
    return int(feet), float(inches)

def conv_ftin2in(str):
    #str =input("enter ft in")
    ftin = parse_ftin2in(str)
    inch = (ftin[0]*12 + ftin[1])
    print("%d'- %3.2f\" = %3.2f\"" % (ftin[0], ftin[1], inch ))

def conv_ftin2m(str):
    #str =input("enter ft in")
    ftin = parse_ftin2in(str)
    m = (ftin[0]*12 + ftin[1])*.0254
    print("%d'- %3.2f\" = %3.4f meters^2" % (ftin[0], ftin[1], m ))
    # return "{:.4f}".format((ftin[0]*12 + ftin[1])*.0254)


def conv_sf2sm(sf):
    #sf =input("enter sf")
    f=0.092903
    print("{:.4f}".format(f*float(sf)))

def conv_sm2sf(sm):
    #sf =input("enter sf")
    f=10.7639
    print("{:.4f}".format(f*float(sm)))

def conv_cuf2cum(cuf):
    #sf =input("enter sf")
    f=0.0283168
    print("{:.4f} cu ft".format(f*float(cf)))

def conv_cum2cuf(cum):
    #sf =input("enter sf")
    f=35.3147
    print("dosc are:{:.4f}".format(f*float(cm)))    

def conv_c2f(c):
    f = (c*9/5)+32
    print("%3.1f celsius = %3.1f farenheit" % (c,f))

def conv_f2c(f):    
    c = (f-32)*5/9
    print("%3.1f farenheit = %3.1f celsius" % (f,c))