import SnmpOperations

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




    ip = input("Gib IP-Adresse ein!!")

    resultarray = SnmpOperations.get(ip, oidarray, "public")

    j = 0;

    for i in oidarray:
        print(oidsname[j] + ": " + str(resultarray[i]))
        j = j+1
