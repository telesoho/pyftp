import os
import ftplib
import glob
import io

localdir = "/root/prjs/pyftp/test/*"
remotedir = "/test"
host = os.environ.get("FTP_HOST")
user = os.environ.get("FTP_USER")
password = os.environ.get("FTP_PASSWORD")
ftp = ftplib.FTP(host, user, password)
ftp.cwd(remotedir)

for upfile in glob.glob(os.path.join(localdir)):
    with open(upfile, 'rb') as thefile:
        print(thefile.name)
        try:
            filename = os.path.basename(thefile.name)
            iret = ftp.storlines('STOR '+ filename, thefile)
            print(iret)
            if iret == "226 Transfer OK":
                # transfer result file to server
                bio = io.BytesIO("DONE")
                iret = ftp.storlines("STOR " + filename[:filename.index(".")], bio)
                # delete the transfered file
                if iret == "226 Transfer OK":
                    os.remove(thefile.name)
        except Exception, e:
            print(e)

ftp.quit()
