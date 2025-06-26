# GetAnomaly

A fast satellite data retrieval system for accessing processed satellite data from various analyzers.

## Overview

GetAnomaly provides a RESTful API for efficient querying of satellite data that has been processed and stored in a MongoDB database. The system is optimized for time-based queries with indexed timestamps for fast data retrieval.

## Features

- Fast time-range based data retrieval
- MongoDB with indexed timestamps for optimal performance
- RESTful API built with FastAPI
- Docker containerized deployment
- Automatic data ingestion from Parquet files
- JSON response format with proper serialization

## Architecture

- **API Server**: FastAPI application running on port 8000
- **Database**: MongoDB for data storage with timestamp indexing
- **Data Format**: Satellite data stored as documents with timestamp fields
- **Deployment**: Docker Compose for easy deployment and scaling

## Quick Start

### Prerequisites

- Docker
- Docker Compose
- Satellite data in Parquet format named `results.parquet`

### Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
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
- `start_time`: ISO format datetime (e.g., `2007-01-01T00:07:30`)
- `end_time`: ISO format datetime (e.g., `2007-01-01T01:00:00`)

**Response:**
```json
{
  "success": true,
  "count": 100,
  "data": [
    {
      "_id": "...",
      "timestamp": "2007-01-01T00:07:30",
      "...": "other_satellite_data_fields"
    }
  ]
}
```

### Get Sample Data
```
GET /getexample?lim=<NUMBER>
```
Returns a limited number of sample records.

**Parameters:**
- `lim`: Maximum number of records to return

### Get All Data
```
GET /getall
```
Returns all data sorted by timestamp (use with caution for large datasets).

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

The API returns structured error responses:

```json
{
  "success": false,
  "error": "error_type"
}
```

Common error types:
- `date_parse_error`: Invalid datetime format
- `no_data_in_range`: No data found for specified time range
- `db_error`: Database connection issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please open a GitHub issue or contact the development team.
