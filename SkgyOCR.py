from tkinter import * 
from tkinter import messagebox
import cv2
import pytesseract
from pytesseract import Output
from tkinter import filedialog
import os.path
import tkinter  as tk
from PIL import Image 
import re

 
number_word =0
number_line =0
#----------------Define---------- 
def imo():
    file = filedialog.askopenfile(mode='r' ,filetypes =[('JPG and PNG Files',['*.jpg','*.png' ]) ] )
    if file:
        filepath =os.path.abspath(file.name)
        En1.delete(0,END)
        En1.insert(0,filepath) 
     
def OCR():     
    
    file =En1.get()
    if  not (file):
        messagebox.showwarning('Warning' ,'\n Select image ')
    else:  
        saveo =En2.get()         
        if  (saveo):
            image = Image.open(file)
            text = OCRextract(file,image,l["text"] )#pytesseract.image_to_string(image)
            with open(saveo, "w") as f:
                f.write(text)
                f.close()
            t1.delete(1.0,END)
            t1.insert(tk.END,text)
            messagebox.showinfo('File saved' ,'\n File saved')

        else:
            messagebox.showwarning('Warning' ,'\n set save path')

def OCRextract(file , img, mod):      
    texts =''
    number_word =0
    number_line  = 0
    
   
    img2 = cv2.imread(file) 
    if (mod != 'All'):
        if (mod == 'Number'):
           date_pattern = '^([0-9])'    

        if (mod == 'Character'):
           date_pattern = '^([0-9]|[a-z]|[A-Z])'        

        if (mod == 'Date'):
           date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'           
      
        if (mod == 'Upper Case'):
           date_pattern = '^([A-Z])'           

        if (mod == 'Lower Case'):
           date_pattern = '^([a-z])'
           
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['text'])
        ytemp= -1
        for i  in range(n_boxes):
            #number_line = number_line +1
            if re.match(date_pattern, d['text'][i]):
                if int(float(d['conf'][i])) > 60:           
                    
                   number_word = number_word +1
                   (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                   
                   img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                   if (ytemp > (y-5)) and (ytemp<(y+5)):
                      texts  = texts + " " +d['text'][i] 
                   else:                      
                      texts  = texts +"\n" +d['text'][i]
                      number_line = number_line +1

                   ytemp  = y   
                     
                      
            #if int(float(d['conf'][i])) < 60:           
            #       texts  = texts +"\n"            

    if (mod == 'All'):
       texts = pytesseract.image_to_string(img)
       number_word = len(texts.split())  
       number_line = len(texts.splitlines()) 
	          
    l2.config( text = number_line )     
    l4.config( text = number_word  ) 
    cv2.imshow('img2', img2)
    cv2.waitKey(0)

    return  texts
    

def print_selection():
    l.config(text = 'All')
    if (var1.get() == 1):
        l.config(text = 'All')
    if (var2.get() == 1):
        l.config(text = 'Character')
    if (var3.get() == 1):
        l.config(text = 'Number')
    if (var4.get() == 1):
        l.config(text = 'Date')
    if (var5.get() == 1):
        l.config(text = 'Upper Case')
    if (var6.get() == 1):
        l.config(text = 'Lower Case')     
#----------------Tools-----------

window1 =Tk()
window1.geometry('1082x812+100+100')
window1.title('Text extracotr system')
window1.resizable(False, False)
 
window1.configure(bg ='White')

window1.iconbitmap( 'images/logoIcon.ico')
logo = PhotoImage(file = 'images/OCRapp2.png')
logo_label =Label(window1 , image=logo)
logo_label.place(x=0, y=0)

 
F0 =Frame(window1 ,width=200,height =130 ,bg='#4F81BD' ,bd=1 ,relief=SOLID)
F0.place(x=20, y=290)

F1 =Frame(window1 ,width=835,height =130 ,bg='#4F81BD' ,bd=1 ,relief=SOLID)
F1.place(x=230, y=290)

F2 =Frame(window1 ,width=305,height =200 ,bg='#4F81BD' ,bd=1 ,relief=SOLID)
F2.place(x=20, y=440)
F3 =Frame(window1 ,width=705,height =200 ,bg='#4F81BD' ,bd=1 ,relief=SOLID)
F3.place(x=360, y=440)



En1_text = Label(F0 ,text ='Image path: ', fg ='black' , bg ='white' , font=('times for roman',13 ,'bold')  )
En1_text.place(x=20, y=30)

En2_text = Label(F0 ,text ='Save path(*.txt): ', fg ='black' , bg ='white' , font=('times for roman',13 ,'bold')  )
En2_text.place(x=20, y=80)

En1 = Entry(F1, font=('times for roman',16 ,'bold'), width =67 ,bd=1 ,relief=SOLID)
En1.place(x=20, y=26)

brn1 =Button(F1, text='+' ,cursor = 'hand2' , width =3 , command =imo)
brn1.place(x=800, y=27)

En2 = Entry(F1, font=('times for roman',16 ,'bold'), width =67 ,bd=1 ,relief=SOLID)
En2.place(x=20, y=78)


var1 =tk.IntVar()
var2 =tk.IntVar()
var3 =tk.IntVar()
var4 =tk.IntVar()
var5 =tk.IntVar()
var6 =tk.IntVar()
c0 = Checkbutton(F2, text ='All', variable=  var1, onvalue=1 , offvalue=0 , command =print_selection )
c0.place(x=30, y=25)
c1 = Checkbutton(F2, text ='Character',  variable=  var2 ,  onvalue=1 , offvalue=0, command =print_selection ) 
c1.place(x=30, y=85)
c2 = Checkbutton(F2, text ='Number',  variable=  var3 ,  onvalue=1 , offvalue=0, command =print_selection ) 
c2.place(x=30, y=145)
c3 = Checkbutton(F2, text ='Date',  variable=  var4 ,  onvalue=1 , offvalue=0, command =print_selection ) 
c3.place(x=180, y=25)
c4 = Checkbutton(F2, text ='Upper Case',  variable=  var5 ,  onvalue=1 , offvalue=0, command =print_selection ) 
c4.place(x=180, y=85)
c5 = Checkbutton(F2, text ='Lower Case',  variable=  var6 ,  onvalue=1 , offvalue=0, command =print_selection ) 
c5.place(x=180, y=145)

F4 =Frame(F3 ,width=330,height =145   ,bg="#90b743" ,bd=1 ,relief=SOLID)
F4.place(x=20, y=40)




t1 = Text(F4,  width =78 ,height =9 ,fg='red' , font=('times for roman',10  ) )
t1.place(x=20, y=40)
scroll_y = tk.Scrollbar( F4 ,  orient ='vertical',command =t1.yview)
scroll_y.pack(side ="right" ,expand =True, fill ="y")
#t1.configure( yscrollcommand  =scroll_y.set)
t1.pack(side="right")
b1 = Button(F3, text='Extract' ,font=('times for roman',12 ,'bold') , width =9 ,height =7 ,fg='red' ,bg="#90b743" , cursor = 'hand2' ,command =OCR)
b1.place(x=600, y=40)



l=Label(F3,bg ='white' ,width =10 ,height =2 , text ='All')
l.config( bg="#90b743" )
l.place(x=30, y=0)

l1=Label(F3,bg ='white' ,width =14 ,height =2 , text ='Number Line')
l1.config( bg="#90b743" )
l1.place(x=130, y=0)

l2=Label(F3,bg ='white' ,width =7 ,height =2 ,fg="red" , text ='0')
l2.config( bg="#90b743" )
l2.place(x=230, y=0)

l3=Label(F3,bg ='white' ,width =14 ,height =2 , text ='Number word')
l3.config( bg="#90b743" )
l3.place(x=300, y=0)

l4=Label(F3,bg ='white' ,width =7 ,height =2 , fg="red" , text ='0')
l4.config( bg="#90b743" )
l4.place(x=400, y=0)


window1.mainloop()
 