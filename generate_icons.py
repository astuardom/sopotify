"""
Script to generate PWA icons in multiple sizes from a base image
"""
from PIL import Image
import os

def generate_icons(base_image_path, output_dir):
    """Generate PWA icons in various sizes"""
    
    # Create icons directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Icon sizes needed for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Open the base image
    try:
        base_image = Image.open(base_image_path)
        print(f"✓ Loaded base image: {base_image_path}")
        print(f"  Original size: {base_image.size}")
        
        # Generate each size
        for size in sizes:
            # Resize image
            resized = base_image.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save the icon
            output_path = os.path.join(output_dir, f'icon-{size}x{size}.png')
            resized.save(output_path, 'PNG', optimize=True)
            print(f"✓ Generated: icon-{size}x{size}.png")
        
        print(f"\n✓ All icons generated successfully in: {output_dir}")
        
    except FileNotFoundError:
        print(f"✗ Error: Base image not found at {base_image_path}")
        print("\nPlease provide a base icon image (recommended 512x512 or larger)")
        print("You can:")
        print("1. Create an icon using the generated image")
        print("2. Place it in the static folder")
        print("3. Run this script again")
    except Exception as e:
        print(f"✗ Error generating icons: {e}")

if __name__ == "__main__":
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    
    # Try to find a base icon
    possible_base_images = [
        os.path.join(static_dir, 'icon-base.png'),
        os.path.join(static_dir, 'default_cover.png'),
    ]
    
    base_image = None
    for img_path in possible_base_images:
        if os.path.exists(img_path):
            base_image = img_path
            break
    
    if base_image:
        output_dir = os.path.join(static_dir, 'icons')
        generate_icons(base_image, output_dir)
    else:
        print("✗ No base image found. Please create 'static/icon-base.png'")
        print("\nYou can use the generated icon image from the artifacts.")
