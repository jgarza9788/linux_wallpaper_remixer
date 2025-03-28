import os
from itertools import product
from playwright.sync_api import sync_playwright
from Config import Config
from io import StringIO
import logMan as lm

# from PIL import Image, ImageFilter, ImageOps

# this is the main DIR
DIR = os.path.dirname(os.path.realpath(__file__))

# global variables
CONFIG = None
LOGGER = None

# def stylize_icon(
#     input_path,
#     output_path,
#     icon_color=(255, 0, 0, 255),   # Red
#     stroke_color=(0, 0, 0, 255),   # Black
#     stroke_width=4,
#     shadow_offset=(6, 6),
#     shadow_blur=8,
#     shadow_color=(0, 0, 0, 128)    # Semi-transparent black
# ):
#     # Load the image
#     img = Image.open(input_path).convert("RGBA")
    
#     # Create a mask from the alpha channel
#     alpha = img.getchannel("A")
    
#     # Recolor white parts of the image to the desired icon color
#     # (Assumes icon is white and background is transparent)
#     img_colored = Image.new("RGBA", img.size, icon_color)
#     img_colored.putalpha(alpha)

#     # Create stroke by expanding the mask and coloring it
#     stroke_mask = alpha.point(lambda p: 255 if p > 0 else 0)
#     stroke = ImageOps.expand(stroke_mask, border=stroke_width, fill=0)
#     stroke = stroke.filter(ImageFilter.GaussianBlur(1))
#     stroke_img = Image.new("RGBA", stroke.size, stroke_color)
#     stroke_img.putalpha(stroke)

#     # Create shadow
#     shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
#     shadow_mask = alpha.copy()
#     shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))
#     shadow_img = Image.new("RGBA", img.size, shadow_color)
#     shadow_img.putalpha(shadow_mask)

#     # Prepare final image
#     final_size = (
#         max(img.size[0] + shadow_offset[0] + stroke_width * 2, stroke.size[0]),
#         max(img.size[1] + shadow_offset[1] + stroke_width * 2, stroke.size[1])
#     )
#     final = Image.new("RGBA", final_size, (0, 0, 0, 0))

#     # Paste layers: shadow, stroke, icon
#     final.paste(shadow_img, shadow_offset, shadow_img)
#     final.paste(stroke_img, (0, 0), stroke_img)
#     final.paste(img_colored, (stroke_width, stroke_width), img_colored)

#     # Save result
#     final.save(output_path)


def CreateWallpapers():
    """
    The selected code within the CreateWallpapers function is responsible for generating wallpapers based on the provided presets. It iterates through each preset, creates a combination of logo, base color, color, and size, and then generates a wallpaper using the HTML template.
    """
    global LOGGER
    global CONFIG


    # print(template)

    if not os.path.exists(CONFIG.data['output']):
        os.makedirs(CONFIG.data['output'])


    for p in CONFIG.data['presets']:

        preset = list(product([p['name']],p['logos'],p['basecolors'],p['colors'],p['sizes']))

        print(preset)

        for z in preset:

            # stylize_icon(
            #     input_path=f"./logos/{z[1]}",
            #     output_path=f"./temp/logo.png",
            #     icon_color=(0, 150, 255, 255),  # Blue
            #     stroke_color=(255, 255, 255, 255),  # White stroke
            #     stroke_width=50,
            #     shadow_offset=(0, 100),
            #     shadow_blur=0,
            #     shadow_color=(0, 0, 0, 180)  # Darker shadow
            # )

            # return 0

            template = ''
            with open(CONFIG.data['template_path'], 'r', encoding='utf8') as f:
                template = f.read()
        
            template = template.replace('{%logo%}',z[1])
            template = template.replace('{%basecolor%}',z[2])
            template = template.replace('{%color%}',z[3])

            temp_file = os.path.join(DIR,'temp','temp.html')
            print(temp_file)
            with open(temp_file,'w',encoding='utf8') as f:
                f.write(template)

            outfile = os.path.join(DIR,CONFIG.data['output'],f'{z[0]}_{z[1].split(".")[0]}_{z[2]}_{z[3]}_{z[4][0]}x{z[4][1]}.png')

            if os.path.exists(outfile) == False:
                html_to_png(temp_file,outfile,width=z[4][0],height=z[4][1])
                        

def html_to_png(html_file, output_file, width=1920, height=1080):
    html_path = f"file://{os.path.abspath(html_file)}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set viewport size
        page.set_viewport_size({"width": width, "height": height})

        # Load the local HTML file
        page.goto(html_path, wait_until="networkidle")

        # Take a screenshot
        page.screenshot(path=output_file, full_page=True)

        # Close the browser
        browser.close()
    
    print(f"✅ {output_file}")

if __name__ == '__main__':
    # set logger
    LOGGER = lm.createLogger(
        root=os.path.join(DIR,'log'),
        useStreamHandler=True,
        strIO=StringIO(),
    )

    #get config
    CONFIG = Config()

    # create wallpapers
    CreateWallpapers()

