import os

def createTrainvalTxt(baseDirDataSet):
    removeFiles=[]
    buffer = ''
    baseDir = baseDirDataSet+'/Images'
    for filename in os.listdir(baseDir):

        filenameOnly, file_extension = os.path.splitext(filename)
        if filenameOnly+'.xml' in os.listdir(baseDirDataSet+'/Labels'):  # meaning that we labeled that file:
            s = 'Images/'+filenameOnly+'.jpg'+' '+'Labels/'+filenameOnly+'.xml\n'
            print (repr(s))
            img_file, anno = s.strip("\n").split(" ")
            print(repr(img_file), repr(anno))
            buffer+=s
        else:
            removeFiles.append('Images/'+filename)
            removeFiles.append('Labels/'+filenameOnly+'.xml')

    with open(baseDirDataSet+'/Structure/trainval.txt', 'w') as file:
        file.write(buffer)  
    with open(baseDirDataSet+'/Structure/test.txt', 'w') as file:
        file.write(buffer)  
    
    for file in removeFiles:
        try:
            os.remove(file)
        except:
            pass
    print('Done')   
#Usage
createTrainvalTxt('../../MyDataset/bird_dataset')
