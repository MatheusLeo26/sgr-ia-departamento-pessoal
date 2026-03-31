from PIL import Image
import os

def convert_png_to_ico():
    base_dir = r"C:\Users\SrgRH\.gemini\antigravity\scratch\sgr-ia"
    png_path = os.path.join(base_dir, "app", "assets", "robot_report_icon.png")
    ico_path = os.path.join(base_dir, "app", "assets", "robot_report_icon.ico")
    
    if os.path.exists(png_path):
        img = Image.open(png_path)
        # Standard icon sizes
        img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"Convertido: {ico_path}")
    else:
        print("Erro: PNG não encontrado.")

if __name__ == "__main__":
    convert_png_to_ico()
