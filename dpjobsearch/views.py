# *-* coding: utf-8 *-*

<<<<<<< HEAD
import os
=======
>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b
from flask import Flask, render_template, request
from dpjobsearch import app
from config import cell_info, DataListDir, SchedulesDir
from funcoes import FindHostInJob, CountLineOfFile, CountFileInDir
import codecs
import re

from datetime import datetime
now = datetime.now()
    
@app.route('/', methods=['GET'])
def index():
    NUM_DATALIST = CountFileInDir(DataListDir)
    NUM_SCHEDULE = CountFileInDir(SchedulesDir)

    LISTA_DIARIA = []
    try:
        PARAM = request.args.get('backup')
    except:
        PARAM = ''

<<<<<<< HEAD
=======




>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b
    LISTA_HOSTS = []
    VAR = []
    try:
        PARAM = request.args.get('host')
    except:
        PARAM = ''

    file = codecs.open(cell_info, 'r', encoding='utf-16')
    ''' STRING SPLIT '''
    '''-host "mggenesaplp1.energisa.corp" -os "microsoft i386 wNT-6.0-S" -da A.09.00 -ma A.09.00 -ts_core A.09.00'''
    for line in file.readlines():
        HOST = line.split('"')[1]
        OS = line.split('"')[3]
        VERSION = line.split()[7]
        linha = str(HOST+':'+OS)
        LISTA_HOSTS.append(linha)
        VAR.append(HOST)
        
    file.close()

    JOBS = []
<<<<<<< HEAD
    for _, _, filelist in os.walk(SchedulesDir):
        for FileName in filelist:
            PATHDIR=SchedulesDir+'/'+FileName

            fileSC = codecs.open(PATHDIR, 'r', encoding='utf-16')
=======
    for host in VAR:
        ''' pega os jobs do host '''
        jobs = FindHostInJob(host)
        
        ''' verifica se tem que fazer o job hoje '''
        AUX = []
        for job in jobs:
            SchedulesFile = SchedulesDir+'/'+job
            fileSC = codecs.open(SchedulesFile, 'r', encoding='utf-16')
>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b
            a = False
            b = False
            c = False
            dia = None
            hora = None
            exclude = None
            
            for linesc in fileSC.readlines():
                ''' Verifica quando vai ser executado '''
                if '-every' in linesc:
                    a = True
                    continue

                if a == True:
                    dia = linesc.replace("\t", "").replace("\n", "").replace("\r", "").replace("-day ", "")[:-1]
        
                    a = False
                    b = True
                    continue
                    
                if b:
                    hora = linesc.replace("\t", "").replace("\n", "").replace("\r", "").replace("-at ", "")
                    b = False
                    
                ''' Verifica quando não vai ser executado '''
                if '-exclude' in linesc:
                    c = True
                    continue

                if c:
                    exclude = linesc.replace("\t", "").replace("\n", "").replace("\r", "").replace("-day ", "").replace(" ", "")
                    if exclude.isdigit() and int(exclude) < 10:
                        exclude = '0' + exclude
                    c = False

<<<<<<< HEAD
            if hora is not None:
                h = hora.split(':')
                horaDT = datetime.now()
                horaDT = horaDT.replace(hour=int(h[0]), minute=int(h[1]), second=0, microsecond=0)
            else:
                horaDT = None
            job = {"name": FileName, "dia": dia, "hora": hora, "exclude": exclude, "horaDT": horaDT}

            #Verificação dos jobs diários
            if job['dia'] == "":
                if job['exclude'] is not None:
                    if job['exclude'] != now.strftime('%a') and job['exclude'] != now.strftime('%d'):
                        JOBS.append(job)
                else:
                    JOBS.append(job)

            # Verificação dos jobs semanais 
            if now.strftime('%a') in str(job['dia']):
                if job['exclude'] is not None:
                   if job['exclude'] != now.strftime('%d'):
                       JOBS.append(job)
                else:
                    JOBS.append(job)

            # Verificação dos jobs mensais
=======
            ''' Popula o array com as informações do job '''        
            AUX.append({"name": job, "dia": dia, "hora": hora, "exclude": exclude})
        JOBS.append({"host": host, "jobs": AUX})

    A = []

    for host in JOBS:
        AUX = []
        for job in host['jobs']:
            ''' Verificação dos jobs diários '''
            if job['dia'] == "":
                if job['exclude'] is not None:
                    if job['exclude'] != now.strftime('%a') and job['exclude'] != now.strftime('%d'):
                        AUX.append(job)
                else:
                    AUX.append(job)

            ''' Verificação dos jobs semanais '''
            if now.strftime('%a') in str(job['dia']):
                if job['exclude'] is not None:
                   if job['exclude'] != now.strftime('%d'):
                       AUX.append(job)
                else:
                    AUX.append(job)

            ''' Verificação dos jobs mensais '''
>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b
            if "-month" in str(job['dia']):
                d = job['dia'].replace(' -month', '')
                ''' formata o dia '''
                if d.isdigit() and int(d) < 10:
                    d = '0' + d

                if d == now.strftime('%d'):
<<<<<<< HEAD
                    JOBS.append(job)

    # Ordena os JOBS pela hora
    JOBS = sorted(JOBS, key=lambda dct: dct['horaDT'])      
=======
                    AUX.append(job)
                    
        A.append({'host': host, 'jobs': AUX})
>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b
    
    return render_template('dash.html', dados = [
    CountLineOfFile(cell_info),
    NUM_DATALIST,
    NUM_SCHEDULE,
    now.day,
    now.month,
    VAR,
<<<<<<< HEAD
    JOBS])
=======
    JOBS,
    A])
>>>>>>> 0b42581bd273462778ce3f45664f334bab609e2b


@app.route('/search', methods=['GET'])
def search():
    LISTA_HOSTS = []
    try:
        PARAM = request.args.get('host')
    except:
        PARAM = ''

    file = codecs.open(cell_info, 'r', encoding='utf-16')
    ''' STRING SPLIT '''
    '''-host "mggenesaplp1.energisa.corp" -os "microsoft i386 wNT-6.0-S" -da A.09.00 -ma A.09.00 -ts_core A.09.00'''
    for line in file.readlines():
        HOST = line.split('"')[1]
        OS = line.split('"')[3]
        VERSION = line.split()[7]
        linha = str(HOST+':'+OS)
        LISTA_HOSTS.append(linha)

    file.close()
    return render_template('search.html', hosts = [PARAM, LISTA_HOSTS])

@app.route('/job', methods=['GET'])
def jobsearch():
    JOBDATA = []
    JOBSC = []
    ''' DATALIST '''
    DATA = ''
    DEV = ''
    POOL = ''
    DIRETORIO = ''
    
    ''' SCHEDULE '''
    DAY = 0
    RETENTION = 0
    STATUS = True

    try:
        host = request.args.get('host')
    except:
        host = None
        return str('sem host')

    try:
        JOBNAME = request.args.get('detail')
        DataListFile = DataListDir+'/'+JOBNAME
        SchedulesFile = SchedulesDir+'/'+JOBNAME
    except:
        JOBNAME = ''
        DataListFile = None
        SchedulesFile = None

    if host is not None:
        ''' retorna nome de job que tem o host '''
        retorno = FindHostInJob(host)
    else:
        retorno = None

    if retorno is not None and DataListFile is not None and SchedulesFile is not None:
        fileDL = codecs.open(DataListFile, 'r', encoding='utf-16')
        fileSC = codecs.open(SchedulesFile, 'r', encoding='utf-16')

        for line in fileDL.readlines():
            if 'GROUP' in line:
                JOBDATA.append(line)
            if host in line:
                JOBDATA.append(line)
            if 'DEVICE' in line:
                DEV = DEV + ' ' + line.split('_')[1]
            if '-pool' in line:
                if POOL == '':
                    POOL=line.split('"')[1]
            if '"/' in line and \
                    'RECYCLE' not in line and \
                    'System Volume Information' not in line:
                DIRETORIO = DIRETORIO + ' ' + line

        JOBDATA.append(DEV)
        JOBDATA.append(POOL)
        JOBDATA.append(DIRETORIO)
        fileDL.close()

        for linesc in fileSC.readlines():
            if '-days' in linesc and DAY == 0 and RETENTION != 0:
                DAY = linesc.split(' ')[3]
            if '-disable' in linesc:
                STATUS = False
            if 'protection' in linesc and RETENTION == 0:
                RETENTION = linesc.split(' ')[3]

        JOBSC.append(STATUS)
        JOBSC.append(RETENTION)
        JOBSC.append(DAY)
        fileSC.close()

    return render_template('job.html', jobs = [retorno, host, JOBDATA, JOBSC])
