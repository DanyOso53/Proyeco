import cv2
import mediapipe as mp

puntadedoid = [4,8,12,16,20]
cam = cv2.VideoCapture(0)
mpdraw=mp.solutions.drawing_utils
mphands=mp.solutions.hands
mano=mphands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)


def drawhands(img,landmarks) :

    if landmarks :

        for puntos in landmarks :

            mpdraw.draw_landmarks(img,puntos,mphands.HAND_CONNECTIONS)

def contardedos(img,landmarks,numerodedo= 0):

    if landmarks:

        puntosref= landmarks[numerodedo].landmark
        
        dedos=[]

        for indices in puntadedoid :

            finger_tip_y = puntosref[indices].y
            finger_bottom_y = puntosref[indices-2].y

            if indices != 4:

                    if finger_tip_y < finger_bottom_y :
                         dedos.append(1)
                         print("EL DEDO CON ID : ", indices , "esta abierto")

                    if finger_tip_y > finger_bottom_y :
                          dedos.append(0)
                          print("EL DEDO CON ID : ", indices , "esta cerrado")
            
        totaldedo= dedos.count(1)
        texto = f"dedos : {totaldedo}"
        cv2.putText(img,texto,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

while True :   

    ret,img=cam.read()
    
    result= mano.process(img)
    puntosmano=result.multi_hand_landmarks
    drawhands(img,puntosmano)
    contardedos(img,puntosmano)

    cv2.imshow("cámara",img)
    
    if cv2.waitKey(0)==32:
        break


cam.release()
cv2.destroyAllWindows()
