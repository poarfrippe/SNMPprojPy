import SnmpOperations
import ipaddress
import threading
import time

#ich weiß, bloßes exept nicht so gut weil es alles abfängt und man somit nicht weiß wo genau man einen fehler gemacht hat, aber fuer jetzt hab ich es mal so gemacht

def getThread(iptoscan):
    print("Thread fuer ip " + str(iptoscan)+ " gestartet")
    try:
        #time.sleep(1)
        resultarray = SnmpOperations.get(iptoscan, oidarray, "public")
        print("Informationen zum Geraet mit der IP: " + str(iptoscan))
        j = 0;
        print("")
        print("")
        for i in oidarray:
            print(oidsname[j] + ": " + str(resultarray[i]))
            j = j+1
        print("")
        print("")
    except:
        #print("Kann die Informationen dieser Adresse nicht abrufen.")
        pass

def prbierthread(scannip, oidarrayinfunc):
    print("Probieren mit der IP: " + str(scannip))

    gegettet = SnmpOperations.get(scannip, oidarray, "public")
    for i in oidarrayinfunc:
        print(str(gegettet[i]))
    

if __name__ == "__main__":

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

    while True:
        command = input("was willst du machen? Infos von bestimmter IP bekommen (get) oder ein gesamtes Netzwerk scannen (scan)")
        if command == "get" :
            ip = input("Gib IP-Adresse ein!!")

            #testthread = threading.Thread(target=prbierthread, args=(ip, oidarray))
            #testthread.start()
            #time.sleep(2)

            try:
                resultarray = SnmpOperations.get(ip, oidarray, "public")
                j = 0;
                for i in oidarray:
                    print(oidsname[j] + ": " + str(resultarray[i]))
                    j = j+1
            except:
                print("Kann die Informationen dieser Adresse nicht abrufen.")
        elif command == "scan":
            network = input("Gib Netz-Adresse mit Subnetzmaske ein (z.B.: 192.168.0.0/24)")
            try:
                if '/' not in network:
                    raise Exception

                threads = []
                i = 0
                for ip in ipaddress.IPv4Network(network):
                    threads.append(threading.Thread(target=getThread, args=(str(ip),)))
                    threads[i].start()
                    threads[i].join()   #dauert zwar sehr sehr lange und der Thread hat keinen nutzen, so funktioniert es aber. sonst aus irgend einenm Grund nicht
                    i = i+1

                #print("now joining threads")
                #for k in range(0, 254):
                    #threads[k].join()

            except:
                print("Etwas beim scannen ist Falsch gelaufen")
        else:
            print("falscher Befehl!!")
