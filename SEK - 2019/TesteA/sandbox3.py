mapadecores = []

if True:
    global mapa de cores
    mapadecores = [line.rstrip('\n') for line in open("cores.txt")] # pra ler o arquivo pra lista de novo

if mapadecores[0] == 'amarelo':
    sound.beep()