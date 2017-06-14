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
            basename = '.'.join(key.split('.')[0:-1])
        else:
            basename = '.'.join(key.split('.')[0:])

        posFile0 = basename+'.P'
        nrmFile0 = basename+'.BumpNormals'
        visFile0 = basename+'.Shadows'
        albFile0 = basename+'.DiffuseFilter'
        cauFile0 = basename+'.Caustics'

        posFile1 = posFile0.replace("_denoise0","_denoise1")
        nrmFile1 = nrmFile0.replace("_denoise0","_denoise1")
        visFile1 = visFile0.replace("_denoise0","_denoise1")
        albFile1 = albFile0.replace("_denoise0","_denoise1")
        cauFile1 = cauFile0.replace("_denoise0","_denoise1")

        posExist = True
        nrmExist = True
        visExist = True
        albExist = True
        cauExist = True

        #file exist check
        padInt = len(padN)
        for i in range(sFrame, eFrame+1):
            frameName = '%s.%s'%(str(i).zfill(padInt),ext)     
            
            if posExist:
                if not os.path.isfile('%s/%s.%s'%(root, posFile0,frameName)):
                    print 'File not exist: %s.%s'%(posFile0,frameName)
                    print 'Failed :: Position Pass is required.'
                    posExist = False
                    exit
                else:
                    if not os.path.isfile('%s/%s.%s'%(root, posFile1,frameName)): 
                        print 'File not exist: %s.%s'%(posFile1,frameName)
                        print 'Failed :: Position Pass is required.'
                        posExist = False
                        exit
            
            if nrmExist:
                if not os.path.isfile('%s/%s.%s'%(root, nrmFile0,frameName)):
                    print 'File not exist: %s.%s'% (nrmFile0,frameName)
                    print 'missing nrm pass, skip nrm.'
                    nrmExist = False
                else:
                    if not os.path.isfile('%s/%s.%s'%(root, nrmFile1,frameName)):
                        print 'File not exist: %s.%s'%(nrmFile1,frameName)
                        print 'missing nrm pass, skip nrm.'
                        nrmExist = False
            
            if visExist:
                if not os.path.isfile('%s/%s.%s'%(root, visFile0,frameName)):
                    print 'File not exist: %s.%s'%(visFile0,frameName)
                    print 'missing Shadows pass, skip nrm.'
                    visExist = False
                else:
                    if not os.path.isfile('%s/%s.%s'%(root, visFile1,frameName)):
                        print 'File not exist: %s.%s'%(visFile1,frameName)
                        print 'missing Shadows pass, skip nrm.'
                        visExist = False
            
            if albExist:
                if not os.path.isfile('%s/%s.%s'%(root, albFile0,frameName)):
                    print 'File not exist: %s.%s'%(albFile0,frameName)
                    print 'missing DiffuseFilter pass, skip nrm.'
                    albExist = False
                else:
                    if not os.path.isfile('%s/%s.%s'%(root, albFile1,frameName)):
                        print 'File not exist: %s.%s'%(albFile1,frameName)
                        print 'missing DiffuseFilter pass, skip nrm.'
                        albExist = False
            
            if cauExist:
                if not os.path.isfile('%s/%s.%s'%(root, cauFile0,frameName)):
                    print 'File not exist: %s.%s'%(cauFile0,frameName)
                    print 'missing Caustics pass, skip nrm.'
                    cauExist = False
                else:
                    if not os.path.isfile('%s/%s.%s'%(root, cauFile1,frameName)):
                        print 'File not exist: %s.%s'%(cauFile1,frameName)
                        print 'missing Caustics pass, skip nrm.'
                        cauExist = False


        batCmd = 'REM #%d Denoise %s\n'%(c, key.replace('_denoise0',''))
        batCmd = batCmd + 'set sFrame=%s\n'%sFrame
        batCmd = batCmd + 'set eFrame=%s\n'%eFrame        
        batCmd = batCmd +  '"%s" '%altusCmd
        batCmd = batCmd + '--out-path %s/%s.%s.%s '%(tar,outName,padN,ext)
        batCmd = batCmd + '--rgb-0 %s/%s.%s.%s '%(root,rgbFile0,padN,ext)
        batCmd = batCmd + '--rgb-1 %s/%s.%s.%s '%(root,rgbFile1,padN,ext)
        batCmd = batCmd + '--pos-0 %s/%s.%s.%s '%(root,posFile0,padN,ext)
        batCmd = batCmd + '--pos-1 %s/%s.%s.%s '%(root,posFile1,padN,ext)

        if albExist:
            batCmd = batCmd + '--alb-0 %s/%s.%s.%s '%(root,albFile0,padN,ext)
            batCmd = batCmd + '--alb-1 %s/%s.%s.%s '%(root,albFile1,padN,ext)
        if nrmExist:
            batCmd = batCmd + '--nrm-0 %s/%s.%s.%s '%(root,nrmFile0,padN,ext)
            batCmd = batCmd + '--nrm-1 %s/%s.%s.%s '%(root,nrmFile1,padN,ext)
        if visExist:
            batCmd = batCmd + '--vis-0 %s/%s.%s.%s '%(root,visFile0,padN,ext)
            batCmd = batCmd + '--vis-1 %s/%s.%s.%s '%(root,visFile1,padN,ext)
        if cauExist:
            batCmd = batCmd + '--cau-0 %s/%s.%s.%s '%(root,cauFile0,padN,ext)
            batCmd = batCmd + '--cau-1 %s/%s.%s.%s '%(root,cauFile1,padN,ext)

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
    options['title'] = "Source folder location"
    root=tkFileDialog.askdirectory(**options)
    
    
    
    #print 'source folder %s.\n'%root
    options['initialdir']=root
    options['title'] = "Target folder location"
    tar=tkFileDialog.askdirectory(**options)
    #print 'target folder %s.\n'%tar
    
    sourceFiles = sorted(glob.glob('%s/*_denoise0.*'%root))
    grp=groupby(sourceFiles, lambda x: '.'.join(os.path.basename(x).split('.')[0:-2]))

    tkRoot = tk.Tk()
    tkRoot.title('Redshift denoise')
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
