# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

from PIL import Image

icon = Image.open('../icon.png')
icon.save('JSONly/resources/icon.icns', format='ICNS')
