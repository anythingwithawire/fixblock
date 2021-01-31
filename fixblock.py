import glob, os


print("This reads in the DAD preview*.pdf files and looks for names.txt file with a list of names in it to place on the drawing titleblock.\nThis is usually a copy paste of the layout titles, but does not have to be.\nThe number of names/lines  in the names.txt file must equal number of preview files.\nThen it adds tblock.pdf as a stamp over the top of each drawing using pdftk.\nIt then uses ghostscript and a pdfmark file based on basepdfmark.txt to write in title block description, being the name from from the names.txt file.\nIt also writes AA of BB for sheet numbers based on the number of the drawing being processed and the total number of drawings.\nbasepdfmark.txt will have a replace of XXXXXX with the name from the names.txt and YYYYYY with AA of BB.\nYou must edit the basepdfmark.txt with the desired co-ords, font etc etc and it will be applied to all sheets.\nSee example pdfmark inside source code\nThe final output is a series of files 0001.pdf on, where the number matches the sheet number.\nIn case it is not obvious, the order of the preview files and the names.txt list must match.\nNote this version is for linux and uses gs for ghostscript command, for windows edit second last line of code or make a symlink or batch file for gswin64c to gs\n\n")

#
#%typical basepdfmark.txt
#
#%gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=combine.pdf -dBATCH 1.pdf 2.pdf
#
#
#%gs -o MySuperPDF.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress xxxxxx.pdf addtext.txt
#
#[
#/SrcPg 1 
#/Rect [2100 100 2300 150] 
#/Subtype /FreeText 
#/Color [1 1 1] 
#/DA ([0 0 0] rg /CoBo 22 Tf) 
#
#/BS << /W 2 >> 				% border width
#/Q 1                      % centred
#/Contents (XXXXXX) 
#/ANN pdfmark
#
#[
#/SrcPg 1 
#/Rect [2400 100 2500 150] 
#/Subtype /FreeText 
#/Color [1 1 0] 
#/DA ([0 0 0] rg /Cour 12 Tf) 
#/Q 1                      % centred
#/Contents (YYYYYY) 
#/ANN pdfmark
#
#

 

print(os.getcwd())
os.chdir("/home/gareth/Documents/")

#get new file names
file1 = open("namefile.txt","r")
names=file1.readlines()
file1.close()

if (len(names)==0):
    print("error - no names found")
    exit(2)

print(len(names),"names read \n")

for name in names:
    print(name.strip())

#get files
n=0
for n,f in enumerate(glob.glob("preview*.pdf"), start=1):
    print(n, f)

if (len(names) != n) or (n==0):
    print("\nerror - numbers of names ({}) and number of files ({}) do not match\n".format(len(names), n))
    exit(1)

#now rename the files in order with the names in the list
for n,f in enumerate(glob.glob("preview*.pdf"), start=1):
    pdfname=names[n-1].strip() + ".pdf"
    os.rename(f, pdfname)
    #go thru each file and make a pdfmark to fix it
    #now make the pdf mark file to fix the title blocks
    # Read in the file

    with open('basepdfmark.txt', 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('XXXXXX', names[n-1].strip(".pdf\n"))
    sheet = "{} of {}".format(str(n).zfill(2),str(len(names)).zfill(2))
    filedata = filedata.replace('YYYYYY', sheet)

    # Write the file out again
    with open('pdfmark.txt', 'w') as file:
      file.write(filedata)

    cmd='gs -o {}.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress "'"{}.pdf"'" pdfmark.txt'.format(str(n).zfill(4), names[n-1].strip())

	#cmd='gswin64c -o {}.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress "'"{}.pdf"'" pdfmark.txt'.format(str(n).zfill(4), names[n-1].strip())


    print("\ncmd is : ", cmd)
    print("\n")

    os.system(cmd)
