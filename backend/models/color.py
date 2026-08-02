# ==============================================================================
#
# 256 color combinations
# ------------------------
# 38 = Foreground mode
# 2  = True Color (RGB) mode
# 255;0;255 = Your Magenta values
#
# print("\033[38;2;255;0;255mThis text is Magenta!\033[0m")
#
# ==============================================================================
#
# Old school 16 colors
# --------------------
# 033   - Escape, stop print text normal and start formating
# [     - Control sequence start
# n     - Predefined colors range from 30-37 & 90-97 so, 16 colors in total
# m     - Set the color
#
# ==============================================================================
#
# 256 Color palette: 0-255 predefined colors
# ------------------------------------------
# 033   - Escape, stop the print text normal and start formating
# [     - Control sequence start
# 38/48 - foreground/background color
# n     - Color number from 0-255
# m     - Set the color
#
# Print all ID number in its own color (0, 256)
# ---------------------------------------------
# for i in range(256):
#      print(f"\033[38;5;{i}m{i:3}", end=" ")
#      if (i + 1) % 16 == 0:
#          print() # New line every 16 colors
# ==============================================================================


# COLORS
class Color:
    bold = "\033[01m"
    underline = "\033[4m"
    crossed = "\033[9m"
    blink = "\033[5m"
    grey = "\033[90m"
    red = "\033[31m"
    green = "\033[32m"
    olive = "\033[33m"
    orange = "\033[38;5;208m" # this RGB value is for orange
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    yellow = "\033[93m"
    pink = "\033[95m"
    lightGrey = "\033[37m"
    lightRed = "\033[91m"
    lightGreen = "\033[92m"
    lightBlue = "\033[94m"
    lightCyan = "\033[96m"
    reset = "\033[0m"