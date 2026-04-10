import cv2, matplotlib
import numpy as np

print("OpenCV version :", cv2.__version__)
print("Numpy version :", np.__version__)
print("Matplotlib version :", matplotlib.__version__)

#initialisation de la video
video = cv2.VideoCapture('voitures.mp4') 
#detection d'objet via camera stable
object_detector = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=40)

#variables compteurs
compteur = 0
ligney = 200
objets_deja_comptes = []

while True:
    ret, frame = video.read()
    if not ret:break
    #redim de la video
    frame = cv2.resize(frame, (640, 360))
    #extraction d'une region
    cut = frame[0:360,375:640]

    #detection objet
    mask = object_detector.apply(cut)

    ker = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
    mask_propre = cv2. morphologyEx(mask, cv2.MORPH_CLOSE, ker)
    _,mask_propre = cv2.threshold(mask_propre, 254, 255, cv2.THRESH_BINARY)

    #detection contours
    contours, _ = cv2.findContours(mask_propre, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame, (0,ligney), (frame.shape[1], ligney), (0,0,255), 2)
    nouveaux_centres = []

    #amelioration des contours
    for cnt in contours:
        #calculer l'aire et enlever les petits element
        aire = cv2.contourArea(cnt)
        if aire>1000:
            x,y,w,h = cv2.boundingRect(cnt)

            cx = int(x + w/2)
            cy = int(y + h/2)
            nouveaux_centres.append((cx,cy))

            cv2.rectangle(cut, (x,y), (x+w,y+h), (0,255,0), 2)
    
            for (old_cx, old_cy) in objets_deja_comptes:
                if old_cy < ligney and cy >= ligney and abs(cx - old_cx)<50:
                    compteur+=1
                    print(f'objet detecte, total = {compteur}')
        
        objets_deja_comptes = nouveaux_centres
        cv2.putText(frame, f'{compteur}', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2,)

    #cv2.imshow("cut", cut)
    cv2.imshow("Video", frame)
    #cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == 27: break #touche esc

video.release()
cv2.destroyAllWindows()
