import cv2
img=cv2.imread('deer.png')
k=int(input('Enter the size of the kernel:'))
blur=cv2.boxfilter(img,-1,(k,k), normalize=True)
