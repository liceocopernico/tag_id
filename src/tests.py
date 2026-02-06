
from datastore import DataStore
from data_models import desk,deskStudent,gradeDistribution
from combinatorial_utils import get_list_derangment

data=DataStore()
#data.init_db()

def sample_data():
    data.add_classroom('1.1',28,'Aula 1.1')
    first_classroom=data.get_classroom('1.1')
    data.add_tag_reader('tagreader-at-aula1-1','10.4.60.1',first_classroom,'uep1zWo35eut22PxNsOYd+fsabU1VMHmXkM/RdRtI/k=')
    data.add_grade('1C')


#data.add_table(gradeDistribution)


print(get_list_derangment(5,[3, 4, 1, 2, 0]))

    
    
#sample_data()

