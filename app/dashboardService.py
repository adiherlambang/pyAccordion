
class dashboard:
    data={
        "totalContract":'',
        "activeContract":'',
        "overdueContract":'',
        "signedContract":''
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
    
    def main(self,reqData):
        self.data['totalContract'] = reqData['data']['totalRecords']
        self.data['activeContract']= dashboard.getActiveContract(reqData)
        self.data['overdueContract']= dashboard.getOverdueContract(reqData)
        self.data['signedContract']= dashboard.getSignedContract(reqData)
        return self.data
        
        