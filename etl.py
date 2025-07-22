from ingestion import reddit_ingest

def main():
    print("Starting ETL process...")
    
    print("Ingesting Reddit posts...")
    reddit_ingest.run()

    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()
