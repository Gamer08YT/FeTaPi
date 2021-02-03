# FeTaPi

1. Beweggründe
2. Was wird benötigt
3. Hardware
4. Software
5. Kurzfassung (tl;dr)
6. Funktion des Skriptes
7. Debug

## Beweggründe
FeTaPi ist ein in Python 3 geschriebener Skript, welcher es ermöglicht ein Fernsprechtischapparat (FeTap) mit SIP zu betreiben. Dabei wird die Wählscheibe als direkte Eingabe genutzt und ein SIP Client (linphone), welcher auf dem Raspberry Pi betrieben wird, sorgt für die Telefonie. Der Wecker des FeTaps wird hierbei als Klingel für eingehende Anrufe benutzt und der Hörer über eine USB Soundkarte betrieben.

Ziel war es, die alten Fernsprechtischapparate der alten Post, erneut ein Leben zu geben und an das [Eventphone](https://eventphone.de/) anzubinden, um zum Beispiel auf Events des CCCs diese Telefone ohne TAE Stecker zu nutzen. 

Es werden nur minimale Lötarbeiten benötigt, welche man aus der folgenden Grafik entnehmen kann.

## Was wird benötigt

1. Raspberry Pi Zero
2. Lötwerkzeug
3. 1 Kanal Relais 5V/230V
    4. Alternativ ein Boost-Buck Converter von 5V auf 9V
4. USB Soundkarte
5. USB auf MicorUSB Adapater
6. 9V Batterie + Betterieclip
    7. Entfällt bei der Nutzung des Boost-Buck Converter
7. Fetap 791-1
8. Jumper Kabel 

## Hardware

![https://git.elektrollart.org/Elektroll/fetapi/raw/branch/master/img/pytap-plan.png](https://git.elektrollart.org/Elektroll/fetapi/raw/branch/master/img/pytap-plan.png)

![https://www.elektrollart.org/wp-content/uploads/IMG_7392.jpg](https://www.elektrollart.org/wp-content/uploads/IMG_7392.jpg)
*Fotografie aller Bauteile*

Am Telefonhörer müssen die Leitungen vom Hörer (Gelb und Grün) und vom Mikrofon (Braun und Weiß) an eine USB Soundkarte angebracht werden. Hierzu wurden die Kabel an Klinkenstecker gelötet und diese in die Soundkarte gesteckt. Hierzu wird noch ein Adapter von USB auf Micro USB benötigt, da ich ein Raspberry Pi Zero benutze und dieser nur einen MicroUSB Anschluss hat.

![](https://www.elektrollart.org/wp-content/uploads/IMG_7342-2.jpg)
![](https://www.elektrollart.org/wp-content/uploads/IMG_7396.jpg)
*Fotografie der Wählscheibe von Oben und von der Seite*

Die Wählscheibe besteht aus zwei Kontakten die zur Impulswahl führen. Der Kontakt, wenn die Drehscheibe angezogen wird (Weiß und Braun) und den Impuls für die gewählte Nummer (Grün und Gelb). Hier wird nur Grün und Gelb benötigt. Zwar könnte man Weiß und Braun für die Kontrolle nehmen und nur die Nummer wählen, wenn Braun und Weis deren Kontakt schließen, aber für das Ziel spielt das hierbei keine Relevanz. Grün und Gelb werden beim zurück rotieren der Scheibe vermehrt den Kontakt abbrechen und wieder aufbauen. Diese Impulse werden gezählt, um die gewählte Nummer zu definieren. Die Kabel aus der Wählscheibe (Grün und Gelb) werden an Jumper Kabel gelötet (oder anderweitig verbunden), damit man diese an das GPIO Head (GPIO 26 und GPIO 21) vom Raspberry Pi anbringen kann.

![https://www.elektrollart.org/wp-content/uploads/IMG_7341-1.jpg](https://www.elektrollart.org/wp-content/uploads/IMG_7341-1.jpg)
*Fotografie der Platine*

Auf der Platine des FeTAp befindet sich oben Rechts die Telefongabel (GU), welche die Telefonate terminiert oder annimmt, je nachdem ob die Gabel nach unten gedrückt ist oder oben steht. Hier entnahm ich aus dem gedrückten Zustand der Gabel die Kontakte auf der Platine (Blau und Rot). Damit soll beim geschlossenen Kreislauf eine Anrufbereitschaft bestehen, bzw. wenn die Gabel runtergedrückt wird, das Telefonat beenden. Beim wechsel von gedrückt nach Oben wird der Kontakt gelöst und das Telefonat soll entgegengenommen werden, bzw. es darf eine Nummer gewählt werden. An die Kontakte TWB3 und NS3 auf der Platine können Jumper Kabel gelötet werden, bzw. auf die beiden mittleren Kontakte (Rot und Blau) unter der Gabel (diese muss vom Board gelötet werden) welche ans Raspberry Pi GPIO Head GPIO 20 und GPIO 6 gesteckt wurden.

![https://www.elektrollart.org/wp-content/uploads/IMG_7394.jpg](https://www.elektrollart.org/wp-content/uploads/IMG_7394.jpg)
*Fotografie der Gabel von Unten*

Um den Wecker zu betreiben, habe ich eine 9V Batterie und ein Relais Modul genommen. Das Relais wird an den GPIO 3.3 Volt (Grau), GND (Grün) und GPIO 17 (Magenta) Pin verbunden. Vom Relais geht ein Kabel von NO (Blau) an den Minus Pol des Weckers. Von COM (Schwarz) geht ein Kabel an den Minus Pol der Batterie. Der Plus Pol der Batterie ist mit dem Plus Pol des Weckers verbunden.

In der Zweiten Version wurde anstelle des 9V Blocks, ein Boost-Buck Converter genutzt. ([Zumbeispiel](https://de.aliexpress.com/item/32963598972.html?spm=a2g0o.productlist.0.0.628b2f84lovNSv&algo_pvid=62e085f4-57f2-4a6b-98f8-d2d6d9196dae&algo_expid=62e085f4-57f2-4a6b-98f8-d2d6d9196dae-14&btsid=0b01114516123906300575912e3cc2&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)) 

Hierzu wurde die Verkabelung wie Folgt durchgeführt:

**Raspberry Pi an Converter**
GND -> VIN-
GPIO 17 -> VIN+
5V -> EN

**Converter an Wecker**
Volt + -> Schwarze Ader in der Grafik
Volt - -> Blaue Ader in der Grafik

## Software 

Für den Betrieb wird ein Raspberry Pi, mit Debian Buster, Python 3, linphone und Pulseaudio benötigt:

1. [Download](https://downloads.raspberrypi.org/raspios_lite_armhf_latest) Raspberry Pi OS (32-bit) Lite (Buster)
Source: https://www.raspberrypi.org/downloads/raspberry-pi-os/

2. Zip Archiv entpacken

3. Image auf die SD-Karte schreiben (unter Linux):
```
$ dd if=/path/to/file/2020-05-27-raspios-buster-lite-armhf.img of=/dev/mmcblk0 bs=1M
(/dev/mmcblk0 die SD-Karte gelesen vom intern verbauten Lesegerät )
```

4. Nach Abschluss des Schreibvorganges wird die root und boot Partition 
```
$ mount /dev/mmcblk0p2 /media/root
$ mount /dev/mmcblk0p1 /media/root/boot
```

5. Wifi Credentials in die wpa_supplicant.conf eintragen
```
$ nano /media/root/etc/wpa_supplicant/wpa_supplicant.conf
```
add  wifi credentials
```
network={
        ssid="Netzwerkname"
        psk="meinschluessel"
}
```
6. OnBoard Soundkarte deaktivieren
```
echo 'blacklist snd-bcm2835' >> /media/root/etc/modules
```
6. SSH aktivieren
```
$ touch /media/root/boot/ssh
```
7. root und boot unmounten
```
$ umount /media/root/boot
$ umount /media/root
$ sync
```
8. Den Raspberry Pi starten
9. Via SSH zum Raspberry Pi verbinden:
```
ssh pi@xxx.xxx.xxx.xxx
password: raspberry
``` 
10. Abhängigkeiten installieren
```
$ sudo apt update
$ sudo apt install git linphone pulseaudio python3-pip
$ pip3 install RPi.GPIO
```
11. FeTaPi Repository klonen
```
$ git clone https://git.elektrollart.org/Elektroll/fetapi.git 
```
12. In die run.py unter Zeile 25 die SIP Zugangsdaten eintragen
13. Pulseaudio aktivieren und script ausführen:
```
pulseaudio --start
python3 run.py
```
14. Wenn alles nach funktioniert, kann der Autostart eingerichtet werden.
```
echo "cd /home/pi/fetapi/;/usr/bin/python3 /home/pi/fetapi/run.py" >> /home/pi/.bashrc
sudo raspi-config
```
Stellt ein, dass ein automatischer Login in die CLI nach dem Boot ausgeführt wird.


## Kurzfassung:

1. Lautsprecher und Mikrofon an eine USB Soundkarte anbringen
2. Die Kontakte Gelb und Grün an GPIO 26 und 21 anbringen
3. Telefongabel Rot und Blau an GPIO 20 und 6 anbringen
4. GPIO 17, 3.3v und GND mit dem Relai verbinden, diesen mit dem Wecker verbinden
4. Script auf ein RPi mit Debian Buster kopieren
5. SIP Credentials in Zeile 25 eintragen
6. Autostart einrichten

## Funktion des Skriptes:

**ACHTUNG**
Durch die letzte Anpassung am Skript, stimmt die Dokumentation nicht im ganzen
**/ACHTUNG**

In der Funktion **dialnumber** wird die Rufnummer der Wählscheibe gelesen, in dem beim Zurück rotieren der Wählscheibe, die Kontaktabbrüche von GPIO 21 und GPIO 26 gezählt werden. In Zeile 56 steht **time.sleep(0.109)**, dieser Wert wird als Pause zwischen den Impulsen benötigt und kann gegebenenfalls feiner eingestellt werden, sollte die Wählscheibe schneller oder langsamer rotiert, als die in meinem Telefon. 

Solange GPIO 6 und GPIO 20 einen geschlossenen Kreis bilden, läuft eine Schleife in dem der Status von linphone nach eingehenden Anrufen geprüft wird. In der Funktion **CALL** wird dies mit **if RINGVALUE == 'IncomingReceived':** getätigt. Bei einem eingehenden Anruf wird dann die Funktion **wecker** geschaltet. Diese Funktion gibt nur an das Relais Modul ein Up und Down weiter, welcher den Kreislauf der 9V Batterie mit dem Wecker schließt und damit den Wecker klingeln lässt. 

Sobald der Hörer abgehoben wird und GPIO 6 und GPIO 20 keinen Kreislauf haben, wird nach einem eingehenden Anruf geprüft. Bei einem eingehenden Anruf wird die Funktion **answer** aufgerufen. Diese fragt bei linphonem nach der eingehenden Call ID und gibt diese ID an linphone zur Rufannahme weiter. 

Sollte hingegen beim Hörer heben kein eingehender Anruf vorhanden sein, soll die **dialnumber** Funktion aufgerufen werden. 

Die **dialnumber** Funktion macht solange nichts, bis eine Nummer gewählt wurde. Sobald die erste Nummer gewählt ist, startet ein Countdown, welcher bei jeder weiteren gewählten Nummer resetet wird. Sobald der Countdown runtergezählt wurde, wird die Nummer in die dial.txt geschrieben und von liphone via SHELL aufgerufen und die Nummer gewählt. 

In allen Situationen wird beim Schließen des Kreislaufes von GPIO 6 und GPIO 20 das Telefonat oder die Rufnummernwahl beendet. Das wird in der Funktion hangup definiert. 

![](https://www.elektrollart.org/wp-content/uploads/IMG_7407-1024x633.jpg)

## Debug 
Im Debug Verzeichnis befinden sich zwei Python Skripte.

Die dial.py kann genutzt werden um die Funktionalität der Wählscheibe zu überprüfen und gegebenfalls einzustellen.
Nachdem Ausführen kann direkt getestet werden, ob beim rotieren der Wählscheibe, die korrekte Nummer angezeigt wird. Sollte es dazu kommen, dass die gewählte Nummer abweicht, kann dies im Sleep der 37 angepasst werden. Dieser Sleep steht im Default auf 0.109. In Zeile 39 kann der Countdown vom Zietpunkt der Wahl und Anzeige konfiguriert werden.

Die ring.py lässt sofort den Hammer des Weckers in einer Schleife schlagen. Dies kann benutzt werden um die Verklabung zu überprüfen.