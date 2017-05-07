import numpy as np
import cv2 as cv
import requests
import matplotlib.pyplot as plt
import pickle

st_api_id = 'c58fef57c9224849991e84eeea3bd690'
st_api_secret = 'e155b31d87aa4640b4bf12427dab8293'


def detect_frame(file):
    res = requests.post('https://v1-api.visioncloudapi.com/face/detection',
                        data={'api_id': st_api_id, 'api_secret': st_api_secret, 'attributes': 1},
                        files={'file': file})
    faces = res.json()['faces']
    features = map(lambda f: {
        'rect': f['rect'],
        'emotions': f['emotions'],
        'eye_open': f['attributes']['eye_open'],
        'smile': f['attributes']['smile']
    }, faces)
    return features


def eval_features(features):
    eye_open = map(lambda f: f['eye_open'], features)
    smile = map(lambda f: f['smile'], features)

    concentration = np.mean(eye_open)
    joy = np.mean(smile)

    return (concentration, joy)


def save_object(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def detect_video(video_path, interval=0.5):
    video = cv.VideoCapture(video_path)
    fps = video.get(cv.CAP_PROP_FPS)
    data = []
    msPerFrame = 1 / fps
    currentTime = 0
    features = None
    while 1:
        ret, img = video.read()
        if not ret:
            break
        currentTime += msPerFrame
        if currentTime >= interval:
            cv.imwrite('tmp.png', img)
            with open('tmp.png', 'rb') as file:
                features = detect_frame(file)
                concentration, joy = eval_features(features)
                data.append((len(data) * interval + currentTime, concentration, joy, features))
            currentTime -= interval
    video.release()

    data_path = video_path + '.dat'
    save_object(data, data_path)


def show_video(video_path):
    data_path = video_path + '.dat'
    data = load_object(data_path)

    video = cv.VideoCapture(video_path)
    fps = video.get(cv.CAP_PROP_FPS)
    msPerFrame = 1 / fps
    currentTime = 0
    features = None
    curDataIdx = 0

    x = map(lambda x: x[0], data)
    cc = map(lambda x: x[1], data)
    jj = map(lambda x: x[2], data)

    plt.ion()
    plt.figure(figsize=(6, 3))
    plt.xlabel("Time(s)")
    plt.ylabel("Index")
    plt.title("Realtime Info")

    cv.namedWindow('video', cv.WINDOW_NORMAL)
    cv.resizeWindow('video', 667, 375)

    while 1:
        ret, img = video.read()
        if not ret:
            break
        currentTime += msPerFrame
        if curDataIdx < len(data) and currentTime >= data[curDataIdx][0]:
            _, c, j, features = data[curDataIdx]
            curDataIdx += 1 
            plt.plot(x[:curDataIdx], cc[:curDataIdx], "b", linewidth=1, label='Concentration')
            plt.plot(x[:curDataIdx], jj[:curDataIdx], "r", linewidth=1, label='Joyness')
            plt.pause(0.05)

        if features:
            for face in features:
                rect = face['rect']
                img = cv.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (0, 255, 0), 2)
            size = 2
            color = (255, 255, 255)
            cv.putText(img, "Concentration: {0}".format(c), (10, 50), cv.FONT_HERSHEY_SIMPLEX, size, color, 2)
            cv.putText(img, "Joy: {0}".format(j), (10, 100), cv.FONT_HERSHEY_SIMPLEX, size, color, 2)

        cv.imshow("video", img)
        ch = 0xFF & cv.waitKey(1)
        if ch == 27:
            break
    cv.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    #detect_video('demo.MOV')
    show_video('demo.MOV')
    # with open('demo.MOV.txt', 'w') as file:
    #     file.write(str(load_object('demo.MOV.dat')))