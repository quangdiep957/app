import cv2
import mediapipe as mp
import numpy as np
from transformers import pipeline
import pyttsx3
import time

class AIAssistant:
    def __init__(self):
        # Khởi tạo MediaPipe cho nhận diện khuôn mặt và cử chỉ
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        # Khởi tạo text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Khởi tạo model phân tích cảm xúc
        self.emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        
        # Khởi tạo model đối thoại
        self.chatbot = pipeline("text-generation", model="gpt2")
        
        # Trạng thái tương tác
        self.last_interaction_time = 0
        self.customer_emotion = "neutral"
        self.conversation_history = []
        
    def detect_face(self, frame):
        """Phát hiện khuôn mặt trong frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        return results.detections if results.detections else None
    
    def detect_gestures(self, frame):
        """Phát hiện cử chỉ tay"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks if results.multi_hand_landmarks else None
    
    def analyze_emotion(self, text):
        """Phân tích cảm xúc từ văn bản"""
        result = self.emotion_analyzer(text)[0]
        return result['label']
    
    def generate_response(self, user_input):
        """Tạo phản hồi dựa trên đầu vào của người dùng"""
        response = self.chatbot(user_input, max_length=50, num_return_sequences=1)[0]['generated_text']
        return response
    
    def speak(self, text):
        """Phát âm thanh thông báo"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def process_frame(self, frame):
        """Xử lý frame và tương tác với khách hàng"""
        current_time = time.time()
        
        # Phát hiện khuôn mặt
        faces = self.detect_face(frame)
        if faces:
            # Có khách hàng
            if current_time - self.last_interaction_time > 5:  # Chờ 5 giây giữa các lần tương tác
                self.speak("Xin chào! Chào mừng bạn đến với hệ thống bán nước ép tự động!")
                self.last_interaction_time = current_time
        
        # Phát hiện cử chỉ
        gestures = self.detect_gestures(frame)
        if gestures:
            # Xử lý cử chỉ tay
            for hand_landmarks in gestures:
                # Phát hiện cử chỉ chọn sản phẩm
                if self._is_pointing_up(hand_landmarks):
                    self.speak("Bạn muốn chọn sản phẩm nào?")
        
        return frame
    
    def _is_pointing_up(self, hand_landmarks):
        """Kiểm tra xem ngón tay có đang chỉ lên không"""
        # Lấy tọa độ của các điểm mốc trên ngón tay
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        # Kiểm tra nếu ngón trỏ cao hơn ngón cái
        return index_tip.y < thumb_tip.y
    
    def get_recommendations(self, customer_emotion):
        """Đề xuất sản phẩm dựa trên cảm xúc của khách hàng"""
        recommendations = {
            "joy": "Tôi thấy bạn đang rất vui! Bạn có muốn thử nước ép cam tươi không?",
            "sadness": "Tôi thấy bạn hơi buồn. Nước ép dưa hấu có thể giúp bạn cảm thấy tốt hơn!",
            "anger": "Bạn có vẻ hơi căng thẳng. Nước ép táo có thể giúp bạn thư giãn.",
            "neutral": "Bạn muốn thử loại nước ép nào? Chúng tôi có cam, táo và dưa hấu.",
        }
        return recommendations.get(customer_emotion, recommendations["neutral"]) 