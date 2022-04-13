from flask import Flask, Response, redirect, make_response
from src.utils import prepare_metrics, get_private_ip
import pyexcel as pe
from io import StringIO
from flask_cors import CORS

# EB looks for an 'app' callable by default.
app = Flask(__name__)
CORS(app)

# Home Page (Return X-Private-IP in Header)
@app.route('/')
def home():
    resp = Response("Home")

    # Get Private IP
    private_ip = get_private_ip()['PrivateIP']
    resp = Response(f"Home: {private_ip}")

    # Add to header
    resp.headers['X-Private-IP'] = private_ip
    return resp

# Health Check
@app.route('/health')
def health():

    # Get Private IP
    private_ip = get_private_ip()['PrivateIP']
    resp = Response(f"Healthy: {private_ip}")

    return resp

# Metrics
@app.route('/metrics')
def metrics():

    # Get EC2 Metrics
    try:
        data = prepare_metrics()
    except Exception as e:
        print(e)
        error = f"Error getting metrics. Maybe the metrics csv is not created yet."
        resp = Response(error)
        return resp

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