import os
from pathlib import Path
import json
from openai import OpenAI
import base64
import shutil
import logging
from datetime import datetime
import time
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# OpenAI API configuration
client = OpenAI()

def encode_image(image_path):
    """Encode image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            logger.debug("Successfully encoded image: %s", image_path)
            return encoded
    except Exception as e:
        logger.error("Failed to encode image %s: %s", image_path, str(e))
        raise

def analyze_image(image_path, category="sweaters", product_metadata=None):
    """Analyze image using OpenAI's Vision model with focus on design details, styles, and colors."""
    start_time = time.time()
    logger.info("Starting analysis of image: %s (Category: %s)", image_path, category)
    
    try:
        base64_image = encode_image(image_path)
        
        # Updated JSON template prioritizing design and style elements
        json_template = '''{
  "design": {
    "silhouette": {
      "primary_style": ["Fitted", "Oversized", "Relaxed", "Slim", "Boxy", "Cropped"],
      "shape_details": ["A-line", "Straight", "Trapeze", "Cocoon", "Hourglass"],
      "key_proportions": ["Cropped", "Hip-length", "Tunic", "Oversized", "Fitted"],
      "design_era": ["Contemporary", "Vintage-inspired", "Modern", "Classic", "Avant-garde"]
    },
    "color_analysis": {
      "primary_color": {
        "name": ["Black", "Navy", "Cream", "Grey", "Camel", "White", "Red", "Other"],
        "tone": ["Warm", "Cool", "Neutral"],
        "intensity": ["Vibrant", "Muted", "Pastel", "Deep", "Light"],
        "finish": ["Matte", "Heathered", "Marled", "Space-dyed"]
      },
      "color_combinations": {
        "scheme": ["Solid", "Two-tone", "Multi-color", "Ombré", "Color-blocked"],
        "contrast_level": ["High", "Medium", "Low", "Tonal"],
        "color_harmony": ["Monochromatic", "Complementary", "Analogous", "Triadic"]
      },
      "pattern_colors": {
        "background": ["Light", "Dark", "Medium", "Multi"],
        "accent_colors": ["Contrast", "Tonal", "Multi-colored", "None"],
        "color_distribution": ["Even", "Dominated", "Gradient", "Random"]
      },
      "seasonal_palette": ["Spring", "Summer", "Fall", "Winter", "Year-round"]
    },
    "knit_patterns": {
      "primary_pattern": ["Cable knit", "Ribbed", "Fair Isle", "Argyle", "Intarsia", "Plain stitch"],
      "texture_elements": ["Chunky cables", "Fine ribs", "Honeycomb", "Popcorn", "Lattice"],
      "pattern_placement": ["All-over", "Front panel", "Yoke", "Sleeves", "Hem"],
      "pattern_complexity": ["Simple", "Moderate", "Complex", "Multi-technique"],
      "pattern_scale": ["Fine", "Medium", "Large", "Mixed"],
      "pattern_rhythm": ["Regular", "Irregular", "Graduated", "Random"]
    },
    "style_details": {
      "neckline": {
        "style": ["Crew", "V-neck", "Turtleneck", "Mock neck", "Boat neck", "Cowl"],
        "design_features": ["Ribbed", "Folded", "Split", "Contrast", "Decorative"],
        "depth": ["High", "Medium", "Low", "Plunging"],
        "width": ["Narrow", "Standard", "Wide"]
      },
      "sleeves": {
        "style": ["Raglan", "Set-in", "Drop shoulder", "Dolman", "Bishop", "Bell"],
        "design_elements": ["Ribbed cuff", "Balloon", "Fitted", "Wide", "Statement"],
        "length": ["Full", "Three-quarter", "Short", "Cap", "Sleeveless"],
        "cuff_detail": ["Plain", "Ribbed", "Decorative", "Contrast", "Split"]
      },
      "hem_design": {
        "style": ["Ribbed", "Split", "Curved", "Straight", "Asymmetric"],
        "details": ["Side slits", "High-low", "Banded", "Raw edge", "Decorative"],
        "length": ["Cropped", "Standard", "Extended", "Variable"],
        "finish": ["Clean", "Distressed", "Decorative", "Contrast"]
      }
    },
    "decorative_elements": {
      "trims": ["Contrast edges", "Metallic details", "Buttons", "Zippers", "None"],
      "embellishments": ["Embroidery", "Beading", "Appliqué", "Sequins", "None"],
      "special_techniques": ["Color blocking", "Mixed stitch", "Openwork", "Fringe", "None"],
      "hardware": {
        "type": ["Buttons", "Zippers", "Toggles", "Snaps", "None"],
        "finish": ["Metal", "Plastic", "Wood", "Horn", "Covered"],
        "placement": ["Front", "Shoulder", "Cuff", "None"]
      }
    }
  },
  "style_classification": {
    "aesthetic": {
      "primary": ["Minimalist", "Bohemian", "Preppy", "Avant-garde", "Classic"],
      "secondary": ["Romantic", "Sporty", "Artisanal", "Contemporary", "Vintage"],
      "design_influences": ["Scandinavian", "French", "American", "Japanese", "Italian"]
    },
    "trend_alignment": {
      "current_trends": ["On-trend", "Classic", "Forward", "Timeless"],
      "trend_longevity": ["Seasonal", "Multi-season", "Timeless", "Trend-focused"],
      "design_innovation": ["Traditional", "Contemporary", "Experimental", "Hybrid"]
    }
  },
  "visual_impact": {
    "dominant_features": ["Color", "Pattern", "Texture", "Silhouette", "Details"],
    "visual_weight": ["Light", "Medium", "Heavy"],
    "texture_appearance": ["Smooth", "Textured", "Mixed", "Dimensional"],
    "pattern_impact": ["Subtle", "Moderate", "Bold", "Statement"],
    "overall_contrast": ["High", "Medium", "Low", "Variable"]
  }
}'''

        # Updated analysis prompt focusing on design and style
        analysis_prompt = """As a luxury knitwear design expert, provide an extremely detailed analysis of this sweater/knit item, focusing on design elements, color, and style characteristics.

Key areas to analyze:

1. Color Analysis:
   - Identify precise colors and their relationships
   - Analyze color combinations and harmony
   - Evaluate color application techniques
   - Note any special color effects or treatments

2. Design Details:
   - Identify all distinctive design elements and patterns
   - Analyze special knit techniques and their placement
   - Note unique or innovative design features
   - Evaluate pattern complexity and execution

3. Style Elements:
   - Assess the overall silhouette and its impact
   - Identify key style influences and aesthetic category
   - Evaluate visual balance and proportions
   - Note any signature or distinctive style elements

4. Visual Impact:
   - Analyze the dominant design features
   - Evaluate pattern and texture relationships
   - Assess overall visual harmony
   - Note special visual effects or treatments

Provide your detailed design analysis in this exact JSON format:

{json_template}"""

        logger.info("Sending request to OpenAI API...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Correct model name
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": analysis_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500,
                temperature=0.5,
                response_format={ "type": "json_object" }
            )
            logger.info("Received response from OpenAI API")
            
            if hasattr(response.choices[0].message, 'content'):
                result = json.loads(response.choices[0].message.content)
                logger.info("Successfully parsed JSON response")
                return result
            
        except Exception as e:
            logger.error("Error in API request: %s", str(e))
            return None
            
    except Exception as e:
        logger.error("Error analyzing image %s: %s", image_path, str(e))
        return None

def analyze_shopbop_images():
    """Analyze all images in the shopbop_images directory."""
    try:
        # Setup paths
        images_dir = Path("shopbop_images")
        output_file = "shopbop_analysis.json"
        
        # Load existing analysis if any
        existing_analysis = {}
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_analysis = json.load(f)
        
        # Get list of image files
        image_files = list(images_dir.glob("*.jpg"))
        logger.info(f"Found {len(image_files)} images to analyze")
        
        # Process each image
        for image_path in tqdm(image_files, desc="Analyzing images"):
            image_key = str(image_path)
            
            # Skip if already analyzed
            if image_key in existing_analysis:
                logger.debug(f"Skipping already analyzed image: {image_key}")
                continue
            
            # Analyze image
            logger.info(f"Analyzing {image_path}")
            analysis = analyze_image(image_path)
            
            if analysis:
                # Store analysis with metadata
                existing_analysis[image_key] = {
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat(),
                    "filename": image_path.name
                }
                
                # Save after each successful analysis
                with open(output_file, 'w') as f:
                    json.dump(existing_analysis, f, indent=2)
                
                # Add delay to respect rate limits
                time.sleep(1)
            
        logger.info("Analysis complete")
        
    except Exception as e:
        logger.error(f"Error in analyze_shopbop_images: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info(f"Starting image analysis process at {datetime.now()}")
    logger.info("=" * 80)
    
    analyze_shopbop_images() 