import json
import urllib.parse
import boto3
import random
import string

print('Loading function')

s3 = boto3.client('s3')
comprehendmedical = boto3.client(service_name='comprehendmedical', region_name='us-east-1')


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(bucket)
    print(key)

    notes = ''

    obj = s3.get_object(Bucket=bucket, Key=key)

    notes = obj['Body'].read().decode('utf-8')
    print(notes)

    result = comprehendmedical.detect_entities(Text=notes)
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
    bin_notes = notes_mod.encode()
    klst = key.rsplit('/')
    nkey = 'anonymized/' + klst[len(klst) - 1]
    s3.put_object(Body=bin_notes, Bucket=bucket, Key=nkey)
