import csv
import requests
import json
import sys

class CuffLinkDatabase ():
    def __init__ (self, file):
        self.CSVFile = file
        self.data = {}

        reader = csv.reader(self.CSVFile, delimiter = ',', quotechar='"')

        headers = next(reader)
        
        for row in reader:
            self.data[row[0]] = dict(list(zip(headers,row)))

    def get (self, xlocId):
        if xlocId in self.data:
            return self.data[xlocId]
        else:
            return None

    def getAll (self):
        return self.data


class OutputCSV ():
    def __init__ (self, path, headers):
        self.path = path
        self.headers = headers

    def write (self, listOfWormDatas):

        if sys.version_info >= (3,0,0):
           with open(self.path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                for wormData in listOfWormDatas:
                    writer.writerow(wormData.describe())
        else:
            with open(self.path, 'wb') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                for wormData in listOfWormDatas:
                    writer.writerow(wormData.describe())
        
            


class WormData ():
    headers = {'Content-Type':'application/json'}
    GENE_BASE = "http://api.wormbase.org/rest/field/gene"
    PROTEIN_BASE= "http://api.wormbase.org/rest/field/protein"
    
    def __init__ (self, xlocID, geneID, database):
        self.geneID = geneID
        self.data = {}
        self.xlocID = xlocID
        self.data['gene_id'] = geneID
        self.database = database
        self.populate()

    def populate (self):
        print(('geneID = ' + self.geneID))
        if self.geneID and self.geneID.startswith("WBGene"):
        
            self.data['up/down'] = self.database.get(self.xlocID)['log2(fold_change)']

            sequence = self.fetch(self.GENE_BASE, self.geneID, 'sequence_name')
            self.data['sequence_name'] = sequence

            description = self.fetch(self.GENE_BASE, self.geneID, 'concise_description')
            self.data['description'] = description['text']

            geneModels = self.fetch(self.GENE_BASE, self.geneID, 'gene_models')
            self.data['protein_id'] = []
            if geneModels and 'table' in geneModels:
                for item in geneModels['table']:
                    if item and 'protein' in item and 'id' in item['protein']:
                        self.data['protein_id'].append(item['protein']['id'])

            self.joinIfExtant('protein_id')


            geneClass = self.fetch(self.GENE_BASE, self.geneID, 'gene_class')
            self.data['gene_class'] = geneClass

            humanOrthologs = self.fetch(self.GENE_BASE, self.geneID, 'human_orthologs')
            self.data['human_orthologs'] = []
            if humanOrthologs:
                for item in humanOrthologs:
                    self.data['human_orthologs'].append(item['ortholog']['label'])

            self.joinIfExtant('human_orthologs')

            nematodeOrthologs = self.fetch(self.GENE_BASE, self.geneID, 'nematode_orthologs')
            self.data['nematode_orthologs'] = []
            if nematodeOrthologs:
                for item in nematodeOrthologs:
                    self.data['nematode_orthologs'].append(item['ortholog']['label'])

            self.joinIfExtant('nematode_orthologs')

            otherOrthologs = self.fetch(self.GENE_BASE, self.geneID, 'other_orthologs')
            self.data['other_orthologs'] = []
            if otherOrthologs:
                for item in otherOrthologs:
                    self.data['other_orthologs'].append(item['ortholog']['label'])

            self.joinIfExtant('other_orthologs')

            self.data['best_human_ortholog'] = []

            isSingular =  hasattr(self.data['protein_id'], '__len__') and (not isinstance(self.data['protein_id'], str))

            if self.data['protein_id'] and not isSingular:
                for proteinID in self.data['protein_id']:
                    bestHumanMatch = self.fetch(self.PROTEIN_BASE, proteinID, 'best_human_match')
                    if bestHumanMatch and 'description' in bestHumanMatch:
                        self.data['best_human_ortholog'].append(bestHumanMatch['description'])
            elif self.data['protein_id']:
                bestHumanMatch = self.fetch(self.PROTEIN_BASE, self.data['protein_id'], 'best_human_match')
                if bestHumanMatch and 'description' in bestHumanMatch:
                    self.data['best_human_ortholog'].append(bestHumanMatch['description'])


            self.joinIfExtant('best_human_ortholog')

    def joinIfExtant (self, datum):
        if len(self.data[datum]) == 0:
            self.data[datum] = None
        else:
            self.data[datum] = ', '.join(self.data[datum])
        
    def get (self, datum):
        if datum in self.data:
            return self.data[datum]
        else:
            return None

    def describe (self):
        return self.data

    def fetch (self, baseUrl, id, datum):
        r = requests.get(baseUrl + '/' + id + '/' + datum, headers=self.headers)

        try:
            j = r.json()
        except:
            return None

        if datum in j and 'data' in j[datum]:
            return j[datum]['data']
        else:
            return None
        
        

    
        
