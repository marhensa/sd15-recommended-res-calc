import os

"""
    
This is the standalone python script, 
for ComfyUI custom node it's on other file: customnode_sd15_recommended_res_calc.py
    
A simple tool to calculate the recommended initial latent size 
for SD 1.5 image generation and its Upscale Factor 
based on the desired Final Resolution output 
    
Marhensa Aditya Hadi (2023)
    
"""

def calculate_aspect_ratios(desiredXSIZE, desiredYSIZE):
    
# Horizontal aspect ratio
    accepted_ratios_horizontal = {
    "4:1": (1536, 384, 4.000000000),
    "31:8": (1488, 384, 3.875000000),
    "15:4": (1440, 384, 3.750000000),
    "29:8": (1392, 384, 3.625000000),
    "28:9": (1344, 432, 3.111111111),
    "3:1": (1296, 432, 3.000000000),
    "26:9": (1248, 432, 2.888888889),
    "5:2": (1200, 480, 2.500000000),
    "12:5": (1152, 480, 2.400000000),
    "23:11": (1104, 528, 2.090909091),
    "2:1": (1056, 528, 2.000000000),
    "21:11": (1008, 528, 1.909090909),
    "7:4": (1008, 576, 1.750000000),
    "5:3": (960, 576, 1.666666667),
    "19:13": (912, 624, 1.461538462),
    "18:13": (864, 624, 1.384615385),
    "9:7": (864, 672, 1.285714286),
    "17:14": (816, 672, 1.214285714),
    "17:15": (816, 720, 1.133333333),
    "16:15": (768, 720, 1.066666667)
    }

# Vertical aspect ratio
    accepted_ratios_vertical = {
    "15:16": (720, 768, 0.937500000),
    "15:17": (720, 816, 0.882352941),
    "14:17": (672, 816, 0.823529412),
    "7:9": (672, 864, 0.777777778),
    "13:18": (624, 864, 0.722222222),
    "13:19": (624, 912, 0.684210526),
    "3:5": (576, 960, 0.600000000),
    "4:7": (576, 1008, 0.571428571),
    "11:21": (528, 1008, 0.523809524),
    "1:2": (528, 1056, 0.500000000),
    "11:23": (528, 1104, 0.478260870),
    "5:12": (480, 1152, 0.416666667),
    "2:5": (480, 1200, 0.400000000),
    "9:26": (432, 1248, 0.346153846),
    "1:3": (432, 1296, 0.333333333),
    "9:28": (432, 1344, 0.321428571),
    "8:29": (384, 1392, 0.275862069),
    "4:15": (384, 1440, 0.266666667),
    "8:31": (384, 1488, 0.258064516),
    "1:4": (384, 1536, 0.250000000)
    }
    
# Square aspect ratio
    accepted_ratios_square = {
    "1:1": (768, 768, 1.00000000)
    }

    
    # Calculate the aspect ratio of the desired size
    desired_ratio = desiredXSIZE / desiredYSIZE
    
    # Find the closest accepted aspect ratio
    closest_ratio = None
    closest_diff = float('inf')
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_horizontal.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_vertical.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    # Compare with square aspect ratio
    x_size, y_size, num_ratio = accepted_ratios_square["1:1"]
    diff = abs(num_ratio - desired_ratio)
    if diff < closest_diff:
        closest_ratio = "1:1"
   
   # ANSI escape sequences for text colors
    colorGREEN = "\033[32m"
    colorRESET = "\033[0m"

    # Display the accepted aspect ratio
    print("=====")
    print("")
    print("Nearest SD 1.5 recommended ratio from", colorGREEN + str(desiredXSIZE) + colorRESET, "x", colorGREEN + str(desiredYSIZE) + colorRESET, ":")
    if closest_ratio in accepted_ratios_horizontal:
        print(colorGREEN + "HORIZONTAL", colorRESET)
    elif closest_ratio in accepted_ratios_vertical:
        print(colorGREEN + "VERTICAL", colorRESET)
    else:
        print(colorGREEN + "SQUARE", colorRESET)
    print(colorGREEN + closest_ratio, colorRESET)
    
    # Display the corresponding accepted XSIZE and YSIZE
    if closest_ratio in accepted_ratios_horizontal:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_horizontal[closest_ratio]
    elif closest_ratio in accepted_ratios_vertical:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_vertical[closest_ratio]
    else:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_square[closest_ratio]
    print("\nRecommended initial SD 1.5 size for", closest_ratio, ":")
    print(colorGREEN + "SD 1.5 Width  :", accepted_XSIZE, colorRESET)
    print(colorGREEN + "SD 1.5 Height :", accepted_YSIZE, colorRESET)
    
    # Calculate the upscale factor for width and height
    upscale_factor_width = desiredXSIZE / accepted_XSIZE
    upscale_factor_height = desiredYSIZE / accepted_YSIZE

    # Compare the upscale factors for width and height and select the larger one
    if upscale_factor_width >= upscale_factor_height:
        more_less = "SD 1.5 Width"
        accepted_size = accepted_XSIZE
        desired_size = desiredXSIZE
        excesstocrop = "Final Height"
        scaling_factor = round(upscale_factor_width, 9)
    else:
        more_less = "SD 1.5 Height"
        accepted_size = accepted_YSIZE
        desired_size = desiredYSIZE
        excesstocrop = "Final Width"
        scaling_factor = round(upscale_factor_height, 9)
    
    print("\nScaling factor to reach", desiredXSIZE, "x", desiredYSIZE)
    print("calculated from (", more_less, ") to avoid shortage,")
    print("you can crop (", excesstocrop, ") excess later")
    print(colorGREEN + "Scale factor :", scaling_factor, colorRESET)

    # Calculate the downscale factor from Upscale 4x Node and round to 9 digits
    downscalefrom2x_factor = round(scaling_factor / 4, 9)
    
    print("\nReverse Upscale Factor after using 4x-Upscaler Node = (", scaling_factor, "/ 4 )")
    print(colorGREEN + "Reverse Upscale Factor for 4x-Upscaler :", downscalefrom2x_factor, colorRESET)
    
    # Calculate the downscale factor from Upscale 2x Node and round to 9 digits
    downscalefrom4x_factor = round(scaling_factor / 2, 9)
    
    print("\nReverse Upscale Factor after using 2x-Upscaler Node = (", scaling_factor, "/ 2 )")
    print(colorGREEN + "Reverse Upscale Factor for 2x-Upscaler :", downscalefrom4x_factor, colorRESET)
    print("")
    print("=====")

# Function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to get user input and ask for another set of sizes
def get_user_input():
    while True:
        clear_screen()  # Clear the terminal screen
        desiredXSIZE = int(input("\nEnter the Desired Final Width (X Size): "))
        desiredYSIZE = int(input("Enter the Desired Final Height (Y Size): "))

        # Call the function to calculate the aspect ratios and scaling factor
        calculate_aspect_ratios(desiredXSIZE, desiredYSIZE)

        another_input = input("Do you want to input another set of sizes? (Y/N): ")
        if another_input.lower() != 'y':
            break

# Start the script by getting user input for the first set of sizes
get_user_input()
