from flask import Blueprint, render_template, jsonify, send_file,request
from flask import current_app as app
from .ciscoEndpoint import cisco_api
from .mailService import gmailServices 
from .dashboardService import dashboard
import time 

bp = Blueprint('main', __name__)
ccwrAPI = cisco_api()
dataDashboard = dashboard()
noData = []

@bp.route('/', methods=['GET']) ## Home Page
def app_home():
    if request.method == 'GET':
        data = "Welcome to PyAccordion"
        app.logger.info("Render Home Page")
        return render_template("index.html",data = data)

@bp.route('/contractSummary') ## Contract Summary Search Page 
def contractSummary():
    app.logger.info("Render contract summary page")
    return render_template("contract_summary.html")

@bp.route('/itemSummary') ## Contract Summary by item Search Page 
def contractSummarybyItem():
    app.logger.info("Render Search by Item Page")
    return render_template("item_summary.html")

@bp.route('/mailService') ## Home Page
def mailService():
    app.logger.info("Render mail service Page")
    return render_template("email_service.html")

@bp.route('/sendMail', methods=['POST']) ## Home Page
def sendMail():
    if request.method == 'POST':
        requestData = request.get_json()
        app.logger.info("Send an email initiate")
        mailService = gmailServices.main(app,to=requestData['emailRecipient'],subject=requestData['emailSubject'],message_text=requestData['mailMessage'])
        return mailService


@bp.route('/SearchContractSummary', methods=['POST'])
def SearchContractSummary():
    retry_counter = 0
    if request.method == 'POST':
        requestData = request.get_json()
        while True:
            app.logger.info("Request Search Contact Summary initiate")
            resData = ccwrAPI.contractSummary(requestData)
            status_code = resData.get('status')

            if status_code == 200:
                finalData = editContractSummary(resData)
                return jsonify(finalData)
            
            elif status_code == 401 or status_code == 403:
                app.logger.error(f"Error {status_code}")
                ccwrAPI.getToken()
            
            elif status_code == 500:
                if retry_counter < 2:
                    app.logger.error(f"Error {status_code}")
                    app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    time.sleep(5)  # Wait for 5 seconds before retrying the request
                    retry_counter += 1
                else:
                    app.logger.error("Maximum retries reached.")
                    return jsonify(noData)

            else:
                app.logger.error(f"Unknown Error {status_code}")
                return jsonify(noData)        

def editContractSummary(resData):
    modifiedData=[]
    count = 1
    for item in resData['data']['contracts']:
                if item.get('endCustomers') and len(item['endCustomers']) > 0:
                    for endCustomer in item['endCustomers']:
                        modifiedData.append({                       
                            'count':count,   
                            'id': endCustomer['id'],
                            'name': endCustomer['name'],
                            'contractNumber': item['contractNumber'],
                            'contractEndDate': item['contractEndDate'],
                            'contractStatus': item['contractStatus'],
                            'listPrice': item['listPrice'],
                            'currency': item['currency']
                        })
                        count+=1
                else:
                    modifiedData.append({
                        'count':count,
                        'id': 'N/A',
                        'name': 'N/A',
                        'contractNumber': item['contractNumber'],
                        'contractEndDate': item['contractEndDate'],
                        'contractStatus': item['contractStatus'],
                        'listPrice': item['listPrice'],
                        'currency': item['currency']
                    })
                    count+=1
                
    return modifiedData

@bp.route('/SearchByItem', methods=['POST'])
def SearchByItem():
    retry_counter = 0
    if request.method == 'POST':
        requestData = request.get_json()

        while True:
            resData = ccwrAPI.searchByItem(requestData)
            status_code = resData.get('status')
            app.logger.info(f"Get response Status from search item endPoint cisco: {status_code}")

            if status_code == 200:
                finalData = editItemSearchData(resData)
                app.logger.info("Request Search by Item initiate")
                return jsonify(finalData)
            
            elif status_code == 401 or status_code == 403:
                if retry_counter < 2:
                    app.logger.error(f"Error {status_code}")
                    app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    time.sleep(5)
                    ccwrAPI.getToken()
                    retry_counter += 1
                else:
                    app.logger.error("Maximum retries reached.")
                    return jsonify(noData)
                
            elif status_code == 500:
                if retry_counter < 2:
                    app.logger.error(f"Error {status_code}")
                    app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    time.sleep(5)  # Wait for 5 seconds before retrying the request
                    retry_counter += 1
                else:
                    app.logger.error("Maximum retries reached.")
                    return jsonify(noData)

            else:
                app.logger.error(f"Unknown Error {status_code}")
                return jsonify(noData)        
            
def editItemSearchData(resData):
    modifiedData = []

    for count, item in enumerate(resData['data']['instances'], 1):
        address2_value = item['endCustomer']['address'].get('address2', '')
        serialNumber_value = item.get('serialNumber', '-')
        lastDateSupport = item.get('lastDateOfSupport', '-')
        serviceSKU_value = item.get('serviceSKU', '-')
        modifiedData.append({
                'count': count,
                'contractNumbers': item['contract']['number'],
                'customerID': item['endCustomer']['id'],
                'customerName': item['endCustomer']['name'],
                'customerAddress': item['endCustomer']['address']['address1'] + "\n" + address2_value + "," +
                                item['endCustomer']['address']['city'] + "," +
                                item['endCustomer']['address']['postalCode'],
                'product': item['product']['number'],
                'description': item['product']['description'],
                'productGroup': item['product']['group'],
                'serialNumber': serialNumber_value,
                'serviceSKU': serviceSKU_value,
                'contractStatus': item['contract']['lineStatus'],
                'billTo': item['contract']['billToGlobalUltimate']['name'],
                'salesOrder': item['salesOrderNumber'],
                'purchaseOrder': item['purchaseOrderNumber'],
                'ldod': lastDateSupport,
                'MsalesOrder': item['maintenanceSalesOrderNumber'],
                'MpurchaseOrder': item['maintenancePurchaseOrderNumber'],
                'startDateContract': item['startDate'],
                'endDateContract': item['endDate'],
                'warrantyType': item['warranty']['type'],
                'warrantyStatus': item['warranty']['status'],
                'warrantyEndDate': item['warranty']['endDate']
            })

    return modifiedData

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    retry_counter = 0
    if request.method == 'GET':
        while True:
            app.logger.info("Request Contact Summary for Dashboard initiate")
            resData = ccwrAPI.dashboard()
            status_code = resData.get('status')

            if status_code == 200:
                valueDashboard = dataDashboard.main(resData)
                return jsonify(valueDashboard)
            
            elif status_code == 401 or status_code == 403:
                if retry_counter < 2:
                    app.logger.error(f"Error {status_code}")
                    app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    time.sleep(5)
                    ccwrAPI.getToken()
                    retry_counter += 1
                else:
                    app.logger.error("Maximum retries reached.")
                    return jsonify(noData)
            
            elif status_code == 500:
                if retry_counter < 2:
                    app.logger.error(f"Error {status_code}")
                    app.logger.info(f"{retry_counter} time, retrying for 5 seconds....")
                    time.sleep(5)  # Wait for 5 seconds before retrying the request
                    retry_counter += 1
                else:
                    app.logger.error("Maximum retries reached.")
                    return jsonify(noData)

            else:
                app.logger.error(f"Unknown Error {status_code}")
                return jsonify(noData)