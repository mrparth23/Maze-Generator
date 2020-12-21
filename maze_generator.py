import random
from tkinter import colorchooser

import PIL
from PIL import ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from tkinter import *


class GraphApi:
    def __init__(self, v):
        self.V = v
        self.adjlist = []
        for i in range(0, self.V):
            self.adjlist.insert(i, [])

    def add_edge(self, src, dest):
        self.adjlist[src].append(dest)
        self.adjlist[dest].append(src)

    def remove_edge(self, src, dest):
        self.adjlist[src].remove(dest)
        self.adjlist[dest].remove(src)

    def print_graph(self):
        for i in range(len(self.adjlist)):
            print("Edge from Vertex ", i, " -> ", end=" ")
            for j in range(len(self.adjlist[i])):
                print(self.adjlist[i][j], end=" ")
            print("\n")

    def dfs(self, vertex):
        visited = [False] * len(self.adjlist)
        self.dfs_visit(vertex, visited)

    def dfs_visit(self, vertex, visited):
        visited[vertex] = True
        print(vertex, end=" ")

        for i in self.adjlist[vertex]:
            if visited[i] is False:
                self.dfs_visit(i, visited)

    def generate_maze(self, mx, my, visit):
        stack = []
        position_list = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        visit[0][0] = True
        stack.append([0, 0])
        self.remove_edge(0, 1)
        self.remove_edge((mx + my * (mx + 1) - 1), (mx + my * (mx + 1)))
        new_edge = 0
        while len(stack) is not 0:
            nlist = []
            (cx, cy) = stack[-1]
            for i in range(4):
                (x, y) = position_list[i]
                nx = cx + x
                ny = cy + y
                if 0 <= nx < mx and 0 <= ny < my:
                    if visit[nx][ny] is False:
                        nlist.append(i)
                        print("tx, ty :", x, y)
                        print("tnx, tny :", nx, ny)

            if len(nlist) is not 0:
                (x, y) = position_list[nlist[random.randint(
                    0, len(nlist) - 1)]]
                nx = cx + x
                ny = cy + y
                print("x, y :", x, y)
                print("nx, ny :", nx, ny)
                if x is 1:
                    temp = nx + (ny * (mx + 1))
                    new_edge = [temp, temp + (mx + 1)]
                elif x is -1:
                    temp = cx + (cy * (mx + 1))
                    new_edge = [temp, temp + (mx + 1)]
                elif y is 1:
                    temp = nx + (ny * (mx + 1))
                    new_edge = [temp, temp + 1]
                elif y is -1:
                    temp = cx + (cy * (mx + 1))
                    new_edge = [temp, temp + 1]
                self.remove_edge(new_edge[0], new_edge[1])
                print("new_edge : ", new_edge)
                visit[nx][ny] = True
                stack.append([nx, ny])
            else:
                [t1, t2] = stack.pop()
                print("t1, t2 : ", t1, t2)
            print("Stack : ", stack)

    def write_svg(self, filename, nx, ny, bgcolor, fgcolor):
        aspect_ratio = nx / ny
        padding = 10
        height = 50 * ny
        width = int(height * aspect_ratio)
        scy, scx = height / ny, width / nx

        def write_wall(f, x1, y1, x2, y2):
            print(
                '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2), file=f)

        with open(filename, 'w') as f:
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}"  height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css">', file=f)
            # print('.background {', file=f)
            # print('    background-color: blue;', file=f)
            # print('}', file=f)
            print('<![CDATA[', file=f)
            print('line {', file=f)
            p = '    stroke:' + fgcolor + ' ;\n    stroke-linecap: square;'
            print(p, file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)

            p = "<rect width=\"98%\" height=\"98%\" fill=\" " + bgcolor + "\" />"
            print(p, file=f)
            for y in range(ny):
                for x in range(nx):

                    if (x + y * (nx + 1)) in self.adjlist[x + y * (nx + 1) + 1]:
                        x1, y1, x2, y2 = x * scx, y * \
                            scy, (x + 1) * scx, y * scy
                        write_wall(f, x1, y1, x2, y2)
                    if (x + y * (nx + 1)) in self.adjlist[x + (y + 1) * (nx + 1)]:
                        x1, y1, x2, y2 = x * scx, y * \
                            scy, x * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if (x + (y + 1) * (nx + 1)) in self.adjlist[x + (y + 1) * (nx + 1) + 1]:
                        x1, y1, x2, y2 = x * \
                            scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if (x + y * (nx + 1) + 1) in self.adjlist[x + y * (nx + 1) + nx + 2]:
                        x1, y1, x2, y2 = (x + 1) * scx, y * \
                            scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

            print('</svg>', file=f)


def fun():
    mx = 10 if (len(e1.get()) is 0) else int(e1.get())
    my = 10 if (len(e2.get()) is 0) else int(e2.get())

    visit = []
    for i in range(0, mx):
        visit.append([])
        for j in range(0, my):
            visit[i].append(False)

    graph = GraphApi((mx + 1) * (my + 1))
    i = 0
    while i < (mx + 1) * (my + 1):
        for j in range(0, mx):
            graph.add_edge(i + j, i + j + 1)
        i += (mx + 1)

    i = 0
    for j in range(0, mx * my):
        while i < (my + 1):
            graph.add_edge(i + j, i + j + (mx + 1))
            i += 1
        i -= 1
    graph.print_graph()
    graph.generate_maze(mx, my, visit)
    graph.print_graph()
    bg = "#ffffff" if (e3 is None) else e3[1]
    fg = "#000000" if (e4 is None) else e4[1]
    graph.write_svg('maze.svg', mx, my, bg, fg)
    drawing = svg2rlg("maze.svg")
    filename = "Figures//Maze_" + str(mx) + "x" + str(my) + ".png"
    renderPM.drawToFile(drawing, filename, fmt="PNG")
    image = PIL.Image.open(filename)
    image.show()

    parent.mainloop()


def cpicker1():
    global e3
    e3 = colorchooser.askcolor()


def cpicker2():
    global e4
    e4 = colorchooser.askcolor()


if __name__ == "__main__":
    parent = Tk()
    parent.title("Maze Generator")
    parent.geometry("750x700+510+120")

    title = Label(parent, text="Maze Generator", fg="Red", bg="White")
    title.config(font=("Courier bold", 50))
    title.pack()
    name = Label(parent, text="X-Dimension")
    name.config(font=("Courier bold", 25))
    name.pack()
    e1 = Entry(parent)

    e1.config(font=("Courier bold", 25))
    e1.pack()
    password = Label(parent, text="Y-Dimension")
    password.config(font=("Courier bold", 25))
    password.pack()
    e2 = Entry(parent)
    e2.config(font=("Courier bold", 25))
    e2.pack()

    e3 = None
    e4 = None

    bg = Button(parent, text="Choose Background Colour",
                font="Courier 25 bold", command=cpicker1)
    bg.pack()
    fg = Button(parent, text="Choose Foreground Colour",
                font="Courier 25 bold", command=cpicker2)
    fg.pack()

    b = Button(parent, text="Generate", font="Courier 25 bold", command=fun)
    b.pack()
    parent.mainloop()
