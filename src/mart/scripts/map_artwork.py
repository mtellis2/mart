"""Command to create image using map data for a specific location.
"""
import logging
import os
import click
import osmnx as ox
from PIL import Image, ImageColor, ImageFont, ImageDraw
from typing import Tuple

LOGGER = logging.getLogger("mart")


@click.command()
@click.option(
    "--border-color",
    default="#000000",
    type=str,
    help="Hex color of the border.",
)
@click.option(
    "--font",
    default="PMINGLIU.ttf",
    type=str,
    help="Font file to use for text.",
)
@click.argument("city_state")
def map_art(
    border_color: str,
    font: str,
    city_state: str,
) -> None:
    """Map Artwork command

    Args:
        city_state (str): US city in `City, State` format
    """
    LOGGER.info(f"Pulling location data for `{city_state}`...")
    # Get data for your city of choice
    location = f"{city_state}, USA"
    location_graph = ox.graph_from_place([location], network_type="all", simplify=True)

    u = []
    v = []
    key = []
    data = []
    # edge -> (u,v,k,d)
    for uu, vv, kkey, ddata in location_graph.edges(keys=True, data=True):
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

    LOGGER.info("Creating map figure...")
    # create the Map
    fig, _ = ox.plot_graph(
        location_graph,
        node_size=0,
        dpi=300,
        bgcolor="#000000",
        save=False,
        edge_color=road_colors,
        edge_alpha=1,
    )

    img_name = f"{city_state.split(',')[0]}.png"
    image_output_path = os.path.join(os.getcwd(), "src/mart/output", img_name)

    LOGGER.info(f"Saving map figure `output/{img_name}`...")
    fig.savefig(
        image_output_path,
        dpi=300,
        bbox_inches="tight",
        format="png",
        facecolor=fig.get_facecolor(),
        transparent=True,
    )

    LOGGER.info("Adding border to map image...")
    # Adding Border to Map
    add_border(
        image_path=image_output_path,
        fill=border_color,
        bottom=400,
    )

    LOGGER.info("Adding location text to map image...")
    # Adding City text to map
    add_text(image_output_path, city_state.upper(), font, img_name)


def _color(hex_color: str, mode: str) -> Tuple:
    color = ImageColor.getcolor(hex_color, mode)
    return color


def expand_image(
    image: Image.Image,
    fill: str = "#000000",
    bottom: int = 50,
    left: int = 0,
    right: int = 0,
    top: int = 0,
) -> Image.Image:
    """Expands map image

    Args:
        image (PIL Image): The image object to be expanded.
        fill (str, optional): Pixel fill value, a hex color value like #e0474c.
            Defaults to "#000000".
        bottom (int, optional): Border width, in pixels. Defaults to 50.
        left (int, optional): Border width, in pixels. Defaults to 0.
        right (int, optional): Border width, in pixels. Defaults to 0.
        top (int, optional): Border width, in pixels. Defaults to 0.

    Returns:
        Image: PIL Image object of the map
    """
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out_image = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out_image.paste(image, (left, top))
    return out_image


def add_border(
    image_path: str,
    fill: str = "#000000",
    bottom: int = 50,
    left: int = 0,
    right: int = 0,
    top: int = 0,
) -> None:
    """Adds border to image and saves it.

    Args:
        image_path (str): Image to be loaded/exported.
        fill (str, optional): Hex color code for the border. Defaults to "#000000".
        bottom (int, optional): Integer object specifying the border with in pixels.
            Defaults to 50.
        left (int, optional): Integer object specifying the border with in pixels.
            Defaults to 0.
        right (int, optional): Integer object specifying the border with in pixels.
            Defaults to 0.
        top (int, optional): Integer object specifying the border with in pixels.
            Defaults to 0.
    """
    if left is None:
        left = 0
    if right is None:
        right = 0
    if top is None:
        top = 0

    img = Image.open(image_path)
    border_image = expand_image(
        img, bottom=bottom, left=left, right=right, top=top, fill=fill
    )
    border_image.save(image_path)


def add_text(image_path: str, text: str, font_file: str, file_name: str) -> None:
    """Adds location text to image.

    Args:
        input_image (str): Image to be loaded.
        text (str): Text to be added to image.
        font (str): Font file
        file_name (str): File name
    """
    img = Image.open(
        image_path,
    )
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        os.path.join(os.getcwd(), "src/mart/font", font_file), 100
    )

    image_width, image_height = img.size
    # text_width, text_height = font.getsize(text.upper())

    # Calculate text position
    # Add the font to the border
    # the font fill currently (105, 105, 105) to fit the border
    draw.text(
        (image_width / 2, image_height / 4 * 3.5),
        text.upper(),
        (105, 105, 105),
        font=font,
        anchor="mm",
    )

    LOGGER.info(f"Saving final map image to `output/{file_name}`")
    img.save(image_path)
