# MongoDB Collection Comparison Script

This script allows you to compare collections between two MongoDB instances, identifying collections that exist in one instance but not in the other. It supports excluding specific databases and collections from the comparison.

## Prerequisites

- Python 3.x
- `pymongo` library (`pip install pymongo`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your/repository.git
   cd repository
   ```

2. Install the required Python packages:
   ```bash
   pip install pymongo
   ```

## Usage

### Arguments

- `--src`: Source MongoDB URI (required)
- `--dest`: Destination MongoDB URI (required)
- `--excludeDbs`: Databases to exclude from comparison (optional)
- `--excludeCollections`: Collections to exclude from comparison (optional)

### Example

Compare collections between two MongoDB instances:

```bash
python compare_collections.py --src="mongodb://username1:password1@host1:port/database1" --dest="mongodb://username2:password2@host2:port/database2" --excludeDbs admin local --excludeCollections collection1 collection2
```

### Notes

- Replace `--src` and `--dest` with your actual MongoDB connection URIs.
- Adjust `--excludeDbs` to specify databases to exclude from the comparison.
- Adjust `--excludeCollections` to specify collections to exclude from the comparison.

## Output

The script will output:
- Total number of collections in the source MongoDB and destination MongoDB.
- Collections present in the source MongoDB but not in the destination MongoDB.
- Collections present in the destination MongoDB but not in the source MongoDB.
