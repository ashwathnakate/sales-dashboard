import pandas as pd
import calendar
import numpy as np
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt

import folium
from folium.plugins import HeatMap

import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly, render_altair, render_widget
from pathlib import Path




ui.tags.style(
    """
    body{
        font-family: "Poppins";
        background: #41295a;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #2F0743, #41295a);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #2F0743, #41295a); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

    }
    
    .header-text{
        margin-top: 20px;
        text-align: center;
        color: #ffffff;
        
    }
    
    .card {
    backdrop-filter: blur(21px) saturate(180%);
    -webkit-backdrop-filter: blur(21px) saturate(180%);
    background-color: rgba(255, 255, 255, 0);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.125);
}

.card-header{
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
}

.bslib-sidebar-layout>.sidebar{
    background-color: rgba(255, 255, 255, 0.05);
    
}

.selectize-input{
    background-color: #E6E6FA;
}

.control-label{
    color: #ffffff;
}

.bslib-sidebar-layout>.collapse-toggle{
    color: #ffffff;
}

.nav-link{
    color: #ffffff;
}

td{ color: white !important; /* All cells will have white font color */ }

    """
)

# ------- set the title of the browser tab -----------
ui.page_opts(window_title="Sales Browser", fillable=False)



# -------- dataset imports for caching the data----------
@reactive.calc
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    df['hour'] = df['order_date'].dt.hour
    df['value'] = df['quantity_ordered'] * df['price_each']
    return df

# -------this is the first chart---------

with ui.div(class_='header-text'):
    ui.div(ui.h2("Sales Dashboard"))
        

with ui.card():  
    ui.card_header("Sales by city 2023")

    with ui.layout_sidebar():  
        with ui.sidebar(bg="#f8f8f8", open='open'):  
            # ------- the multiple input widget ------
            ui.input_selectize(  
                "city",  
                "Select a city:",  
                ['Dallas (TX)', 'Boston (MA)', 'Los Angeles (CA)', 'San Francisco (CA)', 'Seattle (WA)', 'Atlanta (GA)', 'New York City (NY)', 'Portland (OR)', 'Austin (TX)', 'Portland (ME)'],  
                multiple=False,
                selected='Los Angeles (CA)'
            )
      

        # ------ the actual graph based on the multiple input widget ------
        @render_altair
        def sales_over_time():
            df = dat()
            sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
            sales_by_city = sales[sales['city'] == input.city()]
            month_orders = calendar.month_name[1:]
            chart = alt.Chart(sales_by_city).mark_bar(color='#E6E6FA', opacity=0.7, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X('month', sort=month_orders),
                y='quantity_ordered',
                tooltip=['month', 'quantity_ordered']
            ).properties(title=f"Sales over Time -- {input.city()}").configure( background='transparent').configure_axis( labelColor='white', titleColor='white' ).configure_title( color='white' )
            
            return chart
        
with ui.layout_column_wrap(width=1/2):
        
    with ui.navset_card_underline(id="tab", footer=ui.input_numeric("n", "Number of items", 5, min=0, max=20)):  
        with ui.nav_panel("Top Sellers"):
            
            
            # ------ the actual graph based on the above input ------
            @render_altair
            def top_sellers():
                df = dat().copy()
                
                top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
                chart = alt.Chart(top_sales).mark_bar(color='#E5D9F2', opacity=0.7, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X('product', sort=alt.EncodingSortField(field='quantity_ordered', order='descending')),
                    y='quantity_ordered',
                    tooltip=['product', 'quantity_ordered']
                ).properties(
                    title="Top Sellers"
                ).configure(
                    background='transparent'
                ).configure_axis(
                    labelColor='white',
                    titleColor='white'
                ).configure_title(
                    color='white'
                )
    
                return chart


        with ui.nav_panel("Top Sellers Value ($)"):
             # ------ the actual graph based on the above input ------
            @render_altair
            def top_sellers_values():
                df = dat().copy()
                
                top_sales = df.groupby('product')['value'].sum().nlargest(input.n()).reset_index()
                chart = alt.Chart(top_sales).mark_bar(color='#E5D9F2', opacity=0.7,cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X('product', sort=alt.EncodingSortField(field='value', order='descending')),
                    y='value',
                    tooltip=['product', 'value']
                ).properties(
                    title="Top Sellers Values"
                ).configure(
                    background='transparent'
                ).configure_axis(
                    labelColor='white',
                    titleColor='white'
                ).configure_title(
                    color='white'
                )
                
                return chart



        with ui.nav_panel("Lowest Sellers"):
             # ------ the actual graph based on the above input ------
            @render_altair
            def lowest_sellers():
                df = dat().copy()
                
                top_sales = df.groupby('product')['quantity_ordered'].sum().nsmallest(input.n()).reset_index()
                chart = alt.Chart(top_sales).mark_bar(color='#E5D9F2', opacity=0.7,cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X('product', sort=alt.EncodingSortField(field='quantity_ordered', order='ascending')),
                    y='quantity_ordered',
                    tooltip=['product', 'quantity_ordered']
                ).properties(
                    title="Lowest Sellers"
                ).configure(
                    background='transparent'
                ).configure_axis(
                    labelColor='white',
                    titleColor='white'
                ).configure_title(
                    color='white'
                )
                
                return chart


        with ui.nav_panel("Lowest Sellers Value ($)"):
             # ------ the actual graph based on the above input ------
            @render_altair
            def lowest_sellers_values():
                df = dat().copy()
                
                top_sales = df.groupby('product')['value'].sum().nsmallest(input.n()).reset_index()
                chart = alt.Chart(top_sales).mark_bar(color='#E5D9F2', opacity=0.7, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                    x=alt.X('product', sort=alt.EncodingSortField(field='value', order='ascending')),
                    y='value',
                    tooltip=['product', 'value']
                ).properties(
                    title="Lowest Sellers Values"
                ).configure(
                    background='transparent'
                ).configure_axis(
                    labelColor='white',
                    titleColor='white'
                ).configure_title(
                    color='white'
                )
                
                return chart

        
    with ui.card():
        ui.card_header("Sales by Time of Day Heatmap")
        # ---- acutal heatmap -----
        @render.plot
        def plot_sales_by_time():
            df = dat()
            sales_by_hour = df['hour'].value_counts().reindex(np.arange(0,24), fill_value=0)
            heatmap_data = sales_by_hour.values.reshape(24,1)
            fig, ax = plt.subplots()
            sns.heatmap(heatmap_data,
                        annot=True,
                        fmt="d",
                        cmap="coolwarm",
                        xticklabels=[],
                        yticklabels=[f"{i}:00" for i in range(24)],
                        ax=ax,)
            ax.set_facecolor('none') # Set the background of the axes to be transparent fig.patch.set_facecolor('none'
            ax.set_facecolor('none')  # Set the background of the axes to be transparent
            fig.patch.set_facecolor('none')  # Set the background of the figure to be transparent
            plt.title("Number of Orders by Day", color='white')
            plt.xlabel('Hour of Day', color='white')
            plt.ylabel('Order Count', color='white')
            return fig

    
    
    
    
    
with ui.card():
    ui.card_header("Sales by Location Map")
    
    @render.ui
    def plot_us_heatmap():
        df = dat()
        heatmap_data = df[['lat','long','quantity_ordered']].values
        
        map = folium.Map(location=[37.0902,-95.7129], zoom_start=4)
        HeatMap(heatmap_data).add_to(map)
        
        return map
        
        
    
        
    

    
    

# ----- showing the sample data of 100 rows -----
with ui.card():
    ui.card_header("Sample Sales Data")
    @render.data_frame
    def sample_sales_data():
        return render.DataGrid(dat().head(100), filters=True)

