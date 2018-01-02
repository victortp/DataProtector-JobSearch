# *-* coding: utf-8 *-*

import os
from config import DataListDir
import re
import codecs 

def FindHostInJob(HostName):
    HOST_LIST = []
    for _, _, filelist in os.walk(DataListDir):
        for FileName in filelist:
            PATHDIR=DataListDir+'/'+FileName
            try:
                with codecs.open(PATHDIR, 'r', encoding='utf-16') as file:
                    if str(HostName) in file.read():
                        HOST_LIST.append(FileName)
            except:
                with codecs.open(PATHDIR, 'r', encoding='iso-8859-1') as file:
                    if str(HostName) in file.read():
                        HOST_LIST.append(FileName)

    return HOST_LIST

def ChangePool(JOBNAME, NEWPOOL, POOL):
    PATHFILE = DataListDir+'/'+JOBNAME

    with codecs.open(PATHFILE, 'r', encoding='iso-8859-1') as file:
        FILEDATA = file.read()

    FILEDATA = FILEDATA.replace(POOL, NEWPOOL)
    file.close()

    with open(PATHFILE, 'w') as file:
        file.write(FILEDATA)

    file.close()
    return True

def CountLineOfFile(FileName):
    LINESUM = 0
    try:
        with codecs.open(FileName, 'r', encoding='utf-16') as f:
            LINESUM = sum(1 for _ in f)
    except:
        with codecs.open(FileName, 'r', encoding='iso-8859-1') as f:
            LINESUM = sum(1 for _ in f)

    return LINESUM

def CountFileInDir(DirLocation):
    if os.path.isdir(DirLocation):
        return len(os.listdir(DirLocation))
    else:
        return 0

