def RGBtoHSV(rgb):
    x = max(rgb)
    y = min(rgb)
    if x==y:
        z = 1
    else:
        z = x-y
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    if r>=g and r>=b: #se o vermelho é o máximo
        if g>=b:
            h = 60.0*(g-b)/z
        else:
            h = 360.0 + (60.0*(g-b)/z)
    elif g>=r and g>=b: # se verde é o máximo
        h = 120.0 + (60.0*(b-r)/z)
    else:
        h = 240.0 + (60.0*(r-g)/z)
    s = 1.0*z/x
    v = x/255.0
    hsv_lido = [h,s,v]
    return hsv_lido

def definir_rgbmax(snr):
    if snr=='esq':
        sensor=cor_esq
    else:
        sensor=cor_dir
    rgbmax = [sensor.red,sensor.green,sensor.blue]
    return rgbmax
