# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-03-21 17:20:26
# @Last Modified by:   riposa
# @Last Modified time: 2016-03-21 18:10:56

import os
import multiprocessing
import time
import random

ROOT = 'Y:\\VionData\\RecordData\\viondata0\\kk'
TEST_ROOT = 'E:\\VionData\\192.168.1.1'
OUTPUT = 'D:\\OUTPUT'
DEBUG = False

def worker(wRoot):
    
    wOutPut = OUTPUT + '\\' + wRoot.split('\\')[-1]
    #print 'proc %d start'%k
    for root, dirs, files in os.walk(wRoot):
        for f in files:
            if f.split('.')[-1] == 'ini':
                with open(root + '\\' + f, 'r') as file:
                    if '黄底' in file.read().decode('GBK').encode('utf-8'):
                        #print 'cwdir',os.getcwd()
                        if random.randint(1,50) == 2:
                            os.system('copy "%s" "%s"'%(root + '\\' + f.split('.ini')[0] + '.jpg', wOutPut + '\\'))
                            #print root
                            #print '-------------------------- ******* ---------------------------','\n\n'
                            print 'copy %s %s'%(root + '\\' + f.split('.ini')[0] + '.jpg', wOutPut + '\\')
                            #print '\n\n','-------------------------- ******* ---------------------------'

def init():
    dirIn = list()
    for i in os.listdir(ROOT):
        if os.path.isdir(ROOT + '\\' + i):
            dirIn.append(ROOT + '\\' + i)
    pool = multiprocessing.Pool(processes = 8)    
    for i in dirIn:
        os.chdir(OUTPUT)
        os.mkdir('%s'%(i.split('\\')[-1]))
        os.chdir('d:\\')
        pool.apply_async(worker, (i,))        

    pool.close()
    pool.join()

def test():
    worker(TEST_ROOT)

if __name__ == '__main__':
    if DEBUG:
        test()
    else:
        init()
