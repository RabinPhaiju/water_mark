import cv2
from tkinter import *
from pywt import dwt2, idwt2
import matplotlib.pyplot as plt
from tkinter import ttk,filedialog
from PIL import Image,ImageTk,ImageDraw, ImageFont

window = Tk()
window.geometry("826x980")
# window.resizable(0,0)
# window.wm_iconbitmap(os.getcwd()+'/gui/icon.ico')
window.title('Watermark')

style = ttk.Style()
style.theme_use('vista')# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# global variables
result_LL,LL,LH,HL,HH,h,hh,w,ww,manipulated,xoff,yoff =None,None,None,None,None,None,None,None,None,None,None,None

pos_list = ['Center','Top Left','Top Right','Bottom Left','Bottom Right']
noise_list = ['Noise1','Noise2','Noise3','Noise4','Noise5']

cover_image_path = StringVar()
watermark_image_path = StringVar()

current_text = StringVar()
current_text.set('What it does: Add and Remove WaterMark')

# Load model
def load_model():
    print('____model loaded_____')


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
    print(file,type(file))
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
    colorText = "white"
    colorOutline = "black"
    colorBackground = "black"
    
    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+8, height*2))
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    img.save("gui/text_watermark.png")
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
second_sub_frame.grid(row=0,column=2)

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

watermark_pos_text = Label(second_sub_frame,text='Watermark Position',font=('Candara Light',16),width=16)
watermark_pos_text.grid(column=0,row=5)
pos_var = StringVar(second_sub_frame)
pos_var.set(pos_list[0]) # default value
watermark_pos = OptionMenu(second_sub_frame,pos_var,*pos_list)
watermark_pos.grid(column=0,row=6,padx=5)

# row 2
third_frame = ttk.Frame(main_frame)
third_frame.columnconfigure(0, weight=1)
third_frame.grid(row=2,column=0,pady=5)

def add_watermark():
    global result_LL,LL,LH,HL,HH,h,hh,w,ww,manipulated,xoff,yoff
    A = cv2.imread(cover_image_path.get())
    host = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    LL, (LH, HL, HH) = dwt2(host, 'haar')
    h, w = LL.shape
    
    B = cv2.imread(watermark_image_path.get())
    watermark = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    LL_w, (LH_w, HL_w, HH_w) = dwt2(watermark, 'haar')
    hh, ww = LL_w.shape
    
    # pos_list = ['Center','Top Left','Top Right','Bottom Left','Bottom Right']
    if(pos_var.get() == 'Center'):
        yoff = round((h-hh)/2)
        xoff = round((w-ww)/2)
    elif(pos_var.get() == 'Top Left'):
        yoff = 0
        xoff = 0
    elif(pos_var.get() == 'Top Right'):
        yoff = 0
        xoff = w-ww
    elif(pos_var.get() == 'Bottom Left'):
        yoff = h-hh
        xoff = 0
    elif(pos_var.get() == 'Bottom Right'):
        yoff = h-hh
        xoff = w-ww
        
    manipulated = LL_w * 0.98
    result = LL.copy()
    result[yoff:yoff+hh, xoff:xoff+ww] += manipulated
    result_LL = idwt2((result,( LH, HL, HH)), 'haar')
    cv2.imwrite('gui/watermarked.jpg', result_LL)
    upload_watermarked_image('gui/watermarked.jpg')

def upload_watermarked_image(img_path):
    global watermarked_icon
    watermarked_icon = Image.open(img_path)
    watermarked_icon = watermarked_icon.resize((280,280), Image.ANTIALIAS)
    watermarked_icon =  ImageTk.PhotoImage(watermarked_icon)
    watermarked_button = Button(third_frame,image=watermarked_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    watermarked_button.grid(column=0,row=0,padx=5,pady=5)

def extract_watermark():
    wm_LL,( m_LH, wm_HL, m_HH) = dwt2(result_LL, 'haar')
    new_LL = wm_LL - LL
    new_LL = new_LL / 0.98
    new_image = idwt2((new_LL, (LH, HL, HH)), 'haar')
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
    global recover_watermark_icon
    recover_watermark_icon = Image.open('gui/extracted_watermark.jpeg')
    recover_watermark_icon = recover_watermark_icon.resize((280,280), Image.ANTIALIAS)
    recover_watermark_icon =  ImageTk.PhotoImage(recover_watermark_icon)
    recover_watermark_button = Button(fourth_frame,image=recover_watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    recover_watermark_button.grid(column=1,row=0,padx=5,pady=5)

def remove_watermark():
    wm_LL,( m_LH, wm_HL, m_HH) = dwt2(result_LL, 'haar')
    new_LL = wm_LL.copy()
    new_LL[yoff:yoff+hh, xoff:xoff+ww] -= manipulated
    new_LL = new_LL 
    new_image = idwt2((new_LL, (LH, HL, HH)), 'haar')
    cv2.imwrite('gui/extracted_cover.jpg', new_image)
    global recover_cover_icon
    recover_cover_icon = Image.open('gui/extracted_cover.jpg')
    recover_cover_icon = recover_cover_icon.resize((280,280), Image.ANTIALIAS)
    recover_cover_icon =  ImageTk.PhotoImage(recover_cover_icon)
    recovere_cover_button = Button(fourth_frame,image=recover_cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
    recovere_cover_button.grid(column=0,row=0,padx=5,pady=5)

def add_noise():
    pass

watermarked_icon = Image.open('gui/watermarked_icon.jpg')
watermarked_icon = watermarked_icon.resize((280,280), Image.ANTIALIAS)
watermarked_icon =  ImageTk.PhotoImage(watermarked_icon)

watermarked_icon1 = Image.open('gui/noised_watermarked_icon.jpg')
watermarked_icon1 = watermarked_icon1.resize((280,280), Image.ANTIALIAS)
watermarked_icon1 =  ImageTk.PhotoImage(watermarked_icon1)

watermarked_button = Button(third_frame,image=watermarked_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
watermarked_button.grid(column=0,row=0,padx=5)

watermark_button = Button(third_frame,image=watermarked_icon1,borderwidth=1,relief=RIDGE,width=280,height=280)
watermark_button.grid(column=1,row=0,padx=5)

third_sub_frame = ttk.Frame(third_frame)
third_sub_frame.columnconfigure(0, weight=1)
third_sub_frame.grid(row=0,column=2)

add_watermark_cover = Button(third_sub_frame,command=add_watermark,text='Add Watermark',font=('Candara Light',16),width=16)
add_watermark_cover.grid(column=0,row=0,padx=5)

noise_text = Label(third_sub_frame,text='Choose Noise',font=('Candara Light',16),width=16)
noise_text.grid(column=0,row=1)
noise_var = StringVar(third_sub_frame)
noise_var.set(noise_list[0]) # default value
watermark_pos = OptionMenu(third_sub_frame,noise_var,*noise_list)
watermark_pos.grid(column=0,row=2,padx=5)

add_noise_cover = Button(third_sub_frame,command=add_noise,text=' Add Noise',font=('Candara Light',16),width=17)
add_noise_cover.grid(column=0,row=3,padx=5)

remove_watermark_cover = Button(third_sub_frame,command=remove_watermark,text=' Remove Watermark',font=('Candara Light',16))
remove_watermark_cover.grid(column=0,row=4,padx=5)

extract_watermark_cover = Button(third_sub_frame,command=extract_watermark,text=' Extract Watermark',font=('Candara Light',16))
extract_watermark_cover.grid(column=0,row=5,padx=5)



# row 4
fourth_frame = ttk.Frame(main_frame)
fourth_frame.columnconfigure(0, weight=1)
fourth_frame.grid(row=3,column=0,pady=5)

recover_cover_icon = Image.open('gui/watermarked_icon.jpg')
recover_cover_icon = recover_cover_icon.resize((280,280), Image.ANTIALIAS)
recover_cover_icon =  ImageTk.PhotoImage(recover_cover_icon)

recover_watermark_icon = Image.open('gui/noised_watermarked_icon.jpg')
recover_watermark_icon = recover_watermark_icon.resize((280,280), Image.ANTIALIAS)
recover_watermark_icon =  ImageTk.PhotoImage(recover_watermark_icon)

recovere_cover_button = Button(fourth_frame,image=recover_cover_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
recovere_cover_button.grid(column=0,row=0,padx=5)

recover_watermark_button = Button(fourth_frame,image=recover_watermark_icon,borderwidth=1,relief=RIDGE,width=280,height=280)
recover_watermark_button.grid(column=1,row=0,padx=5)

recover_text = Label(fourth_frame,text='________________________',font=('Candara Light',16),width=16)
recover_text.grid(column=2,row=0)

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