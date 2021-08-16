import cv2  
import numpy as np  
from tkinter import *  
import time
from PIL import Image, ImageTk 
from firebase import firebase 


##Lay du lieu tu database firebase###
firebase = firebase.FirebaseApplication('https://tomatoproject-b1282-default-rtdb.firebaseio.com')
data = firebase.get('/', None)

########Giao dien( tieu de,logo,nut close)################
tk = Tk()
tk.title("Tomato Classification")
tk.geometry("800x420+0+0")  # khoi tao man hinh voi size nhieu 800x420, vi tri goc trai tren
tk.resizable(0, 0)  # khong cho resize cua so
tk.configure(background="white")  # background color


# dong ung dung
def close_window():  # ham dong ung dung
    tk.destroy()


bt01 = Button(tk, fg="red", bg="white", font="Times 18", text="Close", command=close_window)  # nut dong ung dung
bt01.pack()  # The Pack geometry manager packs widgets in rows or columns
bt01.place(x=700, y=350)  # de cai nut dong nay o vi tri x = 700 y = 350

# tieu de 1
content1 = "Graduate Project_Tomato Classification"
lb01 = Label(tk, fg="green", bg="white", font="Times 18", text=content1)
lb01.pack()
lb01.place(x=220, y=10)

# tieu de 2
content2 = "Product Classification Using Image Processing"
lb02 = Label(tk, fg="green", bg="white", font="Times 14", text=content2)
lb02.pack()
lb02.place(x=215, y=40)

##logo truong
imagelg = Image.open('hutech_logo.png')  # doc cai link logo
imagelg = imagelg.resize((80, 80), Image.ANTIALIAS)  # resize logo
imagelg = ImageTk.PhotoImage(imagelg)
lb03 = Label(image=imagelg)  # de logo vo cai label roi hien thi len
lb03.image = imagelg
lb03.pack()
lb03.place(x=50, y=0)

# 3 cai label
lb04 = Label(tk, text="Red", font="Times 12", fg="blue", bg="white")
lb04.pack()
lb04.place(x=80, y=90)
lb04 = Label(tk, text="Orange", font="Times 12", fg="blue", bg="white")
lb04.pack()
lb04.place(x=320, y=90)
lb04 = Label(tk, text="Green", font="Times 12", fg="blue", bg="white")
lb04.pack()
lb04.place(x=600, y=90)

##### Hien thi so luong loai###
# 4 cai label
lb11 = Label(tk, fg="green", bg="white", font="Times 18", text="Loai 1:")
lb11.pack()
lb11.place(x=400, y=260)

lb12 = Label(tk, fg="green", bg="white", font="Times 18", text="Loai 2:")
lb12.pack()
lb12.place(x=400, y=290)

lb13 = Label(tk, fg="green", bg="white", font="Times 18", text="Loai 3:")
lb13.pack()
lb13.place(x=400, y=320)

lb14 = Label(tk, fg="green", bg="white", font="Times 18", text="Loai 4:")
lb14.pack()
lb14.place(x=400, y=350)

count_t1 = 0
count_t2 = 0
count_t3 = 0
count_t4 = 0
####cap nhat so luong ban dau len giao dien###
lb21 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t1)
lb21.pack()
lb21.place(x=490, y=260)

lb22 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t2)
lb22.pack()
lb22.place(x=490, y=290)

lb23 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t3)
lb23.pack()
lb23.place(x=490, y=320)

lb24 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t4)
lb24.pack()
lb24.place(x=490, y=350)
###########
red_tc = 0
orange_tc = 0
green_tc = 0


###Viet cac chuong trinh con###
def chupanh():
    path = tkFileDialog.askopenfilename()
    if len(path) > 0:
	    image = cv2.imread(path)
    return image  # tra ve cai anh

btSI = Button(tk, fg="red", bg="white", font="Times 18", text="Select image", command=chupanh)  # nut dong ung dung
btSI.pack()  # The Pack geometry manager packs widgets in rows or columns
btSI.place(x=500, y=350)  # de cai nut dong nay o vi tri x = 700 y = 350

# ham xu lu canh
def edge_processing(image_e):  # dau vao la 1 cai anh
    image_edge = image_e[0:730, 70:950]  # cat anh, lay truc y tu 0 toi pixel 730, trục x lay tu 70 toi 950. why ? dont ask me :)
    img_gr = cv2.cvtColor(image_edge, cv2.COLOR_BGR2GRAY);  # chuyen doi sang anh xam

    cv2.imwrite('gray.jpg', img_gr)  # luu cai anh xam nay lai de coi cho dui

    img_remove_noise = cv2.GaussianBlur(img_gr, (5, 5), 0);  # lam mo anh,giam nhieu
    # _,img_2=cv2.threshold(img_remove_noise,20,255,cv2.THRESH_BINARY)
    img_canny = cv2.Canny(img_remove_noise, 5, 30);  # tim vien cua doi tuong
    kernel = np.ones((9, 9), np.uint8)  # tao kernel de lam day bien
    img_bien = cv2.dilate(img_canny, kernel, iterations=1)  # lamdaybien
    _, contours, _ = cv2.findContours(img_bien, cv2.RETR_LIST,
                                      cv2.CHAIN_APPROX_NONE)  # tim mot doi tuong co vien trang tren nen den
    # cv2.imwrite('img_bien.jpg',img_bien)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]  # ghi lai thu tu contour
    contour = contours[1]  # lay coutour 1
    # c=max(contours,key=cv2.contourArea)

    # contour=max(contours,key=cv2.contourArea)
    # ve ra coi cho dui
    cv2.drawContours(image_edge, contour, -1, 255, 3)
    cv2.imwrite('edge.jpg', image_edge)
    cv2.imwrite('bien.jpg', img_bien)
    cv2.imwrite('canny.jpg', img_canny)

    S = cv2.contourArea(contour)  # tinh dien tich cai contour do
    return contour, S  # tra ve contour va dien tich cua no


# xu ly mau sac
def color_processing(image_c):  # dau vao la 1 tam hinh
    color = 'none'
    hsv_img = cv2.cvtColor(image_c, cv2.COLOR_BGR2HSV)  # doc cai hinh do duoi he mau HSV

    ####cac gia tri mau sac###
    lower_red = np.array([160, 100, 20])
    upper_red = np.array([180, 255, 255])

    lower_orange = np.array([10, 60, 100])
    upper_orange = np.array([32, 255, 255])

    lower_green = np.array([35, 30, 20])
    upper_green = np.array([70, 255, 255])

    # tao mask cho  3 mau
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)
    mask_orange = cv2.inRange(hsv_img, lower_orange, upper_orange)
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)
    ###lam day mang mau##
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.dilate(mask_red, kernel, iterations=1)
    mask_orange = cv2.dilate(mask_orange, kernel, iterations=1)
    mask_green = cv2.dilate(mask_green, kernel, iterations=1)

    img_red = cv2.bitwise_and(image_c, image_c, mask=mask_red)
    img_orange = cv2.bitwise_and(image_c, image_c, mask=mask_orange)
    img_green = cv2.bitwise_and(image_c, image_c, mask=mask_green)
    ####tinh so luong pixel moi mau
    amount_red = cv2.countNonZero(mask_red)
    amount_orange = cv2.countNonZero(mask_orange)
    amount_green = cv2.countNonZero(mask_green)
    amount_3colors = amount_red + amount_orange + amount_green + 1
    p_red = amount_red / amount_3colors
    p_orange = amount_orange / amount_3colors
    p_green = amount_green / amount_3colors
    if p_red > 0.8:
        color = 'red'
    elif p_orange > 0.2:
        color = 'orange'
    elif p_green > 0.6:
        color = 'green'
    return color, img_red, img_orange, img_green


def phanloai(S, red_ck, orange_ck, green_ck, data_js): #dau vao la dien tich, gia tri do cam xanh (0 hoac 1)
    tomato = 'none'
    for tp in data_js: #voi moi gia tri trong datta_js, goi do la tp
        if tp != 'Amount': #neu tp khac Amount (co nghi la tp la type 1 2 3)
            if (S >= int(data_js[tp]['min']) and S < int(data_js[tp]['max']) #so sanh neu dien tich lon hon hoac bang min va be hon max
                    and red_tc == int(data_js[tp]['RED']) #va gia tri mau duoc tra ve co giong gia tri mau duoc quy dinh tren server hay khong
                    and orange_tc == int(data_js[tp]['ORANGE'])  #data_js[tp]['ORANGE'] la 1 = true hoac 0 = false,
                    and green_tc == int(data_js[tp]['GREEN'])):
                tomato = str(tp) #neu dieu kien dung het thi chon loai do
    if tomato == 'none':
        tomato = 'Type_4' #neu khong thoa dieu kien tren thi la loai 4
    return tomato  # tra ve loai ca chua type 1 2 3 4 'Type_1'


def control_servo(tomato_type): #dau vao la loai ca chua, ham de day ca chua sang cac o tuong ung
    if tomato_type == 'Type_1':
        sensor_number = sensor_1 #channel cua sensor = sensor_1 khai bao o tren cung
        servo_number = servo_1 #channel cua servo = servo_1 khai bao o tren cung
        sensor_state = not GPIO.input(sensor_number) #GPIO.input(sensor_number) neu cam dung cong thi se co gia tri True => sensor state hien tai bang false
        pwm = GPIO.PWM(servo_number, 50)  # channel=servo_number,  frequency=50Hz
        pwm.start(6) #the duty cycle = dc = 6 (0.0 <= dc <= 100.0)
        print('Waiting for tomato to reach position  ...')
        while not sensor_state: #neu sensor state la false => not sensor_state = true => lap while
            time.sleep(0.3) #nghi xiu
            sensor_state = not GPIO.input(sensor_number)
            #dieu kien van khong doi khong le lap quai ha ? question: co khi nao sensor_number doi khong ?

        pwm.ChangeDutyCycle(11) #doi duty cycle dc thanh 11
        time.sleep(2)
        pwm.stop()
        print('clasify finish')
    else:
        #tuong tu cho type 2 3
        if tomato_type == 'Type_2':
            sensor_number = sensor_2
            servo_number = servo_2
            sensor_state = not GPIO.input(sensor_number)
            pwm = GPIO.PWM(servo_number, 50)
            pwm.start(12)
            print('Waiting for tomato to reach position  ...')
            while not sensor_state:
                time.sleep(0.3)
                sensor_state = not GPIO.input(sensor_number)

            pwm.ChangeDutyCycle(6)
            time.sleep(2)
            pwm.stop()
            print('clasify finish')
        else:
            if tomato_type == 'Type_3':
                sensor_number = sensor_3
                servo_number = servo_3
                sensor_state = not GPIO.input(sensor_number)
                pwm = GPIO.PWM(servo_number, 50)
                pwm.start(6)
                print('Waiting for tomato to reach position  ...')
                while not sensor_state:
                    time.sleep(0.3)
                    sensor_state = not GPIO.input(sensor_number)

                pwm.ChangeDutyCycle(11)
                time.sleep(2)
                pwm.stop()
                print('clasify finish')

#ket thuc khai bao cac ham

#bat dau chay chuong trinh o day
temp = 0
while True:
    tk.update() #render khung hinh
    # #state = not GPIO.input(17)
    # if (state == 1) and (temp == 0):
    #     time.sleep(1.95)
    #     image_ori = chupanh() #chup anh trai ca chua
    #     contour, S = edge_processing(image_ori) #lay ra vien ca chua va dienj tich
    #     S = S / 1000
    #     if S < 12: #dien tich nho qua thi chac khong phai trai ca chua ? :D
    #         print('processing error')
    #         time.sleep(1)
    #         continue
    #     time.sleep(0.05)

    #     red_tc = 0
    #     orange_tc = 0
    #     green_tc = 0
        
    #     color, red, orange, green = color_processing(image_ori)
    #     #xu ly mau, tra ve gia tri vi du: red, anh nhung phan mau do, anh nhung phan mau cam, anh nhung phan mau xanh

    #     if color == 'red': #neu trai ca chua sau khi xu ly anh tra ve mau do
    #         red_tc = 1; #set gia tri do bang 1, cac gia tri mau khac bang 0
    #         orange_tc = 0;
    #         green_tc = 0
    #     elif color == 'orange':
    #         red_tc = 0;
    #         orange_tc = 1;
    #         green_tc = 0
    #     else:
    #         red_tc = 0;
    #         orange_tc = 0;
    #         green_tc = 1
    #     #print(red_tc, orange_tc, green_tc)
    #     time.sleep(0.03) #nghi xiu

    #     tomato_nha = phanloai(S, red_tc, orange_tc, green_tc, data) #dua vo cai ham phan loai de phan loai

    #     ###in anh ra giao dien###
    #     cv2.imwrite('green.jpg', green) #luu anh xuong
    #     cv2.imwrite('orange.jpg', orange)
    #     cv2.imwrite('red.jpg', red)

    #     #load cac anh da duoc luu xuong len man hinh
    #     imagelg = Image.open('red.jpg')
    #     imagelg = imagelg.resize((210, 150), Image.ANTIALIAS)
    #     imagelg = ImageTk.PhotoImage(imagelg)
    #     lb03 = Label(image=imagelg)
    #     lb03.image = imagelg
    #     lb03.pack()
    #     lb03.place(x=5, y=110)

    #     imagelg = Image.open('orange.jpg')
    #     imagelg = imagelg.resize((210, 150), Image.ANTIALIAS)
    #     imagelg = ImageTk.PhotoImage(imagelg)
    #     lb04 = Label(image=imagelg)
    #     lb04.image = imagelg
    #     lb04.pack()
    #     lb04.place(x=250, y=110)
    #     tk.update()

    #     imagelg = Image.open('green.jpg')
    #     imagelg = imagelg.resize((210, 150), Image.ANTIALIAS)
    #     imagelg = ImageTk.PhotoImage(imagelg)
    #     lb05 = Label(image=imagelg)
    #     lb05.image = imagelg
    #     lb05.pack()
    #     lb05.place(x=490, y=110)
    #     tk.update()

    #     imagelg = Image.open('edge.jpg')
    #     imagelg = imagelg.resize((210, 150), Image.ANTIALIAS)
    #     imagelg = ImageTk.PhotoImage(imagelg)
    #     lb05 = Label(image=imagelg)
    #     lb05.image = imagelg
    #     lb05.pack()
    #     lb05.place(x=5, y=263)
    #     tk.update()

    #     #print(tomato_nha)
    #     #cap nhat lai so luong cac label tren man hinh
    #     if tomato_nha == 'Type_1':
    #         count_t1 = count_t1 + 1 #cong them neu dung loai
    #         lb21 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t1)
    #         lb21.pack()
    #         lb21.place(x=490, y=260)

    #     if tomato_nha == 'Type_2':
    #         count_t2 = count_t2 + 1

    #         lb21 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t2)
    #         lb21.pack()
    #         lb21.place(x=490, y=290)

    #     if tomato_nha == 'Type_3':
    #         count_t3 = count_t3 + 1

    #         lb21 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t3)
    #         lb21.pack()
    #         lb21.place(x=490, y=320)

    #     if tomato_nha == 'Type_4':
    #         count_t4 = count_t4 + 1

    #         lb21 = Label(tk, fg="green", bg="white", font="Times 18", text=count_t4)
    #         lb21.pack()
    #         lb21.place(x=490, y=350)

    #     print(count_t1, count_t2, count_t3, count_t4)

    #     print(S)

    #     time.sleep(0.05)
