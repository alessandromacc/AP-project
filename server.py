from flask import Flask, render_template
from dataset import *
from operations import *
from ds_reader import Gff3Reader

'''Server page with the Flask code'''

myapp = Flask('webapp')

'''Define the operation registry with all the operations instances needed in the webpage.'''
reg = OperationRegistry(BasicInfo(), FeaturesCount(), ListID(), ListTypes(), EntriesCount(), EntireChromosomes(), UnassembledSeq(), EHselect(), EHentries(), EHGeneNames())

'''Use the Gff3Reader class to read a gff3 file and store it into a Dataset object,
pass as argument the path to the gff3 file.'''
df = Gff3Reader.read('/Users/Alessandro/Desktop/Uni/2° year/Advanced Programming/group pj-local/Homo_sapiens.GRCh38.85.gff3')

@myapp.route('/')
def index():
    '''Homepage, parse for jinja rendering the registry'''
    global reg, df
    return render_template('index.html', reg = reg)

@myapp.route('/documentation')
def documentation():
    '''documentation page'''
    return render_template('documentation.html')

@myapp.route('/operations')
def operations(reg = reg):
    '''overview oon the active operations page'''
    return render_template('operations.html', reg=reg)

@myapp.route('/basicInfo')
def basic_info(reg=reg, df=df):
    '''Operation page, parse for jinja rendering just the value of the executed method'''
    bi = df.execute(reg, 'BasicInfo')
    return render_template('BasicInfo.html', bi=bi)

@myapp.route('/FeaturesCount')
def features_count(reg=reg, df=df):
    '''Operation page, parse for jinja rendering the value of the executed method'''
    tdf = df.execute(reg, 'FeaturesCount')
    return render_template('FeaturesCount.html', tdf = tdf)

@myapp.route('/ListID')
def list_IDs(reg=reg, df=df):
    '''Operation page, displays the list of unique IDs found in the genome annotation'''
    types = df.execute(reg, 'ListID')
    return render_template('ListID.html', types = types)

@myapp.route('/ListTypes')
def list_types(reg=reg, df=df):
    d = df.execute(reg, 'ListTypes')
    return render_template('ListTypes.html', d = d)

@myapp.route('/EntriesCount')
def entries_count(reg = reg, df=df):
    d = df.execute(reg, 'EntriesCount')
    return render_template('EntriesCount.html', d=d)

@myapp.route('/EntireChromosomes')
def entire_chromosomes(reg=reg, df=df):
    d=df.execute(reg, 'EntireChromosomes')
    print(d)
    h = len(d.dataframe.columns[0])
    return render_template('EntireChromosomes.html', d=d, h=h, desc=Gff3.description())

@myapp.route('/UnassembledSeq')
def unassembled_seq(reg=reg, df=df):
    d=df.execute(reg, 'UnassembledSeq')
    return render_template('UnassembledSeq.html', d=d)

@myapp.route('/EHselect')
def EH_select(reg=reg, df=df):
    d = df.execute(reg, 'EHselect')
    return render_template('EHselect.html', d=d, desc=Gff3.description())

@myapp.route('/EHentries')
def EH_entries(reg=reg, df=df):
    d = df.execute(reg, 'EHentries')
    return render_template('EHentries.html', d=d)

@myapp.route('/EHGeneNames')
def EH_gene_names(reg=reg, df=df):
    d = df.execute(reg, 'EHGeneNames')
    return render_template('EHGeneNames.html', d=d)


myapp.run()