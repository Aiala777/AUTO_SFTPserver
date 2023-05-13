import os
import paramiko
from datetime import date, timedelta, datetime
import os, gzip, shutil
import schedule
import time

yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m')
today = datetime.now().strftime("%Y%m%d")
aux = ('COB'+today)
host = ""
transport = paramiko.Transport((host))
username = ""
mykey = ""
# localpath = "C:/Users/rafaelvilela/Desktop/MEGAsync/Code/ftp/"
# remotepath = "/processed/COB20220503_0616_FT5Placement_ArrangementsUpdates_01052022_01.txt"

def main():

    print ("Connecting...")
    transport.connect(username = username, pkey = mykey)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print ("Connected.")
    #print (sftp.listdir())
    files = sftp.listdir('/processed')
    for i, file in enumerate(files):
        if file and file.startswith(aux):
            sftp.get(f'/processed/{file}', f'C:/Users/arthuraiala/Desktop/Megasync/Projeto auto de e-mail/sftp/poggers/{file}')
    sftp.close()
    transport.close()
    print ("sftp sucess")       
    tentativas = 0 
    while tentativas < 5:
        try:
            mover()
            tentativas += 1
        except OSError as error:
            time.sleep(10)
            print('Tentando mover novamente')
            mover()

def mover():
  root_src_dir = ''
  root_dst_dir = ''

  for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
      os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
          # in case of the src and dst are the same file
          if os.path.samefile(src_file, dst_file):
            continue
          os.remove(dst_file)
        shutil.move(src_file, dst_dir)

def job():
  #notifyInicio()
  main() 
  
# schedule.every().day.at("08:30:00").do(job)

main()

