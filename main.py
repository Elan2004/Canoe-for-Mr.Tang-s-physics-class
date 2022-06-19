from matplotlib import pyplot as py
import numpy as np
import math
from scipy import integrate
from matplotlib.widgets import Slider, Button

if __name__ == '__main__':

    scales = (-1.1, 1.1, -0.3, 1.1)

    d = 0.5
    di = 0.5
    n = 1000
    angi = 0.6
    ang = 0.6
    cbl = -1 / ang
    intercept = 0
    sth = 0
    ewi = 0.5
    ew = 0.5
    fig = py.gcf()
    ax = py.gca()


    def b(x):
        return x ** 6/3125 -math.exp(-4 * math.fabs(x))


    def w(x):
        global d
        return d


    def intersec():
        i = 0.5
        while w(i) > b(i):
            i = i + 0.001

        return i


    def waterlvl():
        j = -4.9
        k = 4.999
        while ang * j + intercept < b(j):
            j = j + 0.01
        while ang * k + intercept < b(k):
            k = k - 0.01
        return j, k


    def findcb():
        j = 0
        k = -0.1
        while cbl * j + sth > b(j):
            j = j + 0.01
        while cbl * k + sth > ang * k + intercept:
            k = k + 0.01
        return j, k


    int = intersec()

    x = np.linspace(-5, 5, n)
    l = np.linspace(d, d, n)
    boat = np.vectorize(b)
    y = boat(x)
    c = lambda x: d - (x ** 6/3125 -math.exp(-4 * math.fabs(x)))
    e = lambda x: ang * x + intercept - (x ** 6/3125 -math.exp(-4 * math.fabs(x)))
    p = lambda x: ang * x + intercept - (cbl * x + sth)

    ax.plot(x, y)

    area, error = integrate.quad(c, -int, int)


    def findwaterlvl():
        global intercept
        low, up = waterlvl()
        tarea, er = integrate.quad(e, low, up)

        while tarea < area:
            intercept = intercept + 0.001
            low, up = waterlvl()
            tarea, er = integrate.quad(e, low, up)
            if intercept > 10:
                break
        while tarea > area:
            intercept = intercept - 0.001
            low, up = waterlvl()
            tarea, er = integrate.quad(e, low, up)
            if intercept < -10:
                break
        tilt = ang * x + intercept
        ax.plot(x, tilt, color='black')


    def findcbl():
        global sth
        low, up = waterlvl()
        low1, up1 = findcb()
        area1, er = integrate.quad(p, low1, up1)
        area2, er = integrate.quad(e, up1, up)

        while area1 + area2 > area / 2:
            sth = sth + 0.001
            low1, up1 = findcb()
            area1, er = integrate.quad(p, low1, up1)
            area2, er = integrate.quad(e, up1, up)
            if sth > 30:
                break
        while area1 + area2 < area / 2:
            sth = sth - 0.001
            low1, up1 = findcb()
            area1, er = integrate.quad(p, low1, up1)
            area2, er = integrate.quad(e, up1, up)
            if sth < -10:
                break
        cb = cbl * x + sth
        ax.plot(x, cb, color='blue')


    ann = py.annotate('Fg', xy=(sum(x) / len(x), sum(y) / len(y) + ew),
                      xytext=(sum(x) / len(x) + 0.1, sum(y) / len(y) + ew + 0.1 * cbl)
                      , arrowprops=dict(arrowstyle="<-"))
    ax.plot(sum(x) / len(x), sum(y) / len(y) + ew, marker='o', ms=6, color='red')

    py.xlim(-6, 6)
    py.ylim(-1.5, 5.5)
    axamp = py.axes([0.05, 0.25, 0.0225, 0.63])
    amp_slider = Slider(
        ax=axamp,
        label="depth",
        valmin=0,
        valmax=5,
        valinit=di,
        orientation="vertical"
    )
    axang = py.axes([0.25, 0.05, 0.65, 0.03])
    ang_slider = Slider(
        ax=axang,
        label="Angle",
        valmin=0.001,
        valmax=1,
        valinit=angi
    )
    axcm = py.axes([0.25, 0.9, 0.65, 0.03])
    cm_slider = Slider(
        ax=axcm,
        label="CM",
        valmin=0,
        valmax=10,
        valinit=ewi
    )

    line, = ax.plot(x, l, color='orange')

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


    def update(val):
        global d, area, ang, cbl, ann, ew
        for u in ax.get_lines():
            u.remove()
        ax.plot(x, y, color='black')
        ann.remove()

        d = amp_slider.val
        ang = ang_slider.val
        ew = cm_slider.val
        ax.plot(sum(x) / len(x), sum(y) / len(y) + ew, marker='o', ms=6, color='red')
        cbl = -1 / ang
        degree = math.atan(cbl)
        ann = ax.annotate('Fg', xy=(sum(x) / len(x), sum(y) / len(y) + ew),
                          xytext=(sum(x) / len(x) + (0.5 * d + ew) * math.cos(degree),
                                  sum(y) / len(y) + ew + (0.5 * d + ew) * math.sin(degree))
                          , arrowprops=dict(arrowstyle="<-"))

        int = intersec()
        area, error = integrate.quad(c, -int, int)
        waterlvl()

        findcb()

        findwaterlvl()
        findcbl()
        line, = ax.plot(x, l, color='black')
        line.set_ydata(d)
        fig.canvas.draw_idle()


    amp_slider.on_changed(update)
    ang_slider.on_changed(update)
    cm_slider.on_changed(update)
    py.show()
