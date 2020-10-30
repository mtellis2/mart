import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw

# Get data for your city of choice
places = ["Greensboro, North Carolina, USA"]
G = ox.graph_from_place(places, network_type="all", simplify=True)

u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)
# Give color based on length
roadColors = []
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            color = "1.0"
        elif item["length"] > 100 and item["length"] <= 200:
            color = "0.9"
        elif item["length"] > 200 and item["length"] <= 400:
            color = "0.6"
        elif item["length"] > 400 and item["length"] <= 800:
            color = "0.3"
        else:
            color = "0.15"
    roadColors.append(color)

# create the Map
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    dpi=300,
    bgcolor="#FFFFFF",
    save=False,
    edge_color=roadColors,
    edge_alpha=1,
)

# Text and marker size
markersize = 16
fontsize = 16

fig.savefig(
    "Greensboro.png",
    dpi=300,
    bbox_inches="tight",
    format="png",
    facecolor=fig.get_facecolor(),
    transparent=True,
)

# Adding Border to Map
in_img = "Greensboro.png"

# Output Image
add_border(in_img, output_image="Greensboro.png", fill="#000000", bottom=400)

# Adding City text to map
img = Image.open("Greensboro.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/Users/michaelellis/Downloads/pmingliu/PMINGLIU.ttf", 100)

# Add the font to the border
# May need to adjust the position currently (180, 1475),
# and the font size currently (105, 105, 105) to fit the border
draw.text((180, 1475), "GREENSBORO, NORTH CAROLINA", (105, 105, 105), font=font)

img.save("Greensboro.png")

def _color(color, mode):
    color = ImageColor.getcolor(color, mode)
    return color

def expand(image, fill="#000000", bottom=50, left=None, right=None, top=None):
    """
    Expands image
    :param image: The image to be expanded.
    :param bottom, left, right, top: Border width, in pixels.
    :param fill: Pixel fill value, a hex color value like #e0474c.
    :return: An image.
    """

    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0

    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out_image = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out_image.paste(image, (left, top))
    return out_image

def add_border(
    input_image,
    output_image,
    fill= "#000000",
    bottom= 50,
    left= None,
    right= None,
    top= None,
):
    """
    Adds border to image and saves it.
    :param input_image: String for the image to be loaded.
    :param output_image: String for the image to be exported.
    :param fill: Hex color code for the border.
    :param bottom, left, right, top: Integer object specifying the border with in pixels.
    """
    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0

    img = Image.open(input_image)
    border_image = expand(img, bottom=bottom, left=left, right=right, top=top, fill=fill)
    border_image.save(output_image)