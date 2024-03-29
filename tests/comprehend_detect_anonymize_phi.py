import boto3
import random
import string
import json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
notes = 'Patient Jane Doe  is 40yo mother, highschool teacher HPI : Sleeping trouble on present dosage of Clonidine. Severe Rash  on face and leg, slightly itchy.  Meds : Vyvanse 50 mgs po at breakfast daily'
result = client.detect_entities(Text=notes)
entities = result['Entities'];
phidict = {}
# print(phidict[0])
index = 0;
tVal = ''
beg = ''
end = ''
notes_mod = notes

for entity in entities:
    # print('Entity', entity)
    for k, v in entity.items():

        # print(k,v)
        if (k == 'Text'):
            tVal = v
        if (k == 'BeginOffset'):
            beg = v
        if (k == 'EndOffset'):
            end = v
        # print(tVal)

        if (k == 'Category' and v == 'PROTECTED_HEALTH_INFORMATION'):
            # print('PHI')
            index = index + 1
            phidict[index] = {}
            phidict[index]['Text'] = tVal
            phidict[index]['Begin'] = beg
            phidict[index]['End'] = end
        # print(phidict[index])

prv_mb = 0
prv_me = 0

for i, x in enumerate(phidict):
    print(phidict[i + 1])
    mb = 0
    me = 0
    mt = ''

    for k, v in phidict[i + 1].items():
        print('item:')
        print(k, v)
        if (k == 'Text'):
            mt = randomString(len(v))
        if (k == 'Begin'):
            mb = v
        if (k == 'End'):
            me = v
        if (mb > 0 and me > 0):
            print(notes[mb:me])
            print('prv_me', prv_me)
            print('mb', mb)
            print('me', me)

        if (prv_me != 0 and mb > 0):
            notes_mod = notes_mod + notes[prv_me:mb]

        if (mb > 0):
            notes_mod = notes_mod[:mb]
            notes_mod = notes_mod + mt
            print('notes_mod:', notes_mod)

        if (mb > 0 and me > 0):
            print('update prv')
            prv_mb = mb
            prv_me = me

notes_mod = notes_mod + notes[me:]
print(notes_mod)
csv_notes_mod = '"' + 'notes_anonymized' + ',"' + notes_mod +'"'
print(csv_notes_mod)

x =  '{ "clinic_id":"101", "clinic_notes":"' +notes_mod + '"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["clinic_notes"])

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)





