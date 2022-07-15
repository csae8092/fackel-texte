import glob
import os

from typesense.api_call import ObjectNotFound
from acdh_cfts_pyutils import TYPESENSE_CLIENT as client
from acdh_cfts_pyutils import CFTS_COLLECTION
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm


files = glob.glob('./data/editions/*.xml')
SCHEMA_NAME = "fackel-texte"

try:
    client.collections[SCHEMA_NAME].delete()
except ObjectNotFound:
    pass

current_schema = {
    'name': SCHEMA_NAME,
    'fields': [
        {
            'name': 'id',
            'type': 'string'
        },
        {
            'name': 'rec_id',
            'type': 'string'
        },
        {
            'name': 'title',
            'type': 'string'
        },
        {
            'name': 'full_text',
            'type': 'string'
        },
        {
            'name': 'jahrgang',
            'type': 'int32',
            'optional': True,
            'facet': True,
        },
        {
            'name': 'heft',
            'type': 'int32',
            'optional': True,
            'facet': True,
        },
        {
            'name': 'persons',
            'type': 'string[]',
            'facet': True,
            'optional': True
        }
    ]
}

client.collections.create(current_schema)

records = []
cfts_records = []
for x in tqdm(files, total=len(files)):
    record = {}
    cfts_record = {
        'project': SCHEMA_NAME,
    }
    doc = TeiReader(x)
    body = doc.any_xpath('.//tei:body')[0]
    record['id'] = os.path.split(x)[-1].replace('.xml', '')
    try:
        record['jahrgang'] = int(doc.any_xpath('.//tei:title[@type="jahrgang"]/text()')[0])
    except:
        pass
    try:
        record['heft'] = int(doc.any_xpath('.//tei:title[@type="heft"]/text()')[0])
    except:
        pass
    cfts_record['id'] = record['id']
    try:
        resolver = doc.any_xpath('.//tei:bibl[@type="url"]/text()')[0]
    except IndexError:
        continue 
    cfts_record['resolver'] = resolver
    record['rec_id'] = os.path.split(x)[-1]
    cfts_record['rec_id'] = record['rec_id']
    record['title'] = " ".join(" ".join(doc.any_xpath('.//tei:titleStmt/tei:title[@type="main"]//text()')).split())
    cfts_record['title'] = record['title']
    record['persons'] = [
        " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:back//tei:person/tei:persName')
    ]
    cfts_record['persons'] = record['persons']
    record['full_text'] = " ".join(''.join(body.itertext()).split())
    cfts_record['full_text'] = record['full_text']
    records.append(record)
    cfts_records.append(cfts_record)

make_index = client.collections[SCHEMA_NAME].documents.import_(records)
print(make_index)
print('done with indexing')

make_index = CFTS_COLLECTION.documents.import_(cfts_records,  {'action': 'upsert'})
print(make_index)
print('done with central indexing')