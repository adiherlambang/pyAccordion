from datetime import datetime
class dashboard:
    data={
        "totalContract":'',
        "activeContract":'',
        "overdueContract":'',
        "signedContract":'',
        "top5PriceList":'',
        "6MonthfromNow":'',
        "6MonthLessThan1YearfromNow":'',
        "1yearfromNow":''
    }
    
    def getActiveContract(reqData):
        counterActiveContract = 0
        
        for contract in reqData['data']['contracts']:
            if contract.get('contractStatus') == 'ACTIVE':
                counterActiveContract += 1
                
        return counterActiveContract
    
    def getOverdueContract(reqData):
        counterOverdueContract = 0
        
        for contract in reqData['data']['contracts']:
            if contract.get('contractStatus') == 'OVERDUE':
                counterOverdueContract += 1
        
        return counterOverdueContract
    
    def getSignedContract(reqData):
        counterSignedContract = 0
        
        for contract in reqData['data']['contracts']:
            if contract.get('contractStatus') == 'SIGNED':
                counterSignedContract += 1
                
        return counterSignedContract
    
    def getTop5Pricelist(reqData):
        sorted_contracts = sorted(reqData.get('data', {}).get('contracts',[]), key=lambda x: x.get('listPrice', 0), reverse=True)
        top_5_contracts = sorted_contracts[:5]
        return top_5_contracts
    
    def filter_contracts_ended_six_months_before(reqData):
        filtered_contracts=[]
        date_format = "%d-%b-%YT%H:%M:%S.%f%z"
        # print(six_months_ago)
        str_date = datetime.now().strftime("%d-%b-%YT%H:%M:%S.%f+0000")
        today = datetime.strptime(str_date, date_format)        
        count=1
        for index,contract in enumerate(reqData.get('data', {}).get('contracts',[]),1):
            formated_end_contract_date = datetime.strptime(contract.get('contractEndDate'),date_format)
            difference = formated_end_contract_date - today
            # print(f"{selisih} and {contract['contractNumber']}")
            if difference.days <= 180 and difference.days >= 0:
                # print(index)
                filtered_contracts.append({
                    'contractNumber':contract['contractNumber'],
                    'dayLeft':difference.days,
                    'contractEndDate':contract['contractEndDate']
                })
                count+=1
        sorted_contracts = sorted(filtered_contracts, key=lambda x: x['dayLeft'],reverse=False)
        return sorted_contracts
    
    def filter_contracts_ended_six_months_to_one_year(reqData):
        filtered_contracts=[]
        date_format = "%d-%b-%YT%H:%M:%S.%f%z"
        # print(six_months_ago)
        str_date = datetime.now().strftime("%d-%b-%YT%H:%M:%S.%f+0000")
        today = datetime.strptime(str_date, date_format)        
        count=1
        for index,contract in enumerate(reqData.get('data', {}).get('contracts',[]),1):
            formated_end_contract_date = datetime.strptime(contract.get('contractEndDate'),date_format)
            difference = formated_end_contract_date - today
            # print(f"{selisih} and {contract['contractNumber']}")
            if difference.days >= 180 and difference.days <= 365:
                # print(index)
                filtered_contracts.append({
                    'contractNumber':contract['contractNumber'],
                    'dayLeft':difference.days,
                    'contractEndDate':contract['contractEndDate']
                })
                count+=1
        sorted_contracts = sorted(filtered_contracts, key=lambda x: x['dayLeft'],reverse=False)
        return sorted_contracts
    
    def filter_contracts_ended_more_than_one_year(reqData):
        filtered_contracts=[]
        date_format = "%d-%b-%YT%H:%M:%S.%f%z"
        # print(six_months_ago)
        str_date = datetime.now().strftime("%d-%b-%YT%H:%M:%S.%f+0000")
        today = datetime.strptime(str_date, date_format)        
        count=1
        for index,contract in enumerate(reqData.get('data', {}).get('contracts',[]),1):
            formated_end_contract_date = datetime.strptime(contract.get('contractEndDate'),date_format)
            difference = formated_end_contract_date - today
            # print(f"{selisih} and {contract['contractNumber']}")
            if difference.days >= 365:
                # print(index)
                filtered_contracts.append({
                    'contractNumber':contract['contractNumber'],
                    'dayLeft':difference.days,
                    'contractEndDate':contract['contractEndDate']
                })
                count+=1
        sorted_contracts = sorted(filtered_contracts, key=lambda x: x['dayLeft'],reverse=False)
        return sorted_contracts
    
    # def parse_contract_end_date(end_date_str):
    #     return datetime.strptime(end_date_str, "%d-%b-%YT%H:%M:%S.%f+0000")
    
    def main(self,reqData):
        self.data['totalContract']=reqData['data']['totalRecords']
        self.data['activeContract']=dashboard.getActiveContract(reqData)
        self.data['overdueContract']=dashboard.getOverdueContract(reqData)
        self.data['signedContract']=dashboard.getSignedContract(reqData)
        self.data['top5PriceList']=dashboard.getTop5Pricelist(reqData)
        self.data['6MonthfromNow']=dashboard.filter_contracts_ended_six_months_before(reqData)
        self.data['6MonthLessThan1YearfromNow']=dashboard.filter_contracts_ended_six_months_to_one_year(reqData)
        self.data['1yearfromNow']=dashboard.filter_contracts_ended_more_than_one_year(reqData)
        return self.data
        
        