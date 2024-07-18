from pymongo import MongoClient
import argparse

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri)
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return None

def compare_collections(src_client, dst_client, exclude_dbs, exclude_collections):
    try:
        src_dbs = src_client.list_database_names()
        dst_dbs = dst_client.list_database_names()

        src_collections_all = []
        dst_collections_all = []

        for src_db_name in src_dbs:
            if src_db_name in exclude_dbs:
                continue
            
            if src_db_name not in dst_dbs:
                print(f"Database '{src_db_name}' missing in destination MongoDB.")
                continue
            
            print(f"Comparing database '{src_db_name}'...")

            src_db = src_client[src_db_name]
            dst_db = dst_client[src_db_name]

            src_collections = src_db.list_collection_names()
            dst_collections = dst_db.list_collection_names()

            src_collections_all.extend(src_collections)
            dst_collections_all.extend(dst_collections)

        src_collections_set = set(src_collections_all)
        dst_collections_set = set(dst_collections_all)

        src_only = src_collections_set - dst_collections_set
        dst_only = dst_collections_set - src_collections_set

        # Filter out excluded collections
        src_only = [coll for coll in src_only if coll not in exclude_collections]
        dst_only = [coll for coll in dst_only if coll not in exclude_collections]

        print(f"Total collections in source MongoDB: {len(src_collections_set)}")
        print(f"Total collections in destination MongoDB: {len(dst_collections_set)}")

        if src_only:
            print(f"\nCollections in source MongoDB not in destination MongoDB:")
            for coll in src_only:
                print(f" - {coll}")

        if dst_only:
            print(f"\nCollections in destination MongoDB not in source MongoDB:")
            for coll in dst_only:
                print(f" - {coll}")

    except Exception as e:
        print(f"Error during comparison: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Compare collections between two MongoDB instances.')
    parser.add_argument('--src', type=str, required=True, help='Source MongoDB URI')
    parser.add_argument('--dest', type=str, required=True, help='Destination MongoDB URI')
    parser.add_argument('--excludeDbs', type=str, nargs='+', default=[], help='Databases to exclude')
    parser.add_argument('--excludeCollections', type=str, nargs='+', default=[], help='Collections to exclude')

    args = parser.parse_args()

    # Connect to source and destination MongoDB instances
    src_client = connect_to_mongodb(args.src)
    dst_client = connect_to_mongodb(args.dest)

    if src_client and dst_client:
        compare_collections(src_client, dst_client, args.excludeDbs, args.excludeCollections)

        # Close connections
        src_client.close()
        dst_client.close()

if __name__ == "__main__":
    main()
