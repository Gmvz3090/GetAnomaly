# GetAnomaly

A fast satellite data retrieval system for accessing processed satellite data from analyzers.

## Overview

GetAnomaly provides a query API for retrieval of satellite data that has been processed and stored in a MongoDB database. The system is optimized for time-based queries with indexed timestamps for fast data retrieval.

## Features

- MongoDB with indexed timestamps for flexibility (Additional data that isint in every record)
- Query API built with FastAPI
- Docker containerized deployment
- Automatic data ingestion from Parquet files
- JSON response format with proper serialization

## Architecture

- **API Server**: FastAPI application running on port 8000
- **Database**: MongoDB for data storage with timestamp indexing
- **Deployment**: Docker Compose for easy deployment and scaling

## Quick Start

### Prerequisites

- Docker
- Docker Compose
- Satellite data in Parquet format named `results.parquet`

### Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Gmvz3090/GetAnomaly
cd GetAnomaly
```

2. Place your satellite data file (`results.parquet`) in the project root directory

3. Build and run the system:
```bash
sudo docker compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /check
```
Returns connection status.

**Response:**
```json
{"Connection": true}
```

### Get Data by Time Range
```
GET /get?start_time=<ISO_DATETIME>&end_time=<ISO_DATETIME>
```
Retrieves satellite data within the specified time range.

**Parameters:**

- `start_time`/`end_time`: ISO format datetime (For ex. : `2007-01-01T00:07:30`)

**Example:**
```bash
curl "http://localhost:8000/get?start_time=2007-01-01T00:07:30&end_time=2007-01-01T01:00:00"
```

**Response:**
```json
{
  "success": true,
  "count": 100,
  "data": [
    {
      "_id": "...",
      "timestamp": "2007-01-01T00:07:30",
      "...": "satellite_data_fields"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "no_data_in_range"
}
```

### Get Sample Data
```
GET /getexample?lim=<NUMBER>
```
Returns a limited number of sample records for testing.

**Parameters:**
- `lim`: Maximum number of records to return

**Example:**
```bash
curl "http://localhost:8000/getexample?lim=5"
```

### Get All Data
```
GET /getall
```
**Warning**: Use with caution for large datasets as this endpoint returns all records.

**Example:**
```bash
curl "http://localhost:8000/getall"
```

## Data Format

The system expects satellite data in Parquet format with at minimum a `timestamp` field. The data is automatically ingested into MongoDB during container startup.

## Performance

- **Time Complexity**: O(log n + k) where n is total records and k is result size
- **Indexing**: Automatic timestamp indexing for optimal query performance
- **Memory**: Efficient MongoDB queries without loading full dataset into memory

## Configuration

### Environment Variables

- `MONGODB_URL`: MongoDB connection string (default: `mongodb://mongo:27017/`)

### Docker Configuration

The system uses Docker Compose with two services:
- `api`: FastAPI application
- `mongo`: MongoDB database with persistent volume

## Development

### Project Structure
```
GetAnomaly/
├── api.py                 # FastAPI application
├── uploadtomongo.py       # Data ingestion script
├── Dockerfile            # API container configuration
├── docker-compose.yml    # Multi-container setup
├── results.parquet       # Satellite data (user provided)
└── README.md
```

### Local Development

1. Install dependencies:
```bash
pip install fastapi uvicorn pymongo pandas pyarrow
```

2. Run MongoDB locally:
```bash
docker run -d -p 27017:27017 mongo:latest
```

3. Update connection string in `api.py` to `mongodb://localhost:27017/`

4. Run the API:
```bash
uvicorn api:app --reload
```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Error Handling

The API returns structured error responses with `success: false`:

```json
{
  "success": false,
  "error": "error_type"
}
```

Common error types:
- `date_parse_error`: Invalid datetime format in query parameters
- `no_data_in_range`: No satellite data found for specified time range
- `db_error`: Database connection or query issues

## Roadmap

- `More Compression` for further memory optim.
- `Time Based Partitioning` for quicker queries and easier manual investigation.
- `MongoDB -> ClickHouse` for faster queries.

