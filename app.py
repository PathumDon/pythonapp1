# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# # Use the PORT environment variable if available, otherwise use default
# port = int(os.environ.get("PORT", 5000))

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=port)

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import qrcode
import os
import time

app = Flask(__name__)

# Ensure static/qr_codes directory exists
os.makedirs('static/qr_codes', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    text = request.form['text']
    timestamp = int(time.time())  # Use a timestamp to avoid filename conflicts
    filename = f'qr_{timestamp}.png'
    filepath = os.path.join('static', 'qr_codes', filename)

    # Generate QR Code
    qr_img = qrcode.make(text)
    qr_img.save(filepath)

    qr_code_url = url_for('static', filename=f'qr_codes/{filename}')
    return render_template('result.html', qr_code_url=qr_code_url)

@app.route('/static/qr_codes/<filename>')
def download_qr(filename):
    return send_from_directory('static/qr_codes', filename)

if __name__ == '__main__':
    app.run(debug=True)
