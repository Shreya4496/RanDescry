from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file1 = drive.CreateFile()
file1.SetContentFile('abc.txt')
file1.Upload() # Files.insert()

####main.py content





time.sleep(10)
file3 = drive.CreateFile({'id': file1['id']})
print('Downloading file %s from Google Drive' % file3['title'])
file3.GetContentFile('abc.txt')  # Save Drive file as a local file'''























'''
file1['title'] = 'HelloWorld.txt'  # Change title of the file
file1.Upload() # Files.patch()

content = file1.GetContentString()  # 'Hello'
file1.SetContentString(content+' World!')  # 'Hello World!'
file1.Upload() # Files.update()
'''




'''file2 = drive.CreateFile()
file2.SetContentFile('hello.png')
file2.Upload()
print('Created file %s with mimeType %s' % (file2['title'],
file2['mimeType']))
# Created file hello.png with mimeType image/png

file3 = drive.CreateFile({'id': file2['id']})
print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
file3.GetContentFile('world.png')  # Save Drive file as a local file'''

# or download Google Docs files in an export format provided.
# downloading a docs document as an html file:
#docsfile.GetContentFile('test.html', mimetype='text/html')
