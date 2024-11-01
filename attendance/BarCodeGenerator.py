import barcode
from barcode.writer import ImageWriter

def generate_barcode(item_id):
    # Generate EAN13 barcode with ImageWriter for image generation
    ean13_barcode = barcode.get('ean13', item_id, writer=ImageWriter())
    
    # Save barcode image
    filename = f"{item_id}"
    ean13_barcode.save(filename)
    
    return f"{filename}.png"

# Example usage
item_id = input("Enter the item ID (12 digits): ")
img = generate_barcode(item_id)
print(f"Barcode saved as {img}")
