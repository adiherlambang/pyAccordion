from time import sleep
from threading import Thread
from app.mailService import gmailServices
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .dashboardService import dashboard
from .ciscoEndpoint import cisco_api
from flask import jsonify,json

class schedulerService:

    def __init__(self,parentApp):
      self.app = parentApp
      self.scheduler = BackgroundScheduler()
      self.counter = 0

    def getData(self):
        noData=[]
        ccwrAPI = cisco_api()
        dataDashboard = dashboard()
        while True:
            self.app.logger.info("Request Contact Summary for email initiate")
            resData = ccwrAPI.dashboard()
            status_code = resData.get('status')
            
            if status_code == 200:
                getDataContract = dataDashboard.main(resData)
                return jsonify(getDataContract)
            
            elif status_code == 401 or status_code == 403:
                if retry_counter < 2:
                    # self.app.logger.error(f"Error {status_code}")
                    # self.app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    sleep(5)
                    ccwrAPI.getToken()
                    retry_counter += 1
                else:
                    # self.app.logger.error("Maximum retries reached.")
                    return jsonify(noData)
            
            elif status_code == 500:
                if retry_counter < 2:
                    # self.app.logger.error(f"Error {status_code}")
                    # self.app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    self.time.sleep(5)  # Wait for 5 seconds before retrying the request
                    retry_counter += 1
                else:
                    # self.app.logger.error("Maximum retries reached.")
                    return jsonify(noData)

            else:
                # self.app.logger.error(f"Unknown Error {status_code}")
                return jsonify(noData)
            
    def background_task(self):
        # Schedule the task to run every day at 08:00 AM
        trigger = CronTrigger(hour=4, minute=35)
        self.scheduler.add_job(
            self.send_email_task,
            trigger=trigger,
            id='daily_email_task'
        )
        self.scheduler.start()

    # task that runs at a fixed interval
    def send_email_task(self):
        
        data_array = json.loads(self.getData())
        
        table_rows = ""
        for record in data_array:
            table_rows += f"""
                <tr>
                    <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{record.get('contractNumber', '')}</td>
                    <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{record.get('dayLeft', '')}</td>
                    <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{record.get('contractEndDate', '')}</td>
                </tr>
            """
            
        email_body = f"""
        <html>
        <body>
            <h2>Your Table in an Email</h2>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Contract Number</th>
                        <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Day Left</th>
                        <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Contract End Date</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </body>
        </html>
        """
        # run forever
        if self.counter <1:
            self.app.logger.info(f"Task execution email services counter: #{self.counter}")
            gmailServices.main(self.app,
                               to="septian.adi@mastersystem.co.id",
                               cc="kadek.sena@mastersystem.co.id",
                               subject="AUTOMATIC EMAIL",
                               message_text=email_body)
            self.counter+=1

    def main(self):
        # create and start the daemon thread
        try:
            self.app.logger.info('Starting background task email services...')          
            daemon = Thread(target=self.background_task, daemon=True, name='Background')
            daemon.start()
            # sleep(60)
        except Exception as error:
            self.app.logger.info(error)