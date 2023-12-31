from flask import Flask, render_template,flash,get_flashed_messages,send_file, request,jsonify, send_from_directory
from .routes import bp
from .logging import configure_logger
from datetime import datetime
from dotenv import load_dotenv
from app.schedulerService import SchedulerService
import os,sys,signal,platform

current_date = datetime.now().strftime('%Y-%m-%d')
app = Flask(__name__,static_folder='static', template_folder='templates')

app.register_blueprint(bp)

configure_logger(app)

load_dotenv()

service = SchedulerService(app)
service.main()

app.logger.info(f"{app} pyAccordion is running , DateTime: {datetime.now()}")

# Signal handler for SIGHUP
def handle_sighup(signum, frame):
    app.logger.info("Received SIGHUP signal. Restarting the application...")
    restart_program()

 # Function to restart the application
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
if platform.system() != 'Windows':
    signal.signal(signal.SIGHUP, handle_sighup)
else:
    app.logger.info("SIGHUP signal not supported on Windows. Signal handling not set up.")

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
