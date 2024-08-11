from tkinter import *
from customtkinter import *
from PIL import Image
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f=''
flag=''
flags=''

login=sqlite3.connect("admin.db")
l=login.cursor()    

c=sqlite3.connect("medicine.db")
cur=c.cursor()

columns=('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')

def open_win(): #OPENS MAIN MENU----------------------------------------------------------------------------MAIN MENU
    global apt, flag
    flag = 'apt'

    apt = CTk()
    set_appearance_mode("dark")
    apt.geometry("800x480")  # Adjusted width to accommodate sidebar
    apt.title("Main Menu")

    set_appearance_mode("light")
    # Sidebar setup
    sidebar_frame = CTkFrame(master=apt, fg_color="#ffffff",  width=200, height=650, corner_radius=10)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("Uz.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150, 100))
    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    text_label = CTkLabel(master=sidebar_frame, text="\nDBMS Project\nPharmacy Managment System\n\n\nMembers\n\nZain-ul-Wara [2022F-BCS-071]\n Ushna-Zia [2022F-BCS-285]", 
                          font=("Gotham Ultra", 12), text_color="#000000")
    text_label.pack(pady=(2, 0), anchor="center")
    
    # Main frame setup
    main_frame = CTkFrame(master=apt, fg_color="#121317")
    main_frame.pack(side="left", fill="both", expand=True)

    CTkLabel(main_frame, text="UZ Pharmacy Management", font=("Gotham Ultra", 24), text_color="#ffffff").grid(row=0, column=0, columnspan=3, pady=(20, 10))
    CTkLabel(main_frame, text=(' ' * 5)+('*' * 105), font=("Gotham Ultra", 12), text_color="#ffffff").grid(row=1, column=0, columnspan=3)
    CTkLabel(main_frame, text=(' ' * 5)+('-' * 115), font=("Gotham Ultra", 12), text_color="#ffffff").grid(row=3, column=0, columnspan=6) 

    CTkLabel(main_frame, text="Stock Maintenance", font=("Gotham Ultra", 16), text_color="#ffffff").grid(row=2, column=0, pady=(10, 10))
    CTkButton(main_frame, text='New Customer', width=100, command=val_cus, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=4, column=0, pady=(5, 5))
    CTkButton(main_frame, text='Add product to Stock', width=100, command=stock, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=5, column=0, pady=(5, 5))
    CTkButton(main_frame, text='Delete product from Stock', width=100, command=delete_stock, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=6, column=0, pady=(5, 5))

    CTkLabel(main_frame, text="Access Database", font=("Gotham Ultra", 16), text_color="#ffffff").grid(row=2, column=1, pady=(10, 10))
    CTkButton(main_frame, text='Modify', width=100, command=modify, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=4, column=1, pady=(5, 5))
    CTkButton(main_frame, text='Search', width=100, command=search, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=5, column=1, pady=(5, 5))
    CTkButton(main_frame, text="Check Today's Revenue", command=show_rev, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=6, column=1, pady=(5, 5))

    CTkLabel(main_frame, text="Handle Cash Flows", font=("Gotham Ultra", 16), text_color="#ffffff").grid(row=2, column=2, pady=(10, 10))
    CTkButton(main_frame, text='Expiry Check', width=100, command=exp_date, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=5, column=2, pady=(5, 5))
    CTkButton(main_frame, text='Billing', width=100, command=billing, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=4, column=2, pady=(5, 5))

    CTkLabel(main_frame, text='-' * 80, font=("Gotham Ultra", 12), text_color="#ffffff").grid(row=12, column=0, columnspan=3)
    CTkButton(main_frame, text='Logout', command=again, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=13, column=1)

    apt.mainloop()

def delete_stock():  # OPENS DELETE WINDOW
    global cur, c, flag, lb1, d, selected_product_label
    apt.destroy()
    flag = 'd'
    d = CTk()
    set_appearance_mode("dark")
    d.geometry("600x400")
    d.title("Delete a product from Stock")

    # Header
    CTkLabel(d, text="Delete a product from Stock", font=("Gotham Ultra", 20), text_color="#ffffff").grid(row=0, column=0, columnspan=4, pady=(20, 10))
    
    # Product Entry
    CTkLabel(d, text='Select a Product & Press to delete:', font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=1, column=1, pady=(10, 10))
    
    # Product Details
    CTkLabel(d, text='Product', font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=2, column=0, pady=(10, 10))
    CTkLabel(d, text='Qty.   Exp.dt.   Cost', font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=2, column=1, pady=(10, 10))
    
    ren()
    
    # Buttons
    CTkButton(d, text='Delete', command=delt, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=3, column=3, pady=(20, 10))
    CTkButton(d, text='Main Menu', command=main_menu, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=4, column=3, pady=(20, 10))
    
    # Selected Product Label
    selected_product_label = CTkLabel(d, text='', font=("Gotham Ultra", 14), text_color="#ffffff")
    selected_product_label.grid(row=0, column=1, pady=(20, 10))

    d.mainloop()

def ren():
    global lb1, d, cur, c, lb2
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
    def onmousewheel(event):
        lb1.yview('scroll', event.delta, 'units')
        lb2.yview('scroll', event.delta, 'units')
        return 'break'
    
    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N+S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("select * from med")
    for i in cur:
        cx += 1
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[6]), str(i[4])]
        lb1.insert(cx, '. '.join(s1))
        lb2.insert(cx, '   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)

def sel_del(e):
    global lb1, d, cur, c, p, sl2, selected_product_label
    p = lb1.curselection()
    x = 0
    sl2 = ''
    cur.execute("select * from med")
    for i in cur:
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    cur.execute('Select * from med')
    for i in cur:
        if i[0] == sl2:
            selected_product_label.configure(text=i[0] + '. ' + i[1])
    c.commit()

    
def delt():
    global p,c,cur,d
    cur.execute("delete from med where sl_no=?",(sl2,))
    c.commit()
    ren()

def modify():    # window for modification-----------------------------------------------------------------------MODIFY
    global cur, c, accept, flag, att, up, n, name_, apt, st, col,col_n
    col=('', 'name', 'type', 'qty_left', 'cost', 'purpose', 'expdt', 'loc', 'mfg')
    col_n=('', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
    flag='st'
    name_=''
    apt.destroy()
    n=[]
    cur.execute("select * from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    st=CTk()
    set_appearance_mode("dark")
    st.title('MODIFY')
    CTkLabel(st, text='-'*48+' MODIFY DATABASE '+'-'*48, font=("Gotham Ultra", 14), text_color="#ededed").grid(row=0, column=0,columnspan=6)
    def onvsb(*args):
        name_.yview(*args)
    def onmousewheel():
        name_.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    vsb.grid(row=1,column=3,sticky=N+S)
    name_=Listbox(st,width=43,yscrollcommand=vsb.set)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        name_.insert(cx,(str(i[0])+'.  '+str(i[1])))
        name_.grid(row=1,column=1,columnspan=2)
    c.commit()
    name_.bind('<MouseWheel>',onmousewheel)
    name_.bind('<<ListboxSelect>>', sel_mn)

    CTkLabel(st, text='Enter Medicine Name: ', font=("Gotham Ultra", 14), text_color="#ededed").grid(row=1, column=0)
    CTkLabel(st, text='Enter changed Value of: ', font=("Gotham Ultra", 14), text_color="#ededed").grid(row=2, column=0)
    att=Spinbox(st, values=col_n)
    att.grid(row=2, column=1)
    up=Entry(st)
    up.grid(row=2, column=2)
    CTkButton(st,width=10,text='Submit', command=save_mod, fg_color="#e04a32", hover_color="#e04a32").grid(row=2, column=4)
    CTkButton(st,width=10,text='Reset', command=res, fg_color="#e04a32", hover_color="#e04a32").grid(row=2, column=5)
    CTkButton(st,width=10,text='Show data', command=show_val,fg_color="#e04a32", hover_color="#e04a32").grid(row=1, column=4)
    CTkLabel(st, text='-'*120, font=("Gotham Ultra", 14), text_color="#ededed").grid(row=3,column=0,columnspan=6)
    CTkButton(st,width=10,text='Main Menu',command=main_menu, fg_color="#e04a32", hover_color="#e04a32").grid(row=5,column=5)
    st.mainloop()

def res():
    global st, up
    up=Entry(st)
    up.grid(row=2, column=2)
    Label(st,width=20, text='                         ').grid(row=5,column=i)

def sel_mn(e):
    global n,name_, name_mn, sl, c, cur
    name_mn=''
    p=name_.curselection()
    print (p)
    x=0
    sl=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl=i[0]
            break
        x+=1
    c.commit()
    print (sl)
    name_nm=n[int(sl)]
    print (name_nm)
    
def show_val():
    global st, name_mn, att, cur, c, col, col_n, sl
    for i in range(3):
        Label(st,width=20, text='                         ').grid(row=5,column=i)
    cur.execute("select * from med")
    for i in cur:
        for j in range(9):
            if att.get()==col_n[j] and sl==i[0]:
                Label(st, text=str(i[0])).grid(row=5,column=0)
                Label(st, text=str(i[1])).grid(row=5,column=1)
                Label(st, text=str(i[j])).grid(row=5,column=2)
    c.commit()

def save_mod(): #save modified data
    global cur, c, att, name_mn, st, up, col_n, sl
    for i in range(9):
        if att.get()==col_n[i]:
            a=col[i]
    sql="update med set '%s' = '%s' where sl_no = '%s'" % (a,up.get(),sl)
    cur.execute(sql)
    c.commit()
    Label(st, text='Updated!').grid(row=5,column=4)
    
    
def stock():    #add to stock window------------------------------------------------------------------------ADD TO STOCK
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag='sto'
    accept=['']*10
    sto=CTk()
    set_appearance_mode("dark")
    sto.title('STOCK ENTRY')
    CTkLabel(sto, text='ENTER NEW PRODUCT DATA TO THE STOCK', font=("Gotham Ultra", 14), text_color="#ededed").grid(row=0, column=0, columnspan=4, sticky='nsew')

    CTkLabel(sto,text=(' '*20)+('-'*70), font=("Gotham Ultra", 14), text_color="#ededed").grid(row=1,column=0,columnspan=2)
    for i in range(1,len(columns)):
        CTkLabel(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':', font=("Gotham Ultra", 11), text_color="#ededed").grid(row=i+2,column=0)
        accept[i]=CTkEntry(sto,width=220)
        accept[i].grid(row=i+2, column=1)
    CTkButton(sto,width=15,text='Submit',command=submit, fg_color="#e04a32", hover_color="#e04a32").grid(row=12,column=1)
    CTkLabel(sto,text='-'*165, font=("Gotham Ultra", 14), text_color="#ededed").grid(row=13,column=0,columnspan=7)
    CTkButton(sto,width=15,text='Reset',command=reset, fg_color="#e04a32", hover_color="#e04a32").grid(row=12,column=0)
    CTkButton(sto,width=15,text='Refresh stock',command=ref, fg_color="#e04a32", hover_color="#e04a32").grid(row=12,column=4)
    for i in range(1,6):
        CTkLabel(sto,text=columns[i]).grid(row=14,column=i-1)
    CTkLabel(sto,text='Exp           Rack   Manufacturer                      ').grid(row=14,column=5)
    CTkButton(sto,width=10,text='Main Menu',command=main_menu, fg_color="#e04a32", hover_color="#e04a32").grid(row=12,column=5)
    ref()
    sto.mainloop()

def ref(): # creates a multi-listbox manually to show the whole database 
    global sto, c, cur
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        lb3.ywiew=('scroll',event.delta,'units')
        lb4.ywiew=('scroll',event.delta,'units')
        lb5.ywiew=('scroll',event.delta,'units')
        lb6.ywiew=('scroll',event.delta,'units')
        
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(sto,yscrollcommand=vsb.set)
    lb2=Listbox(sto,yscrollcommand=vsb.set)
    lb3=Listbox(sto,yscrollcommand=vsb.set,width=10)
    lb4=Listbox(sto,yscrollcommand=vsb.set,width=7)
    lb5=Listbox(sto,yscrollcommand=vsb.set,width=25)
    lb6=Listbox(sto,yscrollcommand=vsb.set,width=37)
    vsb.grid(row=15,column=6,sticky=N+S)
    lb1.grid(row=15,column=0)
    lb2.grid(row=15,column=1)
    lb3.grid(row=15,column=2)
    lb4.grid(row=15,column=3)
    lb5.grid(row=15,column=4)
    lb6.grid(row=15,column=5)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    lb3.bind('<MouseWheel>',onmousewheel)
    lb4.bind('<MouseWheel>',onmousewheel)
    lb5.bind('<MouseWheel>',onmousewheel)
    lb6.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        seq=(str(i[0]),str(i[1]))
        lb1.insert(cx,'. '.join(seq))
        lb2.insert(cx,i[2])
        lb3.insert(cx,i[3])
        lb4.insert(cx,i[4])
        lb5.insert(cx,i[5])
        lb6.insert(cx,i[6]+'    '+i[7]+'    '+i[8])
    c.commit()

def reset():
    global sto, accept
    for i in range(1,len(columns)):
        CTkLabel(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':', font=("Arial Bold", 11), text_color="#601E88").grid(row=i+2,column=0)
        accept[i]=CTkEntry(sto,width=220)
        accept[i].grid(row=i+2, column=1)
    
def submit(): #for new stock submission
    global accept, c, cur, columns, sto
    x=['']*10
    cur.execute("select * from med")
    for i in cur:
        y=int(i[0])
    for i in range(1,9):
        x[i]=accept[i].get()
    sql="insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (y+1,x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()
    top=CTk()
    set_appearance_mode("dark")
    CTkLabel(top,width=20, text='Success!', font=("Arial Bold", 25)).pack()
    top.mainloop()
    main_menu()

def chk(): #checks if the medicine is already present so that can be modified
    global cur, c, accept, sto
    cur.execute("select * from med")
    for i in cur:
        if accept[6].get()==i[6] and i[1]==accept[1].get():
            sql="update med set qty_left = '%s' where name = '%s'" % (str(int(i[3])+int(accept[3].get())),accept[1].get())
            cur.execute(sql)
            c.commit()
            top=Tk()
            Label(top,width=20, text='Modified!').pack()
            top.mainloop()
            main_menu()
        else:
            submit()
    c.commit()

def exp_date(): # expiry window open-----------------------------------------------------------------------------EXPIRY
    global exp, s,c, cur, flag, apt, flags
    apt.destroy()
    flag='exp'
    from datetime import date
    now=time.localtime()
    n=[]
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    exp=CTk()
    set_appearance_mode("dark")
    exp.geometry("450x450")
    exp.title('EXPIRY CHECK')
    CTkLabel(exp,text='Today : '+str(now[2])+'/'+str(now[1])+'/'+str(now[0]), font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=0, column=0, columnspan=3)
    CTkLabel(exp,text='Selling Expired Medicines and Drugs is Illegal', font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=1, column=0,columnspan=3)
    CTkLabel(exp,text='-'*80, font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=2, column=0,columnspan=3)
    s=Spinbox(exp,values=n)
    s.grid(row=3, column=0)
    CTkButton(exp,text='Check Expiry date', command=s_exp, fg_color="#e04a32", hover_color="#e04a32").grid(row=3, column=1)
    CTkLabel(exp,text='-'*80, font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=4, column=0,columnspan=3)
    if flags=='apt1':
        CTkButton(exp,text='Main Menu', command=main_cus, fg_color="#e04a32", hover_color="#e04a32").grid(row=5, column=2)
    else:
        CTkButton(exp,width=20,text='Check Products expiring', command=exp_dt, fg_color="#e04a32", hover_color="#e04a32").grid(row=5, column=0)
        CTkButton(exp,text='Main Menu', command=main_menu,fg_color="#e04a32", hover_color="#e04a32").grid(row=5, column=2)
    exp.mainloop()

def s_exp():    # shows the expiry date of the medicine entered
    global c, cur, s, exp, top
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if(i[1]==s.get()):
            q=i[6]
            d2=date(int('20'+q[8:10]),int(q[3:5]),int(q[0:2]))
            if d1>d2:
                Label(exp, text='EXPIRED! on '+i[6]).grid(row=3, column=2)
                top=Tk()
                Label(top, text='EXPIRED!').pack()
            else:
                Label(exp, text=i[6]).grid(row=3, column=2)
    c.commit()

def exp_dt(): # shows medicine to expire in the coming week
    global c, cur, exp, top
    x=0
    z=1
    from datetime import datetime, timedelta 
    N = 7
    dt = datetime.now() + timedelta(days=N)
    d=str(dt)
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    d3 = date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    Label(exp,text='S.No'+'   '+'Name'+'     Qty.    '+'Exp_date').grid(row=6,column=0,columnspan=2)
    cur.execute("select * from med")
    for i in cur:
        s=i[6]
        d2=date(int('20'+s[8:10]),int(s[3:5]),int(s[0:2]))
        
        if d1<d2<d3:
            Label(exp,text=str(z)+'.      '+str(i[1])+'    '+str(i[3])+'    '+str(i[6])).grid(row=x+7,column=0,columnspan=2)
            x+=1
            z+=1
        elif d1>d2:
            top=Tk()
            Label(top,width=20, text=str(i[1])+' is EXPIRED!').pack()
    c.commit()
    
def billing(): # to create bills for customer-------------------------------------------------------------BILLING system
    global c, cur, apt, flag, t, name, name1, add, st, names, qty, sl, qtys, vc_id, n, namee, lb1
    t=0
    vc_id=''
    names=[]
    qty=[]
    sl=[]
    n=[]
    qtys=['']*10
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    if flag=='st':
        st.destroy()
    else:
        apt.destroy()
    flag='st'
    st=CTk()
    set_appearance_mode("dark")
    st.title('BILLING SYSTEM')
    CTkLabel(st,text='-'*48+'BILLING SYSTEM'+'-'*49,font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=0,column=0,columnspan=7)
    CTkLabel(st,text='Enter Name: ',font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=1,column=0)
    name1=CTkEntry(st)
    name1.grid(row=1, column=1)
    CTkLabel(st,text='Enter Address: ',font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=2,column=0)
    add=CTkEntry(st)
    add.grid(row=2, column=1)
    CTkLabel(st,text="Value Id (if available): ",font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=3, column=0)
    vc_id=CTkEntry(st)
    vc_id.grid(row=3, column=1)
    CTkButton(st,text='Check V.C.', command=blue,fg_color="#e04a32", hover_color="#e04a32").grid(row=4, column=0)
    CTkLabel(st,text='-'*115,font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=6, column=0,columnspan=7)
    CTkLabel(st,text='SELECT PRODUCT',width=25,font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=7, column=0)
    CTkLabel(st,text=' RACK  QTY LEFT     COST          ',width=25,font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=7, column=1)
    CTkButton(st,text='Add to bill',width=15,command=append2bill, fg_color="#e04a32", hover_color="#e04a32").grid(row=8, column=6)
    CTkLabel(st,text='QUANTITY',width=20,font=("Gotham Ultra", 14), text_color="#ffffff").grid(row=7, column=5)
    qtys=CTkEntry(st)
    qtys.grid(row=8,column=5)
    refresh()
    CTkButton(st,width=15,text='Main Menu', command=main_menu, fg_color="#e04a32", hover_color="#e04a32").grid(row=1,column=6)
    CTkButton(st,width=15,text='Refresh Stock', command=refresh, fg_color="#e04a32", hover_color="#e04a32").grid(row=3,column=6)
    CTkButton(st,width=15,text='Reset Bill', command=billing, fg_color="#e04a32", hover_color="#e04a32").grid(row=4,column=6)
    CTkButton(st,width=15,text='Print Bill', command=print_bill, fg_color="#e04a32", hover_color="#e04a32").grid(row=5,column=6)
    CTkButton(st,width=15,text='Save Bill', command=make_bill, fg_color="#e04a32", hover_color="#e04a32").grid(row=7,column=6)
    
    st.mainloop()

def refresh():
    global cur, c, st, lb1, lb2, vsb
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(st,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(st ,width=25,yscrollcommand=vsb.set)
    vsb.grid(row=8,column=2,sticky=N+S)
    lb1.grid(row=8,column=0)
    lb2.grid(row=8,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        lb1.insert(cx,str(i[0])+'. '+str(i[1]))
        lb2.insert(cx,' '+str(i[7])+'        '+str(i[3])+'             Rs '+str(i[4]))
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)

def select_mn(e): #store the selected medicine from listbox
    global st, lb1, n ,p, nm, sl1
    p=lb1.curselection()
    x=0
    sl1=''
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if x==int(p[0]):
            sl1=int(i[0])
            break
        x+=1    
    c.commit()
    print (sl1)
    nm=n[x]
    print (nm)
    
def append2bill(): # append to the bill
    global st, names, nm , qty, sl,cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print (qty)
    print (sl[len(sl)-1],names[len(names)-1],qty[len(qty)-1])
    
def blue(): # check if valued customer
    global st ,c, cur, named, addd, t, vc_id
    cur.execute("select * from cus")
    for i in cur:
        if vc_id.get()!='' and int(vc_id.get())==i[2]:
            named=i[0]
            addd=i[1]
            Label(st,text=named,width=20).grid(row=1, column=1)
            Label(st,text=addd,width=20).grid(row=2, column=1)
            Label(st,text=i[2],width=20).grid(row=3, column=1)
            Label(st, text='Valued Customer!').grid(row=4, column=1)
            t=1
            break
    c.commit()

def make_bill(): # makes bill
    global t, c, B, cur, st, names, qty, sl , named, addd, name1, add,det, vc_id
    price=[0.0]*10
    q=0
    det=['','','','','','','','']
    det[2]=str(sl)
    for i in range(len(sl)):
        print (sl[i],' ',qty[i],' ',names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?",(sl[k],))
        for i in cur:
            price[k]=int(qty[k])*float(i[4])
            print (qty[k],price[k])
            cur.execute("update med set qty_left=? where sl_no=?",(int(i[3])-int(qty[k]),sl[k]))
        c.commit()
    det[5]=str(random.randint(100,999))
    B='bill_'+str(det[5])+'.txt'
    total=0.00
    for i in range(10):
        if price[i] != '':
            total+=price[i] #totalling
    m='\n\n\n'
    m+="==========================================\n"
    m+="                                  No :%s\n\n" % det[5]
    m+="          UZ Pharmacy                       \n"
    m+=" Karachi City / Sir Syed University \n\n"
    m+="-----------------------------------------------\n"
    if t==1:
        m+="Name: %s\n" % named
        m+="Address: %s\n" % addd
        det[0]=named
        det[1]=addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0]==named:
                det[7]=i[2]
    else:
        m+="Name: %s\n" % name1.get()
        m+="Address: %s\n" % add.get()
        det[0]=name1.get()
        det[1]=add.get()
    m+="-----------------------------------------------\n"
    m+="Product                      Qty.       Price\n"
    m+="-----------------------------------------------\n"#47, qty=27, price=8 after 2
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1=' '
            s1=(names[i]) + (s1 * (27-len(names[i]))) + s1*(3-len(qty[i])) +qty[i]+ s1*(15-len(str(price[i])))+str(price[i]) + '\n'
            m+=s1
    m+="\n-----------------------------------------------\n"
    if t==1:
        ntotal=total*0.8
        m+='Total'+(' '*25)+(' '*(15-len(str(total)))) + str(total)+'\n'
        m+="Valued customer Discount"+ (' '*(20-len(str(total-ntotal))))+'-'+str(total-ntotal)+'\n'
        m+="-----------------------------------------------\n"
        m+='Total'+(' '*25)+(' '*(12-len(str(ntotal)))) +'Rs '+ str(ntotal)+'\n'
        det[3]=str(ntotal)
    else:
        m+='Total'+(' '*25)+(' '*(12-len(str(total)))) +'Rs '+ str(total)+'\n'
        det[3]=str(total)
        
    m+="-----------------------------------------------\n\n"
    m+="Dealer 's signature:___________________________\n"
    m+="===============================================\n"
    print (m)
    p=time.localtime()
    det[4]=str(p[2])+'/'+str(p[1])+'/'+str(p[0])
    det[6]=m
    bill=open(B,'w')
    bill.write(m)
    bill.close()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',(det[0],det[1],det[2],det[3],det[4],det[5],det[6],det[7]))
    c.commit()
    
def print_bill():
    win32api.ShellExecute (0,"print",B,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
    
def show_rev(): # opens revenue window-----------------------------------------------------------------------TOTAL REVENUE
    global c, cur, flag,rev
    apt.destroy()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    flag='rev'
    rev=CTk()
    set_appearance_mode("dark")
    rev.title("Todays Revenue~")
    total=0.0
    today=str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])
    CTkLabel(rev,text='Today: '+today, font=("Arial Bold", 14), text_color="#601E88").grid(row=0,column=0)
    cur.execute('select * from bills')
    for i in cur:
        if i[4]==today:
            total+=float(i[3])
    print (total)
    Label(rev,width=22,text='Total revenue: Rs '+str(total), bg='black',fg='white').grid(row=1,column=0)
    cx=0
    vsb=Scrollbar(orient='vertical')
    lb1=Listbox(rev,width=25, yscrollcommand=vsb.set)
    vsb.grid(row=2,column=1,sticky=N+S)
    lb1.grid(row=2,column=0)
    vsb.config( command = lb1.yview )
    cur.execute("select * from bills")
    for i in cur:
        if i[4]==today:
            cx+=1
            lb1.insert(cx,'Bill No.: '+str(i[5])+'    : Rs '+str(i[3]))
    c.commit()
    Button(rev,text='Main Menu',command=main_menu).grid(row=15,column=0)
    rev.mainloop()


def search():   #search window medicine and symptom details---------------------------------SEARCH MEDICINE RACK & SYMPTOMS
    global c, cur, flag, st, mn, sym, flags
    flag='st'
    apt.destroy()
    cur.execute("Select * from med")
    symp=['nil']
    med_name=['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st=CTk()
    set_appearance_mode("dark")
    st.title('SEARCH')
    CTkLabel(st, text=' SEARCH FOR MEDICINE ',font=("Gotham Ultra", 14), text_color="#ededed").grid(row=0, column=0,columnspan=3)
    CTkLabel(st, text='~'*40,font=("Gotham Ultra", 14), text_color="#ededed").grid(row=1, column=0,columnspan=3)
    CTkLabel(st, text='Symptom Name',font=("Gotham Ultra", 14), text_color="#ededed").grid(row=3, column=0)
    sym=Spinbox(st,values=symp)
    sym.grid(row=3, column=1)
    CTkButton(st,width=15, text='Search', command=search_med,fg_color="#e04a32", hover_color="#e04a32").grid(row=3, column=2)
    CTkLabel(st, text='-'*70).grid(row=4, column=0,columnspan=3)    
    if flags=='apt1':
        CTkButton(st,width=15, text='Main Menu', command=main_cus,fg_color="#e04a32", hover_color="#e04a32").grid(row=6, column=2)
    else:
        CTkButton(st,width=15, text='Main Menu', command=main_menu,fg_color="#e04a32", hover_color="#e04a32").grid(row=6, column=2)
    st.mainloop()

def search_med():
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y=[]
    x=0
    for i in cur:
        if i[5]==sym.get():
            y.append(str(i[0])+'. '+str(i[1])+'  Rs '+str(i[4])+'    Rack : '+str(i[7])+'    Mfg : '+str(i[8]))
            x=x+1
    top=Tk()
    for i in range(len(y)):
        Label(top,text=y[i]).grid(row=i, column=0)
    Button(top,text='OK',command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()

def val_cus():  # to enter new valued customer
    global val, flag, dbt, name_vc, add_vc, cur, c, vc_id
    apt.destroy()
    cur.execute("select * from cus")
    flag = 'val'
    set_appearance_mode("dark")
    val = CTk()
    val.geometry("600x480")
    val.title("New Valued Customer")

    # Header
    CTkLabel(val, text="ENTER VALUED CUSTOMER DETAILS", font=("Gotham Ultra", 20), text_color="#ffffff").grid(row=0, column=0, columnspan=3, pady=(20, 10))
    CTkLabel(val, text="-" * 60, font=("Gotham Ultra", 12), text_color="#ffffff").grid(row=1, column=0, columnspan=3)

    # Form
    CTkLabel(val, text="Name:   ", font=("Gotham Ultra", 11), text_color="#ffffff").grid(row=2, column=0, pady=(10, 10))
    name_vc = CTkEntry(val, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    name_vc.grid(row=2, column=1, pady=(10, 10))

    CTkLabel(val, text="Address:   ", font=("Gotham Ultra", 11), text_color="#ffffff").grid(row=3, column=0, pady=(10, 10))
    add_vc = CTkEntry(val, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    add_vc.grid(row=3, column=1, pady=(10, 10))

    CTkLabel(val, text="Value Id:   ", font=("Gotham Ultra", 11), text_color="#ffffff").grid(row=4, column=0, pady=(10, 10))
    vc_id = CTkEntry(val, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    vc_id.grid(row=4, column=1, pady=(10, 10))

    # Buttons
    CTkButton(val, text='Submit', command=val_get, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=5, column=1, pady=(20, 10))
    CTkButton(val, text='Main Menu', command=main_menu, fg_color="#e04a32", hover_color="#e04a32", font=("Gotham Ultra", 12)).grid(row=5, column=2, pady=(20, 10))

    # Footer
    CTkLabel(val, text="-" * 60, font=("Gotham Ultra", 12), text_color="#ffffff").grid(row=6, column=0, columnspan=3, pady=(10, 20))

    val.mainloop()


def val_get():  #to submit new valued customer details
    global name_vc, add_vc, val, dbt ,c, cur, apt, vc_id
    cur.execute("insert into cus values(?,?,?)",(name_vc.get(),add_vc.get(),vc_id.get()))
    l.execute("insert into log values(?,?)",(name_vc.get(),vc_id.get()))
    cur.execute("select * from cus")
    for i in cur:
        print (i[0], i[1], i[2])
    c.commit()
    login.commit()

def again():    #for login window
    global un, pwd, flag, app, apt
    if flag=='apt':
        apt.destroy()
    set_appearance_mode("dark")
    app = CTk()
    app.title("Wara & CO. PVT LTD")
    app.geometry("600x480")
    app.resizable(1, 1)

    side_img_data = Image.open("side-img.jpg")
    email_icon_data = Image.open("key.png")
    password_icon_data = Image.open("lock (1).png")


    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(30, 30))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(30, 30))

    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=480, fg_color="#121317")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="UZ Pharmacy", text_color="#ededed", anchor="w", justify="left", font=("Gotham Ultra", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Sign in to your account", text_color="#eaeaea", anchor="w", justify="left", font=("Gotham Ultra", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Username:", text_color="#ededed", anchor="w", justify="left", font=("Gotham Ultra", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    un = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#ededed", border_width=1, text_color="#000000")
    un.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Password:", text_color="#ededed", anchor="w", justify="left", font=("Gotham Ultra", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    pwd = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#ededed", border_width=1, text_color="#000000", show="*")
    pwd.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Login", fg_color="#e04a32", font=("Gotham Ultra", 12), text_color="#ffffff", width=225, command=check).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=frame, text="Close", fg_color="#e04a32", font=("Gotham Ultra", 12), text_color="#ffffff", width=225, command=app.destroy).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    app.mainloop()
    

def check():    #for enter button in login window
    global un, pwd, login, l, app
    u = un.get()
    p = pwd.get()
    l.execute("select * from log")
    for i in l:
        if i[0] == u and i[1] == p:
            app.destroy()
            open_win()
        elif i[0] == u and i[1] == p:
            root.destroy()
            open_cus()
    login.commit()

def main_menu(): #controls open and close of main menu window----------------------------------------RETURN TO MAIN MENU
    global sto, apt, flag, root, st, val, exp, st1,rev
    if flag=='sto':
        sto.destroy()
    if flag=='rev':
        rev.destroy()
    elif flag=='st':
        st.destroy()
    elif flag=='st1':
        st1.destroy()
    elif flag=='val':
        val.destroy()
    elif flag=='exp':
        exp.destroy()
    elif flag=='d':
        d.destroy()
    open_win()    

def main_cus():
    global st, flag, exp
    if flag=='exp':
        exp.destroy()
    elif flag=='st':
        st.destroy()
    open_cus()
    
def open_cus(): #OPENS MAIN MENU----------------------------------------------------------------------------MAIN MENU
    global apt, flag, flags
    flags='apt1'
    apt=Tk()
    apt.title("Interface")
    Label(apt, text="MEDPLUS CHEMIST AND DRUGGIST").grid(row=0,column=0)
    Label(apt, text='*'*40).grid(row=1,column=0)
    Label(apt, text='*  WELCOME  *').grid(row=2,column=0)
    Label(apt, text='-'*40).grid(row=3,column=0)
    Label(apt, text="Customer Services").grid(row=4,column=0)
    Label(apt, text='-'*40).grid(row=5,column=0)
    Button(apt,text='Search', width=15, command=search).grid(row=6,column=0)
    Button(apt,text='Expiry Check', width=15, command=exp_date).grid(row=7,column=0)
    
    Label(apt, text='-'*40).grid(row=8,column=0)    
    Button(apt,text='Logout',command=again1).grid(row=9, column=0)
    apt.mainloop()
def again1():
    global flags
    apt.destroy()
    flags=''
    again()
again()

