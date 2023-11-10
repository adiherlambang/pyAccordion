import requests
from flask import current_app as app
import os


class cisco_api:

    def __init__(self):
        self.clientID = os.environ.get('ccwr_client_id')
        self.clientSecret = os.environ.get('ccwr_client_secret')
        self.responseData = {
            'status':{},
            'data':{}
        }

    def getToken(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',  # Set the content type if necessary
            'Request-Id':'MSI-GetToken'
        }

        auth = (self.clientID,self.clientSecret)

        try:
            response = requests.post(url=os.getenv("TOKEN_URL"),headers=headers, auth=auth)
            # print(headers)
        
            # Check the response
            if response.status_code == 200:
                response_json = response.json()
                self.responseData['status'] = response.status_code
                app.logger.info('POST request getToken was successful')
                os.environ['TOKEN'] = response_json['access_token']
                # print(os.environ.get('TOKEN'))
                return self.responseData
            else:
                self.responseData['status'] = response.status_code
                app.logger.error(f"POST request failed with status code: {response.status_code} and {response.content}")
                return self.responseData
            
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            app.logger.warning(f"Request failed: {e}")
            self.responseData['status'] = response.status_code
            self.responseData['data'] = response_json
            return self.responseData

    def contractSummary(self,value):

        data = {
            'billToLocation': [value],
            'limit':999
        }

        headers={
            'Authorization': f'Bearer {os.environ.get("TOKEN")}',
            'Content-Type': 'application/json',  # Set the content type if necessary
            'Request-Id':'MSI-ContractSummary'
        }

        try:
            response = requests.post(os.getenv('CONTRACT_SUMMARY_URL'), json=data, headers=headers)
            # print(headers)
            # Check the response
            if response.status_code == 200:
                response_json = response.json()
                self.responseData['status'] = response.status_code
                self.responseData['data'] = response_json
                app.logger.info(f"POST request contact summary search with {data['billToLocation']} was successful")
                return self.responseData
            else:
                self.responseData['status'] = response.status_code
                self.responseData['data'] = 'No Data'
                app.logger.error(f"POST request failed with status code: {response.status_code} and {response.content}")
                # print(self.responseData)
                return self.responseData
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            app.logger.warning(f"Request failed: {e}")
            self.responseData['status'] = response.status_code
            self.responseData['data'] = response_json
            return self.responseData
    
    def searchByItem(self,value):
       

        if value['selected']=='serialNumber':
            data={
                'serialNumbers':value['items'],
                'limit':900
            }
            head = "MSI-SearchSerialNumber"
        elif value['selected']=='contractNumber':
            data={
                'contractNumbers':value['items'],
                'limit':999
            }
            head = "MSI-SearchContractNumber"
        # print(data)
        headers={
            'Authorization': f'Bearer {os.environ.get("TOKEN")}',
            'Content-Type': 'application/json',  # Set the content type if necessary
            'Request-Id':head
        }

        try:
            response = requests.post(os.getenv('ITEM_SEARCH_URL'), json=data, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                self.responseData['status'] = response.status_code
                self.responseData['data'] = response_json
                app.logger.info(f"POST request search by item with {data} was successful")
                return self.responseData
            else:
                self.responseData['status'] = response.status_code
                self.responseData['data'] = 'No Data'
                app.logger.error(f"POST request failed with status code: {response.status_code} and {response.content}")
                # print(self.responseData)
                return self.responseData
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            app.logger.warning(f"Request failed: {e}")
            self.responseData['status'] = response.status_code
            self.responseData['data'] = response_json
            return self.responseData
        
    def dashboard(self):
        data = {
            'billToLocation': [338983795],
            'limit':999
        }

        headers={
            'Authorization': f'Bearer {os.environ.get("TOKEN")}',
            'Content-Type': 'application/json',  # Set the content type if necessary
            'Request-Id':'MSI-DashboardSummary'
        }
        
        try:
            response = requests.post(os.getenv('CONTRACT_SUMMARY_URL'), json=data, headers=headers)
            # print(headers)
            # Check the response
            if response.status_code == 200:
                response_json = response.json()
                self.responseData['status'] = response.status_code
                self.responseData['data'] = response_json
                app.logger.info(f"POST request contact summary search with {data['billToLocation']} was successful")
                return self.responseData
            else:
                self.responseData['status'] = response.status_code
                self.responseData['data'] = 'No Data'
                app.logger.error(f"POST request failed with status code: {response.status_code} and {response.content}")
                # print(self.responseData)
                return self.responseData
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            app.logger.warning(f"Request failed: {e}")
            return self.responseData