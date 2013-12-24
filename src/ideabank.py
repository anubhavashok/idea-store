import sqlite3 as lite
import sys
import nltk
from nltk.corpus import stopwords

con = None

con = lite.connect('ideabank.db')
cur = con.cursor();
try:
	cur.execute("CREATE TABLE tags( id integer primary key,tag text)");
	cur.execute("CREATE TABLE ideas( id integer primary key, title text, description text)");
	cur.execute("CREATE TABLE ideatags( iid integer REFERENCES ideas(id), tid integer REFERENCES tags(id) )");
	
except:
	pass

from Tkinter import *
import ttk
import tkFont

allTags = []

def submitvals():
	titleval= str(titleInput.get())
	descriptionval= str(descriptionInput.get(0.0,END))
	#tagsval= str(tagsInput.get())
	cur.execute("SELECT Count(*) from ideas")
	iid = cur.fetchall()[0][0];
	cur.execute("INSERT into ideas(title,description) values (?,?)", (titleval, descriptionval))
	con.commit()
	
	#tags = tagsval.split(", ")
	tags=[]
	for button in allTags:
		try:
			tags.append(button.config('text')[-1])
		except:
			pass
	print tags
	for tag in tags:
		cur.execute("SELECT id from tags where tag==?",(tag,))
		tid = None
		tid = cur.fetchall()
		if not tid:
			cur.execute("INSERT into tags(tag) values (?)",(tag,))
			con.commit()
			cur.execute("SELECT Count(*) from tags")
			tid = cur.fetchall()[0][0]
		else:
			tid=tid[0][0]
		print str(tid)
		cur.execute("INSERT into ideatags(iid, tid) values (?,?)", (str(iid+1), str(tid)))
		con.commit()

def submitvals_verify(verify_window):
	submitvals()
	verify_window.destroy()

def viewideas():
	ideas_window = Tk()
	ideas_window.title("All ideas")
	ideas_window.geometry('450x250+200+200')
	dataCols = ('id','title','description','tags')
	
	mlb = ttk.Treeview(ideas_window,columns=dataCols,show='headings')
	for c in dataCols:
		mlb.heading(c, text=c.title())           
		mlb.column(c, width=100)
	cur.execute("SELECT * from ideas")
	ideas_all = cur.fetchall()
	for i in ideas_all:
		mlb.insert('','end',values=i)
	mlb.grid(row=0, column=0)
	button_frame = Frame(ideas_window)
	button_frame.grid(row=1,column=0, sticky=E)
	Ok = Button(button_frame, text ="Ok", command = ideas_window.destroy)
	Ok.grid(row=0, column=1)

def verifyinput():
	titleval= str(titleInput.get())
	descriptionval= str(descriptionInput.get(0.0,END))
	tagsval= str(tagsInput.get())
	cur.execute("SELECT Count(*) from ideas")
	idea_count = cur.fetchall()[0][0]
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
	print ideas_count
	ideatagcount = [0 for i in range(ideas_count+1)]
	ideatags = []
	
	cur.execute("SELECT * from ideatags")
	ideatags=cur.fetchall()
	if ideatags:
		for entry in ideatags:
			if entry[1] in tagids:
				ideatagcount[int(entry[0])]+=1
	print ideatagcount
	display = []
	#change to top ten results
	#current implementation is threshold > 2
	for i in range(len(ideatagcount)):
		if ideatagcount[i]>2:
			display.append(i)
	if display:
		verify_window = Tk()
		verify_window.title("Verify existing idea")
		verify_window.geometry('450x250+200+200')
		dataCols = ('id','title','description','tags')
	
		mlb = ttk.Treeview(verify_window,columns=dataCols,show='headings')
		for c in dataCols:
			mlb.heading(c, text=c.title())           
			mlb.column(c, width=100)
	
		for i in display:
			cur.execute("SELECT * from ideas where id==?",(i,))
			print "final_ideas is:"
			final_ideas = cur.fetchall()[0]
			print final_ideas
			mlb.insert('','end',values=final_ideas)
		mlb.grid(row=0, column=0)
		button_frame = Frame(verify_window)
		button_frame.grid(row=1,column=0, sticky=E)
		Cfm = Button(button_frame, text ="Confirm", command = lambda: submitvals_verify(verify_window))
		Cfm.grid(row=0, column=1)
		Cnl = Button(button_frame, text ="Cancel", command = verify_window.destroy)
		Cnl.grid(row=0, column=2)
	else:
		submitvals()

def generateKeywords(event):
	textval = str(descriptionInput.get(0.0,END))
	textval = textval[:-1]
	global allTags
	allTags = []
	# remove stopwords
	stop = stopwords.words('english')
	textval = [i for i in textval.split(' ') if i not in stop];
	print textval
	i=0
	# for each remaining word
	for word in textval:
		i+=1
		# create a button containing the word
		f=Frame(tagsFrame)
		f.pack(side='top')
		b = Button(f,text=word,command = f.destroy)
		allTags.append(b)
		f.grid(row=0,column=i)
		b.grid(row=0,column=0)


app = Tk()
app.title("IdeaBank")
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
descriptionText.set("Description (press Return when done): ")
description = Label(app, textvariable=descriptionText, height=4)
description.pack()

descriptionVal = StringVar(None)
descriptionInput = Text(app, height=8)
descriptionInput.bind("<Return>", generateKeywords)
descriptionInput.pack()

tagsText = StringVar()
tagsText.set("Tags: ")
tags = Label(app, textvariable=tagsText, height=4)
tags.pack()

#tagsVal = StringVar(None)
#tagsInput = Entry(app, textvariable = tagsVal)
#tagsInput.pack()

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open existing ideabank")
filemenu.add_command(label="View all ideas", command=viewideas)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=app.destroy)
menubar.add_cascade(label="file",menu=filemenu)
app.config(menu=menubar)
#show existing tags
#or show related tags

tagsFrame = Frame(app)
tagsFrame.pack()


submit = Button(app, text="Submit", width=20, command= verifyinput)
submit.pack(side='bottom',padx=15, pady=15)

app.mainloop()


