import click
import osmnx as ox
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw


@click.command()
@click.option(
    "--border-color",
    default="#000000",
    type=str,
    help="Hex color of the border.",
)
@click.argument("city_state")
def map_art(
    border_color,
    city_state,
):
    """Map Artwork command

    Args:
        city_state (str): US city in `City, State` format
    """
    # Get data for your city of choice
    location = f"{city_state}, USA"
    G = ox.graph_from_place([location], network_type="all", simplify=True)

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
    road_colors = []
    color = "1.0"
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
        road_colors.append(color)

    # create the Map
    fig, _ = ox.plot_graph(
        G,
        node_size=0,
        dpi=300,
        bgcolor="#FFFFFF",
        save=False,
        edge_color=road_colors,
        edge_alpha=1,
    )

    # TODO needed?
    # # Text and marker size
    # markersize = 16
    # fontsize = 16

    img_name = f"{city_state.split(',')[0]}.png"

    fig.savefig(
        f"../output/{img_name}",
        dpi=300,
        bbox_inches="tight",
        format="png",
        facecolor=fig.get_facecolor(),
        transparent=True,
    )

    # Adding Border to Map
    # Output Image
    _add_border(img_name, output_image=img_name, fill=border_color, bottom=400)

    # Adding City text to map
    img = Image.open(
        f"../output/{img_name}",
    )
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("../font/pmingliu/PMINGLIU.ttf", 100)

    # Add the font to the border
    # May need to adjust the position currently (180, 1475),
    # and the font size currently (105, 105, 105) to fit the border
    draw.text((180, 1475), city_state.upper(), (105, 105, 105), font=font)

    img.save(img_name)


def _color(color, mode):
    color = ImageColor.getcolor(color, mode)
    return color


def _expand(image, fill="#000000", bottom=50, left=0, right=0, top=0):
    """Expands map image

    Args:
        image (PIL Image): The image object to be expanded.
        fill (str, optional): Pixel fill value, a hex color value like #e0474c. Defaults to "#000000".
        bottom (int, optional): Border width, in pixels. Defaults to 50.
        left (int, optional): Border width, in pixels. Defaults to 0.
        right (int, optional): Border width, in pixels. Defaults to 0.
        top (int, optional): Border width, in pixels. Defaults to 0.

    Returns:
        Image: PIL Image object of the map
    """
    # if left == None:
    #     left = 0
    # if right == None:
    #     right = 0
    # if top == None:
    #     top = 0

    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out_image = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out_image.paste(image, (left, top))
    return out_image


def _add_border(
    input_image,
    output_image,
    fill="#000000",
    bottom=50,
    left=None,
    right=None,
    top=None,
):
    """Adds border to image and saves it.

    Args:
        input_image (str): Image to be loaded.
        output_image (str): Image to be exported.
        fill (str, optional): Hex color code for the border. Defaults to "#000000".
        bottom (int, optional): Integer object specifying the border with in pixels. Defaults to 50.
        left (int, optional): Integer object specifying the border with in pixels. Defaults to None.
        right (int, optional): Integer object specifying the border with in pixels. Defaults to None.
        top (int, optional): Integer object specifying the border with in pixels. Defaults to None.
    """
    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0

    img = Image.open(f"../output/{input_image}")
    border_image = _expand(
        img, bottom=bottom, left=left, right=right, top=top, fill=fill
    )
    border_image.save(f"../output/{output_image}")
