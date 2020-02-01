# synchronize-folder

The program synchronizes folder pathTo to pathFrom and vice versa.  </br>
Get files and dirs from pathsFrom and if not exists in pathTo then copy to pathTo. </br>
Compare files in pathTo with pathFrom. If file in pathFrom is more recent then replace. </br>
</br>
## Usage: </br>
python synch_folders.py pathFrom pathTo [trace] [mode] </br></br>
trace:</br>
    0 : no trace </br>
    1 : print dirs </br>
    2 : print dirs, files</br>
    3 : print dirs, files, replaced files 
</br></br>
mode: </br>
    -o : one side, then pathTo is synchronized with pathFrom </br>
    -t : two sides, then pathTo is synchronized with pathFrom and vice versa
</br></br>

## Example:
python synch_folders.py "C:/Folder1" "F:/Folder2" 0 -t
