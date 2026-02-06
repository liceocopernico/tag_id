import csv
import os
import csv
from datastore import DataStore


data=DataStore()




base_path=os.path.dirname(os.path.realpath(__file__))+"/assets/init_data/"


with open(base_path+"teachers.csv") as users_data:
    new_users=csv.reader(users_data,delimiter=";")
    #print headers
    print(next(new_users))
    
    for row in new_users:
    
        current_grade=data.get_grade(row[5])
        current_user=data.add_user(row[3],current_grade,row[2],row[1],row[4])
        data.add_tag(row[0],current_user)
        