################
#   by Menghan Ho
#       2017/04/10
#

import os,fnmatch,sys,datetime,glob
from operator import itemgetter
from itertools import *
import tkFileDialog
import Tkinter as tk

# No Error Handle, Users have to make sure all images exists
# works for redshift only
# Can't find . in file name prefix, the format should be in redshift naming format
#   NamePrefix_denoise#.aovPassName.####.ext

def genCmd(listbox,root,tar,aov,sFrame,eFrame,ext,padN):
    altusCmd = os.path.abspath('C:\\Program Files\\Altus Denoiser\\bin\\altus-cli.exe')

    if  not os.path.isfile(altusCmd):
        print 'can not find altus-cli command.\n'
        exit
        
    tarAov = []
    for k in listbox.curselection():
        tarAov.append(aov[int(k)])

    #print aov
    c = 0
    
    if not tarAov:
        print 'no aov selected.'
        exit
    if len(tarAov) > 1:
        batFileName = 'misc'
    else:
        batFileName = tarAov[0].replace("_denoise0","")
    fileToWrite = '%s/%s_denoise.bat'%(tar,batFileName)
    numPad=0
    
    while True:
        if not os.path.isfile(fileToWrite):
            break
        numPad = numPad + 1    
        fileToWrite ='%s/%s_denoise%d.bat'%(tar,batFileName,numPad)
            
        
    f=open(fileToWrite,'w+')
    for key in tarAov:
        c = c+1
        #rgb
        outName = key.replace("_denoise0","_denoise")
        rgbFile0 = key
        rgbFile1 = key.replace("_denoise0","_denoise1")
        
        if len(key.split('.'))>1:
            posFile0 = '.'.join(key.split('.')[0:-1])+'.P'
        else:
            posFile0 = '.'.join(key.split('.')[0:])+'.P'
        posFile1 = posFile0.replace("_denoise0","_denoise1")
        
       

        batCmd = 'REM #%d Denoise %s\n'%(c, key.replace('_denoise0',''))
        batCmd = batCmd + 'set sFrame=%s\n'%sFrame
        batCmd = batCmd + 'set eFrame=%s\n'%eFrame        
        batCmd = batCmd +  '"%s" '%altusCmd
        batCmd = batCmd + '--out-path %s/%s.%s.%s '%(tar,outName,padN,ext)
        batCmd = batCmd + '--rgb-0 %s/%s.%s.%s '%(root,rgbFile0,padN,ext)
        batCmd = batCmd + '--rgb-1 %s/%s.%s.%s '%(root,rgbFile1,padN,ext)
        batCmd = batCmd + '--pos-0 %s/%s.%s.%s '%(root,posFile0,padN,ext)
        batCmd = batCmd + '--pos-1 %s/%s.%s.%s '%(root,posFile1,padN,ext)
        batCmd = batCmd + '--start-frame %sFrame% --end-frame %eFrame% '
        batCmd = batCmd + '--kc_1 0.45 --kc_2 0.45 --kc_4 0.45 --kf 0.6 --radius 10 --renderer redshift --frame-radius 1 --quality production '
        batCmd = batCmd + '--gpu ' #comment out this line if use openCL
        batCmd = batCmd + '\n\n'
        
        f.write(batCmd)
    f.write('PAUSE')
    f.close()
    print 'Writing bat to %s'%fileToWrite

    
def main():    
   
        
    defaultPath=os.path.abspath(__file__)
    options={}
    options['initialdir'] = defaultPath
    options['title'] = "source folder location"
    root=tkFileDialog.askdirectory(**options)
    
    
    
    #print 'source folder %s.\n'%root
    options['initialdir']=root
    options['title'] = "target folder location"
    tar=tkFileDialog.askdirectory(**options)
    #print 'target folder %s.\n'%tar
    
    sourceFiles = sorted(glob.glob('%s/*_denoise0.*'%root))
    grp=groupby(sourceFiles, lambda x: '.'.join(os.path.basename(x).split('.')[0:-2]))

    tkRoot = tk.Tk()
    tkRoot.title('redshift denoise')
    label = tk.Label(tkRoot,text = 'Select AOVs to denoise.')
    listbox = tk.Listbox(tkRoot,selectmode=tk.EXTENDED)
    aov=[]
    for key,group in groupby(sourceFiles, lambda x: '.'.join(os.path.basename(x).split('.')[0:-2])):
        aov.append(key)
        k=key.split('.')
        if len(k)<2:
            k='Beauty'
        else:
            k=k[-1]
        listbox.insert(tk.END,k)
        
        fileSort = sorted([n for n in group])
        sFrame = int(fileSort[0].split('.')[-2])
        eFrame = int(fileSort[-1].split('.')[-2])        
        ext = fileSort[-1].split('.')[-1]
        padN = ''
        for i in range(len(fileSort[0].split('.')[-2])):
            padN = padN + '#'
        

    btn1 = tk.Button(tkRoot,text='Create',command=lambda : genCmd(listbox,root,tar,aov,sFrame,eFrame,ext,padN))
    label.pack()
    listbox.pack(fill=tk.BOTH, expand=1)
    btn1.pack()
    tkRoot.mainloop()
 
main()
