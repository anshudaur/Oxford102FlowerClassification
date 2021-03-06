import os
import urllib.request
import scipy.io
import numpy as np
from sklearn.model_selection import train_test_split 
import shutil
import glob

def write_to_file(filename, base_path, img_paths, img_labels):
    with open(os.path.join(base_path, filename), 'w+') as f:
        for i in range(0, len(img_paths)):
            f.write('%s\t%s\n' % (os.path.join(base_path, img_paths[i]), img_labels[i]))
            
             
def move_files(data_dir, dir_name, labels):
    
    cur_dir_path = os.path.join(data_dir, dir_name)
    if not os.path.exists(cur_dir_path):
        os.mkdir(cur_dir_path)

    for i in range(1,103):
        class_dir = os.path.join(data_dir, dir_name, str(i))
        os.mkdir(class_dir)
    
    for label in labels:
        filename = str(label[0])
        src = os.path.join(data_dir,filename)
        dst = os.path.join(data_dir, dir_name, label[1], src.split(os.sep)[-1])
        #print(src,dst)
        try:
            shutil.copyfile(src, dst)
        # If source and destination are same 
        except shutil.SameFileError: 
            print("Source and destination represents the same file.",filename)           
        # If destination is a directory. 
        except IsADirectoryError: 
            print("Destination is a directory.",filename)          
        # If there is any permission issue 
        except PermissionError: 
            print("Permission denied.",filename)           
        # For other errors 
        except: 
            print("Error occurred while copying file." , filename) 
    
if __name__ == '__main__':
    data_dir      = "segmim\\"    
    dataset = []
    image_list = []

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    class_limit = 102
    # take all the images from the dataset
    image_paths = glob.glob(data_dir + "*.jpg")
    label = 0
    i = 0
    j = 8189
    
    #read imagelabels.mat file
    mat = scipy.io.loadmat('imagelabels.mat')
    labelID = mat['labels']
    print(labelID.shape)
       
    # loop over the images in the dataset and make array of images name,labels
    for index, image_path in enumerate(image_paths[i:j], start=1):
        original_path   = image_path
        image_path      = image_path.split("\\")        
        image_file_name = image_path[-1]
        image_list.append(image_file_name)
        image_ID = int(image_file_name[image_file_name.rindex('_')+1:image_file_name.rindex('.jpg')])
        dataset.append([image_file_name,labelID[0,index-1]])  
        
    dataset = np.asarray(dataset)
    #print(dataset[:,1],dataset.shape)
    train_set = []
    test_valid_set = []
    valid_set = []
    test_set = []
    
    train, test_valid = train_test_split(dataset, test_size=0.40,random_state=1, stratify=dataset[:,1])    
    print("Training Dataset : ",train.shape) 
    
    test, valid = train_test_split(test_valid, test_size=0.50,random_state=1, stratify=test_valid[:,1])    
    print("Test and Validation Dataset : " ,test.shape, valid.shape)  
    #print(train[:,-1])[:,-1]
    
    move_files(data_dir,'train', train)    
    move_files(data_dir,'test', test)
    move_files(data_dir,'valid', valid)
