import base64
from io import BytesIO
from .my_captcha_lib import CustomCaptchaEngine # Note the dot before my_captcha_lib

def get_captcha_data(challenge_type="1"):
    engine = CustomCaptchaEngine()
    
    if challenge_type == "2":
        img, correct_ans = engine.generate_math()
    elif challenge_type == "3":
        img, correct_ans = engine.generate_inverse()
    else:
        img, correct_ans = engine.generate_numeric()
        
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_b64, correct_ans