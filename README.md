# real_estate_helper
objective : 
        Allows users to ask natural-language questions (Arabic or English) for units specifications and getting a real-time available units details

Here you can find a flowchart that represents briefly the pipeline
<img width="1426" height="759" alt="image" src="https://github.com/user-attachments/assets/d6c6de6c-e433-482f-8515-59d0fde2da42" />


## Project Structure

- `main.py`: The entry point of the FastAPI application.
- `llm/`: Contains the logic for interacting with the Google GenAI API (`client.py`) and prompt management.
- `db/`: Database models (`model.py`), connection logic (`session.py`), and configuration.
- `scraping/`: Modules for scraping data sources (e.g., WhatsApp).
- `config/`: Configuration files and text prompts for the LLM.


