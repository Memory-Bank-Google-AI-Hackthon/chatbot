from google.cloud import bigquery
import os


class BigQueryManager:
    
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
        self.project = "memory-bank-315712"
        self.database = "memory_bank"
        self.table = "note"
        self.dataset_id = "memory_bank"

        self.client = bigquery.Client()

        for dataset in self.client.list_datasets():
            print("\t{}".format(dataset.dataset_id)) 

    def _create_dataset(self):
        dataset = self.client.Dataset(self.dataset_id)
        dataset.location = "asia-east1"
        dataset.default_table_expiration_ms = 30 * 24 * 60 * 60 * 1000  # 設定資料過期時間，這邊設定 30 天過期
        dataset.description = 'This is a dataset for memory bank.'
        print('Start creating dataset {}'.format(self.dataset_id))
        dataset = client.create_dataset(dataset)
        print('Finish created dataset {}'.format(dataset.dataset_id))

    def _create_note_table(self):
        schema = [
            bigquery.SchemaField("note_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("note_title", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("note_content", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("note_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title_tensor", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("content_tensor", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP", mode="REQUIRED"),
        ]

        table = bigquery.Table(self.table, schema=schema)
        table = self.client.create_table(table)
        

client = BigQueryManager()
