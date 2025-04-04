# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# This Python file converts the PNG icon to Windows ICO format\
# pillow needs to be installed in order to run

from PIL import Image

logo = Image.open("..\\icon.png")
logo.save("icon.ico", format='ICO')
