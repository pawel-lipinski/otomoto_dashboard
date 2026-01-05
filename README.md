# Otomoto.pl Polish Market Analysis Dashboard (as of 10DEC2025)

A data-driven web application built with **Streamlit** and **Plotly** to visualize and analyze used car listings from the Otomoto.pl marketplace.

## Project Purpose
This dashboard provides an interactive interface to explore automotive trends. It transforms raw scraped data into actionable insights, allowing users to analyze pricing, vehicle conditions, and geographical distributions across Poland.

## Features
* **Dynamic Multi-tier Filtering:** Filter the entire dataset by Brand, Model, and Condition. The Model selection dynamically updates based on the selected Brand.
* **Advanced Visualizations:**
    * **Price vs. Power Heatmaps:** Identify value trends based on engine performance.
    * **Mileage & Year Distributions:** Box plots and histograms with dynamic binning to maintain clarity across different sample sizes.
    * **Technical Specifications:** Visual breakdowns of fuel types, transmission, drive types, and door counts.
* **3D Geospatial Mapping:** A **PyDeck Hexagon Layer** map that visualizes the density of car listings across Poland using latitude and longitude coordinates.
* **Data Resiliency:** Automatic handling of data inconsistencies, such as converting invalid coordinates and managing missing engine power values for scatter plots.

## Technical Architecture
The dashboard is built using a modern Python stack:
* **Frontend:** [Streamlit](https://streamlit.io/) for the web interface and layout.
* **Data Engine:** [Pandas](https://pandas.pydata.org/) for data manipulation and cleaning.
* **Graphics:** [Plotly Express](https://plotly.com/python/plotly-express/) for interactive statistical charts.
* **Mapping:** [PyDeck](https://deckgl.readthedocs.io/en/latest/) for high-performance large-scale spatial rendering.

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/pawel-lipinski/otomoto_dashboard.git
    cd otomoto-dashboard
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pandas plotly streamlit pydeck
    ```

3.  **Data Preparation:**
    Place your dataset file named `otomoto_plain_data.csv` in the root directory. The script expects columns including `brand`, `model`, `price`, `mileage`, `lat`, and `lon`.

4.  **Run the Application:**
    ```bash
    streamlit run streamlit_dashboard.py
    ```

## Usage
* **Sidebar/Top Filters:** Use the dropdown menus to narrow down specific car segments.
* **Interactive Charts:** Hover over bars and data points to see specific values. Charts like "Car Mileage Distribution" include marginal box plots to show outliers.
* **3D Map:** Use `Right Click + Drag` to rotate the map and view the 3D height of listing density in different Polish districts.

---
*Developed by Pawel Lipinski*