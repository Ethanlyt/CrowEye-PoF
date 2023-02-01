import numpy as np
import os
import shutil
import requests
import base64
import cv2


def record():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter('test.mp4', cv2.VideoWriter_fourcc(
        *'H', '2', '6', '4'), 20, (width, height))
    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()

        if elapsed_time > 6:
            break

        writer.write(frame)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    writer.release()
    cap.release()
    cv2.destroyAllWindows()


def evaluate_crowd(width, height):
    filename = "test.mp4"
    fps = 30
    count = 6
    videoCapture = cv2.VideoCapture(filename)
    i = 0
    j = 0
    while True:
        success, frame = videoCapture.read()

        i += 1
        if (i % count == 0):
            j += 1
            try:
                savedname = filename.split(
                    '.')[0] + '_' + str(j) + '_' + str(i) + '.jpg'
                cv2.imwrite("image/"+savedname, frame)
                print('image of %s is saved' % (savedname))

                request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
                f = open("image/" + savedname, 'rb')
                img = base64.b64encode(f.read())
                
                x1 = 1
                y1 = 1
                x2 = width-10
                y2 = y1
                x3 = x2
                y3 = height-10
                x4 = x1
                y4 = y3
                params = {"area": f"{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4}", "case_id": 16, "case_init": "true", "dynamic": "true",
                          "image": img, "show": "true"}
                access_token = '24.fbf034f14af4e9a7f6606d57b0804f81.2592000.1676737364.282335-29804345'

                request_url = request_url+"?access_token="+access_token
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                response = requests.post(
                    request_url, data=params, headers=headers)

                if response:
                    with open(f"image/{savedname}", 'wb') as f:
                        f.write(base64.b64decode(response.json()['image']))
                    result_crowd=response.json()

            except:
                continue

        if not success:
            path = 'image/'
            filelist = os.listdir(path)

            img = cv2.imread(path + filelist[0])
            fps = 5
            size = (img.shape[1], img.shape[0])

            video = cv2.VideoWriter(filename.split(
                ".")[0] + "_return.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

            for item in filelist:
                item = path + item
                img = cv2.imread(item)
                video.write(img)
                os.remove(item)

            video.release()
            cv2.destroyAllWindows()
            print('video is all read')
            break
    return result_crowd

def crowd_density_algorithm(width, height, person_number, person_in, person_out):
    actual_person_number=person_number+person_in-person_out
    density=actual_person_number/10*100
    return density