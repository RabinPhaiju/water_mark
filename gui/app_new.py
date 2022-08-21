import cv2
import random
import numpy as np
import pytesseract
from math import log10, sqrt
from skimage.util import random_noise
from tkinter import *
from pywt import dwt2, idwt2
import matplotlib.pyplot as plt
from tkinter import ttk,filedialog
from PIL import Image,ImageTk,ImageDraw, ImageFont

window = Tk()
window.geometry("1140x720")
window.resizable(0,0)
# window.wm_iconbitmap(os.getcwd()+'/gui/icon.ico')
window.title('Watermark using DWT')

style = ttk.Style()
style.theme_use('xpnative')# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# global variables
result_LL,LL,LH,HL,HH,h,hh,w,ww,manipulated,manipulated2,xoff,yoff =None,None,None,None,None,None,None,None,None,None,None,None,None
result_LL2,LL2,LH2,HL2,HH2,h2,hh2,w2,ww2,xoff2,yoff2 =None,None,None,None,None,None,None,None,None,None,None
current_noise_type =''

dwt_level = 1
# q = 1.5
# q = 1
q = 0.98
# q = 0.95
# q = 0.90
# q = 0.85
# q = 0.78
# q = 0.6

k = 0.09

pos_list = ['Center','Top Left','Top Right','Bottom Left','Bottom Right']
noise_list = ['Gaussian','Salt & Pepper']
rotate_list = [30,60,90,120,150,180,210,240]
crop_list = ['Center','Top Left','Top Right','Bottom Left','Bottom Right']

cover_image_path = StringVar()
watermark_image_path = StringVar()

current_text = StringVar()
current_text.set('What it does: Add and Remove WaterMark')

# main notebook
main_notebook = ttk.Notebook(window)
main_notebook.grid(row=0,column=0)
main_frame = Frame(main_notebook)
main_frame.columnconfigure(0, weight=1)
main_frame.grid(row=0,column=0)

# row 0
first_frame = ttk.Frame(main_frame)
first_frame.columnconfigure(0, weight=1)
first_frame.grid(row=0,column=0)
 

first_sub_frame = ttk.Frame(first_frame)
first_frame.columnconfigure(0, weight=1)
first_sub_frame.grid(row=0,column=0)

heading1 = Label(first_sub_frame,text='Watermark Project',font=("Comic Sans MS",24,"normal"))
heading1.grid(column=0,row=0)
heading2 = Label(first_sub_frame,textvariable=current_text,font=('Candara Light',12),width=72)
heading2.grid(column=0,row=1)


# row 1
second_frame = ttk.Frame(main_frame)
second_frame.columnconfigure(0, weight=1)
second_frame.grid(row=1,column=0)

def uplaod_cover_image():
    file = filedialog.askopenfilename()
    cover_image_path.set(file)
    global cover_icon
    cover_icon = Image.open(file)
    cover_icon = cover_icon.resize((280,280), Image.ANTIALIAS)
    cover_icon =  ImageTk.PhotoImage(cover_icon)
    cover_button = Button(second_frame,image=cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    cover_button.grid(column=0,row=0,padx=5,pady=5)
    

def uplaod_watermark_image(src):
    if src != '':
        file = src
    else:    
        file = filedialog.askopenfilename()
    watermark_image_path.set(file)
    global watermark_icon
    watermark_icon = Image.open(file)
    watermark_icon = watermark_icon.resize((280,280), Image.ANTIALIAS)
    watermark_icon =  ImageTk.PhotoImage(watermark_icon)
    watermark_button = Button(second_frame,image=watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    watermark_button.grid(column=1,row=0,padx=10,pady=10)

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def create_watermark_image():
    print(pos_var.get())
    
    text = watermark_input.get('1.0',END)
    if len(text)<=1 or text == '':
        text = 'Watermark'
    fontname = "gui/Roboto-Black.ttf"
    fontsize = 34
    colorText = "gray"
    colorOutline = "black"
    colorBackground = "black"
    
    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+9, height*2))
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    img.save("gui/text_watermark.png",'PNG')
    uplaod_watermark_image('gui/text_watermark.png')
    
# cover_icon = PhotoImage(file='gui/cover_icon.png')
cover_icon = Image.open('gui/cover_icon.png')
cover_icon = cover_icon.resize((280,280), Image.ANTIALIAS)
cover_icon =  ImageTk.PhotoImage(cover_icon)

# watermark_icon = PhotoImage(file='gui/watermark_icon.jpg')
watermark_icon = Image.open('gui/watermark_icon.jpg')
watermark_icon = watermark_icon.resize((280,280), Image.ANTIALIAS)
watermark_icon =  ImageTk.PhotoImage(watermark_icon)

cover_button = Button(second_frame,image=cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
cover_button.grid(column=0,row=0,padx=5)

watermark_button = Button(second_frame,image=watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
watermark_button.grid(column=1,row=0,padx=5)

second_sub_frame = ttk.Frame(second_frame)
second_frame.columnconfigure(0, weight=1)
second_sub_frame.grid(row=0,column=3)

watermarked_icon = Image.open('gui/watermarked_icon.jpg')
watermarked_icon = watermarked_icon.resize((280,280), Image.ANTIALIAS)
watermarked_icon =  ImageTk.PhotoImage(watermarked_icon)
watermarked_button = Button(second_frame,image=watermarked_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
watermarked_button.grid(column=2,row=0,padx=5)

upload_cover = Button(second_sub_frame,command=uplaod_cover_image,text='Upload Cover Image',font=('Candara Light',16),width=16)
upload_cover.grid(column=0,row=0,padx=5)
watermark_cover = Button(second_sub_frame,command=lambda :uplaod_watermark_image(''),text=' Upload Watermark',font=('Candara Light',16))
watermark_cover.grid(column=0,row=1,padx=5)

watermark_text = Label(second_sub_frame,text='Enter Text',font=('Candara Light',16),width=16)
watermark_text.grid(column=0,row=2)
watermark_input = Text(second_sub_frame,height=2,width=18,font=('Candara Light',14))
watermark_input.grid(column=0,row=3,padx=5)
watermark_create = Button(second_sub_frame,command=create_watermark_image,text=' Create Watermark',font=('Candara Light',16))
watermark_create.grid(column=0,row=4,padx=5)

second_sub_sub_frame = ttk.Frame(second_sub_frame)
second_sub_frame.columnconfigure(0, weight=1)
second_sub_sub_frame.grid(row=5,column=0)

watermark_pos_text = Label(second_sub_sub_frame,text='Position',font=('Candara Light',16),width=10)
watermark_pos_text.grid(column=0,row=0)
pos_var = StringVar(second_sub_sub_frame)
pos_var.set(pos_list[2]) # default value
watermark_pos = OptionMenu(second_sub_sub_frame,pos_var,*pos_list)
watermark_pos.grid(column=1,row=0)

# dwt_level_text = Label(second_sub_sub_frame,text='DWT Level',font=('Candara Light',16),width=10)
# dwt_level_text.grid(column=0,row=1)
# dwt_level1 = StringVar(second_sub_sub_frame)
# dwt_level1.set(1) # default value
# dwt_level_pos = OptionMenu(second_sub_sub_frame,dwt_level,*[1,2])
# dwt_level_pos.grid(column=1,row=1)

# row 2
third_frame = ttk.Frame(main_frame)
third_frame.columnconfigure(0, weight=1)
third_frame.grid(row=2,column=0,pady=5)

def add_watermark():
    global result_LL,LL,LH,HL,HH,h,hh,w,ww,manipulated,manipulated2,xoff,yoff
    global result_LL2,LL2,LH2,HL2,HH2,h2,hh2,w2,ww2,xoff2,yoff2
    
    A = cv2.imread(cover_image_path.get())
    host = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    LL, (LH, HL, HH) = dwt2(host, 'haar')
    h, w = LL.shape
    if(dwt_level==2):
        LL2, (LH2, HL2, HH2) = dwt2(LL, 'haar')
        h2, w2 = LL2.shape
    
    B = cv2.imread(watermark_image_path.get())
    watermark = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    LL_w, (LH_w, HL_w, HH_w) = dwt2(watermark, 'haar')
    hh, ww = LL_w.shape
    if(dwt_level==2):
        LL_w2, (LH_w2, HL_w2, HH_w2) = dwt2(LL_w, 'haar')
        hh2, ww2 = LL_w2.shape
    
    # pos_list = ['Center','Top Left','Top Right','Bottom Left','Bottom Right']
    if(pos_var.get() == 'Center'):
        if(dwt_level == 1):
            yoff = round((h-hh)/2)
            xoff = round((w-ww)/2)
        elif(dwt_level == 2):
            yoff = round((h2-hh2)/2)
            xoff = round((w2-ww2)/2)
    elif(pos_var.get() == 'Top Left'):
        yoff = 0
        xoff = 0
    elif(pos_var.get() == 'Top Right'):
        yoff = 0
        if(dwt_level == 1):
            xoff = w-ww
        elif(dwt_level == 2):
            xoff = round(w2-ww2)
    elif(pos_var.get() == 'Bottom Left'):
        if(dwt_level == 1):
            yoff = h-hh
        elif(dwt_level == 2):
            yoff = round(h2-hh2)
        xoff = 0
    elif(pos_var.get() == 'Bottom Right'):
        if(dwt_level == 1):
            yoff = h-hh
            xoff = w-ww
        elif(dwt_level == 2):
            yoff = round(h2-hh2)
            xoff = round(w2-ww2)
        
    if(dwt_level == 1):
        manipulated = LL_w * q
        manipulated2 = LL_w * q
    elif(dwt_level == 2):
        manipulated = LL_w2 * q
        manipulated2 = LL_w2 * q

    result = LL.copy()
    result2 = None

    if(dwt_level == 1):
        text = watermark_input.get('1.0',END)
        if len(text)<=1 or text == '':
            print('add k')
            result[yoff:yoff+hh, xoff:xoff+ww] *=k
        result[yoff:yoff+hh, xoff:xoff+ww] += manipulated
        result_LL = idwt2((result,( LH, HL, HH)), 'haar')
    elif(dwt_level == 2):
        result2 = LL2.copy()
        text = watermark_input.get('1.0',END)
        if len(text)<=1 or text == '':
            result2[yoff:yoff+hh2, xoff:xoff+ww2] *=k
        result2[yoff:yoff+hh2, xoff:xoff+ww2] += manipulated
        result_LL2 = idwt2((result2,( LH2, HL2, HH2)), 'haar')
        result_LL =  idwt2((result_LL2,( LH, HL, HH)), 'haar')
    cv2.imwrite('gui/watermarked.jpg', result_LL)
    cv2.imwrite('gui/watermarked_for_edit.jpg', result_LL)
    upload_watermarked_image('gui/watermarked.jpg')
    # MSE_PSNR()

def MSE_PSNR():
    img1, img2 = None,None
    # I1 = cv2.imread('gui/mountain_512.jpg')
    # I2 = cv2.imread('gui/watermarked.jpg')
    I1 = cv2.imread('gui/lena256.png')
    I2 = cv2.imread('gui/extracted_watermark.jpeg')
    img1 = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)

    mse = np.mean((img1 - img2) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    print('mse',mse)
    print('psnr',psnr)

def upload_watermarked_image(img_path):
    global watermarked_icon
    watermarked_icon = Image.open(img_path)
    watermarked_icon = watermarked_icon.resize((280,280), Image.ANTIALIAS)
    watermarked_icon =  ImageTk.PhotoImage(watermarked_icon)
    watermarked_button = Button(second_frame,image=watermarked_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    watermarked_button.grid(column=2,row=0,padx=5,pady=5)

def extract_watermark():
    I = cv2.imread('gui/watermarked.jpg', 1)
    I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    if(current_noise_type!=''):
        kernel = np.ones((2,2),np.float32)/4
        I = cv2.filter2D(I,-1,kernel)

    wm_LL,( m_LH, wm_HL, m_HH) = dwt2(I, 'haar')
    wm_LL2,new_LL,new_image,new_image2 = None,None,None,None
    if(dwt_level == 2):
        wm_LL2,( m_LH2, wm_HL2, m_HH2) = dwt2(wm_LL, 'haar')

    if(dwt_level == 1):
        new_LL = wm_LL - LL*k
    elif(dwt_level == 2):
        new_LL = wm_LL2 - LL2*k

    # new_LL = new_LL / q
    if(dwt_level == 1):
        new_image = idwt2((new_LL, (LH, HL, HH)), 'haar')
    elif(dwt_level == 2):
        new_image2 = idwt2((new_LL, (LH2, HL2, HH2)), 'haar')
        new_image = idwt2((new_image2, (LH, HL, HH)), 'haar')

    new_crop_image = new_image.copy()
    
    if pos_var.get() == 'Center':
        new_crop_image = new_crop_image[h-hh:h+hh, w-ww:w+ww]
    elif pos_var.get() == 'Top Left':
        new_crop_image = new_crop_image[0:hh*2, 0:ww*2]
    elif pos_var.get() == 'Top Right':
        new_crop_image = new_crop_image[0:hh*2, w*2-ww*2:w*2+ww*2]
    elif pos_var.get() == 'Bottom Left':
        new_crop_image = new_crop_image[h*2-hh*2:h*2, 0:ww*2]
    elif pos_var.get() == 'Bottom Right':
        new_crop_image = new_crop_image[h*2-hh*2:h*2, w*2-ww*2:w*2+ww*2]
    cv2.imwrite('gui/extracted_watermark.jpeg', new_crop_image)

    img_0 = cv2.imread("gui/extracted_watermark.jpeg",cv2.IMREAD_GRAYSCALE)
    new_img = img_0.copy()

    if(len(watermark_input.get('1.0',END))>1):
        for i, row in enumerate(img_0):
            for j,pixel in enumerate(row):
                if(pixel > 170):
                    new_img[i][j] = 220
                else:
                    new_img[i][j] = 60
        cv2.imwrite('gui/extracted_watermark.jpeg', new_img)
        global current_text
        imagetotext = 'gui/extracted_watermark.jpeg'
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(Image.open(imagetotext), lang="eng")
        current_text.set('Extracted Text: '+text)


    global recover_watermark_icon
    recover_watermark_icon = Image.open('gui/extracted_watermark.jpeg')
    recover_watermark_icon = recover_watermark_icon.resize((280,280), Image.ANTIALIAS)
    recover_watermark_icon =  ImageTk.PhotoImage(recover_watermark_icon)
    recover_watermark_button = Button(third_frame,image=recover_watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    recover_watermark_button.grid(column=3,row=0,padx=5,pady=5)
    # MSE_PSNR()

def remove_watermark():
    new_LL,wm_LL2,wm_LH2,wm_HL2,wm_HH2,new_image,new_image2 = None,None,None,None,None,None,None
    text = watermark_input.get('1.0',END)
    maniputated_used = None
    if len(text)<=1 or text == '':
        maniputated_used = manipulated
    else:
        maniputated_used = manipulated2
    I = cv2.imread('gui/watermarked.jpg', 1)
    I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    wm_LL,( wm_LH, wm_HL, wm_HH) = dwt2(I, 'haar')
    if(dwt_level == 2):
        wm_LL2,( wm_LH2, wm_HL2, wm_HH2) = dwt2(wm_LL, 'haar')
    
    if(dwt_level == 1):
        new_LL = wm_LL.copy()
        new_LL[yoff:yoff+hh, xoff:xoff+ww] -= maniputated_used
        if len(text)<=1 or text == '':
            new_LL[yoff:yoff+hh, xoff:xoff+ww] /=k
    elif(dwt_level == 2):
        new_LL = wm_LL2.copy()
        new_LL[yoff:yoff+hh2, xoff:xoff+ww2] -= maniputated_used
        
        if len(text)<=1 or text == '':
            new_LL[yoff:yoff+hh2, xoff:xoff+ww2] /=k
 
    if(dwt_level == 1):
        new_image = idwt2((new_LL, ( wm_LH, wm_HL, wm_HH)), 'haar')
    if(dwt_level == 2):
        new_image2 = idwt2((new_LL, (wm_LH2, wm_HL2, wm_HH2)), 'haar')
        new_image = idwt2((new_image2, (wm_LH, wm_HL, wm_HH)), 'haar')
    cv2.imwrite('gui/extracted_cover.jpg', new_image)
    global recover_cover_icon
    recover_cover_icon = Image.open('gui/extracted_cover.jpg')
    recover_cover_icon = recover_cover_icon.resize((280,280), Image.ANTIALIAS)
    recover_cover_icon =  ImageTk.PhotoImage(recover_cover_icon)
    recovere_cover_button = Button(third_frame,image=recover_cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    recovere_cover_button.grid(column=2,row=0,padx=5,pady=5)

def crop_watermark():
    global manipulated
    crop_type = crop_var.get()
    #crop half
    img = cv2.imread("gui/watermarked_for_edit.jpg")
    A = manipulated
    (h, w) = img.shape[:2]
    (ha, wa) = A.shape[:2]
    if(crop_type == 'Center'):
        img = img[int(h/2-h/4):int(h/2+h/4), int(w/2-w/4):int(w/2+w/4)]
        A = A[int(ha/2-ha/4):int(ha/2+ha/4), int(wa/2-wa/4):int(wa/2+wa/4)]
    elif(crop_type == 'Top Left'):
        img = img[0:int(h/2), 0:int(w/2)]
        A = A[0:int(ha/2), 0:int(wa/2)]
    elif(crop_type == 'Top Right'):
        img = img[0:int(h/2), int(w/2):int(w)]
        A = A[0:int(ha/2), int(wa/2):int(wa)]
    elif(crop_type == 'Bottom Left'):
        img = img[int(h/2):int(h), 0:int(w/2)]
        A = A[int(ha/2):int(ha), 0:int(wa/2)]
    elif(crop_type == 'Bottom Right'):
        img = img[int(h/2):int(h), int(w/2):int(w)]
        A = A[int(ha/2):int(ha), int(wa/2):int(wa)]
    #scale double
    scale_percent = 200 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    widtha = int(A.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    heighta = int(A.shape[0] * scale_percent / 100)
    dim = (width, height)
    dima = (widtha, heighta)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    resized_A = cv2.resize(A, dima, interpolation = cv2.INTER_AREA)
    cv2.imwrite('gui/watermarked.jpg', resized)
    manipulated = resized_A # remove this
    upload_watermarked_image('gui/watermarked.jpg')

def rotate_watermark():
    global manipulated
    rotate_type = rotate_var.get()
    image = cv2.imread("gui/watermarked_for_edit.jpg")
    A = manipulated
    (h, w) = image.shape[:2]
    (ha, wa) = A.shape[:2]
    center = (w / 2, h / 2)
    centera = (wa / 2, ha / 2)
    angle = int(rotate_type)
    scale = 1
    M = cv2.getRotationMatrix2D(center, angle, scale)
    Ma = cv2.getRotationMatrix2D(centera, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    rotateda = cv2.warpAffine(A, Ma, (wa, ha))
    manipulated = rotateda # remove this
    cv2.imwrite('gui/watermarked.jpg', rotated)
    upload_watermarked_image('gui/watermarked.jpg')

def add_noise():
    global noised_watermark,current_noise_type
    noise_type = noise_var.get()
    
    if(noise_type == 'Gaussian'):
        current_noise_type = 'gaussian'
    elif(noise_type == 'Salt & Pepper'):
        current_noise_type = 's&p'

    if(noise_type == 'Salt & Pepper'):
        I = cv2.imread('gui/watermarked.jpg',1)
        sp = random_noise(I,mode=current_noise_type,seed=None,clip=True)
        sp = cv2.convertScaleAbs(sp, alpha=(255.0))
        cv2.imwrite('gui/watermarked.jpg', sp)

    if(noise_type == 'Gaussian'):
        img_0 = cv2.imread('gui/watermarked.jpg',cv2.IMREAD_GRAYSCALE)
        rw,cl = img_0.shape
        num_pix = random.randint(30,100)
        for i in range(num_pix):
            y_crd = random.randint(0,rw-1)
            x_crd = random.randint(0,cl-1)
            img_0[y_crd][x_crd] = 255
        for i in range(num_pix):
            y_crd = random.randint(0,rw-1)
            x_crd = random.randint(0,cl-1)
            img_0[y_crd][x_crd] = 0
        cv2.imwrite('gui/watermarked.jpg', img_0)
        cv2.imwrite('gui/noised.jpg', img_0)


    noised_image_icon = Image.open('gui/watermarked.jpg')
    noised_watermark = noised_image_icon.resize((280,280), Image.ANTIALIAS)
    noised_watermark =  ImageTk.PhotoImage(noised_watermark)
    noised_watermark_button = Button(third_frame,image=noised_watermark,borderwidth=1,relief=RIDGE,width=280,height=280)
    noised_watermark_button.grid(column=1,row=0,padx=5,pady=5)
    # MSE_PSNR()
    

noised_watermark = Image.open('gui/noised_watermarked_icon.jpg')
noised_watermark = noised_watermark.resize((280,280), Image.ANTIALIAS)
noised_watermark =  ImageTk.PhotoImage(noised_watermark)
watermark_button = Button(third_frame,image=noised_watermark,borderwidth=1,relief=RIDGE,width=280,height=280)
watermark_button.grid(column=1,row=0,padx=5)

recover_cover_icon = Image.open('gui/watermarked_icon.jpg')
recover_cover_icon = recover_cover_icon.resize((280,280), Image.ANTIALIAS)
recover_cover_icon =  ImageTk.PhotoImage(recover_cover_icon)
recovere_cover_button = Button(third_frame,image=recover_cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
recovere_cover_button.grid(column=2,row=0,padx=5)

recover_watermark_icon = Image.open('gui/noised_watermarked_icon.jpg')
recover_watermark_icon = recover_watermark_icon.resize((280,280), Image.ANTIALIAS)
recover_watermark_icon =  ImageTk.PhotoImage(recover_watermark_icon)
recover_watermark_button = Button(third_frame,image=recover_watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
recover_watermark_button.grid(column=3,row=0,padx=5)

third_sub_frame = ttk.Frame(third_frame)
third_sub_frame.columnconfigure(0, weight=1)
third_sub_frame.grid(row=0,column=4)

add_watermark_cover = Button(third_sub_frame,command=add_watermark,text='Add Watermark',font=('Candara Light',16),width=16)
add_watermark_cover.grid(column=0,row=0,padx=5)

third_sub_sub_frame = ttk.Frame(third_sub_frame)
third_sub_sub_frame.columnconfigure(0, weight=1)
third_sub_sub_frame.grid(row=1,column=0)

noise_text = Button(third_sub_sub_frame,command=add_noise,text='Add Noise',font=('Candara Light',10),width=10)
noise_text.grid(column=0,row=0)
noise_var = StringVar(third_sub_sub_frame)
noise_var.set(noise_list[0]) # default value
noise_selected = OptionMenu(third_sub_sub_frame,noise_var,*noise_list)
noise_selected.grid(column=1,row=0)

rotate_text = Button(third_sub_sub_frame,command=rotate_watermark,text='Rotate',font=('Candara Light',10),width=10)
rotate_text.grid(column=0,row=1)
rotate_var = StringVar(third_sub_sub_frame)
rotate_var.set(rotate_list[0]) # default value
rotate_selected = OptionMenu(third_sub_sub_frame,rotate_var,*rotate_list)
rotate_selected.grid(column=1,row=1)

crop_text = Button(third_sub_sub_frame,command=crop_watermark,text='Crop',font=('Candara Light',10),width=10)
crop_text.grid(column=0,row=2)
crop_var = StringVar(third_sub_sub_frame)
crop_var.set(crop_list[0]) # default value
crop_selected = OptionMenu(third_sub_sub_frame,crop_var,*crop_list)
crop_selected.grid(column=1,row=2)


remove_watermark_cover = Button(third_sub_frame,command=remove_watermark,text=' Remove Watermark',font=('Candara Light',16))
remove_watermark_cover.grid(column=0,row=4,padx=5)

extract_watermark_cover = Button(third_sub_frame,command=extract_watermark,text=' Extract Watermark',font=('Candara Light',16))
extract_watermark_cover.grid(column=0,row=5,padx=5)


# second main tab
graph_frame = ttk.Frame(main_notebook)
graph_frame.columnconfigure(0, weight=1)
graph_frame.grid(row=0,column=0)
graph_output = PhotoImage(file='gui/output.png',width=810)
graph_button = Button(graph_frame,image=graph_output,borderwidth=0,relief=RIDGE)
graph_button.grid(column=0,row=0)

main_notebook.add(main_frame,text='Main')
main_notebook.add(graph_frame,text='Graph')

window.mainloop()