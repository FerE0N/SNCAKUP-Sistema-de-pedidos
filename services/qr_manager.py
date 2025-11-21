import qrcode
import os
import time

class QRCodeManager:
    """
    Singleton Pattern (Creational).
    Manages QR code generation and cleanup.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QRCodeManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.qr_directory = "static/qrcodes"
        if not os.path.exists(self.qr_directory):
            os.makedirs(self.qr_directory)

    def generate_qr(self, data: str, filename: str) -> str:
        """Generates a QR code and saves it to the static directory."""
        qr_img = qrcode.make(data)
        path = os.path.join(self.qr_directory, filename)
        qr_img.save(path)
        return filename

    def cleanup_expired_qrs(self, max_age_seconds: int = 3600):
        """Removes QR codes older than max_age_seconds."""
        now = time.time()
        if not os.path.exists(self.qr_directory):
            return
            
        for filename in os.listdir(self.qr_directory):
            path = os.path.join(self.qr_directory, filename)
            if os.path.isfile(path):
                file_age = now - os.path.getmtime(path)
                if file_age > max_age_seconds:
                    try:
                        os.remove(path)
                        print(f"[QRCodeManager] Removed expired QR: {filename}")
                    except OSError as e:
                        print(f"[QRCodeManager] Error removing {filename}: {e}")
