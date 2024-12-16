from tkinter import *
from tkinter import messagebox
import ast

root = Tk()
root.title('Login')
root.geometry('965x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

def signin():
    global login_success
    username=user.get()
    password=code.get()

    try:

        file = open('datasheet.txt','r')
        d=file.read()
        r=ast.literal_eval(d)
        file.close()

        # print(r.keys())
        # print(r.values())

        if username in r.keys() and password == r[username]:
            login_success = True  # Set login_success to True on a successful login
            # screen = Toplevel(root)
            # screen.title("App")
            # screen.geometry('965x500+300+200')
            # screen.config(bg="white")

            # # Label(screen,text='Hello Everyone!',bg='#fff' , font=('Calibri(Body)',50,'bold')).pack(expand=True)

            # screen.mainloop()
            root.destroy()

        else:
            messagebox.showerror('Invalid','invalid username or password')
            login_success = False  # Set login_success to False on failure

    except FileNotFoundError:
        messagebox.showerror('Error', 'No user data found, please sign up.')
        login_success = False  # Set login_success to False on failure
###################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def signup_command():
    window=Toplevel(root)

    window.title("SignUp")
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False,False)

    def signup():
        username=user.get()
        password=code.get()
        conform_password=conform_code.get()

        if password==conform_password:
            try:
                file= open('datasheet.txt','r+')
                d= file.read()
                r=ast.literal_eval(d)

                dict2= {username:password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file=open('datasheet.txt', 'w')
                w=file.write(str(r))

                messagebox.showinfo('Signup','Sucessfully sign up')
                window.destroy()

            except:
                file=open('datasheet.txt','w')
                pp=str({'Username':'password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invalid','Both password should match')

    def sign():
        window.destroy()


    img = PhotoImage(file='Baksters.png')
    Label(window,image=img,border=0,bg='white').place(x=50, y=0)

    frame = Frame(window,width=350,height=390,bg='#fff')
    frame.place(x=550,y=50)

    heading= Label(frame,text='Sign up',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    #################################-------------------------------------------------------
    def on_enter(e):
        code.delete(0,'end')
    def on_leave(e):
        if code.get() == '':
            code.insert(0,'Password')

    code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind("<FocusIn>",on_enter)
    code.bind("<FocusOut>", on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
    #################################-------------------------------------------------------
    def on_enter(e):
        conform_code.delete(0,'end')
    def on_leave(e):
        if conform_code.get() == '':
            conform_code.insert(0,'Confirm Password')

    conform_code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    conform_code.place(x=30,y=220)
    conform_code.insert(0,'Confirm Password')
    conform_code.bind("<FocusIn>",on_enter)
    conform_code.bind("<FocusOut>", on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)
    #################################-------------------------------------------------------
    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get() == '':
            user.insert(0,'Username')

    user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>", on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    #################################-------------------------------------------------------

    #-----------------------------------
    Button(frame,width=39,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label = Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=90,y=340)

    signin = Button(frame,width=6,text='Sign in',border=0,bg='white',cursor='hand2',fg='#57a1f8', command= sign)
    signin.place(x=200,y=340)

    window.mainloop()

###################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


img = PhotoImage(file='Baksters.png')
Label(root,image=img,bg='white').place(x=50,y=0)

frame = Frame(root,width=350,height=350,bg="white")
frame.place(x=580, y=70)

heading=Label(frame,text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100 , y=5)

#######################################-------------------------------------------------------------------------------------

def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2, bg='black').place(x=25,y=107)

#######################################-------------------------------------------------------------------------------------
def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2, bg='black').place(x=25,y=177)

###########################################################################################################################

Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8', fg='white',border=0, command=signin).place(x=35,y=204)
label=Label(frame,text="Don't have an account?",fg='black', bg= 'white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up=Button(frame,width=6,text='Sigh up' ,border=0, bg='white', cursor='hand2',fg='#57a1f8' , command=signup_command)
sign_up.place(x=215,y=270)



root.mainloop()