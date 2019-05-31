import boto3
client = boto3.client('glue')
#imp = client.get_ingestor(Name="lakeformationdemoimporter")
#print(imp)
#client.delete_ingestor(Name="lakeformationdemoimporter")
resp = client.get_data_lake_settings("716664005094/datalake")
#print(resp)
