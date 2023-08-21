
import logging
#from msilib.schema import Feature
import os
from turtle import circle
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import warnings
import pyautogui
import cv2

def get_Middle_Str(content, startStr, endStr):
    """
    根据字符串首尾字符来获取指定字符
    :param content: 字符内容
    :param startStr: 开始字符
    :param endStr: 结束字符
    :return:
    """
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

# 比對圖片，獲取圖片的特徵點
def get_image_element_point(src_path,dst_path):
    """
    获取图像目标的坐标点
    :param src_path: 原图像
    :param dst_path: 目标识别图像
    :return: 目标元素的中心坐标点
    """

    print('src_path:%s,dst_path:%s'%(src_path,dst_path))

    #以灰度模式读取图像
    src_img = cv.imread(src_path,cv.IMREAD_GRAYSCALE)
    dst_img = cv.imread(dst_path,cv.IMREAD_GRAYSCALE)

    #plt.imshow(src_img, 'gray'), plt.show()
    #plt.imshow(dst_img, 'gray'), plt.show()

    # 创建SITF对象
    sift = cv.SIFT_create()

    # 使用SITF找到关键点和特征描述
    kp1, des1 = sift.detectAndCompute(src_img,None)
    kp2, des2 = sift.detectAndCompute(dst_img,None)


    # FLANN 匹配算法参数
    FLANN_INDEX_KDTREE = 2

    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5) #第一个参数指定算法
    search_params = dict(checks=50) #指定应递归遍历索引中的树的次数


    # flann特征匹配
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)


    # 初始化匹配模板表
    matchesMask = [[0,0] for i in range(len(matches))]

    good=[]

    # 匹配阈值
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.5*n.distance:
            good.append(m)
            matchesMask[i]=[1,0]

    MIN_MATCH_COUNT=5

    #获取转换矩阵
    if len(good)>MIN_MATCH_COUNT:
        #获取关键点坐标
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #获取变换矩阵，M就是变化矩阵
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        #获得原图像高和宽
        h,w = src_img.shape

        #print("h :",h)
        #print("w :",w)
        #使用得到的变换矩阵对原图像的四个角进行变换，获得在目标上对应的坐标
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)

        #提取坐标点
        cordinate_x1=get_Middle_Str(str(dst[2]),'[[',']]').split()[0].split('.')[0]
        cordinate_y1=get_Middle_Str(str(dst[2]),'[[',']]').split()[1].split('.')[0]

        cordinate_x2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[0].split('.')[0]
        cordinate_y2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[1].split('.')[0]

        #提取目标元素中心坐标点
        mid_cordinate_x=(int(cordinate_x1)-int(cordinate_x2))/2+int(cordinate_x2)
        mid_cordinate_y=(int(cordinate_y1)-int(cordinate_y2))/2+int(cordinate_y2)

        #原图像还原为灰度
        img2 = cv.polylines(dst_img,[np.int32(dst)],True,255,10, cv.LINE_AA)

        ############打印图像轮廓#################
        draw_params = dict(matchColor=(0, 255, 0),
                           # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv.drawMatches(src_img, kp1, dst_img, kp2, good, None, **draw_params)
        #plt.imshow(img3, 'gray'), plt.show()
        #cv2.drawContours(img3, good, 0, 255, -1)#绘制轮廓，填充
        #cv2.circle(img1, (mid_cordinate_x, mid_cordinate_y), 0, 255, -1)#绘制中心点
        #plt.imsave('C:/Users/brent_yang/Desktop/Selenium/KKGAME_PIC_VS/new_1.png',img3)

        #print("圖像比對 :成功，有符合的圖像")
        Feature = int(format(len(good)))
        print("<span class = yellow-bg1>Fearure :",Feature,"<br></span>")
        print("座標點 :(",mid_cordinate_x,",",mid_cordinate_y,")")
        #print("座標點1 :(",cordinate_x1,",",cordinate_y1,")")
        return Feature
    else:
        #logging.exception("error --------")
        print( "<span class = yellow-bg1><br>Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) ,".</span>")
        Feature = int(format(len(good)))
        print("<span class = yellow-bg1>Fearure :",Feature,"<br></span>")
        #print("座標點1 :(",cordinate_x1,",",cordinate_y1,")")
        #print("座標點2 :(",cordinate_x2,",",cordinate_y2,")")
        matchesMask = None
        return Feature

# 獲得特徵點X座標點
def get_point_x(src_path,dst_path):
    #以灰度模式读取图像
    src_img = cv.imread(src_path,cv.IMREAD_GRAYSCALE)
    dst_img = cv.imread(dst_path,cv.IMREAD_GRAYSCALE)

    # 创建SITF对象
    sift = cv.SIFT_create()

    # 使用SITF找到关键点和特征描述
    kp1, des1 = sift.detectAndCompute(src_img,None)
    kp2, des2 = sift.detectAndCompute(dst_img,None)

    # FLANN 匹配算法参数
    FLANN_INDEX_KDTREE = 1

    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5) #第一个参数指定算法
    search_params = dict(checks=50) #指定应递归遍历索引中的树的次数

    # flann特征匹配
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # 初始化匹配模板表
    matchesMask = [[0,0] for i in range(len(matches))]

    good=[]

    # 匹配阈值
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.5*n.distance:
            good.append(m)
            matchesMask[i]=[1,0]

    MIN_MATCH_COUNT=5

    #获取转换矩阵
    if len(good)>MIN_MATCH_COUNT:
        #获取关键点坐标
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #获取变换矩阵，M就是变化矩阵
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        #获得原图像高和宽
        h,w = src_img.shape

        #使用得到的变换矩阵对原图像的四个角进行变换，获得在目标上对应的坐标
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)

        #提取坐标点
        cordinate_x1=get_Middle_Str(str(dst[2]),'[[',']]').split()[0].split('.')[0]
        cordinate_y1=get_Middle_Str(str(dst[2]),'[[',']]').split()[1].split('.')[0]


        cordinate_x2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[0].split('.')[0]
        cordinate_y2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[1].split('.')[0]

        #提取目标元素中心坐标点
        mid_cordinate_x=round((int(cordinate_x1)-int(cordinate_x2))/2)
        mid_cordinate_y=(int(cordinate_y1)-int(cordinate_y2))/2+int(cordinate_y2)

        #原图像还原为灰度
        img2 = cv.polylines(dst_img,[np.int32(dst)],True,255,10, cv.LINE_AA)

        ############打印图像轮廓#################
        draw_params = dict(matchColor=(0, 255, 0),
                           # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv.drawMatches(src_img, kp1, dst_img, kp2, good, None, **draw_params)

        Feature = int(format(len(good)))
        #print("座標點y :",mid_cordinate_x)
        return mid_cordinate_x

# 獲得特徵點Y座標點
def get_point_y(src_path,dst_path):

    #以灰度模式读取图像
    src_img = cv.imread(src_path,cv.IMREAD_GRAYSCALE)
    dst_img = cv.imread(dst_path,cv.IMREAD_GRAYSCALE)

    # 创建SITF对象
    sift = cv.SIFT_create()

    # 使用SITF找到关键点和特征描述
    kp1, des1 = sift.detectAndCompute(src_img,None)
    kp2, des2 = sift.detectAndCompute(dst_img,None)

    # FLANN 匹配算法参数
    FLANN_INDEX_KDTREE = 1

    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5) #第一个参数指定算法
    search_params = dict(checks=50) #指定应递归遍历索引中的树的次数

    # flann特征匹配
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # 初始化匹配模板表
    matchesMask = [[0,0] for i in range(len(matches))]

    good=[]

    # 匹配阈值
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.5*n.distance:
            good.append(m)
            matchesMask[i]=[1,0]

    MIN_MATCH_COUNT=5

    #获取转换矩阵
    if len(good)>MIN_MATCH_COUNT:
        #获取关键点坐标
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #获取变换矩阵，M就是变化矩阵
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        #获得原图像高和宽
        h,w = src_img.shape

        #使用得到的变换矩阵对原图像的四个角进行变换，获得在目标上对应的坐标
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)

        #提取坐标点
        cordinate_x1=get_Middle_Str(str(dst[2]),'[[',']]').split()[0].split('.')[0]
        cordinate_y1=get_Middle_Str(str(dst[2]),'[[',']]').split()[1].split('.')[0]


        cordinate_x2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[0].split('.')[0]
        cordinate_y2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[1].split('.')[0]

        #提取目标元素中心坐标点
        mid_cordinate_x=(int(cordinate_x1)-int(cordinate_x2))/2+int(cordinate_x2)
        mid_cordinate_y=round((int(cordinate_y1)-int(cordinate_y2))/2)

        #原图像还原为灰度
        img2 = cv.polylines(dst_img,[np.int32(dst)],True,255,10, cv.LINE_AA)

        ############打印图像轮廓#################
        draw_params = dict(matchColor=(0, 255, 0),
                           # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv.drawMatches(src_img, kp1, dst_img, kp2, good, None, **draw_params)

        Feature = int(format(len(good)))
        #print("座標點y :",mid_cordinate_y)
        return mid_cordinate_y

# 比對圖片，獲取圖片的特徵點
def get_vsimage(src_path,dst_path):
    """
    获取图像目标的坐标点
    :param src_path: 原图像
    :param dst_path: 目标识别图像
    :return: 目标元素的中心坐标点
    """

    print('src_path:%s,dst_path:%s'%(src_path,dst_path))

    #以灰度模式读取图像
    src_img = cv.imread(src_path,cv.IMREAD_GRAYSCALE)
    dst_img = cv.imread(dst_path,cv.IMREAD_GRAYSCALE)

    # 创建SITF对象
    sift = cv.SIFT_create()

    # 使用SITF找到关键点和特征描述
    kp1, des1 = sift.detectAndCompute(src_img,None)
    kp2, des2 = sift.detectAndCompute(dst_img,None)


    # FLANN 匹配算法参数
    FLANN_INDEX_KDTREE = 1

    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5) #第一个参数指定算法
    search_params = dict(checks=50) #指定应递归遍历索引中的树的次数


    # flann特征匹配
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)


    # 初始化匹配模板表
    matchesMask = [[0,0] for i in range(len(matches))]

    good=[]

    # 匹配阈值
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.5*n.distance:
            good.append(m)
            matchesMask[i]=[1,0]

    MIN_MATCH_COUNT=5

    #获取转换矩阵
    if len(good)>MIN_MATCH_COUNT:
        #获取关键点坐标
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #获取变换矩阵，M就是变化矩阵
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        #获得原图像高和宽
        h,w = src_img.shape

        #print("h :",h)
        #print("w :",w)
        #使用得到的变换矩阵对原图像的四个角进行变换，获得在目标上对应的坐标
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)


        #提取坐标点
        cordinate_x1=get_Middle_Str(str(dst[2]),'[[',']]').split()[0].split('.')[0]
        cordinate_y1=get_Middle_Str(str(dst[2]),'[[',']]').split()[1].split('.')[0]


        cordinate_x2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[0].split('.')[0]
        cordinate_y2 = get_Middle_Str(str(dst[0]), '[[', ']]').split()[1].split('.')[0]

        #提取目标元素中心坐标点
        mid_cordinate_x=(int(cordinate_x1)-int(cordinate_x2))/2+int(cordinate_x2)
        mid_cordinate_y=(int(cordinate_y1)-int(cordinate_y2))/2+int(cordinate_y2)

        #原图像还原为灰度
        img2 = cv.polylines(dst_img,[np.int32(dst)],True,255,10, cv.LINE_AA)

        ############打印图像轮廓#################
        draw_params = dict(matchColor=(0, 255, 0),
                           # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv.drawMatches(src_img, kp1, dst_img, kp2, good, None, **draw_params)
        return img3
    else:
        #logging.exception("error --------")
        #print( "<span class = yellow-bg1><br>Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) ,".</span>")
        Feature = int(format(len(good)))
        #print("<span class = yellow-bg1>Fearure :",Feature,"<br></span>")
        matchesMask = None
        return Feature
        
if __name__ == '__main__':
    img1 = r'C:/Users/brent_yang/Desktop/Selenium/pic/background_function.png'
    img2 = r'C:/Users/brent_yang/Desktop/Selenium/pic/rule.png'
    getFeature = get_image_element_point(img1,img2)
    getpointx = get_point_x(img1,img2)
    getpointy = get_point_y(img1,img2)
    getimage = get_vsimage(img1,img2)
    #pyautogui.moveTo(getpointx,getpointy)
    
