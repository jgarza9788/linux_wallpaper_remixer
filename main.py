import os
from itertools import product
from playwright.sync_api import sync_playwright
from Config import Config
from io import StringIO
import logMan as lm

# this is the main DIR
DIR = os.path.dirname(os.path.realpath(__file__))

# global variables
CONFIG = None
LOGGER = None


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

