from PIL import Image
import os

max_width = 800
max_size_kb = 100
min_quality = 30
quality_step = 5

input_folder = 'images'
output_folder = 'images_optimized'

def resize_image(img):
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        return img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return img

def save_jpeg_with_size_limit(img, output_path):
    quality = 85
    while quality >= min_quality:
        img.save(output_path, optimize=True, quality=quality)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= max_size_kb:
            return size_kb, quality
        quality -= quality_step
    # Si no alcanza el tamaño con calidad mínima, redimensionar más y guardar
    width = img.width
    while size_kb > max_size_kb and width > 200:
        width = int(width * 0.9)
        ratio = width / img.width
        height = int(img.height * ratio)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(output_path, optimize=True, quality=min_quality)
        size_kb = os.path.getsize(output_path) / 1024
    return size_kb, min_quality

def save_png_with_size_limit(img, output_path):
    # Solo redimensionamos si es muy grande y comprimimos al máximo
    img = resize_image(img)
    img.save(output_path, optimize=True, compress_level=9)
    size_kb = os.path.getsize(output_path) / 1024
    return size_kb

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            with Image.open(input_path) as img:
                img = resize_image(img)
                ext = filename.lower().split('.')[-1]
                if ext in ['jpg', 'jpeg']:
                    size_kb, quality = save_jpeg_with_size_limit(img, output_path)
                    print(f"JPEG {filename}: {size_kb:.1f} KB, calidad={quality}")
                elif ext == 'png':
                    size_kb = save_png_with_size_limit(img, output_path)
                    print(f"PNG {filename}: {size_kb:.1f} KB")
                else:
                    img.save(output_path)
                    size_kb = os.path.getsize(output_path) / 1024
                    print(f"Otro formato {filename}: {size_kb:.1f} KB")

if __name__ == '__main__':
    process_images(input_folder, output_folder)
