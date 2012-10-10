#!/usr/bin/python
import time
import MySQLdb
import os
import smtplib

user='root'
passwd='dinga'
host='localhost'

try:
        filestamp = time.strftime('%Y-%m-%d')
        conn = MySQLdb.connect (host, user, passwd)

        cursor = conn.cursor()

        cursor.execute("SHOW DATABASES")

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        for result in results:
                backupfile=result[0]+".sql.gz"
                cmd="echo 'Back up "+result[0]+" database to yourLocation/"+backupfile+"'"
                os.system(cmd)
                cmd="mysqldump -u "+user+" -h "+host+" -p"+passwd+" --opt --routines --flush-privileges --single-transaction --database "+result[0]+" | gzip -9 --rsyncable > /home/bitnami/database_back/"+backupfile+filestamp
                os.system(cmd)

except:

        try:
                sender = 'database_backupmanager@yourdomain.com'
                receivers = ['blah@yourdomain.com']
                message = """From: From Database Manager <database_backupmanager@yourdomain.com>
                To: To Person <anto@yourdomain.com>
                MIME-Version: 1.0
                Content-type: text/html
                Subject:Database Backup Manager

                Scheduled DB backup failed !!!.
                """
                smtpObj = smtplib.SMTP('localhost')
                smtpObj.sendmail(sender, receivers, message)
                print "Successfully sent email"



        except IOError as e:
                print ("Error: unable to send email({}))".format(e))
