import numpy as np 
import cv2 
import os
import math

#distance funtion
def difdistance(a1,a2,b1,b2,c1,c2):
    a=abs(a1-a2)
    b=abs(b1-b2)
    c=abs(c1-c2)
    
    return (a+b+c)//3
def mindistance(img1,img2):
    mindist=[255*math.sqrt(3),0]
    mindist1=difdistance(img1[0][0],img2[0],img1[0][1],img2[1],img1[0][2],img2[2])
    i1=0
    for img in img1:
        if mindist1<mindist[0]:
            mindist=[mindist1,i1]
            mindist1 =difdistance(img[0],img2[0],img[1],img2[1],img[2],img2[2])
        else:
            mindist1=difdistance(img[0],img2[0],img[1],img2[1],img[2],img2[2])
        i1+=1
    return mindist[1]


   

folder='/home/black-pearl/Documents/archive/flowers'

#binary_search to find particular flower
globalindex=0
def binary_search(arr,index, low, high, x): 
     
    # Check base case 
    if high >= low: 
  
        mid = (high + low) // 2
        
  
        # If element is present at the middle itself 
        if arr[mid][index] == x: 
            globalindex=arr[mid][3]
            return globalindex
  
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid][index] > x: 
            return binary_search(arr,index, low, mid - 1, x) 
  
        # Else the element can only be present in right subarray 
        else: 
            return binary_search(arr,index, mid + 1, high, x) 
  
    else: 
        globalindex=arr[low][3]
        # Element is not present in the array 
        return globalindex 

def load_images_from_folder(folder):
    images=[]
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),1)
        if img is not None:
            images.append(img)
    return images

#big image
big_img=cv2.imread(os.path.join(folder, 'test1.jpg'),1)
H,W =big_img.shape[:2]

H1 , W1= (1050,int(1050*H/W)) 

bigimage=cv2.resize(big_img,(H1,W1))
blankimage=np.zeros(bigimage.shape[:3], dtype=np.uint8)
print(blankimage.shape[2])


#small image
smallimages=load_images_from_folder(os.path.join(folder,'flowers'))
smallimages2 =[]
h,w=smallimages[1].shape[:2]
singlearea = H1*W1/len(smallimages)
h1=int(math.sqrt(singlearea*h/w))
w1=int(h1*h/w)
avg_colors=[]
i=0
#resize
for im in smallimages:
    smallimages2.append(cv2.resize(im,(h1,w1)))
    

    avg_color_per_row =np.average(im, axis=0)
    avg=list(np.array(np.average(avg_color_per_row, axis=0),dtype=np.uint32))
    avg=avg+[i]
    i+=1
    avg_colors.append(avg)
#test
test =0
for im1 in smallimages2:
    test+=1
    print(im1.shape[:2]) 
print(test)
#sort
#avg_colors.sort(key= lambda bgr: bgr[0]*bgr[0]+ bgr[1]*bgr[1]+ bgr[2]*bgr[2])

print(h1,w1)

#combining image
for ix in range(0,H1,h1):
    for iy in range(0,W1,w1):
        img3=cv2.resize(bigimage[iy:iy+w1 , ix:ix+h1],(h1,w1))
        index=mindistance(avg_colors,bigimage[iy+w1//2][ix+h1//2])
        print(h1,w1)
        
        #blankimage[iy:iy+w1 , ix:ix+h1]=
        if bigimage[iy:iy+h1 , ix:ix+w1].shape[0:2]==(h1,w1):
            #cv2.addWeighted(img1, wt1, img2, wt2, gammaValue)
            print('hello')
            blankimage[iy:iy+w1 , ix:ix+h1]=cv2.addWeighted(smallimages2[index],0.7,bigimage[iy:iy+w1 , ix:ix+h1],0.2,0)
            
        
         



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
