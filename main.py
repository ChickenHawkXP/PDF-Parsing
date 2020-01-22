import os
import sys
import xlsxwriter
import time
import datetime

date = "test"#datetime.date.today()

finalad = list()
finaltown = list()
finalnyad = list()
finalnytown = list()
#Function that takes a list, and fixes addresses that get separated by \n
def fixlist(adlist):
    for i in range(len(adlist)):
        try:
            if adlist[i].find(" ") == -1 or adlist[i].find(" ",len(adlist[i])-1) != -1:
                adlist[i] = adlist[i] + adlist[i+1]
                adlist.pop(i+1)
        except IndexError:
            break
    return adlist

def fixtown(townlist):
    for i in range(len(townlist)):
        try:
            if townlist[i] == "North ":
                townlist[i] = townlist[i] + townlist[i+1]
                townlist.pop(i+1)
        except IndexError:
            break
    return townlist

#Function being used to write into columns in excel
def write_excel(lista,listb):#,nylista,nylistb):
    headers = ["Full Address","Real Address","Town","State","ZIP","Name"]
    workbook = xlsxwriter.Workbook("%s.xlsx" %date)
    worksheet = workbook.add_worksheet()
    count = 2
    worksheet.write_row("A1",headers)
    for i in range(len(lista)):
        worksheet.write("B%d" %count,"%s"%lista[i])
        worksheet.write("C%d" %count,"%s"%listb[i])
        worksheet.write("F%d" %count,"Current Resident")
        worksheet.write("A%d" %count,"%s %s"%(lista[i],listb[i]))
        worksheet.write("D%d" %count,"CT")
        count = count + 1
    '''
    for i in range(len(nylista)):
        worksheet.write("B%d" %count,"%s"%nylista[i])
        worksheet.write("C%d" %count,"%s"%nylistb[i])
        worksheet.write("F%d" %count,"Current Resident")
        worksheet.write("A%d" %count,"%s %s"%(nylista[i],nylistb[i]))
        worksheet.write("D%d" %count,"NY")
        count = count+1
    '''
    print("Addresses Successfully Loaded into Excel!")
    workbook.close()

files = os.listdir("C:\\Users\\jayma\\OneDrive\\Documents\\GitHub\\WorkParser")
hotsheets = list()
cmas = list()

for pdfs in files: #Get each file that ends .PDF
    if pdfs.find("Hot_") != -1:
        hotsheets.append(pdfs)
    if pdfs.find("CMA_") != -1:
        cmas.append(pdfs)
    

for readpdf in range(len(hotsheets)): #Loop through the amount of hotsheets
    os.system("pdf2txt -o workpdf.txt -F 1.0 -L 2.0 C:\\Users\\jayma\\OneDrive\\Documents\\GitHub\\WorkParser\\%s" %hotsheets[readpdf])

    with open("workpdf.txt","r") as txtfile:
        text = txtfile.read()

    splittxt = text.split("Featured properties") #Split text by the bottom of each page

    streetad = list()

    print(hotsheets[readpdf])
    for i in range(len(splittxt)): #Loop throught the splits
        try:
            addressidx = splittxt[i].index("Address") # Find "Address" list 
            style = splittxt[i].index("Presented By") # Find "Presented By" list 
        except ValueError:
            break

        textrange = splittxt[i][addressidx:style]
        adrange = textrange.splitlines()

        rangeidx = adrange.index("Address")

        try:
            stopidx = adrange.index('')
        except ValueError:
            stopidx = len(adrange)
        
        for j in adrange[rangeidx:stopidx]:
            if j == "Address":
                continue
            streetad.append(j)
            index = streetad.index(j)

    newad = fixlist(streetad)
    towns = list()
    for i in range(len(splittxt)):
        
        try:
            addressidx = splittxt[i].index("Town\n")
            style = splittxt[i].index("Presented By")
        except ValueError:
            break

        textrange = splittxt[i][addressidx:style]

        adrange = textrange.splitlines()
        rangeidx = adrange.index("Town")

        try:
            stopidx = adrange.index('')
        except ValueError:
            stopidx = len(adrange)

        for j in adrange[rangeidx:stopidx]:
            if j == "Town":
                continue
            towns.append(j)

    newtowns = fixtown(towns)
    print(newad)
    print(newtowns)
    print(len(newad))
    print(len(newtowns))

    for ads in newad:
        finalad.append(ads)
    for ftowns in newtowns:
        finaltown.append(ftowns)
ctcount = len(finalad)+len(finaltown)
    #os.remove("C:\\Users\\jayma\\OneDrive\\Documents\\GitHub\\WorkParser\\%s" %hotsheets[readpdf])

"""
for readcma in range(len(cmas)): #Loop through the amount of cmas
    os.system("pdf2txt -o workpdf.txt C:\\Users\\jayma\\OneDrive\\Documents\\GitHub\\WorkParser\\%s" %cmas[readcma])

    with open("workpdf.txt","r") as txtfile:
        text = txtfile.read()

    splittxt = text.split("Information deemed") #Split text by the bottom of each page

    nystreetad = list()

    print(cmas[readcma])
    for i in range(len(splittxt)): #Loop throught the splits
        try:
            addressidx = splittxt[i].index("Address") # Find "Address" list 
            style = splittxt[i].index("© 2020 Hudson") # Find "© 2020 Hudson" list 
        except ValueError:
            break

        textrange = splittxt[i][addressidx:style]
        adrange = textrange.splitlines()

        rangeidx = adrange.index("Address")

        try:
            stopidx = adrange.index('')
        except ValueError:
            stopidx = len(adrange)
        
        for j in adrange[rangeidx:stopidx]:
            if j == "Address":
                continue
            nystreetad.append(j)
            index = nystreetad.index(j)

    nynewad = fixlist(nystreetad)
    nytowns = list()
    for i in range(len(splittxt)):
        
        try:
            addressidx = splittxt[i].index("Post Office\n")
            style = splittxt[i].index("© 2020 Hudson")
        except ValueError:
            break

        textrange = splittxt[i][addressidx:style]

        adrange = textrange.splitlines()
        rangeidx = adrange.index("Post Office")

        try:
            stopidx = adrange.index('')
        except ValueError:
            stopidx = len(adrange)
        for j in adrange[rangeidx:stopidx]:
            if j == "Post Office":
                continue
            nytowns.append(j)
    
    print(nynewad)
    print(nytowns)
    print(len(nynewad))
    print(len(nytowns))

    for ads in nynewad:
        finalnyad.append(ads)
    for ftowns in nytowns:
        finalnytown.append(ftowns)

    #os.remove("C:\\Users\\jayma\\OneDrive\\Documents\\GitHub\\WorkParser\\%s" %cmas[readcma])
"""   
write_excel(finalad,finaltown)#,finalnyad,finalnytown)