import SnmpOperations
import ipaddress
import threading
import time
from tkinter import *
from tkinter import ttk



oidsname = []
oidsname.append("uptime")
oidsname.append("contact")
oidsname.append("name")
oidsname.append("location")
oidsname.append("systemdescription")
oidsname.append("processnumber")
oidsname.append("ramsize")

uptime = "1.3.6.1.2.1.1.3.0"
contact =  "1.3.6.1.2.1.1.4.0"
name = "1.3.6.1.2.1.1.5.0"
location = "1.3.6.1.2.1.1.6.0"
systemDescription = "1.3.6.1.2.1.1.1.0"
processnumber = "1.3.6.1.2.1.25.1.6.0"
ramsize = "1.3.6.1.2.1.25.2.2.0"

oidarray = []
oidarray.append(uptime)
oidarray.append(contact)
oidarray.append(name)
oidarray.append(location)
oidarray.append(systemDescription)
oidarray.append(processnumber)
oidarray.append(ramsize)


root = None

ipEntry = None
comEntry = None
oidEntry = None

ipLabel = None
comLabel = None
oidLabel = None

getbutton = None

getsingleOIDbutton = None
scanbutton = None
getbutton = None

#ich weiß, bloßes exept nicht so gut weil es alles abfängt und man somit nicht weiß wo genau man einen fehler gemacht hat, aber fuer jetzt hab ich es mal so gemacht

def normget(ip, comunitystring):

    if comunitystring == "":
        comunitystring = "public"
    try:
        resultarray = SnmpOperations.get(ip, oidarray, comunitystring)
        j = 0;
        for i in oidarray:
            print(oidsname[j] + ": " + str(resultarray[i]))
            j = j+1
    except:
        print("Kann die Informationen dieser Adresse nicht abrufen.")


def sendget():
    ipformEntry = ipEntry.get()
    comfromEntry = comEntry.get()

    ipLabel.grid_forget()
    ipEntry.grid_forget()
    comLabel.grid_forget()
    comEntry.grid_forget()
    getbutton.grid_forget()

    print("")
    print("Infos ueber bestimmte IP:")
    print("")
    choosecommand()
    normget(ipformEntry, comfromEntry)

def scannet(network):
    
    try:
        if '/' not in network:
            raise Exception

        print("scanne Netzwerk " + network + " Es könnte einige Zeit dauern.")

        i = 0
        threads = []
        for ip in ipaddress.IPv4Network(network):
            threads.append(threading.Thread(target=getThread, args=(str(ip),)))
            threads[i].start()
            i = i+1

        print("Warte auf Antwort der Hosts...")
        for k in range(0, 254):
            threads[k].join()
        print("Netzwerkscan abgeschlossen!")


    except:
        print("Etwas beim scannen ist Falsch gelaufen")


def sendscan():
    ipformEntry = ipEntry.get()

    ipLabel.grid_forget()
    ipEntry.grid_forget()
    getbutton.grid_forget()

    print("")
    print("Netzwerkscan:")
    print("")
    choosecommand()
    scannet(ipformEntry)


def oidGet(ip, oid, comunitystring):
    if comunitystring == "":
        comunitystring = "public"

    varBinds = resultarrayspecific = SnmpOperations.getsingleoid(ip, oid, comunitystring)
    for varBind in varBinds:
        print(ip + ": " + varBind[1])

def sendOID():
    ipformEntry = ipEntry.get()
    comfromEntry = comEntry.get()
    oidfromEntry = oidEntry.get()

    ipLabel.grid_forget()
    ipEntry.grid_forget()
    comLabel.grid_forget()
    comEntry.grid_forget()
    oidLabel.grid_forget()
    oidEntry.grid_forget()
    getbutton.grid_forget()

    print("")
    print("Bestimmte OID:")
    choosecommand()
    oidGet(ipformEntry, oidfromEntry, comfromEntry)

def getThread(iptoscan):
    try:
        SnmpOperations.getsingleoid(iptoscan, oidarray[2], "public", True)
    except:
        #print("Kann die Informationen dieser Adresse nicht abrufen.")
        pass


def removecommandbuttons():
    getbutton.grid_forget()
    scanbutton.grid_forget()
    getsingleOIDbutton.grid_forget()

def guiGetIn():

    removecommandbuttons()

    global ipLabel
    ipLabel = Label(root, text="IP-Addresse", bg="white", fg="black")
    ipLabel.grid()
    global ipEntry
    ipEntry = Entry(root)
    ipEntry.grid()

    global comLabel
    comLabel = Label(root, text="comunity (wenn leer = public)", bg="white", fg="black")
    comLabel.grid()
    global comEntry
    comEntry = Entry(root)
    comEntry.grid()

    global getbutton
    getbutton = Button(root, text="send", bg="black", fg="white", command=sendget)
    getbutton.grid()


def guiScanIn():

    removecommandbuttons()

    global ipLabel
    ipLabel = Label(root, text="Netzwerk (z.B. 192.168.0.0/24)", bg="white", fg="black")
    ipLabel.grid()
    global ipEntry
    ipEntry = Entry(root)
    ipEntry.grid()

    global getbutton
    getbutton = Button(root, text="send", bg="black", fg="white", command=sendscan)
    getbutton.grid()


def guiGetoidIn():

    removecommandbuttons()

    global ipLabel
    ipLabel = Label(root, text="IP-Addresse", bg="white", fg="black")
    ipLabel.grid()
    global ipEntry
    ipEntry = Entry(root)
    ipEntry.grid()

    global comLabel
    comLabel = Label(root, text="comunity (wenn leer = public)", bg="white", fg="black")
    comLabel.grid()
    global comEntry
    comEntry = Entry(root)
    comEntry.grid()

    global oidLabel
    oidLabel = Label(root, text="OID", bg="white", fg="black")
    oidLabel.grid()
    oidLabel.grid()
    global oidEntry
    oidEntry = Entry(root)
    oidEntry.grid()

    global getbutton
    getbutton = Button(root, text="send", bg="black", fg="white", command=sendOID)
    getbutton.grid()


def choosecommand():

    global getbutton
    getbutton = Button(root, text="Get", height="5", width="30", bg="black", fg="white", command=guiGetIn)
    getbutton.grid()

    global scanbutton
    scanbutton = Button(root, text="Scan Network", height="5", width="30", bg="black", fg="white", command=guiScanIn)
    scanbutton.grid()

    global getsingleOIDbutton
    getsingleOIDbutton = Button(root, text="get single OID", height="5", width="30", bg="black", fg="white", command=guiGetoidIn)
    getsingleOIDbutton.grid()


def guiInit():
    
    global root
    root = Tk()
    root.geometry("220x258")
    root.title("SNMP GUI")


    """
    useGuibutton = Button(root, text="GUI verwenden", bg="black", fg="white", command=choosecommand)
    useGuibutton.grid()
    closeGui = Button(root, text="Gui schließen und Comandozeile Verwenden", bg="black", fg="white", command=root.destroy)
    closeGui.grid()
    """

    choosecommand()

    root.mainloop()


if __name__ == "__main__":

    guijanein = input("Willst du die Gui verwenden oder die Komandozeile benuzen? (GUI = ja/ Komandozeile = nein)")

    while True:
        if guijanein == "ja":
            print("Jetzt kannst du im GUI Fenster weitermachen. Ausgaben findest du jedoch trotzdem noch in der Komandozeile")
            guiInit()
            quit()
        elif guijanein == "nein":
            while True:
                command = input("was willst du machen? Infos von bestimmter IP bekommen (get), ein gesamtes Netzwerk scannen (scan), eine bestimmte OID einer IP (getOID), das Programm beenden(quit): ")
                if command == "get" :
                    ip = input("Gib IP-Adresse ein: ")
                    comunitystring = input("Geben sie einen Comunity String ein (nichts = public): ")
                    normget(ip, comunitystring)
                elif command == "scan":
                    network = input("Gib Netz-Adresse mit Subnetzmaske ein (z.B.: 192.168.0.0/24): ")
                    scannet(network)
                elif command == "getOID":
                    ip = input("Gib IP-Adresse ein: ")
                    oid = input("Gib die OID ein, die du auslesen moechtest: ")
                    comunitystring = input("Geben sie einen Comunity String ein (nichts = public): ")
                    oidGet(ip, oid, comunitystring)
                elif command == "quit":
                    quit()
                else:
                    print("falscher Befehl!!")

