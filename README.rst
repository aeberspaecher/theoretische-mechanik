=====================
Theoretische Mechanik
=====================

Zur Vorlesung Mechanik und Elektrodynamik (Teilmodul 1) von Prof. Wiersig
wollen wir ab und an Aufgaben stellen, die mit dem Computer zu bearbeiten
sind. Beispiel-Lösungen dazu will ich hier veröffentlichen.

Außerdem soll Material aus dem Seminar - insbesondere Computer-Code - auch
hier zugänglich gemacht werden.

Hier eine Liste der einzelnen Verzeichnisse und eine kurze Beschreinung
dessen, was darin zu finden ist:

Seminar1
========

Das Aufgabenblatt aus dem ersten Seminar und eine Beispiellösung für die
dritte Aufgabe ("ein erster Kontakt mit dem Chaos"). Benötigt dafür: Python,
NumPy, SciPy, matplotlib. Linux-Nutzer wissen wahrscheinlich, wie sie die
benötigte Software installieren können, Windows-Nutzer besuchen bitte
http://www.lfd.uci.edu/~gohlke/pythonlibs/

Übung 2
=======

Die vierte Aufgabe (Doppelmuldenpotential) wird hier numerisch gelöst. Das
Python-Skript erlaubt die numerische Integration der Bewegungsgleichung
(ohne Näherung!). Gezeigt werden:

- oben links: die Potentiallandschaft und die Energie des Teilchens, das
  sich darin bewegt
- oben rechts: x(t) und y(t), numerisch exakt ausintegriert
- unten links: potentielle Energie V und kinetische Energie T als Funktionen
  der Zeit t sowie die Summe von beiden (hoffentlich erhalten, da
  konservatives System)
- unten rechts: diskrete Fourier-Transformation von x(t) - mit anderen Worten:
  eine Zerlegung der Schwingung nach harmonischen Schwingungen. Sie sehen
  den Betrag der Amplitude des Beitrages durch die jeweilige Frequenz.
  Eingezeichnet wird außerdem wird die Frequenz des harmonischen Oszillator,
  den sie durch die Taylor-Näherung in den Potentialminima erhalten haben.

Was wird simuliert?
-------------------

Es wird die Bewegung eines Teilchens, das sich bei t=0 im linken
Potential-Minimum befindet simuliert. Die Gesamtenergie E = T + V wird durch
Wahl einer passenden Anfangsgeschwindigkeit v_0 so gewählt, dass das Teilchen
genau die Energie E hat, die sie mit dem Regler einstellen können (v_0 > 0,
also am Anfang Bewegung nach rechts).

Für die Simulation ist a=2.

Was sehen sie?
--------------

Bei kleinen Energien passt die harmonische Näherung fantastisch. Sie bekommen
harmonische Schwingungen mit der Frequenz des harmonischen Oszillators. Der
Beitrag von der 'Schwingung' mit Frequenz 0 erklärt sich dadurch, dass die
Schwingung nicht um x=0 herum geschieht, sondern um x=-2.

Bei größeren Energien (aber E<0, also so dass das Teilchen noch nicht über den
Potentialberg bei x=0 rutschen kann) sehen Sie, wie die Schwingung anharmonisch
wird. Bei E nahe 0 sehen Sie, wie das Teilchen sich auf den Berg zubewegt, dort
langsam wird (fast die gesamte Energie steckt ist dort potentielle, nicht
kinetische Energie), und schließlich wieder zurückschwingt.

Bei Energien > 0 kann das Teilchen den Berg passieren, der Beitrag der
Schwingung mit Frequenz 0 verschwindet. Das Teilchen kann beide Minima besuchen.

Bei sehr großen Energien spürt das Teilchen kaum noch etwas vom Berg (man
beachte hier die winzigen Dips in der kinetischen Energie).

Spitzfindigkeit
---------------

Um hier intensiv mit der Fourieranalyse zu arbeiten müssten wir eigentlich
voraussetzen, dass das analysierte Signal (hier: 0 < t < 10) periodisch ist,
was hier i.a. nicht so ist - die resultierenden Effekte (Gibbsches Phänomen)
spielen hier aber keine Rolle.
