import pandas as pd
from operations import *
import typing
from utility import *

class Dataset:
    '''Dataset class, wraps around a pandas DataFrame, each attribute is converted to a property,
    but no chance for modifying them is offered to the user.'''
    def __init__(self, df: pd.DataFrame):
        self.__dataframe: pd.DataFrame = df
        self.__queried: bool = False
    
    @property
    def dataframe(self) -> pd.DataFrame:
        '''getter for the pandas dataframe'''
        return self.__dataframe
    
    @property
    def queried(self) -> bool:
        '''getter for the queried attribute'''
        return self.__queried
    
    def __query(self, r: OperationRegistry, op: str) -> bool:
        '''Verifies wether the requested operation is marked as active in the reference registry,
        returning a boolean value: True for active and vice versa. The queried property is set True
        as part of the mechanism that forces the user to execute any operation by means of the Dataset method
        execute.'''
        self.__queried = True
        return r.status_registry[op]
    
    def execute(self, r: OperationRegistry, op: str):
        '''Takes as arguments the registry where an operation is supposed to be found and the name of such operation,
        also retrievable as the name property of any operation. Looks into the registry for the operation and calls it,
        returning whatever the operation returns it. Only successfully executed if the operation is active and the
        operation name parsed is found in the registry.'''
        try:
            if self.__query(r, op) == True:
                result = r.registry[op].operation(self)
                self.__queried = False
                return result
            else:
                self.__queried = False
                return 'Operation not active'
        except KeyError:
            return 'Not existing operation'

class BasicInfo(Operation):
    def __init__(self, status: bool = False, name: str = 'BasicInfo'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> list:
        '''getting the some basic information about the dataset. The basic information are the name and data type ofeach column'''
        if d.queried == True:
            return Dataset(pd.DataFrame([[i,j] for i,j in Gff3.description().items()]))

class FeaturesCount(Operation):
    def __init__(self, status: bool = False, name: str = 'FeaturesCount'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''counting the number of features provided by the same source'''
        if d.queried == True:
            return Dataset(d.dataframe.value_counts('Source', dropna=True))

class ListID(Operation):
    def __init__(self, status: bool = False, name: str = 'ListID'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''obtaining the list of unique sequence IDs available in the dataset'''
        if d.queried==True:
            return Dataset(pd.DataFrame(d.dataframe['Chromosome or scaffold name'].unique()))

class ListTypes(Operation):
    def __init__(self, status: bool = False, name: str = 'ListTypes'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''obtaining the list of unique type of operations available in the dataset'''
        if d.queried == True:
            return Dataset(pd.DataFrame(d.dataframe['Type'].unique()))

class EntriesCount(Operation):
    def __init__(self, status: bool = False, name: str = 'EntriesCount'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''counting the number of entries for each type of operation'''
        if d.queried == True:
            return Dataset(d.dataframe.value_counts('Type'))

class EntireChromosomes(Operation):
    def __init__(self, status: bool = False, name: str = 'EntireChromosomes'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38'''
        if d.queried == True:
            return Dataset(d.dataframe.loc[d.dataframe['Type'].isin(['chromosome'])])

class UnassembledSeq(Operation):
    def __init__(self, status: bool = False, name: str = 'UnassembledSeq'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''calculating the fraction of unassembled sequences from source GRCh38'''
        if d.queried == True:
            selected = d.dataframe.loc[d.dataframe['Source'].isin(['GRCh38'])].value_counts('Type')
            return Dataset(pd.DataFrame([['Fraction of unassembled sequences',f'{100*selected.loc["supercontig"]/selected.sum()} %']]))

class EHselect(Operation):
    def __init__(self, status: bool = False, name: str = 'EHselect'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''obtaining a new dataset containing only entries from source  ensembl,  havana  and ensembl_havana'''
        if d.queried == True:
            return Dataset(d.dataframe[d.dataframe['Source'].isin(['ensembl', 'havana', 'ensembl_havana'])])

class EHentries(Operation):
    def __init__(self, status: bool = False, name: str = 'EHentries'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset):
        '''counting the number of entries for each type of operation for the dataset containing containing onlyentries from source  ensembl,  havana  and  ensembl_havana'''
        if d.queried==True:
            return Dataset(d.dataframe[d.dataframe['Source'].isin(['ensembl', 'havana', 'ensembl_havana'])].value_counts('Type'))

class EHGeneNames(Operation):
    def __init__(self, status: bool = False, name: str = 'EHGeneNames'):
        super().__init__(status, name)
    
    def operation(self, d: Dataset) -> Dataset:
        '''returning the gene names from the dataset containing containing only entries from source  ensembl, havana  and  ensembl_havana'''
        if d.queried == True:
            selected = d.dataframe[d.dataframe['Source'].isin(['ensembl', 'havana', 'ensembl_havana']) & d.dataframe['Type'].isin(['gene'])]
            a = pd.Series([i.split(';')[1].split('=')[1] for i in selected['Attributes']])
            n = pd.Series([i for i in selected['Chromosome or scaffold name']])
            d={'genename':a, 'name':n}
            return Dataset(pd.DataFrame(data=d))