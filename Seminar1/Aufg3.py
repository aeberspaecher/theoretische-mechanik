#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Beispiel-Lösung für die Aufgabe III aus dem ersten Tutorium zur
theoretischen Mechanik.

Benötigte Python-Module: NumPy, SciPy, Matplotlib

Alexander Eberspächer, Oktober 2011
"""

# Importe:
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.integrate import ode

# Parameter für Integration:
tInit = 0.0
tFinal = 250.0
numSteps = 2000 # Zahl der Zeitschritte
dt = (tFinal - tInit)/numSteps

# Anfangsbedingungen:
phi0 = 0.0
omega0 = 0.0

gamma = 0.25
omegad = 2.0/3.0

# Wertebereich von A für User-Interface:
Amin = 0.0
Amax = 2.5
A = 0.5 # erster Wert für A

def bewGl(t, x):
    """Bewegungsgleichung für das gedämpfte getriebene Pendel.

    Die Funktion gibt für ein gegebene x=(phi, omega) und t die Ableitungen
    d/dt x = (d/dt phi, d/dt omega) zurück.

    Eingaben:
    ---------
    x : array
        Array (phi, omega)
    t : float
        Zeit t

    Rückgaben:
    ----------
    dx : array
        Array (d/dt phi, d/dt omega)
    """

    return np.array([ x[1], -np.sin(x[0]) - 2.0*gamma*x[1] + A*np.sin(omegad*t) ])


def Achanged(value):
    """Funktion, die nach einer Änderung von A die Daten neu berechnet
    und plottet.

    Eingaben:
    ---------
    value : float
        Der neue Wert von A
    """

    global A # benutze das globale A

    A = value

    # DGL integrieren:

    t = tInit
    integrator.set_initial_value([phi0, omega0], tInit)
    values = np.zeros([2, numSteps]) # leeres array für Werte erzeugen
    values[:, 0] = np.array([ phi0, omega0 ])

    for i in range(1, numSteps):
        integrator.integrate(integrator.t + dt)
        if(not integrator.successful()):
            print("Problem in der Integration!")
            break
        values[:, i] = integrator.y
        t += dt

    # Werte plotten:
    ax1.clear()
    ax2.clear()
    ax1.set_xlabel(r"Zeit $t$"); ax1.set_ylabel(r"Winkel $\varphi$")
    ax2.set_xlabel(r"Winkel $\varphi$"); ax2.set_ylabel(r"Frequenz $\omega$")
    ax1.plot(np.linspace(tInit, tFinal, numSteps), values[0]) # plotte phi(t)
    ax2.plot(values[0], values[1]) # plotte w(phi)

def setMPLoptions():
    """Ein paar Matplotlib-Optionen für hübschere Darstellung setzen.
    """

    # Benötigt eine LaTeX-Installation. Falls eine solche nicht vorhanden ist,
    # einfach probieren, ob das Programm auch ohne den Aufrug dieser Funktion
    # funktioniert.
    
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["text.usetex"] = True # LaTeX für Achsenbeschriftung etc benutzen
    plt.rcParams["figure.dpi"] = 150 # LaTeX für Achsenbeschriftung etc benutzen
    plt.rcParams["font.size"] = 18.0 # font size for text
    plt.rcParams["xtick.labelsize"] = 18.0 # fontsize of the tick labels
    plt.rcParams["ytick.labelsize"] = 17.0 # fontsize of the tick labels
    plt.rcParams["legend.fontsize"] = 15.0 # legend font size
    plt.rcParams["legend.shadow"] = True # shadow around legend
    plt.rcParams["axes.titlesize"] = 18 # fontsize of the axes title
    plt.rcParams["axes.labelsize"] = 18 # fontsize of the x any y labels
    plt.rcParams["axes.linewidth"] = 2
    plt.rcParams["xtick.major.size"] = 5   # major tick size in points
    plt.rcParams["xtick.minor.size"] = 2.5   # minor tick size in points
    plt.rcParams["ytick.major.size"] = 5   # major tick size in points
    plt.rcParams["ytick.minor.size"] = 2.5   # minor tick size in points
    plt.rcParams["lines.markeredgewidth"] = 1.5 # tick width
    plt.rcParams["lines.linewidth"] = 2.0

#-----------------------------------------------------------------------
# das "Hauptprogramm":

fig = plt.figure(facecolor="white") # Matplotlib-Fenster
setMPLoptions()

# Matplotlib: Subplots hinzufügen:
ax1 = fig.add_subplot(121, autoscale_on=True,
                      xlabel=r"Zeit $t$", ylabel=r"Winkel $\varphi$")

ax2 = fig.add_subplot(122, autoscale_on=True,
                      xlabel=r"Winkel $\varphi$", ylabel=r"Frequenz $\omega$")

fig.subplots_adjust(bottom=0.2) # unter den Plots etwas Platz schaffen

# Regler für A hinzufügen:
ax_E = plt.axes([0.125, 0.1, 0.675, 0.03], axisbg="white")
sliderA  = Slider(ax_E, r'$A=$', Amin, Amax, valinit=A, valfmt='%1.2f')
sliderA.on_changed(Achanged) # Bei Werte-Änderung: Achanged() aufrufen

# Integrator erzeugen:
integrator = ode(bewGl).set_integrator('dopri5')

# Plot anzeigen:
plt.show()
