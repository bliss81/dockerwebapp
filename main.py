#importing flask for web capabilities
from flask import Flask,render_template,request
#importing os and subprocess for running shell commands and getting output
import os
#importing sqlite for usuing database
import sqlite3
import subprocess

#flask application definition.
app = Flask(__name__)
global login
login="no" 

#flask site route for image download form
@app.route('/downim')   
def downim():
        
    return render_template('downim.html',header='Doron Fiala - download image from docker hub', sub_header='download image', list_header="download image",
                       site_title="doron.docker")
#flask route to catch the download image form and download the image
@app.route('/downimd')
def downimd():
 imgname=request.args.get('imgname')
#get the "get" data  from the form
 cmd=['sudo', 'docker', 'pull', "{}".format(imgname)]
 data=[]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 #use of subprocess mosule to run docker as subproces of python and catch output
 for line in proc.stdout:
  data.append(line.decode('utf-8').split())
#decode output from bytes to string and insert to list
 newdata=[]
 for lst in data:
  for i in lst:
   newdata.append(i)
 strings=''
 strings=' '.join(newdata)
 print(newdata)
 print("edededdededed",strings)
#return the output as list and send it to html template
 return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

#flask site route for create conttainer form
@app.route('/cr8con')   
def cr8con():
       
    return render_template('cr8con.html',header='Doron Fiala - Create New Container', sub_header='download image', list_header="download image",
                       images=get_images(),site_title="doron.docker")
        
 #flask site route to catch the data from create container form
@app.route('/cr8cond',methods=['POST'])   
def cr8cond():
    #get the "post" data  from the form
    imgname=request.form.get('imgname')
    contname=request.form.get('contname')
    command=request.form.get('command')
    cport=request.form.get('cport')
    hport=request.form.get('hport')
    if cport != "" and hport !="": 
     if command !="": 
      cmd=['sudo', 'docker', 'run','-d','--rm','-ti','-p','{}:{}'.format(hport,cport),'--name','{}'.format(contname),'{}'.format(imgname),'{}'.format(command)]
     else:
      cmd=['sudo', 'docker', 'run','-d','--rm','-ti','-p','{}:{}'.format(hport,cport),'--name','{}'.format(contname),'{}'.format(imgname)]
#use of subprocess mosule to run docker as subproces of python and catch output
     proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
     data=[]
     for line in proc.stdout:
      data.append(line.decode('utf-8').split())
     newdata=[]
     for lst in data:
      for i in lst:
       newdata.append(i)
     strings=''
     strings=' '.join(newdata)
    else:  
     if command !="": 
      cmd=['sudo', 'docker', 'run','-d','--rm','-ti','--name','{}'.format(contname),'{}'.format(imgname), '{}'.format(command)]
     else:
      cmd=['sudo', 'docker', 'run','-d','--rm','-ti','--name','{}'.format(contname),'{}'.format(imgname)]
#use of subprocess mosule to run docker as subproces of python and catch output
     proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
     data=[]
     for line in proc.stdout:
      data.append(line.decode('utf-8').split())
     newdata=[]
     for lst in data:
      for i in lst:
       newdata.append(i)
     strings=''
     strings=' '.join(newdata)    
#return the output as list and send it to html template
    return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

#flask site route for image push form
@app.route('/push')   
def push():
        #use sqlite database to store the dockerhub credentials and login status
   conn = sqlite3.connect('data.db')
   c = conn.cursor()
   c.execute('SELECT * FROM login')
   logdet=[]
   print("login check")
   print(logdet)
   logdet=c.fetchone()
   conn.close()
   print(logdet[0])
   if logdet[0]=="yes":
    username=logdet[1]
    print("logged in")
    return render_template('push.html',header='Doron Fiala - Docker Menu', sub_header='push Images', list_header="Images:",
                       images=get_images(),username=username,site_title="doron.docker")
   else:   
    print("not logged in")
#return the output as list and send it to html template
    return render_template('login.html',header='Doron Fiala - Docker Menu', sub_header='push Images', list_header="Images:",
                       images=get_images(), site_title="doron.docker")   
 #flask site route for getting iform information from image push form
@app.route('/pushd',methods=['POST'])   
def pushd():
    imgname=request.form.get('imgname')
    tagname=request.form.get('tagname')
    user=request.form.get('user')
    repo=request.form.get('repo')
    cmd=['sudo', 'docker', 'tag','{}'.format(imgname),'{}/{}:{}'.format(user,repo,tagname)]
#use of subprocess mosule to run docker as subproces of python and catch output
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    data=[]
    for line in proc.stdout:
     data.append(line.decode('utf-8').split())
    cmd=['sudo', 'docker', 'push','{}/{}:{}'.format(user,repo,tagname)]
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for line in proc.stdout:
     data.append(line.decode('utf-8').split())
    newdata=[]
    for lst in data:
     for i in lst:
      newdata.append(i)
    strings=''
    strings=' '.join(newdata)
#return the output as list and send it to html template
    return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")


#flask site route for docker hub login form
@app.route('/login')
def login():
        #return the output as list and send it to html template
    return render_template('login.html',header='Doron Fiala - login docker hub', sub_header='Delete Container', list_header="containers:",
                       site_title="doron.docker")

#flask site route for getting information from login  form
@app.route('/logind',methods=['POST'])
def logind():
 user=request.form.get('user')
 passw=request.form.get('pass')
 if passw != "" and user != "":
        #use of subprocess mosule to run docker as subproces of python and catch output
  cmd=['sudo', 'docker', 'login','-u','{}'.format(user),'-p','{}'.format(passw)]
  proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  data=[]
  for line in proc.stdout:
   data.append(line.decode('utf-8').split())
  newdata=[]
  for lst in data:
   for i in lst:
    newdata.append(i)
  strings=''
  strings=' '.join(newdata)
        #use sqlite database to store/recall the dockerhub credentials and login status
  if "Login Succeeded" in strings:
   conn = sqlite3.connect('data.db')
   c = conn.cursor()
   c.execute('''Drop table if exists login''')
   c.execute('''CREATE TABLE if not EXISTS login(status text, user text)''')
   c.execute("INSERT INTO login VALUES ('yes','{}')".format(user))
   conn.commit()
   conn.close()
   print("logged in")
  else:
   conn = sqlite3.connect('data.db')
   c = conn.cursor()
   c.execute('''Drop table if exists login''')
   c.execute('''CREATE TABLE login(status text, user text)''')
   c.execute("INSERT INTO login VALUES ('no',{})".format(user))
   conn.commit()
   conn.close()
   print("not logged in")
 else:
  strings="error: user or password empty"
#return the output as list and send it to html template
 return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

#flask site route for logout form
@app.route('/logout')
def logout():
  cmd=['sudo', 'docker', 'logout']
#use of subprocess mosule to run docker as subproces of python and catch output
  proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  data=[]
  for line in proc.stdout:
   data.append(line.decode('utf-8').split())
  newdata=[]
  for lst in data:
   for i in lst:
    newdata.append(i)
  strings=''
  strings=' '.join(newdata)
        #use sqlite database to store / recall the dockerhub credentials and login status
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('''Drop table if exists login''')
  c.execute('''CREATE TABLE if not EXISTS login(status text, user text)''')
  c.execute("INSERT INTO login VALUES ('no','none')")
  conn.commit()
  conn.close()
  print("logged out")
#return the output as list and send it to html template
  return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")
                       
        #flask site route for image list form
@app.route('/lstim')
def lstim():
        #call funtion and send  the output to html template
    return render_template('lstim.html',header='Doron Fiala - Docker Menu', sub_header='list Images', list_header="Images:",
                       images=get_images(), site_title="doron.docker")
#flask site route for container list form
@app.route('/lstco')
def lstco():
    return render_template('lstco.html',header='Doron Fiala - Docker Menu', sub_header='list containers', list_header="Images:",
                       containers=get_containers(), site_title="doron.docker")

#flask site route for image deletion form
@app.route('/delim',methods=['GET', 'POST'])
def delim():
    imgname=request.args.get('img')
    cmd="sudo docker image rm -f {}".format(imgname)
        #use of os mosule to run docker as shell process not catching output
    os.system('echo "$({})"'.format(cmd))
    return render_template('delim.html',header='Doron Fiala - Docker Menu', sub_header='Delete Image', list_header="Images:",
                       images=get_images(), site_title="doron.docker")
#flask site route for getting information from image deletion form
@app.route('/delimd',methods=['POST'])   
def delimd():
    imgname=request.form.get('imgname')
    cmd='sudo docker rmi -f {}'.format(imgname)
    print(cmd)
    os.system('echo "$({})"'.format(cmd))
    return render_template('delim.html',header='Doron Fiala - Docker Menu', sub_header='List images', list_header="images:",
                       images=get_images(), site_title="doron.docker")
#flask site route for container deletion form
@app.route('/delcon')
def delcon():
    return render_template('delcon.html',header='Doron Fiala - Docker Menu', sub_header='Delete Container', list_header="containers:",
                       containers=get_containers(), site_title="doron.docker")
#flask site route for getting uinformation from container deletion form
@app.route('/delcond',methods=['POST'])   
def delcond():
    cont=request.form.get('cont')
    cmd='sudo docker rm -f {}'.format(cont)
    print(cmd)
    os.system('echo "$({})"'.format(cmd))
    return render_template('delcon.html',header='Doron Fiala - Docker Menu', sub_header='Delete Container', list_header="Containers:",
                       containers=get_containers(), site_title="doron.docker")

#flask site route for main menu 
@app.route('/')
def index():
                #use sqlite database to store / recall the dockerhub credentials and login status
 conn = sqlite3.connect('data.db')
 c = conn.cursor()
 c.execute('''CREATE TABLE if not EXISTS login(status text, user text)''')
 c.execute("INSERT INTO login VALUES ('no','none')")
 conn.commit()
 conn.close()
 return render_template('index.html',header='Doron Fiala Docker App', sub_header='Main Menu:', site_title="doron.docker")

#function to get container list from docker   
def get_containers():
 containers=[]
 cmd=["docker","ps"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  containers.append(line.decode('utf-8').split())
 containers.pop(0)
 print(containers)
 return containers
 
 
#function to get image list from docker
def get_images():
 images=[]
 cmd=["docker","images"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  images.append(line.decode('utf-8').split())
 images.pop(0)
 print(images)
 return(images) 
 
 
#starting the flask app 
if __name__ == '__main__':
 app.run()    
 
  
