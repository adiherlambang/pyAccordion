from flask import Flask, render_template,flash,get_flashed_messages,send_file, request,jsonify, send_from_directory
from .routes import bp
from .logging import configure_logger
from datetime import datetime
from dotenv import load_dotenv
from app.schedulerService import schedulerService

current_date = datetime.now().strftime('%Y-%m-%d')
app = Flask(__name__,static_folder='static', template_folder='templates')

app.register_blueprint(bp)

configure_logger(app)

load_dotenv()

service = schedulerService(app)
service.main()

app.logger.info(f"{app} pyAccordion is running")

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
