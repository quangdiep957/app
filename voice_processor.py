import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
import tempfile
import threading
import time

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.listen_thread = None
        print("VoiceProcessor đã được khởi tạo")
        
    def speak(self, text):
        try:
            print(f"Đang chuyển đổi văn bản thành giọng nói: {text}")
            tts = gTTS(text=text, lang='vi')
            
            # Tạo file tạm thời với đường dẫn đầy đủ
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, 'temp_audio.mp3')
            print(f"Lưu file âm thanh tại: {temp_file}")
            
            tts.save(temp_file)
            print("Đã lưu file âm thanh thành công")
            
            playsound(temp_file)
            print("Đã phát âm thanh thành công")
            
            # Xóa file tạm sau khi phát
            try:
                os.remove(temp_file)
                print("Đã xóa file tạm")
            except Exception as e:
                print(f"Lỗi khi xóa file tạm: {e}")
                
        except Exception as e:
            print(f"Lỗi trong phương thức speak: {str(e)}")
            raise
            
    def listen(self, callback):
        try:
            with sr.Microphone() as source:
                print("Đang điều chỉnh môi trường...")
                self.recognizer.adjust_for_ambient_noise(source)
                print("Đã điều chỉnh môi trường")
                
                while self.is_listening:
                    try:
                        print("Đang lắng nghe...")
                        audio = self.recognizer.listen(source, timeout=5)
                        print("Đã ghi âm xong")
                        
                        try:
                            text = self.recognizer.recognize_google(audio, language='vi-VN')
                            print(f"Đã nhận dạng: {text}")
                            callback(text)
                        except sr.UnknownValueError:
                            print("Không thể nhận dạng giọng nói")
                        except sr.RequestError as e:
                            print(f"Lỗi khi gọi Google Speech Recognition: {e}")
                            
                    except sr.WaitTimeoutError:
                        continue
                        
        except Exception as e:
            print(f"Lỗi trong phương thức listen: {str(e)}")
            self.is_listening = False
            raise
            
    def start_listening(self, callback):
        if not self.is_listening:
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self.listen, args=(callback,))
            self.listen_thread.start()
            print("Đã bắt đầu lắng nghe")

    def stop_listening(self):
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join()
        print("Đã dừng lắng nghe")

    def process_command(self, text):
        try:
            text = text.lower()
            print(f"Đang xử lý lệnh: {text}")
            
            if text in ['xin chào', 'chào']:
                self.speak("Xin chào! Tôi là trợ lý AI của máy bán nước ép. Tôi có thể giúp gì cho bạn?")
            elif text in ['menu', 'thực đơn']:
                self.speak("Chúng tôi có các loại nước ép sau: Nước ép cam giá 15.000đ, Nước ép táo giá 20.000đ, Nước ép dưa hấu giá 25.000đ, Nước ép xoài giá 30.000đ")
            elif 'nước ép cam' in text:
                self.speak("Bạn đã chọn nước ép cam giá 15.000đ. Vui lòng thanh toán và nhận nước ép.")
            elif 'nước ép táo' in text:
                self.speak("Bạn đã chọn nước ép táo giá 20.000đ. Vui lòng thanh toán và nhận nước ép.")
            elif 'nước ép dưa hấu' in text:
                self.speak("Bạn đã chọn nước ép dưa hấu giá 25.000đ. Vui lòng thanh toán và nhận nước ép.")
            elif 'nước ép xoài' in text:
                self.speak("Bạn đã chọn nước ép xoài giá 30.000đ. Vui lòng thanh toán và nhận nước ép.")
            elif text in ['cảm ơn']:
                self.speak("Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!")
            elif text in ['tạm biệt']:
                self.speak("Tạm biệt! Hẹn gặp lại bạn!")
            else:
                self.speak("Xin lỗi, tôi không hiểu lệnh của bạn. Bạn có thể nói 'menu' để xem danh sách nước ép.")
        except Exception as e:
            print(f"Lỗi trong phương thức process_command: {str(e)}")
            self.speak("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.") 