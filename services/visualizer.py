# visualizer.py
import plotly.express as px
# import plotly.graph_objects as go
import pandas as pd
from typing import List 
import random


class DataVisualizer:
    def __init__(self):
        self.plots = {}
    
    def create_basic_plots(self, df : pd.DataFrame, imp_cols : List[str]) :
        """Create basic plots for the dataset"""
        num_cols = df[imp_cols].select_dtypes(include=['int64', 'float64']).columns
        cat_cols = df[imp_cols].select_dtypes(include=['object', 'category']).columns
        # 1. Distribution plot for numeric columns

        if len(num_cols) > 0:
            for num_col in num_cols:
                plot_type = random.choice(['histogram', 'Box'])

                if plot_type == 'histogram':
                    self.plots[f'distribution_histogram_{num_col}'] = px.histogram(
                        df, 
                        x=num_col,
                        title=f"Distribution of {num_col}"
                    )
                else:
                    self.plots[f'distribution_Box_{num_col}'] = px.box(
                        df,
                        x=num_col,
                        title=f"Distribution of {num_col}"
                    )
        #2 Plots for categorical cols
        if len(cat_cols) > 0:
            for cat_col in cat_cols:
                category_counts = df[cat_col].value_counts().reset_index()
                category_counts.columns = [cat_col, 'Count']
                self.plots[f'distribution_Bar_{cat_col}'] = px.bar(category_counts, x= cat_col, y='Count', title=f"Distribution of {cat_col}", color=cat_col)


        # 3. Correlation heatmap
        if len(num_cols) > 1:
            self.plots['correlation'] = px.imshow(
                df[num_cols].corr(),
                title="Correlation Heatmap"
            )
        
        # 4. Time series plot (if date column exists)
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0 and len(num_cols) > 0:
            self.plots['time_series'] = px.line(
                df,
                x=date_cols[0],
                y=num_cols[0],
                title=f"{num_cols[0]} over Time"
            )
        
        return self.plots