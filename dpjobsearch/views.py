# *-* coding: utf-8 *-*

from flask import Flask, render_template, request
from dpjobsearch import app
from config import cell_info, DataListDir, SchedulesDir
from funcoes import FindHostInJob, CountLineOfFile, CountFileInDir
import codecs
import re

@app.route('/', methods=['GET'])
def index():
    NUM_DATALIST = CountFileInDir(DataListDir)
    NUM_SCHEDULE = CountFileInDir(SchedulesDir)
    return render_template('dash.html', dados = [
        CountLineOfFile(cell_info),
        NUM_DATALIST,
        NUM_SCHEDULE ])

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

