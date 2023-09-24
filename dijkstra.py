from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import math
import heapq

master=Tk()
master.attributes('-fullscreen',True)
master.title('Pathfinding Visualizer')
canvas=tk.Canvas(master)
canvas.pack(fill=tk.BOTH,expand=True)
cell_height=10
cell_width=10
cells=[[canvas.create_rectangle(i*cell_width,j*cell_height,(i+1)*cell_width,(j+1)*cell_height,fill='darkgreen') for i in range(1000)] for j in range(1000)]
dragging=True
def drag(event):
    global dragging
    if not dragging:
        return
    x,y=event.x,event.y
    row,col=event.y//cell_height,event.x//cell_width
    canvas.itemconfig(cells[row][col],fill='blue')
def switchModes(event):
    global dragging
    dragging=not dragging

canvas.bind('<B1-Motion>',drag)
canvas.bind('<Button-3>',switchModes)

DIRECTIONS=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
def retrace(row,col,dictionary):
    global startCoordinates
    while row!=startCoordinates[0] or col!=startCoordinates[1]:
        canvas.itemconfig(cells[row][col],fill='red')
        row,col=dictionary[(row,col)]


def dijkstra():
    heap=[(0,startCoordinates[0],startCoordinates[1])]
    parents={}
    matrix=canvas2matrix(1000,1000)
    while heap:
        weight,row,col=heapq.heappop(heap)
        canvas.itemconfig(cells[row][col],fill='white')
        for dr,dc in DIRECTIONS:
            if 0<=row+dr<1000 and 0<=col+dc<1000 and matrix[row+dr][col+dc]!=1:
                if (row+dr,col+dc) in parents:
                    continue
                parents[(row+dr,col+dc)]=(row,col)
                if row+dr==endCoordinates[0] and col+dc==endCoordinates[1]:
                    retrace(row,col,parents)
                    return
                if isDiagonal(dr,dc):
                    heapq.heappush(heap,(weight+1.4,row+dr,col+dc))
                else:
                    heapq.heappush(heap,(weight+1,row+dr,col+dc))
started=False
ended=False
startCoordinates=()
endCoordinates=()
def on_left_click(event):
    global startCoordinates
    global endCoordinates
    global started
    global ended
    global dragging
    if dragging:
        return
    x,y=event.x,event.y
    row,col=event.y//cell_height,event.x//cell_width
    if ended:
        dijkstra()
    elif started:
        canvas.itemconfig(cells[row][col],fill='yellow')
        endCoordinates=(row,col)
        ended=True
    else:
        canvas.itemconfig(cells[row][col],fill='white')
        started=True
        startCoordinates=(row,col)

canvas.bind('<Button-1>',on_left_click)
def getHcosts(rows,cols):
    global endCoordinates
    matrix=[[float('inf')]*cols for x in range(rows)]
    endRow,endCol=endCoordinates
    for r in range(rows):
        for c in range(cols):
            matrix[r][c]=math.sqrt((endRow-r)**2+(endCol-c)**2)
    return matrix
def getGcosts(rows,cols):
    matrix=[[float('inf')]*cols for x in range(rows)]
    startRow,startCol=startCoordinates
    for r in range(rows):
        for c in range(cols):
            matrix[r][c]=math.sqrt((startRow-r)**2+(startCol-c)**2)
    return matrix
def canvas2matrix(rows,cols):
    matrix=[[0]*cols for x in range(rows)]
    for r in range(rows):
        for c in range(cols):
            color=canvas.itemcget(cells[r][c],'fill')
            if color=='blue':
                matrix[r][c]=1
            elif color=='yellow':
                matrix[r][c]=2
            elif color=='white':
                matrix[r][c]=-1
    return matrix
def isDiagonal(r,c):
    return r and c
mainloop()
