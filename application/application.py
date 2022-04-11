from flask import Flask, Response, redirect, make_response
from src.metrics import get_ec2_metrics
import pyexcel as pe
from io import StringIO

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Home Page (Return X-Private-IP in Header)
@application.route('/')
def home():
    resp = Response("Home")
    resp.headers['X-Private-IP'] = 'MY.EC2.PRIVATE.IP'
    return resp

# Health Check
@application.route('/health')
def health():
    return Response("Healthy")

# Metrics
@application.route('/metrics')
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
@application.route('/<any>')
def default(any):
    return redirect('/')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()