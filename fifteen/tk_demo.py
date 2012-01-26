#
# Torbert, 10.8.2008
#
# Tkinter Demo, Version 1.0
#
#   Input: none
# Process: a square with a message tries to run off the screen
#  Output: graphical display updated every 10 milliseconds
#

from Tkinter import *
from sys import exit

w,h=800,600
x,y,dx,dy=100,50,175,175

def tick():
	global x
	x+=1
#	x1,y1,x2,y2=cnvs.coords(rect)
#	print x1,y1,x2,y2
	print cnvs.itemcget(objt,'text')
	cnvs.coords(rect,x,y,x+dx,y+dy) # move the objects
	cnvs.coords(objt,x+dx/2,y+dy/2)
	cnvs.after(10,tick) # animation

def click(evnt):
	global x,y
	x,y=evnt.x,evnt.y
	cnvs.itemconfigure(objt,text='Hey!',font='Courier 48')

def quit(evnt):
	exit(0)

#
# Initialize.
#
root=Tk()
cnvs=Canvas(root,width=w,height=h,bg='white')
cnvs.pack()
#
# Graphics objects. 
#
rect=cnvs.create_rectangle(x,y,x+dx,y+dy,fill='black',outline='black')
objt=cnvs.create_text(x+dx/2,y+dy/2,text='Bye!',fill='white')
#
# Callbacks.
#
root.bind('<Button-1>',click)
root.bind('<q>',quit)
cnvs.after(10,tick) # animation
#
# Here we go.
#
root.mainloop()
