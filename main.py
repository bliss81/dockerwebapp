from flask import Flask,render_template,request
import sqlite3
import subprocess

app = Flask(__name__)
global login
login="no" 

@app.route('/downim')   
def downim():
        
    return render_template('downim.html',header='Doron Fiala - download image from docker hub', sub_header='download image', list_header="download image",
                       site_title="doron.docker")
@app.route('/downimd')
def downimd():
 imgname=request.args.get('imgname')
 cmd=['sudo', 'docker', 'pull', "{}".format(imgname)]
 data=[]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 
 for line in proc.stdout:
  data.append(line.decode('utf-8').split())
 newdata=[]
 for lst in data:
  for i in lst:
   newdata.append(i)
 strings=''
 strings=' '.join(newdata)
 print(newdata)
 print("edededdededed",strings)
 return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

@app.route('/cr8con')   
def cr8con():
       
    return render_template('cr8con.html',header='Doron Fiala - Create New Container', sub_header='download image', list_header="download image",
                       images=get_images(),site_title="doron.docker")
                       
@app.route('/cr8cond',methods=['POST'])   
def cr8cond():
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
    return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

@app.route('/push')   
def push():
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
    return render_template('login.html',header='Doron Fiala - Docker Menu', sub_header='push Images', list_header="Images:",
                       images=get_images(), site_title="doron.docker")   
                       
@app.route('/pushd',methods=['POST'])   
def pushd():
    imgname=request.form.get('imgname')
    tagname=request.form.get('tagname')
    user=request.form.get('user')
    repo=request.form.get('repo')
    cmd=['sudo', 'docker', 'tag','{}'.format(imgname),'{}/{}:{}'.format(user,repo,tagname)]
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
    return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")



@app.route('/login')
def login():
        
    return render_template('login.html',header='Doron Fiala - login docker hub', sub_header='Delete Container', list_header="containers:",
                       site_title="doron.docker")

@app.route('/logind',methods=['POST'])
def logind():
 user=request.form.get('user')
 passw=request.form.get('pass')
 if passw != "" and user != "":
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
 return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")

@app.route('/logout')
def logout():
  cmd=['sudo', 'docker', 'logout']
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
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('''Drop table if exists login''')
  c.execute('''CREATE TABLE if not EXISTS login(status text, user text)''')
  c.execute("INSERT INTO login VALUES ('no','none')")
  conn.commit()
  conn.close()
  print("logged out")
  return render_template('results.html',header=strings, sub_header='Main Menu:',site_title="doron.docker")
                       
@app.route('/lstim')
def lstim():
    return render_template('lstim.html',header='Doron Fiala - Docker Menu', sub_header='list Images', list_header="Images:",
                       images=get_images(), site_title="doron.docker")

@app.route('/lstco')
def lstco():
    return render_template('lstco.html',header='Doron Fiala - Docker Menu', sub_header='list containers', list_header="Images:",
                       containers=get_containers(), site_title="doron.docker")

@app.route('/delim',methods=['GET', 'POST'])
def delim():
    imgname=request.args.get('img')
    cmd="sudo docker image rm -f {}".format(imgname)
    os.system('echo "$({})"'.format(cmd))
    return render_template('delim.html',header='Doron Fiala - Docker Menu', sub_header='Delete Image', list_header="Images:",
                       images=get_images(), site_title="doron.docker")
@app.route('/delimd',methods=['POST'])   
def delimd():
    imgname=request.form.get('imgname')
    cmd='sudo docker rmi -f {}'.format(imgname)
    print(cmd)
    os.system('echo "$({})"'.format(cmd))
    return render_template('delim.html',header='Doron Fiala - Docker Menu', sub_header='List images', list_header="images:",
                       images=get_images(), site_title="doron.docker")

@app.route('/delcon')
def delcon():
    return render_template('delcon.html',header='Doron Fiala - Docker Menu', sub_header='Delete Container', list_header="containers:",
                       containers=get_containers(), site_title="doron.docker")
@app.route('/delcond',methods=['POST'])   
def delcond():
    cont=request.form.get('cont')
    cmd='sudo docker rm -f {}'.format(cont)
    print(cmd)
    os.system('echo "$({})"'.format(cmd))
    return render_template('delcon.html',header='Doron Fiala - Docker Menu', sub_header='Delete Container', list_header="Containers:",
                       containers=get_containers(), site_title="doron.docker")

@app.route('/')
def index():
 conn = sqlite3.connect('data.db')
 c = conn.cursor()
 c.execute('''CREATE TABLE if not EXISTS login(status text, user text)''')
 c.execute("INSERT INTO login VALUES ('no','none')")
 conn.commit()
 conn.close()
 return render_template('index.html',header='Doron Fiala Docker App', sub_header='Main Menu:', site_title="doron.docker")
   
def get_containers():
 containers=[]
 cmd=["docker","ps"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  containers.append(line.decode('utf-8').split())
 if containers:
  containers.pop(0)
  print(containers)
 return containers
 
 

def get_images():
 images=[]
 cmd=["docker","images"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  images.append(line.decode('utf-8').split())
 if images:
  images.pop(0)
  print(images)
 return(images) 
 
 
if __name__ == '__main__':
 app.run()    
 
  