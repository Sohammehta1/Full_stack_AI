class bank_record:

    def __init__(self, name):
        self.record = {
                        "name": name,
                        "balance": 100,
                        "transaction":[100]
                        }
    def __getitem__(self,key):
        return self.record[key]
    
    def __setitem__(self,key,newValue):
        if key == "balance" and newValue != None and (self.record[key] + newValue) > 100:
            self.record[key] += newValue
        
        elif key == "transaction" and newValue != None:
            self.record[key].append(newValue)
    
    def transaction(self,amount):
        if amount != 0:
            self.__setitem__("balance", amount)
        else:
            raise ValueError(str("Transaction amount cannot be 0"))
        print(f"Successfully completed transaction of {amount}")
        print(f"New balance is : {self.__getitem__("balance")}")
    
    def checkBalance(self):
        return self.__getitem__("balance")

    
sam_account: bank_record = bank_record("Sam")

sam_account.transaction(100)

