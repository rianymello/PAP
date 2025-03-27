import json
import cv2
import numpy as np
import os
import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=10, grid_x=8, grid_y=8)
trainer_path = os.path.join(os.path.dirname(__file__), 'Treiner', 'trainer.yml')
recognizer.read(trainer_path)

cascadePath = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

names = ['Riany', 'Bruno', 'Pedro', 'Diogo']

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.08 * cam.get(3)
minH = 0.08 * cam.get(4)

log_file = os.path.join(os.path.dirname(__file__), 'reconhecimento_log.json')

try:
    with open(log_file, "r") as file:
        session_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    session_data = []

def find_or_create_user(name):
    for user in session_data:
        if user["name"] == name:
            return user
    new_user = {"name": name, "entries": []}
    session_data.append(new_user)
    return new_user

def log_recognition(event, name=None, confidence_value=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = ""
    user = find_or_create_user(name)

    if event == "entrou":
        user["entries"].append({
            "entry_time": current_time,
            "exit_time": None,
            "time_inside": None
        })
        log_message = f"{current_time} - {name} entrou"
    elif event == "saiu" and user["entries"]:
        last_entry = user["entries"][-1]
        if last_entry["exit_time"] is None:
            exit_time = datetime.datetime.now()
            entry_time = datetime.datetime.strptime(last_entry["entry_time"], "%Y-%m-%d %H:%M:%S")
            time_inside = exit_time - entry_time
            last_entry["exit_time"] = exit_time.strftime("%Y-%m-%d %H:%M:%S")
            last_entry["time_inside"] = str(time_inside)
            log_message = f"{current_time} - {name} saiu. Tempo dentro da sala: {time_inside}"

    with open(log_file, "w") as json_file:
        json.dump(session_data, json_file, indent=4)
    
    print(f"[LOG] {log_message}")

recognized_last_time = {}
last_position_x = {}

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        confidence_value = round(100 - confidence)

        if confidence_value >= 50:
            id = names[id]
        else:
            id = "Desconhecido"

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, f"{confidence_value}%", (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        if id != "Desconhecido":
            center_x = x + w // 2
            if id not in last_position_x:
                last_position_x[id] = center_x
                recognized_last_time[id] = None

            if center_x > last_position_x[id] + 100 and recognized_last_time[id] != id:
                log_recognition("entrou", id, confidence_value)
                recognized_last_time[id] = id
                last_position_x[id] = center_x

            elif center_x < last_position_x[id] - 100 and recognized_last_time[id] == id:
                log_recognition("saiu", id, confidence_value)
                recognized_last_time[id] = None
                last_position_x[id] = center_x

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

print("\n [INFO] Saindo do programa e limpando os recursos")
cam.release()
cv2.destroyAllWindows()
