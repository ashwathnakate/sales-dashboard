
# 📊 Sales Dashboard

This project is a Sales Dashboard application developed using Python. The application utilizes various libraries and frameworks such as pandas, seaborn, altair, folium, plotly, and shinywidgets to visualize and analyze sales data.

## Folder Structure

```plaintext
assets/
├── shiny-logo.png
├── shiny.jpeg
├── students.csv
├── video1.png
├── video2.png
├── video3.png
├── video4.png
├── sales/
│   ├── data/
│   │   └── sales.csv
│   └── rsconnect-python/
├── app.py
├── requirements.txt
├── .gitignore
├── how to run-deploy.txt
└── LICENSE
```

## ✅ Requirements

The following Python packages are required to run the application:

- pandas
- numpy
- seaborn
- altair
- matplotlib
- folium
- plotly
- shiny
- shinywidgets

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command in the terminal:

```bash
python app.py
```

## ⭐ Features

The Sales Dashboard application includes the following features:

1. **Sales by City 2023**: Visualizes sales data by city for the year 2023 using a bar chart.
2. **Top Sellers**: Displays the top-selling products.
3. **Top Sellers Value ($)**: Displays the top-selling products based on sales value.
4. **Lowest Sellers**: Displays the lowest-selling products.
5. **Lowest Sellers Value ($)**: Displays the lowest-selling products based on sales value.
6. **Sales by Time of Day Heatmap**: Visualizes the number of orders by the hour of the day using a heatmap.
7. **Sales by Location Map**: Shows a heatmap of sales by location using Folium.

## 🗂️ Data

The application uses the `sales.csv` file located in the `assets/sales/data/` directory. The data includes columns such as `order_date`, `quantity_ordered`, `price_each`, `city`, and `product`.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## ▶️ How to Run and Deploy

Instructions on how to run and deploy the application can be found in the `how to run-deploy.txt` file.

## Contact

https://github.com/ashwathnakate



