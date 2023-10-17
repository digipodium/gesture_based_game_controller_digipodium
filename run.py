import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pydirectinput

mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 540)
pose = ""
status = 0

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)     
        
        # Make Detections
        results = holistic.process(image)   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        height, width, channel = image.shape
        
        try: 
            right_hand = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * width,
                              results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * height)

        
            line_x1 = 2 * (width//5)
            line_x2 = 3 * (width//5)
            line_y1 = 2 * (height//5)
            line_y2 = 3 * (height//5)

        
            
            if (right_hand[0]>line_x2) and (right_hand[1]<line_y1) and  (right_hand[1]>0):
                pose = "Start"
                pydirectinput.keyDown('space')
                pydirectinput.keyUp('space')
                status = 1
            
            elif (right_hand[0]>line_x2) and (right_hand[1]>line_y1) and  (right_hand[1]<line_y2) and status == 1:
                pose = "Right"
                pydirectinput.keyDown('right')
                pydirectinput.keyUp('right')
            elif  (right_hand[0]<line_x1) and (right_hand[1]>line_y1) and  (right_hand[1]<line_y2) and status == 1:
                pose = "Left"
                pydirectinput.keyDown('left')
                pydirectinput.keyUp('left')
            elif (right_hand[1]<line_y1) and status == 1:
                pose="Jump"
                pydirectinput.keyDown('up')
                pydirectinput.keyUp('up')
                
            elif (right_hand[1]>line_y2) and status == 1:
                pose="Slide"
                pydirectinput.keyDown('down')
                pydirectinput.keyUp('down')
            elif status == 0:
                pose = "Please start the Game"
            else:
                pose="Run"
        except:
            pass

        cv2.putText(image, pose, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 3)
        cv2.line(image, (line_x1, 0), (line_x1, height), (255, 255, 255), 2)
        cv2.line(image, (line_x2, 0), (line_x2, height), (255, 255, 255), 2)

        cv2.line(image, (0, line_y1), (width, line_y1), (255, 255, 255), 2)
        cv2.line(image, (0, line_y2), (width, line_y2), (255, 255, 255), 2)

        # display a red outline circle on right hand
        cv2.circle(image, (int(right_hand[0]), int(right_hand[1])), 10, (0, 0, 255), 2)
       
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        
                        
        cv2.imshow('Temple Run', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()