import requests
from io import BytesIO
from PIL import Image
import streamlit as st
from utils.pixabay_api import get_rural_india_image, get_placeholder_image_url

def get_color_scale(scale_name):
    """
    Return color scales for visualizations
    
    Args:
        scale_name (str): Name of the color scale
        
    Returns:
        list: Color scale values
    """
    color_scales = {
        "india_flag": ["#FFFFFF", "#FF9933", "#138808"],  # White, Saffron, Green
        "saffron_green": ["#FF9933", "#138808"],          # Saffron, Green
        "blue_white": ["#000080", "#FFFFFF"]              # Navy Blue, White
    }
    
    return color_scales.get(scale_name, ["#FFFFFF", "#000080"])

@st.cache_data(ttl=3600, show_spinner=False)
def load_image_from_url(url, category=None):
    """
    Load image from URL or fetch from Pixabay if URL is a category keyword
    
    Args:
        url (str): Image URL or category keyword
        category (str, optional): Image category for Pixabay API. Defaults to None.
        
    Returns:
        PIL.Image: Image object
    """
    # If URL starts with 'https://', it's an actual URL, otherwise treat as a category
    if url.startswith('https://'):
        image_url = url
    else:
        # Use the provided category or the URL as a category
        img_category = category if category else url
        # Get image URL from Pixabay API
        image_url = get_rural_india_image(img_category)
        
        # If no image found, use placeholder
        if not image_url:
            image_url = get_placeholder_image_url(img_category)
    
    # Attempt to load the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Open image from response content
        image = Image.open(BytesIO(response.content))
        return image
    
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        
        # If loading fails, try to use placeholder
        try:
            fallback_url = get_placeholder_image_url(category if category else "connectivity")
            response = requests.get(fallback_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return image
        except:
            # If all fails, create a plain colored image as ultimate fallback
            fallback_image = Image.new('RGB', (800, 400), color=(255, 153, 51))  # Saffron color
            return fallback_image
