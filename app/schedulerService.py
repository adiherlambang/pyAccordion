from time import sleep
from threading import Thread
from app.mailService import gmailServices
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .ciscoEndpoint import cisco_api
from flask import jsonify
from .dashboardService import dashboard
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

NO_DATA = []

class SchedulerService:

    def __init__(self, parent_app):
        self.app = parent_app
        self.scheduler = BackgroundScheduler()
        self.counter = 0
        self.retry_limit = 2
        self.retry_sleep_time = 5

    def get_data(self):
        cisco_api_instance = cisco_api(self.app)
        data_dashboard = dashboard(self.app)
        retry_counter = 0

        while retry_counter < self.retry_limit:
            req_data = cisco_api_instance.dashboard()
            status_code = req_data.get('status')

            if status_code == 200:
                value_dashboard = data_dashboard.main(req_data)
                return value_dashboard

            elif status_code in {401, 403, 500}:
                self.app.logger.error(f"Error {status_code}")
                self.app.logger.info(f"{retry_counter + 1} time, retrying for {self.retry_sleep_time} seconds....")
                sleep(self.retry_sleep_time)
                cisco_api_instance.getToken()
                retry_counter += 1

            else:
                self.app.logger.error(f"Unknown Error {status_code}")
                return jsonify(NO_DATA)

        self.app.logger.error("Maximum retries reached.")
        return jsonify(NO_DATA)

    def background_task(self):
        trigger = CronTrigger(hour=8, minute=0)
        self.scheduler.add_job(
            self.send_email_task,
            trigger=trigger,
            id='daily_email_task'
        )
        self.scheduler.start()
    
    def generate_pdf(self,data_dict,output_file_path):
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        
        element=[]
        # Add content to the PDF
        content = []
        styles = getSampleStyleSheet()
        header_content1 = f"MSAnalytics Apps"
        paragraph1 = Paragraph(header_content1,styles['Heading1'])
        element.append(paragraph1)
        header_content2 = f"You have {len(data_dict['6MonthfromNow'])} contracts expiring in less than 6 months"
        paragraph2 = Paragraph(header_content2,styles['Normal'])
        element.append(paragraph2)

        element.append(Spacer(1, 12))
        
        # Set up table headers
        table_headers = ["No","Contract Number", "Day Left", "Contract End Date"]
        content.append(table_headers)

        key_dict = ["contractNumber", "dayLeft", "contractEndDate"]
        # Add table rows
        # self.app.logger.info(data_dict['6MonthfromNow'])
        for idx, record in enumerate(data_dict['6MonthfromNow'], start=1):
            if isinstance(record, dict):
                row_data = [idx]
                for key in key_dict:
                    if key == "contractEndDate":
                        date_part = record.get(key, '').split("T")[0]
                        row_data.append(date_part)
                    else:
                        row_data.append(record.get(key, ''))
                content.append(row_data)
                # self.app.logger.info(f"Row data: {row_data}")
            else:
                self.app.logger.warning(f"Unexpected data format: {record}")

        # Create the table
        table = Table(content)
        style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
        table.setStyle(style)
        element.append(table)
        # Build the PDF
        pdf.build(element)
        # Write the contents of the buffer to a file
        
        with open(output_file_path, 'wb') as output_file:            
            output_file.write(buffer.getvalue())
        buffer.seek(0)
        
        return buffer

    def send_email_task(self):
        self.app.logger.info(f"Preparing to send data")
        data_dict = self.get_data()
        
        if not data_dict:
            self.app.logger.warning("No data to send in email.")
            return
        
        output_file_path = './app/out/contract_info.pdf'
        pdf_buffer = self.generate_pdf(data_dict, output_file_path)
        
        email_body = f"""
        <html>
        <body>
            <h4>### Please do not, reply this message ###</h4>
            <p>You have {len(data_dict['6MonthfromNow'])} contract had to expired less then 6 month</p>
            <p>Please found details in the attachment</p>
            <br>
            <p>Best Regards,</p>
            <p>MSAnalytics Application</p>
            <h4>### Please do not, reply this message ###</h4>
        </body>
        </html>
        """
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                if self.counter < 1:
                    self.app.logger.info(f"Task execution email services counter: #{self.counter}")
                    gmailServices.send_email_with_attachment(
                        app=self.app,
                        to=['meilinie@mastersystem.co.id','cinthiya@mastersystem.co.id'],
                        cc=['septian.adi@mastersystem.co.id'],
                        subject="AUTOMATIC EMAIL - MSAnalytics",
                        attachment_data=pdf_buffer,
                        attachment_filename=output_file_path,
                        message_text=email_body
                    )
                self.counter += 1
                break
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    self.app.logging.warning(f"Retrying ({retry_count}/{max_retries}) after a short delay...")
                    sleep(5)  # Add a short delay before retrying
        if retry_count == max_retries:
            self.app.logging.error(f"Failed to send email after {max_retries} retries")

    def main(self):
        try:
            self.app.logger.info('Starting background task email services...')
            daemon = Thread(target=self.background_task, daemon=True, name='Background')
            daemon.start()
        except Exception as error:
            self.app.logger.error(error)
