# import cv2
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
# # from gtts import gTTs 
# from playsound import playsound

# video = cv2.VideoCapture(0)
# labels = []
# while True:
#     ret, frame = video.read()
#     bbox, label, conf = cv.detect_common_objects(frame, confidence= 0.5, model='yolov3-tiny')
#     output_image = draw_bbox(frame, bbox, label, conf)
#     cv2.imshow("-object detection-", output_image)
#     for item in label:
#         if item in labels:
#             pass
#         else:
#             labels.append(item)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# for i in labels:
#    print(i)q


import cv2
import cvlib as cv
from playsound import playsound

def draw_bbox_thicker(image, bbox, label, confidence, color=(0, 255, 0), thickness=2):
    for i, box in enumerate(bbox):
        (startX, startY, endX, endY) = box
        cv2.rectangle(image, (startX, startY), (endX, endY), color, thickness)

        label_text = f"{label[i]}: {confidence[i]:.2f}"
        cv2.putText(image, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    return image

video = cv2.VideoCapture(0)
labels = []

while True:
    ret, frame = video.read()
    bbox, label, conf = cv.detect_common_objects(frame, confidence=0.25, model='yolov3-tiny')
    output_image = draw_bbox_thicker(frame, bbox, label, conf, thickness=5)
    cv2.imshow("-object detection-", output_image)

    for item in label:
        if item in labels:
            pass
        else:
            labels.append(item)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

for i in labels:
    print(i)
