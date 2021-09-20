#importiere benötigte Erweiterungen
import serial
import time


keynotes = "Megalovania.txt" #Name der Textdatei
arduino = None
#Warte bis ein Arduino gefunden wurde
while arduino is None:
    try:
        arduino = serial.Serial("COM4", 9600, timeout = 0.05) #Sucht nach dem Microcontroller. "COM4" muss an wenn nötig verändert werden!!!
    except:
        time.sleep(1) #Wurde kein Arduino gefunden, soll eine Sekunde gewartet werden
        pass

file = open(keynotes, "r") #Öffne die Textdatei



contents = file.read().replace(" ", "") #Lies den Text und entferne alle Leerzeichen
buzzers = contents.split(":") #Die Textdatei enthält Informationen über zwei Buzzer. Diese werden durch ein ':' getrennt. Hier werden die Buzzer aufgeteilt

#Die Abschnitte der Buzzer sind nochmals in eigene Abschnitte eingeteilt. Im ersten Abschnitt sind die Daten über die Frequenzen, im zweiten über die Längen.
#Diese Abschnitte werden durch ein '#' getrennt. Hier werden die Abschnitte den Zeilen nach aufgeteilt
frequencies1 = buzzers[0].split("#")[0].split("\n")
durations1 = buzzers[0].split("#")[1].split("\n")
frequencies2 = buzzers[1].split("#")[0].split("\n")
durations2 = buzzers[1].split("#")[1].split("\n")

#Eine Funktion mit einer Directory wird definiert, welche die Frequenzenvon allen Noten, sowie die Längen, beinhaltet.
def switch(argument):
    switcher = {
        "B0": "31",
	"C1": "33",
    	"CS1": "35",
    	"D1": "37",
    	"DS1": "39",
    	"E1": "41",
    	"F1": "44",
    	"FS1": "46",
    	"G1": "49",
        "GS1": "52",
    	"A1": "55",
        "AS1": "58",
	"B1": "62",
    	"C2": "65",
    	"CS2": "69",
    	"D2": "73",
    	"DS2": "78",
    	"E2": "82",
    	"F2": "87",
    	"FS2": "93",
    	"G2": "98",
    	"GS2": "104",
    	"A2": "110",
    	"AS2": "117",
    	"B2": "123",
    	"C3": "131",
    	"CS3": "139",
    	"D3": "147",
    	"DS3": "156",
    	"E3": "165",
    	"F3": "175",
    	"FS3": "185",
    	"G3": "196",
    	"GS3": "208",
    	"A3": "220",
    	"AS3": "233",
    	"B3": "247",
    	"C4": "262",
    	"CS4": "277",
    	"D4": "294",
    	"DS4": "311",
    	"E4": "330",
    	"F4": "349",
    	"FS4": "370",
    	"G4": "392",
    	"GS4": "415",
    	"A4": "440",
    	"AS4": "466",
    	"B4": "494",
    	"C5": "523",
    	"CS5": "554",
    	"D5": "587",
    	"DS5": "622",
    	"E5": "659",
    	"F5": "698",
    	"FS5": "740",
    	"G5": "784",
    	"GS5": "831",
    	"A5": "880",
    	"AS5": "932",
    	"B5": "988",
    	"C6": "1047",
    	"CS6": "1109",
    	"D6": "1175",
    	"DS6": "1245",
    	"E6": "1319",
    	"F6": "1397",
    	"FS6": "1480",
    	"G6": "1568",
    	"GS6": "1661",
    	"A6": "1760",
    	"AS6": "1865",
    	"B6": "1976",
    	"C7": "2093",
    	"CS7": "2217",
    	"D7": "2349",
    	"DS7": "2489",
    	"E7": "2637",
    	"F7": "2794",
    	"FS7": "2960",
    	"G7": "3136",
    	"GS7": "3322",
    	"A7": "3520",
    	"AS7": "3729",
    	"B7": "3951",
    	"C8": "4186",
    	"CS8": "4435",
    	"D8": "4699",
    	"DS8": "4978",
        "P":"0",
        "_1":4,
        "_2":2,
        "_4":1,
        "_8":0.5,
        "_16":0.25,
        "_32":0.125
    }
    return switcher.get(argument, argument)

#In unserer Textdatei sind manchmal Ausdrücke wie '_8 - _32' zu finden. Die nachfolgenden beiden Funktionen haben die Aufgabe solche mathematischen Operationen in Strings möglich zu machen.
#checkIfMath Funktion wird definiert. Sie testet, ob eine (weitere) mathematische Operation durchgeführt werden muss
def checkIfMath(elem):
    if elem.find('-') != -1 or elem.find('+') != -1 or elem.find('/') != -1:
        return True
    return False
#math Funktion wird definiert. Sie führt die mathematischen Operationen innerhalb eines Strings aus.
def math(elem):
    #Teste, ob eine Subtraktion durchgeführt werden muss
    if elem.find('-') != -1:
        elements = elem.split("-")
        if checkIfMath(elements[0])==True:
            elements[0] = math(elements[0])
        if checkIfMath(elements[1])==True:
            elements[1] = math(elements[1])
        return float(switch(elements[0]))-float(switch(elements[1]))
    #Teste, ob eine Addition durchgeführt werden muss
    if elem.find('+') != -1:
        elements = elem.split('+')
        if checkIfMath(elements[0])==True:
            elements[0] = math(elements[0])
        if checkIfMath(elements[1])==True:
            elements[1] = math(elements[1])
        return float(switch(elements[0]))+float(switch(elements[1]))
    #Teste, ob eine Division durchgeführt werden muss
    if elem.find('/') != -1:
        elements = elem.split('/')
        if checkIfMath(elements[0])==True:
            elements[0] = math(elements[0])
        if checkIfMath(elements[1])==True:
            elements[1] = math(elements[1])
        return float(switch(elements[0]))/float(switch(elements[1]))
#changeContent Funktion wird definiert. Sie ändert die Namen der Noten auf Freqeunzen und die Notenlängen auf Dezimalzahlen.    
def changeContent(array):
    #Teile den Array nach Zeilen auf
    for line in array:
        lineElements = line.split(",") #Teile die Zeile in ihre Elemente
        x = "" #Umgewandelter String
        i = 0
        for elem in lineElements:#Für jedes Element in der Zeile
            #Füge ein Beistrich an den String an, außer es ist das erste Element
            if not i == 0:
                x += ","
            #Teste, ob eine mathematische Operation durchgeführt werden muss
            if checkIfMath(elem)==True:
                x += str(math(elem)) #Hänge das Ergebnis an den String an
                i+=1
                continue
            #Wenn das Element nicht leer ist
            if not elem == "":
                x += str(switch(elem)) #Hänge das Element an den String an
            i+=1
        array[array.index(line)]="".join(x) #Ersetze die Zeile durch den neuen String
    #Entferne das letzte Element des Arrays, wenn dieses leer ist
    if array[len(array)-1]=="":
        array.pop()
#Ändere den Inhalt von allen vier Listen        
changeContent(frequencies1)
changeContent(durations1)
changeContent(frequencies2)
changeContent(durations2)

#Definiere die Funktion getTwoLines. Sie fügt zwei Zeilen aneinander und gibt diese als ganzen String aus.
def getTwoLines(i, array):
    fourLines = ""
    for j in range(i, len(array)):
        if not j == i:
            fourLines+=","
        fourLines+=array[j]
        if j >= i+1:
            break;
        
    return fourLines
firstTime = True;
input("Press 'Enter' to Start") #Frage nach Input zum Fortfahren
repeat = ""
while repeat!="q":
    for i in range(0,len(frequencies1),2):
        #Warte auf Erlaubnis vom Arduino, außer beim ersten Mal
        while arduino.readline().decode('ascii') == "" and firstTime==False:
            time.sleep(0.01)
        firstTime = False;
        print("Sending...")
        arduino.write(bytes(getTwoLines(i,frequencies1),"utf-8"))#Sende die Frequenzen vom ersten Buzzer
        while arduino.readline().decode('ascii') == "": #Warte auf Erlaubnis zum Fortfahren
            time.sleep(0.01)
        arduino.write(bytes(getTwoLines(i,frequencies2),"utf-8"))#Sende die Frequenzen vom zweiten Buzzer
        while arduino.readline().decode('ascii') == "": #Warte auf Erlaubnis zum Fortfahren
            time.sleep(0.01)
        arduino.write(bytes(getTwoLines(i,durations1),"utf-8")) #Sende die Tonlängen vom ersten Buzzer
        while arduino.readline().decode('ascii') == "": #Warte auf Erlaubnis zum Fortfahren
            time.sleep(0.01)
        arduino.write(bytes(getTwoLines(i,durations2),"utf-8")) #Sende die Tonlängen vom zweiten Buzzer
        while arduino.readline().decode('ascii') == "": #Warte auf Erlaubnis zum Fortfahren
            time.sleep(0.01)
        print("Done!")
    while arduino.readline().decode('ascii') == "" and firstTime==False: #Warte auf Erlaubnis zum Fortfahren
        time.sleep(0.01)
    firstTime = True
    repeat = input("Type 'q' to quit or press 'Enter' to repeat!\n") #Wiederhole die Melodie, außer wenn 'q' eingegeben wurde




