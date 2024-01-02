from PIL import Image

def encrypt_string(input_string, letter_mapping, number_mapping):
    encrypted_string = ''
    for char in input_string:
        if char.isalpha():
            encrypted_string += letter_mapping.get(char, char)
        elif char.isdigit():
            encrypted_string += number_mapping.get(char, char)
        else:
            encrypted_string += char
    return encrypted_string

def read_r_values_until_black(image_filename):
    try:
      
        image = Image.open(image_filename)
        image = image.convert("RGB")
        pixels = image.load()

        r_values = []

        for y in range(image.height):
            for x in range(image.width):
                r, g, b = pixels[x, y]
                r_values.append(r)

                if r == 0 and g == 0 and b == 0:
                   
                    image.close()
                    return r_values

    
        image.close()
        return r_values

    except FileNotFoundError:
        print("The file does not exist.")

def modify_image_with_ascii_data(image_filename, data_filename, output_filename, letter_mapping, number_mapping):
    try:
        with open(data_filename, "r") as file:
            data = file.read()
            
            personalInfoASCII = []

            ascii_values = [ord(char) for char in encrypt_string(data, letter_mapping, number_mapping)]
            personalInfoASCII.extend(ascii_values)

            # Open the image you want to modify
            image = Image.open(image_filename)
            image = image.convert("RGB")
            pixels = image.load()

            for i, ascii_value in enumerate(personalInfoASCII):
                x = i % image.width
                y = i // image.width
                pixels[x, y] = (ascii_value, ascii_value, ascii_value)

            extra_pixel_x = len(personalInfoASCII) % image.width
            extra_pixel_y = len(personalInfoASCII) // image.width
            pixels[extra_pixel_x, extra_pixel_y] = (0, 0, 0)

            
            image.save(output_filename)

        
            image.close()

    except FileNotFoundError:
        print("The file does not exist.")


def decrypt_r_values(r_values, letter_mapping, number_mapping):
    decrypted_characters = [chr(r) for r in r_values]

    decrypted_string = ''.join(decrypted_characters)
    decrypted_text = encrypt_string(decrypted_string, letter_mapping, number_mapping)
    return decrypted_text

alphabet = 'abcdefghijklmnopqrstuvwxyz'
keyForAlphabet = 'lwfbtnxotipqurhzsmgdycaejv'
numbers = '0123456789'
keyForNumbers = '3719042865'

modify_image_with_ascii_data("image.png", "data.txt", "modified_image.png", dict(zip(alphabet, keyForAlphabet)), dict(zip(numbers, keyForNumbers)))

r_values = read_r_values_until_black("modified_image.png")
print("R values until (0, 0, 0):", r_values)

decrypted_text = decrypt_r_values(r_values, dict(zip(keyForAlphabet, alphabet)), dict(zip(keyForNumbers, numbers)))
print("Decrypted Text:", decrypted_text)

