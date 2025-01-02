# Fashion Understander - Shopbop Sweater Analysis System

A comprehensive AI-powered system for analyzing fashion trends and patterns from Shopbop's sweater collection. This system combines web scraping, image analysis using OpenAI's Vision API, and pattern recognition to provide detailed insights into fashion trends.

## System Overview

This system consists of three main components:
1. **Web Scraper**: Collects sweater images from Shopbop's website
2. **Image Analyzer**: Uses OpenAI's Vision API to analyze design details of each sweater
3. **Pattern Analyzer**: Identifies common style combinations and trends across the collection

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Google Chrome browser (latest version)
- Git (for cloning the repository)
- A text editor (VS Code recommended)
- An OpenAI API key (paid account required)

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

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage Guide

### 1. Downloading Images
The `download_images.py` script scrapes sweater images from Shopbop:

```bash
python download_images.py
```

This will:
- Create a `shopbop_images` directory
- Download images from the first 5 pages of Shopbop's sweater section
- Save images with descriptive filenames

**Note**: The script includes random delays to be respectful to Shopbop's servers.

### 2. Analyzing Images
The `image_to_tags.py` script analyzes each downloaded image:

```bash
python image_to_tags.py
```

This will:
- Process each image in `shopbop_images`
- Generate detailed design analysis using OpenAI's Vision API
- Save results in `shopbop_analysis.json`

The analysis includes:
- Color analysis
- Design details
- Style elements
- Visual impact assessment

### 3. Identifying Patterns
The `analyze_tags.py` script identifies trends and patterns:

```bash
python analyze_tags.py
```

This generates:
- A markdown report with identified patterns
- Visual examples for each trend
- Price point analysis
- Common style combinations

## Output Files

1. `shopbop_images/`: Directory containing downloaded sweater images
2. `shopbop_analysis.json`: Raw analysis data for each image
3. `shopbop_style_patterns_[timestamp].md`: Final trend analysis report

## Logging and Monitoring

- All scripts include detailed logging
- Logs are saved in `image_analysis.log`
- Console output shows progress and any errors

## Troubleshooting

Common issues and solutions:

1. **Chrome Driver Issues**:
   - Ensure Chrome browser is up to date
   - Try clearing Chrome's cache
   - Check if antivirus is blocking the driver

2. **API Rate Limits**:
   - The system includes built-in delays
   - Monitor your OpenAI API usage
   - Adjust delays if needed in the code

3. **Image Download Failures**:
   - Check your internet connection
   - Verify Shopbop's website is accessible
   - Try running the script again for failed downloads

## Best Practices

1. **Rate Limiting**:
   - Don't modify the built-in delays
   - Be respectful of Shopbop's servers
   - Monitor your API usage

2. **Data Management**:
   - Regularly backup your analysis results
   - Clean up old images if not needed
   - Keep your API key secure

3. **System Resources**:
   - Close other Chrome instances before running
   - Ensure sufficient disk space for images
   - Monitor memory usage during analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the Vision API
- Shopbop for the source material
- Selenium and BeautifulSoup4 for web scraping capabilities