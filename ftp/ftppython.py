#ftppython
from ftplib import FTP

#domain name or server ip:
ftp = FTP('54.237.192.107')

ftp.login(user='redesie1', passwd = 'redesie2017')

#ftp.cwd('/folder1/')

#Subir archivo
filename = 'exampleFile1.txt'
ftp.storbinary('STOR '+filename, open(filename, 'rb'))
#ftp.quit()

#Bajar Archivo
filename = 'archivo.txt'

localfile = open(filename, 'wb')
ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

ftp.quit()
localfile.close()
