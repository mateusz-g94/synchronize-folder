# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 13:34:05 2019

@author: Mateusz

Synchronize folder pathTo with pathFrom; 
Gets files and dirs from pathsFrom and if not exists in pathTo then copy to pathTo;
Compare files in pathTo with pathFrom. If file in pathFrom is more recent then replace;

Usage:
python synch_folders.py pathFrom pathTo [trace] [mode]
trace: if 0 -> no trace, 1 -> print dirs, 2 -> print dirs, files, 3 -> print dirs, files, replaced files;
Choses synchronization mode;
    if -o : one side, then pathTo is synchronized with pathFrom
    if -t : two sides, then pathTo is synchronized with pathFrom and vice versa

Example:
python synch_folders.py "C:/Folder1" "F:/Folder2" 0 -t

Result:
Both folders are identical.

## Develop: czy pliki sa takie same?

"""

import os, sys
maxfileload = 1000000
bulksize = 1024 * 500

def copyfile(pathFrom, pathTo, maxfileload = maxfileload):
    """
    Copy file pathFrom to PathTo, byte for byte;
    uses binary file modes to supress unicode decode and endline transform;
    """
    if os.path.getsize(pathFrom) <= maxfileload:
        bytesFrom = open(pathFrom, 'rb').read()                                 # read small files all at once
        fileTo = open(pathTo, 'wb')
        fileTo.write(bytesFrom)
    else:
        fileFrom = open(pathFrom, 'rb')                                         # read a big file in a chunks
        fileTo = open(pathTo, 'wb')                                             # neeed b mode for both
        while True:
            bytesFrom = fileFrom.read(bulksize)                                 # get one block
            if not bytesFrom: break
            fileTo.write(bytesFrom)
            
def compare_files_modification_time(pathTo, pathFrom):
    """
    Compare time modification time file pathTo to pathFrom
    Return True if pathTo is more current else False;
    """
    if os.path.getmtime(pathFrom) < os.path.getmtime(pathTo): return True
    else: return False

def reset_global_params():
    """
    Set global params;
    Print in console;
    """
    global num_mk_dirs, num_copy_files, num_replaced_files, files_not_to_syn 
    num_mk_dirs = num_copy_files = num_replaced_files = 0
    files_not_to_syn = []                                                       # Files that has been copied or replaced before and tehre is no need to synch
    
def synch_folders(pathFrom, pathTo, trace = 0):
    """
    Synchronize folder pathTo with pathFrom; 
    Gets files and dirs from pathsFrom and if not exists in pathTo then copy to pathTo;
    Compare files in pathTo with pathFrom. If file in pathFrom is more recent then replace;
    trace: if 1 -> print dirs, 2 -> print dirs, files, 3 -> print dirs, files, replaced files;
    """
    global num_mk_dirs, num_copy_files, num_replaced_files
    for (thisDir, dirsHere, filesHere) in os.walk(pathFrom):
        rel_path = os.path.relpath(thisDir, pathFrom)                           # cut thisDir path to relative path
        if thisDir != pathFrom: full_pathTo = os.path.join(pathTo, rel_path)
        else: full_pathTo = pathTo                                              # gets same relative path in destination place if/else becouse of .
        for dirHere in dirsHere:                                                # if dir doesnt exist in relativ pathTo then create
            dir_pathTo = os.path.join(full_pathTo, dirHere)
            if not os.path.exists(dir_pathTo):
                os.mkdir(dir_pathTo)
                num_mk_dirs += 1
                if trace > 0: print('Dir has been created: ', dir_pathTo)
        for fileHere in filesHere:                                              
            file_pathTo = os.path.join(full_pathTo, fileHere)
            file_pathFrom = os.path.join(thisDir, fileHere)
            if not os.path.exists(file_pathTo):                                 # if file doesnt exist in destination then copy
                copyfile(file_pathFrom, file_pathTo)
                files_not_to_syn.append(file_pathFrom)
                num_copy_files += 1
                if trace > 1: print('File has been copied.. from',file_pathFrom,'to', file_pathTo)
            elif os.path.exists(file_pathTo) and (not compare_files_modification_time(file_pathTo, file_pathFrom)) and (file_pathTo not in files_not_to_syn):       # if file exists then compare last modification date this two files
                os.remove(file_pathTo)
                copyfile(file_pathFrom, file_pathTo)
                files_not_to_syn.append(file_pathFrom)
                num_replaced_files += 1
                if trace > 2: print('File has been replaced', file_pathTo)
                
def synch_mode(pathFrom, pathTo, trace = 0, mode = '-o'):
    """
    Choses synchronization mode;
    if -o : one side, then pathTo is synchronized with pathFrom
    if -t : two sides, then pathTo is synchronized with pathFrom and vice versa
    """
    if mode == '-o':
        synch_folders(pathFrom = pathFrom, pathTo = pathTo, trace = trace)
    if mode == '-t':
        synch_folders(pathFrom = pathFrom, pathTo = pathTo, trace = trace)
        synch_folders(pathFrom = pathTo, pathTo = pathFrom, trace = trace)
        
                
def start_synch():
    """
    Get and verify directory name arguments, returns deafult None on errors
    """
    # Get params 
    if len(sys.argv) == 3:
        (pathTo, pathFrom) = sys.argv[1:3]
        params = {'pathFrom' : pathFrom, 'pathTo' : pathTo}
            
    elif len(sys.argv)  == 4:
        (pathTo, pathFrom) = sys.argv[1:3]
        trace = int(sys.argv[3])
        params = {'pathFrom' : pathFrom, 'pathTo' : pathTo, 'trace' : trace}
    
    elif len(sys.argv)  == 5:
        (pathTo, pathFrom) = sys.argv[1:3]
        trace = int(sys.argv[3])
        mode = sys.argv[4]
        params = {'pathFrom' : pathFrom, 'pathTo' : pathTo, 'trace' : trace, 'mode' : mode}
        if params['mode'] not in ('-o', '-t'):
            print('Mode error, choose one of (-o, -t)')
            print('Exiting...')
            sys.exit()   
    else:
        print('Usage error')
        print('Exiting...')
        sys.exit()
    
    # Check paths corectness
    if not os.path.exists(params['pathFrom']):
        print('PathFrom doesn\'t exists')
        print('Exiting...')
        sys.exit()
    if not os.path.exists(params['pathTo']):
        print('PathTo doesn\'t exists')
        print('Exiting...')
        sys.exit()
    
    # Printing progress and run    
    print('Synchronize is in progress...')
    if params['mode'] == '-o':
        print('Mode one side')
    else:
        print('Mode: two sides')
    print('Folder: ', params['pathTo'])
    print('With:', params['pathFrom'])
    ask = input('Continue? (y/n)')
    if ask == 'y':
        print('Start', '-' * 50)
        reset_global_params()
        synch_mode(**params)
        print('Finish', '-' * 50)
        print('Created: ', num_mk_dirs, 'dirs.')
        print('Copied: ', num_copy_files, 'files.')
        print('Replaced: ', num_replaced_files, 'files.')
    else:
        sys.exit()
        
if __name__ == '__main__':
    start_synch()

