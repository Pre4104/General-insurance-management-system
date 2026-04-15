#party code
import random
type_of_insurance=input("Enter:")
year=input("Enter year:")
def party_code(type_of_insurance,year):
    #NP=family floater,TU=Top up,UK=New med claim
    #SH=Shopkeeper,MI=money insurance,BI=burgalry
    branch_no="67200"
    if type_of_insurance in ["TW",'PC','CV']:
        product_code="31" #motor
    if type_of_insurance in ['NP','TU','UK']:
        prodduct_code="34" #health
    if type_of_insurance in ['FS']:#FS=fire insurance
        product_code="11"
    if type_of_insurance in ['SH','MI','BI']:
        product_code="46" #miscellanous
    if type_of_insurance in ["PU"]:
        product_code="42"# personal accident
    random_no = random.randint(10000000, 99999999)
    party_code=branch_no+product_code+year+str(random_no)
    
    return int(party_code)
        
t=party_code(type_of_insurance,year)
print(t)
