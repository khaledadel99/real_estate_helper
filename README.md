# real_estate_helper
### Objective
- Allows users to ask natural-language questions (Arabic or English) for units specifications and getting a real-time available units details

### Flowchart
- Here you can find a flowchart that represents briefly the pipeline
<img width="1426" height="759" alt="image" src="https://github.com/user-attachments/assets/d6c6de6c-e433-482f-8515-59d0fde2da42" />


## Project Structure

- `main.py`: The entry point of the FastAPI application.
- `llm/`: Contains the logic for interacting with the Google GenAI API (`client.py`) and prompt management.
- `db/`: Database models (`model.py`), connection logic (`session.py`), and configuration.
- `scraping/`: Modules for scraping data sources (e.g., WhatsApp).
- `config/`: Configuration files and text prompts for the LLM.


## Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Google GenAI API Key

### Environment Variables

Create a `.env` file in the root directory (based on `.env.example` if available) with the following variables:

```env
# Google GenAI
API_KEY=your_google_api_key

# Database Connection
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

### Running Locally

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd project
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```


### Running with Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t real-estate-helper .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8000:8000 --env-file .env real-estate-helper
    ```
    
    Either ways the API will be available at `http://localhost:8000`.
    
## API Endpoints

### `POST /scrape`
Triggers the scraping process to collect new real estate data.
- **Returns**: Status and number of inserted records.

### `POST /ask`
Queries the database using natural language.
- **Parameters**: `question` (string)
- **Returns**: The generated SQL query, number of units found, and a natural language answer.
