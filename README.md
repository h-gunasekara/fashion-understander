# Fashion Understander - Shopbop Sweater Analysis System

A comprehensive AI-powered system for analyzing fashion trends and patterns from Shopbop's sweater collection. This system combines web scraping, image analysis using OpenAI's Vision API, and pattern recognition to provide detailed insights into fashion trends.

## System Overview

This system consists of three main components:
1. **Web Scraper**: Collects sweater images from Shopbop's website
2. **Image Analyzer**: Uses OpenAI's Vision API to analyze design details of each sweater
3. **Pattern Analyzer**: Identifies common style combinations and trends across the collection

## Prerequisites

You need:
- Python 3.8 or higher
- Google Chrome browser
- OpenAI API key (paid account required)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fashion-understander.git
cd fashion-understander
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```
This will install all necessary packages including:
- openai: For AI image analysis
- python-dotenv: For environment variable management
- selenium & undetected-chromedriver: For web scraping
- beautifulsoup4: For HTML parsing
- requests: For downloading images
- tqdm: For progress bars

4. Set up your OpenAI API key:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage Guide

### 1. Downloading Images
Run the scraper:
```bash
python download_images.py
```

This will:
- Create a `shopbop_images` directory
- Download images from Shopbop's sweater section
- Save images with descriptive filenames

**Note**: The script includes delays to respect Shopbop's servers.

### 2. Analyzing Images
Run the analyzer:
```bash
python image_to_tags.py
```

This analyzes each image for:
- Color analysis
- Design details
- Style elements
- Visual impact

### 3. Identifying Patterns
Generate the trend report:
```bash
python analyze_tags.py
```

This creates:
- A markdown report with trends
- Visual examples
- Price analysis
- Style combinations

## Output Files

1. `shopbop_images/`: Downloaded sweater images
2. `shopbop_analysis.json`: Raw analysis data
3. `shopbop_style_patterns_[timestamp].md`: Trend report
4. `image_analysis.log`: Process logs

## Troubleshooting

1. **Chrome Driver Issues**:
   - Update Chrome to latest version
   - Clear Chrome's cache
   - Check antivirus settings

2. **API Rate Limits**:
   - Monitor OpenAI API usage
   - Adjust delays if needed

3. **Image Download Failures**:
   - Check internet connection
   - Verify Shopbop's accessibility
   - Retry failed downloads

## Best Practices

1. **Rate Limiting**:
   - Keep default delays
   - Monitor API usage

2. **Data Management**:
   - Backup analysis results
   - Clean old images
   - Secure API key

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- OpenAI for Vision API
- Shopbop for source material
- Selenium and BeautifulSoup4