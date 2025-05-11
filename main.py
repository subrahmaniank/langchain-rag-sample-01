import sys
from ingestion.loaders import UniversalLoader




def ingestion_pipeline(file_path: str):
    loader = UniversalLoader(file_path)
    documents = loader.load()
    for doc in documents:
        print(doc.page_content)
    

def main(file_path: str):
    print(f"Receieved file path {file_path}")
    ingestion_pipeline(file_path)


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    main(file_path)
