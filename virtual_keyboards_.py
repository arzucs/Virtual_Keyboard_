import cv2
import math
import cvzone
import imutils
import numpy as np
from time import sleep
from pynput.keyboard import Controller #not defterine yazabilmek için kullanılan kütüphane
from cvzone.HandTrackingModule import HandDetector

cap= cv2.VideoCapture(0)

# cap.set(3, 1280)
# cap.set(4, 720)

#detector = HandDetector(detectionCon=0.1, maxHands=1)
detector = HandDetector(detectionCon=0.8) #güvenilirlik değeri ne düşükse o kadr iyi bulur eli



keys= [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
       ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
       ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText= ""

keyboard= Controller()

class Button():
    def __init__(self , pos, text, size = [ 85 , 85 ]): #constructor(__init__) nesnenin durumunu başlatmak için kullanılır. constructor görevi, sınıfın bir nesnesi oluşturulduğunda sınıfın veri üyelerine ilk değer atamaktır.
        self.pos=pos
        self.size=size
        self.text=text
        #Not : eşitliğin sağ tarafı fonksiyonun parametreleridir. Sol tarafı ise classın içine tanımladığın veriler.
        #Böyle bir constructor methodu ile her şeyi daha hızlı tanımlayabiliriz
        #self.pos = pos gibi. Fonksiyon parametresi olan posu, benim içimdeki veri yapısı olan posa ata şeklinde.
        
        
# def drawAll(img , buttonlist):
#     for button in buttonlist:
#         x , y =button.pos
#         w , h = button.size
#         cv2.rectangle( img, button.pos , (x + w, y + h), (255 , 0 , 0 ), cv2.FILLED)
#         cv2.putText( img , button.text , (x+ 25, y + 65), cv2.FONT_HERSHEY_PALIN , 4 , (255 , 255, 255), 4 )
#         cvzone.cornerRect( img , (button.pos[0] , button.pos[1], button.size[0] , button.size[1]) , 20 , rt=0)
        
#         return img
    
def drawAll(img, buttonList): #burda oluşturulan her butonun içinde "class Button: " içinde oluştuurlan özellikler saklanıyor zaten /// drawAll yerine transparent_layout'da yazılabilir
     imgNew = np.zeros_like(img, np.uint8) #Bu numpy yöntemi, verilen şekil ve türdeki bir diziyi verilen dizi olarak sıfırlarla döndürür. 
     for button in buttonList:
         x,y = button.pos ##butonun konumu
         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255 , 0 , 0), cv2.FILLED) ##çizilecek olan tuşun özellikleri
         #ilk nereye yapılacak(nerden başlasın nerde bitsin),renk, kalınlık,yazı tipi
         cv2.putText(imgNew, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)  #tuş içine yazılacak olan harfin özellikleri
         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)


     out = img.copy()
     alpha = 0.3 # transparanlık derecesi
     mask = imgNew.astype(bool) #Numpy veya altyapısında numpy içeren bir kütüphane kullanırken elimizdeki verileri istediğimiz tiplere – eğer mümkünse- değiştirebilmemiz gerekmektedir. 
     #Bunun için kullandığımız metot astype() metodudur. Numpy python veritiplerinin yanında kendine özel veritipleri de kullanmaktadır.
     
     #print(mask.shape)
     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
     # oluşturulan şekil görüntüsünü yeni bir değişkene kopyalayıp bir imgNew maskesi oluşturuyoruz ve 
     # maskeyi gerçek görüntünün üstüne yerleştirmek için OpenCV'nin addWeighted() işlevini kullanıyoruz.
     #cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output) ==> alpha= transparanlık derecesi, 1 - alpha= beta değeridir
     # alpha + beta(1 - alpha) = 1,0 olmalı

     return out

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) #y eksenine göre simetrik
    img = imutils.resize(img, width=1280, height=720)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bboxInfo = hand["bbox"]

        # print("El Noktaları:", lmList)
        # print("Sınırlayıcı Kutu Bilgisi:", bboxInfo)

        for lm in lmList:
            x, y = lm[1], lm[2]
            #cv2.circle(img, (x, y), 10, (0, 255, 0), -1)

        img = drawAll(img, buttonList)

        if lmList:
           for button in buttonList:
                x,y = button.pos
                w,h = button.size

                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:  #8 numaralı işaret parmak ucu x değerleri x ve x+w arasında ise aşağıdakileri yap
                    cv2.rectangle(img, (x-5, y-5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    
                    point1 = lmList[8]  # Örneğin işaret parmak ucu
                    point2 = lmList[4]  # Örneğin başparmak ucu

                    # İki nokta arasındaki mesafeyi hesapla
                    distance = math.dist((point1[1], point1[2]), (point2[1], point2[2])) #math.dist=İki nokta arasındaki Öklid mesafesini hesaplamak için

                    print(distance)
                    
                    # When Clicked
                    if 20 < distance < 70: 
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        finalText += button.text
                        sleep(0.2)
                        keyboard.press(button.text) #not defteri açılınca ona da yazar
                        
                # finalText özellikleri
                cv2.rectangle(img, (50, 350), (1070, 450),(175, 10, 175), cv2.FILLED)
                cv2.putText(img, finalText, (60, 425),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()      
        