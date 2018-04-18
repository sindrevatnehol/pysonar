# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 09:26:07 2018

@author: sindrev
"""

import os
import numpy as np
from shutil import copyfile
import Raw2NetcdfConverter
import Raw2NetcdfConverter_old


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = ' '):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()
        

        
        
        
def WelcomeScreen(projectName): 
    print(projectName)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('    >=>      /\      >=>          >=>           ')
    print('  >=>       /  \           >=>         >=>      ')
    print('           / >=>\                               ')
    print('   >=>    /      \                 >=>          ')
    print('         /   >=>  \      >=>                >=> ')
    print('        / >=>      \              >=>    >=>    ')
    print('_______/________>=>_\___________________________')
    print('                              Sindre N. Vatnehol')
    print('                    Institute of Marine Research')
    print('                                          Norway')
    print('')

    
       
            
            
class FolderStructure(object):
    
    def __init__(self, dir_cruice,equipment):
        self.dir_cruice = dir_cruice+'/'
        self.dir_acoustic_data = dir_cruice+'/ACOUSTIC_DATA/'
        self.dir_su90 = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/'
        self.dir_PySonar = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar'
        self.dir_nc = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/netcdf'
        self.dir_work = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/WorkFiles'
        self.dir_search = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/Search'
        self.dir_result = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/Result'
        self.dir_rawdata = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/RAWDATA'
        self.dir_originalrawdata = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/ORIGINALRAWDATA'
        self.dir_src = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/src'
        self.dir_NCconvertProgress = dir_cruice+'/ACOUSTIC_DATA/'+equipment+'/PySonar/src/NCconvertProgress'
            
        
        
        
        
def MakeNewFolders(directory2Data):
    if not os.path.exists(directory2Data.dir_cruice):
        os.makedirs(directory2Data.dir_cruice)
    if not os.path.exists(directory2Data.dir_acoustic_data):
        os.makedirs(directory2Data.dir_acoustic_data)
    if not os.path.exists(directory2Data.dir_su90):
        os.makedirs(directory2Data.dir_su90)
    if not os.path.exists(directory2Data.dir_work):
        os.makedirs(directory2Data.dir_work)
    if not os.path.exists(directory2Data.dir_PySonar):
        os.makedirs(directory2Data.dir_PySonar)
    if not os.path.exists(directory2Data.dir_search):
        os.makedirs(directory2Data.dir_search)
    if not os.path.exists(directory2Data.dir_result):
        os.makedirs(directory2Data.dir_result)
    if not os.path.exists(directory2Data.dir_nc):
        os.makedirs(directory2Data.dir_nc)
    if not os.path.exists(directory2Data.dir_originalrawdata):
        os.makedirs(directory2Data.dir_originalrawdata)
    if not os.path.exists(directory2Data.dir_rawdata):
        os.makedirs(directory2Data.dir_rawdata)
    if not os.path.exists(directory2Data.dir_src):
        os.makedirs(directory2Data.dir_src)
    if not os.path.exists(directory2Data.dir_work):
        os.makedirs(directory2Data.dir_work)
    if not os.path.exists(directory2Data.dir_NCconvertProgress):
        os.makedirs(directory2Data.dir_NCconvertProgress)
        
               
        
        
        


def DataConverter(CruiceIndex,WorkDirectory,current_dir,maxPingInFile,
                  MaxNumberOfFilesInNC,directory2Data) :
    
    #Protocol to convert the data

    
    #Vessel and platform information
    vessel_name = CruiceIndex.getAttribute('vessel')
    platform_type = CruiceIndex.getAttribute('platform_type')
    platform_code = CruiceIndex.getAttribute('platform_code')
    
    
    
    
    #gLoop through each fishery sonar type
    for i in ['SU90','SX90','SH90']: 
        
        
        #Do the old nc convertion. 
        #When the search matrix function are addapted for the new nc format, this will be redundant. 
#        if not os.path.exists(directory2Data.dir_NCconvertProgress + '/finished.txt'):
#            Raw2NetcdfConverter_old.Raw2NetcdfConverter2(directory2Data.dir_originalrawdata,
#                                                     directory2Data.dir_nc,
#                                                     directory2Data.dir_NCconvertProgress)
#            
#            
#            #When convertion is finnished, make a txt file to indicate this
#            f = open(directory2Data.dir_NCconvertProgress + '/finished.txt','w')
#            f.write('0')
#            f.close()
#       
            
            
        #Convert the .raw data to nc. 
        if not os.path.exists(directory2Data.dir_NCconvertProgress + '/finishedNC.txt'):
            os.chdir(current_dir)
            Raw2NetcdfConverter.convert.Raw2NetcdfConverter(directory2Data.dir_originalrawdata,vessel_name,platform_type,
                        platform_code,maxPingInFile,MaxNumberOfFilesInNC,
                        directory2Data.dir_rawdata)
            
            
            #When convertion is finnished, make a txt file to indicate this
            f = open(directory2Data.dir_NCconvertProgress + '/finishedNC.txt','w')
            f.write('0')
            f.close()
        
       
            
            
        
def TransectTimeIDX(CruiceIndex): 
    TimeIDX =[]
    TransCode = CruiceIndex.getElementsByTagName("transect")
    for t in TransCode: 
        if TimeIDX == []: 
            TimeIDX = np.array([CruiceIndex.getAttribute("code")+'_'+t.getAttribute('num'),
                                t.getAttribute('startTime'),t.getAttribute('endTime')
                                ])[:,np.newaxis].T
        else: 
            TimeIDX  = np.vstack((TimeIDX,np.array([CruiceIndex.getAttribute("code")+'_'+t.getAttribute('num'),
                                t.getAttribute('startTime'),t.getAttribute('endTime')
                                ])[:,np.newaxis].T))      
    return TimeIDX
    
    
    
    
    
        
        
        
def OrginizeData(CruiceIndex,WorkDirectory,OS): 
    
    
    #Get the vessel, cruice and equipment information
    vesselCode = CruiceIndex.getAttribute("vesselCode")
    cruiceCode = CruiceIndex.getAttribute("code")
    equipment =  CruiceIndex.getAttribute("Equipment")
    
    
    #Loop through each fishery sonar type
    for i in ['SU90','SX90','SH90']: 
        
        
        if i == equipment: 
            
            
            #Make a correct sonar folder structure
            directory2Data =FolderStructure(WorkDirectory+'/'+cruiceCode[:4]+'/S'+cruiceCode+'_P'+vesselCode,i)        
            MakeNewFolders(directory2Data)
        
            
            #Get list of files that has not been copied to the correct structure
            print('    -Get files from server  ',end='\r')
            ListFromServer = os.listdir(OS+CruiceIndex.getAttribute('CruicePath'))
            ListOfFilesNotcopied = list(set(ListFromServer)-set(os.listdir(directory2Data.dir_originalrawdata)))
            
            
            #Go through each file
            for i in np.arange(len(ListOfFilesNotcopied)): 
                
                #Print a progressbar
                printProgressBar(i, len(ListOfFilesNotcopied), prefix = 'Copy files', suffix = 'Files left: '+
                                 str(len(ListOfFilesNotcopied)-i) , decimals = 1, length = 50)
                
                #Copy the files
                try:  
                    try:
                        copyfile(OS+CruiceIndex.getAttribute('CruicePath')+'/'+ListOfFilesNotcopied[i], 
                             directory2Data.dir_originalrawdata+'/'+ListOfFilesNotcopied[i])
                    except PermissionError: 
                        print(' ')
                except IsADirectoryError:  
                    print('')
                    
    
    return(directory2Data)
   