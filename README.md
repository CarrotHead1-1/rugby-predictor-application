# Rugby Union Match Prediction Application

### Video Demo: <https://youtu.be/74hNLOz-1Zw>

## Project Overview

This project aims to develop a predictive application for Rugby Union match outcomes using machine learning. With Rugby Union growing in popularity and analytics becoming a critical component of performance evaluation in sports, the project leverages historical match data and statistical indicators to forecast outcomes in a user-friendly web interface. The application is primarily intended for coaches, analysts, fans, and enthusiasts seeking data-informed predictions, and includes key features such as an Elo rating system, a Random Forest classifier, and a modern graphical user interface (GUI).

## Project Goals

The primary goals of this project are:
- To investigate and implement a suitable machine learning model for Rugby Union match prediction.
- To collect, clean, and process relevant historical rugby data.
- To create an intuitive frontend that displays predictions, match details, and insights.
- To evaluate the predictive model’s accuracy using established performance metrics.

The outcome is a functional, modular web application integrating a trained model with a modern, accessible frontend.

---

## Project Structure

The project is composed of several core modules, each addressing a distinct component of the overall system:

### `data_collection.py`
- A modular Python script using **Selenium**, **BeautifulSoup**, and **Requests** to extract data from sources such as RugbyPass, StatsPerform, and LiveSports.
- Handles different website schemas with custom parsing logic.
- Integrates the **Bright Data API** to bypass bot restrictions and CAPTCHAs.

### `data_processing.py`
- Cleans, merges, and encodes raw match data.
- Standardizes features, handles missing values, removes duplicates, and encodes categorical variables for model compatibility.
- Implements normalization and outlier detection to improve model training.

### `elo_rating.py`
- Calculates Elo scores across seasons, incorporating match results into team strength assessments.
- Designed to be trained on multiple seasons (2018/19–2024/25), enhancing reliability.
- Outputs both Elo ratings and visualizations for display in the GUI.

### `model_training.py`
- Implements a **Random Forest Classifier** using **Scikit-learn**.
- Includes model evaluation using metrics like accuracy, F1-score, and precision.
- Supports parameter tuning for tree depth, count, and feature subsets.
- Uses `Pickle` to serialize the trained model for deployment.

### `api.py`
- A **FastAPI** backend for serving predictions, Elo scores, and match data to the frontend.
- Handles HTTP requests from the GUI and provides JSON responses.
- Includes endpoints for updating predictions and retrieving historical data.

### `frontend/` (Next.js Application)
- A fully functional frontend built with **Next.js** and styled using **Tailwind CSS**.
- Pages include: Home (match list and predictions), Elo Ratings (team strength overview), and History (past predictions).
- Components dynamically fetch backend data and display match outcomes, scores, and model performance metrics.

---

## Key Features

- **Machine Learning-Powered Predictions:** Uses historical data and KPIs such as tries, tackles, metres gained, and possession to generate predictions.
- **Elo Rating System:** Evaluates relative team strength over time, offering another dimension to match analysis.
- **Interactive User Interface:** Accessible, mobile-friendly GUI designed with usability and clarity in mind.
- **Data Transparency:** While limited, the design anticipates future feature explanation (feature importance) and custom input functionality.

---

## Design Choices and Rationale

### Random Forest Classifier
After an extensive literature review, Random Forest (RF) was chosen over alternatives like Artificial Neural Networks (ANNs) due to its:
- High accuracy (88% achieved in final version)
- Resilience against overfitting
- Ability to handle non-linear and categorical data
- Proven success in sports analytics, particularly Rugby Union

While hybrid models and deep learning approaches were considered, they were deemed impractical due to dataset limitations and time constraints.

### Hybrid Methodology: Agile + Waterfall
The development process followed a hybrid project management approach:
- **Waterfall** provided structured planning (via Gantt charts and milestones).
- **Agile (Scrum)** enabled iterative development, problem-solving, and modular implementation.
This combination offered the necessary structure while allowing flexibility during model tuning and GUI development.

### Web Scraping vs. Public Datasets
Rugby Union lacks accessible, standardized public datasets. As a result, a custom scraper was developed using multiple modules, tailored to individual site structures. While time-consuming, this ensured the data was fresh, relevant, and rich enough for training a robust model.

### Frontend Framework
**Next.js** was selected over alternatives like React.js or Angular due to:
- Server-side rendering for performance
- Simple routing and API integration
- Strong support for SEO and deployment via Vercel

**Tailwind CSS** was used to reduce repetitive styling code and enforce consistency across pages.

---

## Limitations

- **Responsiveness:** The current UI struggles on small viewports. Improvements are planned for future iterations.
- **Feature Transparency:** The application does not currently show which features influenced the model’s prediction. Implementing SHAP or feature importance charts is a high-priority improvement.
- **Custom Input Functionality:** Users cannot yet generate predictions with manual inputs. This was excluded due to time constraints.
- **Limited User Testing:** Evaluation was done primarily by the developer. Broader user testing would help validate usability and performance.

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- pip packages: `scikit-learn`, `pandas`, `fastapi`, `uvicorn`, `selenium`, `beautifulsoup4`
- Frontend: Next.js, Tailwind CSS

### Running the Application
1. **Backend:**
   ```bash
   cd backend
   uvicorn api:app --reload
