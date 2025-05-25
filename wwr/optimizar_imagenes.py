from PIL import Image
import os

def resize_and_compress(input_path, output_path, target_kb=100, max_width=900, quality=85):
    img = Image.open(input_path)

    # Redimensionar si la imagen es más ancha que max_width
    if img.width > max_width:
        wpercent = (max_width / float(img.width))
        hsize = int((float(img.height) * float(wpercent)))
        img = img.resize((max_width, hsize), Image.Resampling.LANCZOS)
    
    img.save(output_path, optimize=True, quality=quality)

    # Ajustar calidad para llegar al peso objetivo (100 KB)
    while os.path.getsize(output_path) > target_kb * 1024 and quality > 10:
        quality -= 5
        img.save(output_path, optimize=True, quality=quality)
        print(f"Reduciendo calidad a {quality}%. Tamaño actual: {os.path.getsize(output_path)//1024} KB")

    print(f"Imagen guardada: {output_path} | Tamaño final: {os.path.getsize(output_path)//1024} KB | Calidad: {quality}%")

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"Procesando {filename}...")
            resize_and_compress(input_path, output_path)

if __name__ == "__main__":
    input_folder = "images"        # Carpeta con imágenes originales
    output_folder = "images_small" # Carpeta para guardar imágenes optimizadas
    process_images(input_folder, output_folder)
