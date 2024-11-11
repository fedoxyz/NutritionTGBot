import csv
from db import GraphDB

def populate_graphdb(csv_file_path, db_uri, db_user, db_password):
    graph_db = GraphDB(db_uri, db_user, db_password)
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_line = row['product line']
            product = row['product']
            category = row['category']
            graph_db.add_class(product_line, product, category)
    graph_db.close()

if __name__ == "__main__":
    populate_graphdb('path/to/your/dataset.csv', 'bolt://localhost:7687', 'neo4j', 'password')
