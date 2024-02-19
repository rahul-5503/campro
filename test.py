from flask import Flask, Response, render_template, jsonify,json,request
import cv2
import scapy.all as scapy
import os,time
import threading
from testingio import publicip,get_ip_addresses
from connect import conn_check,find_camera_ip,find_status

app = Flask(__name__)

# Dictionary to store camera objects based on MAC addresses
cameras = {}



def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)# frame_rate=10

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in the HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(1 / frame_rate)
        #24:b1:05:72:7c:4e
        
# to get a data from form input
@app.route('/submit', methods=['POST'])
def submit():
    user = request.form.get('name')
    password = request.form.get('password')
    cameratype = request.form.get('cameratype')
    macaddress = request.form.get('macaddress')

    if not user or not password:
        return jsonify({'error': 'User and password are required.'}), 400
    #set a data in json formate
    data = {
        "user": user,
        "password": password,
        "cameratype": cameratype,
        "macaddress": macaddress
    }

    file_path = 'user_data.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
        
        existing_data.append(data)

        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
    else:
        with open(file_path, 'w') as json_file:
            json.dump([data], json_file, indent=4)

    return jsonify({'message': 'Data submitted successfully.'}), 200

def find_uap(mac):
      with open('user_data.json') as file:
        data = json.load(file)
        for obj in data:
            if obj.get('macaddress') == mac:
                return obj
    # If MAC address not found, return a message
      return 'not found' 

@app.route('/check/<mac_address>')
def check(mac_address):
    ip_check =find_camera_ip(mac_address)
    return jsonify({'status': 'connected' if ip_check else 'disconnected'})

@app.route('/video_feed/<mac_address>')
def video_feed(mac_address):
    
    ip_address = find_camera_ip(mac_address)
    userapass=find_uap(mac_address)#return the below data from user_data.json file
    if userapass != 'not found':
            username =userapass['user']
            password =userapass['password']
            cameratype = userapass['cameratype']
            print("username",username)
            #return username
            #return cameratype
            #return jsonify({'message':'data reterived successful'})
    else:
          return jsonify({'message': 'Data reterived failed.'})
    if ip_address:
        rtsp_urls = [
          #0/28:18:fd:95:58:6c/admin/admin123       cpplus  
         f'rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/0',
         #1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
         f'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0'
        ]
        rtsp_stream_url =rtsp_urls[int(cameratype)]
        return Response(generate_frames(rtsp_stream_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return jsonify({'message': 'camera reterived failed.'})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    t1=threading.Thread(target=publicip)
    t2=threading.Thread(target=conn_check)
    t1.start()
    t2.start()
    #conn_check()
  #  publicip()
    app.run(host='0.0.0.0', port=8034, debug=True)
    
