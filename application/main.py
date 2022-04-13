from flask import Flask, Response, redirect, make_response
from src.metrics import get_ec2_metrics
import pyexcel as pe
from io import StringIO
from flask_cors import CORS
import os

# EB looks for an 'app' callable by default.
app = Flask(__name__)
CORS(app)

# Home Page (Return X-Private-IP in Header)
@app.route('/')
def home():
    resp = Response("Home")

    # Get the private IP (from hostname)
    hostname = os.system("hostname") # hostname: ip-10-0-0-0
    ec2_private_ip = '.'.join(hostname.split('-')[1:]) # ip: 10.0.0.0

    # Add to header
    resp.headers['X-Private-IP'] = ec2_private_ip
    return resp

# Health Check
@app.route('/health')
def health():
    return Response("Healthy")

# Metrics
@app.route('/metrics')
def metrics():

    # Get EC2 Metrics
    data = get_ec2_metrics()

    # Create Response
    sheet = pe.Sheet(data)
    io = StringIO()
    sheet.save_to_memory("csv", io)
    output = make_response(io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=metrics.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# Redirect to Home Page
@app.route('/<any>')
def default(any):
    return redirect('/')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()