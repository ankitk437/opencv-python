import numpy as np 
import cv2 
import os
import math
from scipy.spatial import KDTree
#distance funtion
#def difdistance(a1,a2,b1,b2,c1,c2):
 #  a=abs(a1-a2)
 #   b=abs(b1-b2)
 #   c=abs(c1-c2)
 #   return (a+b+c)//3
#def mindistance(img1,img2):
#    mindist=[255*math.sqrt(3),0]
#    mindist1=difdistance(img1[0][0],img2[0],img1[0][1],img2[1],img1[0][2],img2[2])
#    i1=0
#    for img in img1:
#        if mindist1<mindist[0]:
#            mindist=[mindist1,i1]
#            mindist1 =difdistance(img[0],img2[0],img[1],img2[1],img[2],img2[2])
#        else:
#            mindist1=difdistance(img[0],img2[0],img[1],img2[1],img[2],img2[2])
#        i1+=1
 #   return mindist[1]
##
print('Enter folder name(ABSOLUTE PATH) having MULTIPLE( MIN 500-800 FOR BETER LOOK) small IMAGES(FOR BACKGROUND)')

   

folder=input()
#
##binary_search to find particular flower
#globalindex=0
#def binary_search(arr,index, low, high, x): 
#     
#    # Check base case 
#    if high >= low: 
# 
#        mid = (high + low) // 2
 #       
#  
#        # If element is present at the middle itself 
#        if arr[mid][index] == x: 
#            globalindex=arr[mid][3]
#            return globalindex
 # 
 #       # If element is smaller than mid, then it can only 
#        # be present in left subarray 
#        elif arr[mid][index] > x: 
 #           return binary_search(arr,index, low, mid - 1, x) 
#  
#        # Else the element can only be present in right subarray 
#        else: 
#            return binary_search(arr,index, mid + 1, high, x) 
#  
#    else: 
#        globalindex=arr[low][3]
#        # Element is not present in the array 
#        return globalindex 

def load_images_from_folder(folder):
    images=[]
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),1)
        if img is not None:
            images.append(img)
    return images

#big image
print("Enter IMAGE FILE name(ABSOLUTE PATH) having ONE BIG IMAGE (FOR FOREGROUND)")
filelocation=input()
big_img=cv2.imread(filelocation,1)
H,W =big_img.shape[:2]

H1 , W1= (H,W) 

bigimage=cv2.resize(big_img,(H1,W1))
blankimage=np.zeros(bigimage.shape[:3], dtype=np.uint8)
print(blankimage.shape[2])


#small image
smallimages=load_images_from_folder(folder)
smallimages2 =[]
h,w=smallimages[1].shape[:2]
singlearea = H1*W1/len(smallimages)
h1=int(math.sqrt(singlearea*h/w))
w1=int(h1*h/w)
avg_colors=[]

#resize
for im in smallimages:
    smallimages2.append(cv2.resize(im,(h1,w1)))
    

    avg_color_per_row =np.average(im, axis=0)
    avg=list(np.array(np.average(avg_color_per_row, axis=0),dtype=np.uint32))
    
    
    avg_colors.append(avg)

#test
#test =0
#for im1 in smallimages2:
#    test+=1
#    print(im1.shape[:2]) 
#print(test)
#sort
#avg_colors.sort(key= lambda bgr: bgr[0]*bgr[0]+ bgr[1]*bgr[1]+ bgr[2]*bgr[2])
#print(h1,w1)
avg_colors2=[]
#averaging big image pixel image
for ix in range(0,H1,h1):
    for iy in range(0,W1,w1):
        
        
        avg_color_per_row =np.average(bigimage[iy:iy+w1 , ix:ix+h1], axis=0)
        avg=list(np.array(np.average(avg_color_per_row, axis=0),dtype=np.uint32))
        avg_colors2.append(avg)
        
        #blankimage[iy:iy+w1 , ix:ix+h1]=
kdtree=KDTree(avg_colors) 
ist,points=kdtree.query(avg_colors2,1)
#testing

#print(avg_colors[0][:])    
#print(avg_colors2[0][:])   
#print(points)  
counter=0        
for ix in range(0,H1,h1):
    for iy in range(0,W1,w1):
        
        if bigimage[iy:iy+h1 , ix:ix+w1].shape[0:2]==(h1,w1):
            
                blankimage[iy:iy+w1 , ix:ix+h1]=cv2.addWeighted(smallimages2[points[counter]],0.5,bigimage[iy:iy+w1 , ix:ix+h1],0.4,0)    
        counter+=1  
         

cv2.imshow("hello",blankimage)
 
  
# Filename 
filename = 'savedImage.jpg'
  
 
# Saving the image 
cv2.imwrite(filename, blankimage) 
  

k = cv2.waitKey(0) & 0xFF

# wait for ESC key to exit 
if k == 27:  
    cv2.destroyAllWindows() 
      
# wait for 's' key to save and exit 
elif k == ord('s'):  

    cv2.destroyAllWindows() 
