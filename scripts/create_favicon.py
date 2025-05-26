from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import os

def create_favicon():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Read the HTML content
        with open('static/images/favicon.html', 'r') as file:
            html_content = file.read()
        
        # Create a temporary HTML file with proper canvas dimensions
        temp_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generate Favicon</title>
        </head>
        <body>
            <canvas id="canvas" width="32" height="32"></canvas>
            <script>
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                
                // Draw background
                ctx.fillStyle = '#007bff';
                ctx.fillRect(0, 0, 32, 32);
                
                // Draw 'T' letter
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 20px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('T', 16, 16);
                
                // Convert canvas to PNG
                const dataURL = canvas.toDataURL('image/png');
                document.body.innerHTML = '<img id="img" src="' + dataURL + '"/>';
            </script>
        </body>
        </html>
        """
        
        # Write to temporary file
        with open('static/images/temp.html', 'w') as file:
            file.write(temp_html)
        
        # Load the HTML in Chrome
        driver.get('file://' + os.path.abspath('static/images/temp.html'))
        
        # Wait for the image to be rendered
        driver.implicitly_wait(2)
        
        # Get the image element
        img = driver.find_element('id', 'img')
        
        # Get the image data
        img_data = img.screenshot_as_png
        
        # Convert to PIL image
        image = Image.open(io.BytesIO(img_data))
        
        # Save as ICO
        image.save('static/images/favicon.ico', format='ICO', sizes=[(32,32)])
        
        print("Favicon created successfully!")
        
    finally:
        # Clean up
        driver.quit()
        if os.path.exists('static/images/temp.html'):
            os.remove('static/images/temp.html')

if __name__ == "__main__":
    create_favicon()
