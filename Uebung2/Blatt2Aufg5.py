#!/usr/bin/env python
#-*- coding:utf-8 -*-

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

a = 2.0 # Form-Parameter für das Potential

def bewGl(xi, t):
    """Werte Bewegungsgleiching aus.

    Eingaben:
    =========
    xi : array
        Erste Komponente: x, zweite Komponente: v.
    t : float
        Zeit t. Wird hier nicht benutzt.

    Rückgaben:
    ==========
    f : array
      Erste Komponente: dot x = v, zweite Komponente: dot v = 4x(x^2 - 1)
    """

    dotX = xi[1]
    dotV = -4.0*xi[0]*(xi[0]**2 - a**2)

    return np.array([dotX, dotV])

def potErg(x):
    """Gebe potentielle Energie am Ort x zurück.

    Eingaben:
    =========
    x : float oder array
        Ort x oder array aus x-Werten.

    Rückgaben:
    ==========

    V : float oder array
        Potential V am Ort x.
    """

    return x**4 - 2.0*(a**2)*(x**2)

def kinErg(v):
    """Gebe kinetische Energie für Geschwindigkeit v zurück.

    Eingaben:
    =========
    v : float oder array
        Geschwindigkeit v oder array aus x-Werten.

    Rückgaben:
    ==========

    T : float oder array
        Kinetische Energie T für Geschwindigkeit v.
    """

    return 0.5*v**2 # Masse m=1

def determineStartingValues(E):
    """Bestimme Anfangsbedingung.

    Gebe Startwerte im linken Minimimum zurück. Wähle die Geschwindigkeit
    so, dass die Energie dem Argument E entspricht. Wir düsen am Anfang nach
    rechts.

    Eingaben:
    ========
    E : float
        Energie

    Rückgaben:
    ==========
    xi0 : array
        Array mit Startbedingung [x0, v0], so dass die Energiebedingung
        erfüllt ist.
    """

    xStart = -a
    vStart = np.sqrt(2.0*(E-potErg(xStart))) # v = sqrt(2*(E-V)), weil E = T + V = 0.5*v^2 + V

    return np.array([xStart, vStart])


def E_changed_action(value):
    """Setze Energie neu. Plotte neue Daten.

    Eingaben:
    =========
    value : float
        Neuer Wert von E.
    """

    global E

    E = value

    print "Neues E = %f " % (E)
    print "Neuberechnung..."
    calc()
    print "\tFertig!"
    print "Neu plotten!"
    plot(replot=True)
    plt.draw()

def calc():
    """Bereche eine neue Trajektorie und diese und weitere Daten in globalen
    Variablen.

    Bemerke:
    ========
    Die Funktion setzt die Variablen xValues, plotValues, startVals, vals,
    freqAmpl, freqAmplPlot und omegaPlot neu.
    """

    global xValues, potValues, startVals, vals, freqAmpl, freqAmplPlot, omegaPlot
    xValues = np.linspace(-3.0, +3.0, 5000)
    potValues = potErg(xValues)
    startVals =  determineStartingValues(E) # starte im linken Minimum mit gegebener Energie E, düse am Angfang Richtung rechts
    vals = scipy.integrate.odeint(bewGl, y0=startVals, t=t) # integriere DGL
    freqAmpl = scipy.fft(vals[:, 0])
    freqAmplPlot = freqAmpl[0:len(freqAmpl)/2] # nur positive Freq plotten
     # berechne Fourier-Frequenzen zu positiven Frequenzen:
    omegaPlot = np.fft.fftfreq(len(t), np.max(t)/len(t))[0:len(t)/2]

def plot(replot=False):
    """Plotte alle Daten.

    Eingaben:
    =========
    replot : boolean
        True, falls bereits Daten gezeichnet wurden.
    """

    if(replot):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

    ax1.set_title("Potential")
    ax1.set_xlabel(r"Ort $x$")
    ax1.set_ylabel(r"Potential $V(x)$")
    ax1.grid()
    ax1.plot(xValues, E*np.ones(len(xValues)), color="blue", ls="-.", label="$E$") # horizontale für Energie
    ax1.plot(xValues, potValues, color="red", ls="-", label=r"$V(x)$")

    # plotte Ort, Geschwindigkeit:
    ax2.set_title("Ort und Geschwindigkeit")
    ax2.set_xlabel(r"Zeit $t$")
    ax2.set_ylabel(r"Ort, Geschwindigkeit")
    ax2.plot(t, vals[:, 0], label=r"$x(t)$", ls="-", color="blue")
    ax2.plot(t, vals[:, 1], label=r"$v(t)$", ls="-", color="red")

    # plotte Energien:
    ax3.set_title("Kinetische und potentielle Energie")
    ax3.set_xlabel(r"Zeit $t$")
    ax3.set_ylabel(r"Energie")
    ax3.plot(t, kinErg(vals[:, 1]), label=r"$T$", ls="-", color="blue")
    ax3.plot(t, potErg(vals[:, 0]), label=r"$V$", ls="-", color="red")
    ax3.plot(t, kinErg(vals[:, 1])+potErg(vals[:, 0]), label=r"$E=T+V$", ls="--", color="gray")

    # berechne Frequenz in harmonischer Näherung:
    omegaHarmOsz = np.sqrt(8.0*a**2)

    # plotte Frequenzen:
    ax4.set_title(r"'Oberschwingungen von $x(t)$'")
    ax4.set_xlabel(r"Frequenz $\omega$")
    ax4.set_ylabel(r"normierte Amplitude $A_\mathrm{norm}$")
    ax4.plot(2*np.pi*omegaPlot, np.abs(freqAmplPlot)/np.max(np.abs(freqAmplPlot)), ls="-", marker="o", c="r", ms=12, label=r"$\vert$Fourierkoeff.$\vert$")
    ax4.axvline(x=omegaHarmOsz, ymin=0, ymax=1.1, ls="--", c="gray", label=r"$\omega_{\mathrm{harm.\,Osz.}}$")
    ax4.axis(xmin=0, xmax=20, ymin=0, ymax=1.1)

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()


def updatePotPlot(data):
    """Neue Daten in den Potential-Plot eintragen"""

#-----------------------------------------------------------------------
# das "Hauptprogramm":

t = np.linspace(0.0, 20.0, 10000) # t-Werte, für die x, v berechnet werden sollen
E = (-a**4)*0.95 # Anfangsenergie

# Plot vorbereiten:

# etwas Optik:
fig = plt.figure(facecolor="white")
plt.rcParams["backend"] = "GTKAgg"
plt.rcParams["ps.papersize"] = "A4"
plt.rcParams["ps.usedistiller"] = "xpdf"
plt.rcParams["text.usetex"] = True # use TeX for all text
plt.rcParams["font.size"] = 18.0 # font size for text
plt.rcParams["xtick.labelsize"] = 18.0 # fontsize of the tick labels
plt.rcParams["ytick.labelsize"] = 17.0 # fontsize of the tick labels
plt.rcParams["legend.fontsize"] = 15.0 # legend font size
plt.rcParams["legend.shadow"] = True # shadow around legend
plt.rcParams["axes.titlesize"] = 18 # fontsize of the axes title
plt.rcParams["axes.labelsize"] = 18 # fontsize of the x any y labels
plt.rcParams["axes.linewidth"] = 2
# Achtung: nur Längen, nicht Dicken!
plt.rcParams["xtick.major.size"] = 5   # major tick size in points
plt.rcParams["xtick.minor.size"] = 2.5   # minor tick size in points
plt.rcParams["ytick.major.size"] = 5   # major tick size in points
plt.rcParams["ytick.minor.size"] = 2.5   # minor tick size in points
plt.rcParams["lines.markeredgewidth"] = 1.5 # tick width
plt.rcParams["lines.linewidth"] = 2.0

ax1 = fig.add_subplot(221, autoscale_on=True,
                      xlabel=r"Ort $x$", ylabel=r"Potential $V$")


ax2 = fig.add_subplot(222, autoscale_on=True,
                         xlabel=(r"Zeit $t$"))

ax3 = fig.add_subplot(223, autoscale_on=True,
                        xlabel=(r"Zeit $t$"), ylabel=(r"Energie"))

ax4 = fig.add_subplot(224, autoscale_on=True,
                        xlabel=(r"Frequenz $\omega$"), ylabel=(r"Fourierkoeffizienten"))

fig.subplots_adjust(bottom=0.2) # unter den Achsen etwas Platz schaffen

# Slider:
axcolor = 'white'
ax_E = plt.axes([0.125, 0.1, 0.675, 0.03], axisbg=axcolor) # Slider-Achse
s_E  = Slider(ax_E, 'E = ', -a**4, 200, valinit=E, valfmt='%1.6f') # Slider erzeugen
s_E.on_changed(E_changed_action) # Funktion, die nach Benutzung des Sliders
                                 # aufgerufen werden soll

calc()
plot()
plt.show()
