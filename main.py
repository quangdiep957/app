import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, Response
import pyttsx3
from PIL import Image
import os
from dotenv import load_dotenv

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo text-to-speech engine
engine = pyttsx3.init()

class JuiceVendingSystem:
    def __init__(self):
        self.camera = None
        self.model = None
        self.juice_inventory = {
            'cam': 10,
            'tao': 10,
            'dua hau': 10
        }
        self.prices = {
            'cam': 15000,
            'tao': 20000,
            'dua hau': 25000
        }
        
    def initialize_camera(self):
        """Khởi tạo camera"""
        self.camera = cv2.VideoCapture(0)
        
    def initialize_model(self):
        """Khởi tạo model AI"""
        # TODO: Load model nhận diện khuôn mặt và cử chỉ
        pass
        
    def detect_customer(self):
        """Phát hiện khách hàng"""
        if self.camera is None:
            self.initialize_camera()
            
        ret, frame = self.camera.read()
        if ret:
            # TODO: Xử lý ảnh để phát hiện khách hàng
            return True
        return False
        
    def process_order(self, juice_type):
        """Xử lý đơn hàng"""
        if juice_type in self.juice_inventory and self.juice_inventory[juice_type] > 0:
            self.juice_inventory[juice_type] -= 1
            return True, self.prices[juice_type]
        return False, 0
        
    def speak(self, text):
        """Phát âm thanh thông báo"""
        engine.say(text)
        engine.runAndWait()

# Khởi tạo hệ thống
vending_system = JuiceVendingSystem()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        if vending_system.detect_customer():
            vending_system.speak("Xin chào! Chào mừng bạn đến với hệ thống bán nước ép tự động!")
        ret, frame = vending_system.camera.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    vending_system.initialize_camera()
    vending_system.initialize_model()
    app.run(debug=True)
