import qrcode
import io
import base64

class QRCodeManager:
    """
    Singleton Pattern (Creational).
    Manages QR code generation.
    Refactored to be ephemeral (returns Base64 string).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QRCodeManager, cls).__new__(cls)
        return cls._instance

    def generate_qr_base64(self, data: str) -> str:
        """Generates a QR code and returns it as a Base64 string."""
        qr_img = qrcode.make(data)
        
        # Save to memory buffer
        buffered = io.BytesIO()
        qr_img.save(buffered, format="PNG")
        
        # Encode to Base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
