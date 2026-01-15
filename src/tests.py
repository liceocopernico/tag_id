
from datastore import DataStore


data=DataStore()
data.init_db()

def sample_data():
    data.add_classroom('1.1',28,'Aula 1.1')
    test_classroom=data.get_classroom('1.1')
    data.add_tag_reader('test_reader','10.27.9.164',test_classroom,'q2zGa0VXoRYivb6MEmo80+bHQpX60RQu+mafCUIuH8A=')
    data.add_grade('1C')
    current_grade=data.get_grade('1C')
    data.add_user('test_user',current_grade)
    current_user=data.get_user('test_user')
    data.add_tag('64c44977-a3b5-420d-8ab8-517482870791',current_user)
    data.add_user('test_user2',current_grade)
    current_user=data.get_user('test_user2')
    data.add_tag('d1accfe5-517f-483a-ba6c-a651cdc875a0',current_user)
    data.add_user('test_user3',current_grade)
    current_user=data.get_user('test_user3')
    data.add_tag('04-B1-F4-A9-7D-26-81',current_user)



def test(value):
    return value if value==10 else None



tmp= _ if test(10) else None
print(tmp)
    
    
