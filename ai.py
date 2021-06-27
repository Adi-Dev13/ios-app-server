import cv2
import mediapipe as mp
import  numpy
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
draw = mp.solutions.drawing_utils
    
def getvid(path):
    cap = cv2.VideoCapture(path)
    return cap

def runAI(cap, path):
    i,p = cap.read()
    h,w,_ = p.shape
    
    out = cv2.VideoWriter(path, 0x7634706d, 10, (w,h))
    while cap.isOpened():
        _, img = cap.read()
        
        if type(img) != numpy.ndarray:
            break
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #stuff
        result = pose.process(rgb)
        if result.pose_landmarks:
            draw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)

        out.write(img)
        
    out.release()