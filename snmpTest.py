import SnmpOperations
import ipaddress

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
                for ip in ipaddress.IPv4Network(network):
                    print(ip)
            except:
                print("Etwas beim scannen ist Falsch gelaufen")
        else:
            print("falscher Befehl!!");
