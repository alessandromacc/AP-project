from ds_reader import *
from operations import *
from dataset import *

reg = OperationRegistry(BasicInfo(name = 'BI'), FeaturesCount(), EntriesCount(), ListID(), EHGeneNames(name='EH'))
#change path to the file on your pc
x = Gff3Reader.read('/Users/Alessandro/Desktop/Uni/2° year/Advanced Programming/group pj-local/Homo_sapiens.GRCh38.85.gff3')

y = x.execute(reg, 'EH')
print(y.dataframe)
print(x.dataframe.head(40))
print(reg.registry['BI'])

