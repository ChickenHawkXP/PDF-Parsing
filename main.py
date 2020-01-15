import os
import sys

os.system("pdf2txt -o workpdf.txt -F 1.0 -L 2.0 C:\\Users\\jayma\\OneDrive\\Desktop\\Python\\WorkParser\\test.pdf")

with open("workpdf.txt","r") as txtfile:
    text = txtfile.read()

splittxt = text.split("Presented By")

streetad = list()
towns = list()

for i in range(len(splittxt)):
    try:
        addressidx = splittxt[i].index("Address")
        style = splittxt[i].index("Rms")
        if addressidx > style:
            style = splittxt[i].index("List Ofc")
    except ValueError:
        break
    textrange = splittxt[i][addressidx:style]

    adrange = textrange.splitlines()
    rangeidx = adrange.index("Address")
    stopidx = adrange.index('')
    
    for j in adrange[rangeidx:stopidx]:
        if j == "Address":
             continue
        streetad.append(j)
        if j.find(" ") == -1:
            index = streetad.index(j)
            streetad[index-1] = streetad[index-1] + j
            streetad.pop(index)

for i in range(len(splittxt)):
    try:
        addressidx = splittxt[i].index("Town")
        style = splittxt[i].index("Rms")
        if addressidx > style:
            style = splittxt[i].index("List Ofc")
    except ValueError:
        break
    textrange = splittxt[i][addressidx:style]

    adrange = textrange.splitlines()
    rangeidx = adrange.index("Town")
    stopidx = adrange.index('')
    
    for j in adrange[rangeidx:stopidx]:
        if j == "Town":
             continue
        towns.append(j)
print(streetad)
print(towns)
with open("test.txt","w") as testing:
    for i in range(len(streetad)):
        testing.write(streetad[i])
        testing.write(" ")
        testing.write(towns[i])
        testing.write("\n")

#addressidx = text.index("Address\n")
#style = text.index("Style/Zoning/\n")
#rental = text.index("Rental Type\n")

#addresses = text[addressidx+1:style]

#ad = list()

#for i in addresses:
#    addressname = i.replace("\n","")
#    index = addresses.index(i)
#    lastaddress = addresses[index - 1].replace("\n","")
#
#    if i.find(" ") == -1 and len(lastaddress) > 16:
#         ad[index-1] = lastaddress + i
#    else:
#        ad.append(i)
#
#for i in ad:
#    print(i.replace("\n",""))


    