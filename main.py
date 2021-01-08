from flask import Flask,render_template,request
import os
import re
import sqlite3
import csv
import subprocess


app = Flask(__name__)


@app.route('/downim')   
def downim():
        
    return render_template('downim.html',header='Doron Fiala - download image from docker hub', sub_header='download image', list_header="download image",
                       site_title="doron.docker")
@app.route('/downimd')
def downimd():
 imgname=request.args.get('imgname')
 cmd=['sudo', 'docker', 'pull', "{}".format(imgname)]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 data=[]
 for line in proc.stdout:
  data.append(line.decode('utf-8').split())
 print(data)
 return render_template('results.html',header=data, sub_header='Main Menu:',site_title="doron.docker")

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
     cmd='sudo docker run -d --rm -ti -p {}:{} --name {} {} {}'.format(hport,cport,contname,imgname,command)
    else:  
     cmd='sudo docker run -d --rm -ti --name {} {} {}'.format(contname,imgname,command)
    print(cmd)
    os.system('echo "$({})"'.format(cmd))
    return render_template('lstco.html',header='Doron Fiala - Docker Menu', sub_header='List Containers', list_header="containers:",
                       containers=get_containers(), site_title="doron.docker")

@app.route('/push')   
def push():
    return render_template('push.html',header='Doron Fiala - Docker Menu', sub_header='push Images', list_header="Images:",
                       images=get_images(), site_title="doron.docker")   
       
                       
@app.route('/pushd',methods=['POST'])   
def pushd():
    imgname=request.form.get('imgname')
    tagname=request.form.get('tagname')
    user=request.form.get('user')
    repo=request.form.get('repo')
    cmd='sudo docker tag {} {}/{}:{}'.format(imgname,user,repo,tagname)
    os.system('echo "$({})"'.format(cmd))
    cmd='sudo docker push {}/{}:{} 2>temp1.txt >>temp1.txt'.format(user,repo,tagname)
    os.system('echo "$({})"'.format(cmd))
    cmd='cat temp1.txt | (grep "Layer already exists\|Error\|The push refers to\|digest\|does not exist\|requested access to the resource is denied" > temp.txt)'
    os.system('echo "$({})"'.format(cmd))
    with open('temp.txt', newline='') as f:
      data = f.readlines()
    return render_template('results.html',header=data, sub_header='push image', list_header="push image", site_title="doron.docker")



@app.route('/login')
def login():
        
    return render_template('login.html',header='Doron Fiala - login docker hub', sub_header='Delete Container', list_header="containers:",
                       site_title="doron.docker")

@app.route('/logind',methods=['POST'])
def logind():
    user=request.form.get('user')
    passw=request.form.get('pass')
    if passw != "" and user != "":
     cmd="sudo docker login -u {} -p {} 2>temp1.txt >>temp1.txt".format(user,passw)
     os.system('echo "$({})"'.format(cmd))
     cmd='cat temp1.txt | (grep -o "Login Succeeded\|Error response" > temp.txt)'
     os.system('echo "$({})"'.format(cmd))
    else:
     cmd='echo "error: user or password empty" > temp.txt)'
     os.system('echo "$({})"'.format(cmd))
    with open('temp.txt', newline='') as f:
      data = f.readlines()
    return render_template('results.html',header=data, sub_header='Main Menu:',
                        site_title="doron.docker")
                       
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
    return render_template('index.html',header='Doron Fiala Docker App', sub_header='Main Menu:', site_title="doron.docker")
   
def lstcont (cmd):
  os.system('echo "$({})">list.txt'.format(cmd))
  os.system('''awk '{print $1"," $2","$3","$4","$5","$6","$7","$8","$9","$10}' list.txt>temp.txt''')
  with open('temp.txt', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)
  #conn = sqlite3.connect('containers.db')
  #conn.execute('''drop TABLE if exists containers''')
  #conn.execute('''CREATE TABLE containers (id text, image text,contname text)''')
  containers=[]
  for x in data:
   containers.append([x[0],x[1],x[2],x[9]])
  #conn.commit()
  return containers 
def lstimg (cmd):
  os.system('echo "$({})">list.txt'.format(cmd))
  os.system('''awk '{print $1"," $2","$3","$4","$5","$6","$7","$8","$9,"$10,"$11}' list.txt>temp.txt''')
  with open('temp.txt', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)
  #conn = sqlite3.connect('containers.db')
  #conn.execute('''drop TABLE if exists images''')
  #conn.execute('''CREATE TABLE images (id text, image text)''')
  images=[]
  for x in data:
   #conn.execute('''INSERT INTO images VALUES ('{}','{}')'''.format(x[0],x[1]))
   images.append([x[0],x[1],x[2],x[3],x[4],x[5]])
  #conn.commit()
  return images 
  
def get_containers():
 containers=[]
 cmd=["docker","ps"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  containers.append(line.decode('utf-8').split())
 containers.pop(0)
 print(containers)
 return containers
 
 

def get_images():
 images=[]
 cmd=["docker","images"]
 proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
 for line in proc.stdout:
  images.append(line.decode('utf-8').split())
 images.pop(0)
 print(images)
 return(images) 
 

 
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000)    