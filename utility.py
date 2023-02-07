class Gff3:
    @staticmethod
    def description() -> dict:
        return {'Chromosome or scaffold name':'Name of the scaffold containing the feature',
                                  'Source':'Assembly the data was taken from',
                                  'Type':'Indicates the different kinds of features, such as "gene", "trascript" and may others',
                                  'Feature Start':'Starting position of the feature in base pairs',
                                  'Feature End':'Ending position of the feature in base pairs',
                                  'Score':'A quality score attributed to the feature from the sequencing rounds',
                                  'Strand':'Indicates which strand is the feature located on, either + or -',
                                  'Phase':'Indicates the reading frame of a feature, possible values are 0,1,2',
                                  'Attributes':'Various characteristics of the feature'}

def switch(f):
    def wrap(self, status: bool, name: str):
        if status == False:
            status = True
        elif status == True:
            status = False
        func = f(self, status, name)
        return func
    return wrap
