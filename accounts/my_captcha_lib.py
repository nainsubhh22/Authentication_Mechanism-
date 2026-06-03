import random
import os
from PIL import Image, ImageDraw, ImageFont

class CustomCaptchaEngine:
    def __init__(self):
        pass

    def _get_font(self, size):
        font_paths = [
            r"C:\Windows\Fonts\arialbd.ttf", 
            r"C:\Windows\Fonts\arial.ttf",    
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
            "/System/Library/Fonts/Helvetica.ttc" 
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def _create_base_image(self, text_to_draw):
        img = Image.new('RGB', (260, 80), color=(15, 23, 42))  
        d = ImageDraw.Draw(img)
        
        for i in range(0, 260, 26):
            d.line([(i, 0), (i, 80)], fill=(30, 41, 59), width=1)
        for j in range(0, 80, 20):
            d.line([(0, j), (260, j)], fill=(30, 41, 59), width=1)

        font = self._get_font(32)
        
        try:
            text_width = d.textlength(text_to_draw, font=font)
            text_height = 32 
        except AttributeError:
            text_width, text_height = d.textsize(text_to_draw, font=font) if hasattr(d, 'textsize') else (140, 30)

        x_start = (260 - text_width) / 2
        y_start = (80 - text_height) / 2

        current_x = x_start
        for char in text_to_draw:
            wobble_y = y_start + random.randint(-3, 3)
            d.text((current_x, wobble_y), char, fill=(129, 140, 248), font=font)
            
            try:
                current_x += d.textlength(char, font=font) + 4
            except AttributeError:
                current_x += 22 

        return img

    def generate_numeric(self):
        number = str(random.randint(10000, 99999))
        img = self._create_base_image(number) 
        return img, number

    def generate_math(self):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        challenge_text = f"{num1} + {num2}"
        correct_ans = str(num1 + num2)
        
        img = self._create_base_image(challenge_text)
        return img, correct_ans

    def generate_inverse(self):
        words = ["DJANGO", "PYTHON", "CAPTCHA", "SECURE", "HUMAN", "CODING"]
        chosen_word = random.choice(words)
        correct_ans = chosen_word[::-1]
        
        img = self._create_base_image(chosen_word) 
        return img, correct_ans