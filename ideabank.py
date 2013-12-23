from Tkinter import *
import ttk
import sqlite3 as lite

con = None
con = lite.connect('ideabank.db')
cur = con.cursor() 

def submitvals():
	cur.execute("SELECT Count(*) from ideas")
	iid = cur.fetchall()[0][0]+1;
	cur.execute("INSERT into ideas(title,description) values (?,?)", (titleval, descriptionval))
	con.commit()
	
	tags = tagsval.split(", ")
	for tag in tags:
		cur.execute("SELECT id from tags where tag==?",(tag,))
		tid = None
		tid = cur.fetchall()
		if tid==None:
			cur.execute("INSERT into tags(tag) values (?)",(tag,))
			con.commit()
			cur.execute("SELECT Count(*) from tags")
			tid = cur.fetchall()[0][0] +1
		
		cur.execute("INSERT into ideatags(iid, tid) values (?,?)", (str(iid), str(tid)))
		con.commit()

def verifyinput():
	titleval= str(titleInput.get())
	descriptionval= str(descriptionInput.get(0.0,END))
	tagsval= str(tagsInput.get())
	cur.execute("SELECT Count(*) from ideas")
	idea_count = cur.fetchall()[0][0]
	if idea_count < 1:
		submitvals()
	#get ids of tags
	tags = tagsval.split(", ")
	tagids=[]
	for tag in tags:
		cur.execute("SELECT id from tags where tag==?",(tag,))
		tagid = cur.fetchall()
		if tagid:
			tagids.append(tagid[0][0])
		
	cur.execute("SELECT Count(*) from ideas")
	ideas_count = cur.fetchall()[0][0]
	ideatagcount = []
	ideatags = []
	
	cur.execute("SELECT * from ideatags")
	ideatags=cur.fetchall()
	
	for entry in ideatags:
		if entry[1] in tagids:
			print entry[1]
			print entry[0]
			ideatagcount[int(entry[0])]+=1
		
	
	display = []
	#change to top ten results
	#current implementation is threshold > 2
	for i in range(len(ideatagcount)):
		if ideatagcount[i]>2:
			display.append(i)
		
	
	verify_window = Tk()
	verify_window.geometry('450x500+200+200')
	mlb = ttk.Treeview(verify_window,columns=('id','title','description','tags'),show='headings')
	
	for i in display:
		cur.execute("SELECT * from ideas where id==?",(i,))
		mlb.insert('','end',cur.fetchall())
	mlb.pack()
	

app = Tk()
app.title("GUI Example")
app.geometry('450x500+200+200')

promptText = StringVar()
promptText.set("Please enter your idea")
prompt = Label(app, textvariable=promptText, height=4)
prompt.pack()

titleText = StringVar()
titleText.set("Title: ")
title = Label(app, textvariable=titleText, height=4)
title.pack()

titleVal = StringVar(None)
titleInput = Entry(app, textvariable = titleVal)
titleInput.pack()


descriptionText = StringVar()
descriptionText.set("Description: ")
description = Label(app, textvariable=descriptionText, height=4)
description.pack()

descriptionVal = StringVar(None)
descriptionInput = Text(app, height=8)
descriptionInput.pack()

tagsText = StringVar()
tagsText.set("Tags: ")
tags = Label(app, textvariable=tagsText, height=4)
tags.pack()

tagsVal = StringVar(None)
tagsInput = Entry(app, textvariable = tagsVal)
tagsInput.pack()

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open existing ideabank")
filemenu.add_separator()
filemenu.add_command(label="Exit",command=app.destroy)
menubar.add_cascade(label="file",menu=filemenu)
app.config(menu=menubar)
#show existing tags
#or show related tags

submit = Button(app, text="Submit", width=20, command= verifyinput)
submit.pack(side='bottom',padx=15, pady=15)

app.mainloop()


