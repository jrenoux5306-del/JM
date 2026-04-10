# JM détection de choses :

from time import time
import matplotlib.pyplot as plt
import numpy as np

plante1=plt.imread("plante1.jpg")
plante2=plt.imread("plante2.jpg")
plante3=plt.imread("plante3.jpg")
plante4=plt.imread("plante4.jpg")
plante5=plt.imread("plante5.jpg")

niv1=2
niv2=5
niv3=8
niv4=11

def luminance(L):
    R,G,B=L
    return R*299/1000 + G*587/1000+B*114/1000

def niveaugris(I):  # luminance de chaque pixel de l'image I
    N,M=len(I),len(I[0])
    return [ [ luminance(I[i][j]) for j in range(M) ] for i in range(N) ]

def gradient(L): # 
    N,M=len(L),len(L[0])
    G=[]
    for i in range(1,N-1):
        ligne=[]
        for j in range(1,M-1):
            tmp_x = float(L[i+1][j-1])-float(L[i+1][j+1]) +\
                2 * (float(L[i][j-1])-float(L[i][j+1])) +\
                float(L[i-1][j-1]) - float(L[i-1][j+1])
            tmp_y = float(L[i+1][j-1]) - float(L[i-1][j-1]) +\
                2 * (float(L[i+1][j])-float(L[i-1][j])) +\
                float(L[i+1][j+1]) - float(L[i-1][j+1])
            tmp = tmp_x**2+tmp_y**2
            ligne.append(tmp)    #gradiant de chaque autour de pixel
        G.append(ligne)
    return G

def contours(image,seuil):
    N,M=len(image),len(image[0])
    C=[]
    for i in range(N):
        ligne=[]
        for j in range(M):
            if image[i][j]>seuil: ligne.append(False)
            else: ligne.append(True)
        C.append(ligne)
    return C




for tomate,seuil in [ ("tomate",10000)]:

    image = np.uint8(plt.imread(tomate+".jpg")[:,:,:3]*255)
    print("***** traitement de "+tomate+" **********")

    t=time()

    L=niveaugris(image)
    print("temps pour convertir l’image en niveau de gris: ",time()-t)

    t=time()
    G=gradient(L)
    print("temps pour calculer les gradients: ",time()-t)

    t=time()
    C=contours(G,seuil)
    print("temps pour calculer les contours: ",time()-t)

    plt.imshow(C,cmap="gray")
    plt.axis("off")
    plt.show()


print()
