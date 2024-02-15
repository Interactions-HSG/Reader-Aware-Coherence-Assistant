# Text-Linker-Coherence-Assistant


# Overview

The Text-Linker Coherence Assistant(TLCA) is developed to assess and improve the coherence between user-submitted texts and specific reader profiles. Leveraging the text analysis feature of OpenAI API, the system fetches relevant text artifacts(considered as "reader profile") from external databases such as [Semantic Scholar](https://www.semanticscholar.org/), providing an analysis that includes actionable suggestions and co-occurrence score calculations. 
TLCA is a tool for researchers, writers, and academics to tailor writings to match the intended audience's comprehension level, or enhance mutual knowledge adaptation.

👀 demo: [here](https://loom.com/share/folder/419e9f272b214d15a0823a5fdda41f14)

# Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.x
- Flask
- Flask-CORS
- OpenAI Python package

Also, you'll need an OpenAI API key to use the text analysis features.

# Installation

1. Clone the project repository.
2. Navigate to the project directory and create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   venv\Scripts\activate.bat  # Windows

4. Install the required Python packages:
   ```
   pip install Flask Flask-CORS OpenAI

# Configuration

Before running the application, configure your OpenAI API key in `app.py` by replacing `OPENAI_API_KEY` with your actual key.

# Project Structure

- `app.py`: The entry point to the application, responsible for initializing the Flask app and integrating server and client components.
- `app.server.py`: Contains server-side logic, including routes for fetching reader profiles, performing coherence analysis, and calculating scores.
- `app.client.py`: Manages client-side interactions, serving HTML templates and handling form submissions.
- `arc/`: A directory housing the Flask app declaration, metrics computation modules, and templates of UI.
  - `__init__.py`
  - `metrics/`: Contains modules for computing coherence scores or related measurements.
  - `static/`: Contains JavaScript files for client-side functionality.
  - `template/`: Stores HTML templates that define the UI of the coherence analysis system.
 
Reference: 
![image](https://github.com/Interactions-HSG/Text-Linker-Coherence-Assistant/assets/49511520/dcc7bc67-2278-41f2-b68d-0b6371862942)
![image](https://github.com/Interactions-HSG/Text-Linker-Coherence-Assistant/assets/49511520/9decee15-932c-41ba-bdeb-bdb454b94185)


# Server (`app.server.py`)

Defines Flask routes for:
- Fetching data based on `personal_id`.
- Performing coherence analysis between user text and abstracts.
- Calculating co-occurrence scores.

# Client (`app.client.py`)

Handles:
- Serving HTML templates for user interaction.
- Capturing and submitting user inputs for analysis.

# Running the Application

To run the application:

1. Set config.json with two fields: "CHATGPT_API_KEY" and "GOOGLE_SCHOLAR_API_KEY"
2. Start the Flask server by executing `app.py`:
   ```
   python app.py

3. Access the web application via your browser at `http://localhost:5000`.

# Usage

Users can interact with the system through the web interface provided by the `app.client.py` routes. This includes submitting texts for analysis, choosing reader profiles, and viewing suggestions and scores for text coherence.

# Contributing

We welcome contributions to TLCA. Feel free to fork the repository, make improvements, and submit pull requests. For bugs and feature requests, please use the issue tracker.

# License

This project is licensed under GPL-3.0 license.

# Contact

For support or collaboration, please contact _ge.li2@studio.unibo.it_.

