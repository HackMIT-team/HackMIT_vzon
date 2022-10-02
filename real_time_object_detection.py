from speech_text import speak
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import speech_recognition as sr 



r=sr.Recognizer()

with sr.Microphone() as source:
    print("Speak now")
    audio=r.listen(source, phrase_time_limit=4.0)
    try:

        query=r.recognize_google(audio)
        print(query)

    except sr.UnknownValueError:
        print("Could not understand")
    except sr.RequestError:
        print("Could not request result from google")


query_split = query.lower().split()
if('what' in query_split):

	ap = argparse.ArgumentParser()
	# ap.add_argument("-p", "--prototxt", required=True,
	# 	help="path to Caffe 'deploy' prototxt file")
	# ap.add_argument("-m", "--model", required=True,
	# 	help="path to Caffe pre-trained model")
	wt = 'MobileNetSSD_deploy.prototxt.txt'
	ht = 'MobileNetSSD_deploy.caffemodel'
	ap.add_argument("-c", "--confidence", type=float, default=0.2,
		help="minimum probability to filter weak predictions")
	args = vars(ap.parse_args())


	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "table",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "laptop","mouse","keybaord","phone"]

	# Assigning random colors to each of the classes
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(wt,ht)   #args["prototxt"], args["model"]

	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()

	time.sleep(2.0)

	fps = FPS().start()
	import time

	t_end = time.time() + 2

	while time.time()<t_end:

		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		print(frame.shape) # (225, 400, 3)

		(h, w) = frame.shape[:2]
		# Resize each frame
		resized_image = cv2.resize(frame, (300, 300))


		blob = cv2.dnn.blobFromImage(resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)

		net.setInput(blob) 
		# Predictions:
		predictions = net.forward()
		object_lst = []
		
		for i in np.arange(0, predictions.shape[2]):

			confidence = predictions[0, 0, i, 2]

			if confidence > args["confidence"]:

				idx = int(predictions[0, 0, i, 1])
				# then compute the (x, y)-coordinates of the bounding box for the object
				box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])

				(startX, startY, endX, endY) = box.astype("int")


				label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
				print("Object detected: ", label)
				n = label.find(':')
				object_lst.append(label[:n])
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15

				cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				


		cv2.imshow("Frame", frame)




		key = cv2.waitKey(1) & 0xFF


		if key == ord("q"):
			break

		
		fps.update()

	fps.stop()

	print("[INFO] Elapsed Time: {:.2f}".format(fps.elapsed()))
	print("[INFO] Approximate FPS: {:.2f}".format(fps.fps()))


	cv2.destroyAllWindows()

	vs.stop()
	s_obj = set(object_lst)
	obj_lst_no_dupli = list(s_obj)
	if(len(obj_lst_no_dupli)>1):
		lst2 = []
		for i in obj_lst_no_dupli:
			lst2.append(',a')
			lst2.append(i)
		lst2[-2] = ',and a'
		words = ' '.join(lst2)
		audio = "I can see " + words
	else:
		audio = "I can see a " + obj_lst_no_dupli[0]
	speak(audio)
else:
	pass
 
