"""Frontend module"""

import plotly.graph_objects as go
import streamlit as st

dic_name = {'elec_consumption': 'Electricité (kWh)',
            'elecday_consumption': 'Electricité jour (kWh)',
            'elecnight_consumption': 'Electricité nuit (kWh)',
            'gas_consumption': 'Gaz (m3)',
            'water_consumption': 'Eau (m3)',
            'rainwater_consumption': 'Eau de pluie (m3)',
            'month': 'Mois',
            'year': 'Année'
            }


def setup_bar_chart(df, x_col, y_cols, title=None):
    bar = [go.Bar(x=df[x_col], y=df[col], name=dic_name[col]) for col in y_cols]
    fig = go.Figure(bar)
    fig.update_layout(
        title=title,
        #xaxis_title=dic_name[x_col.split('_')[1]],
        yaxis_title='Consommation',
        xaxis={'tickformat': ',d'},
        legend_title="Légende",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="White"
        )
    )
    return fig


def plot_consumption(df, x, cols, tavg_cols=None):
    elec_cols = [col for col in cols if 'elec' in col]
    water_cols = [col for col in cols if 'water' in col]
    gas_cols = [col for col in cols if 'gas' in col]

    figures_elec = setup_bar_chart(df, x, elec_cols, 'Electricité (kWh)')
    figures_water = setup_bar_chart(df, x, water_cols, 'Eau (m3)')
    figures_gas = setup_gas_tavg(df, x, gas_cols, tavg_cols)
    figures = [figures_elec, figures_water, figures_gas]
    return figures


def setup_gas_tavg(df, x_col, gas_col, tavg_col=None):
    fig = setup_bar_chart(df, x_col, gas_col, 'Gaz (m3)')
    if tavg_col is not None:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[tavg_col],
            mode='markers',
            name='T°moyenne (°C)',
            line=dict(
                color='rgb(255, 0, 60)',
                width=2
            ),
            yaxis="y2"
        ))
        # Create axis objects
        fig.update_layout(
            xaxis=dict(
                domain=[1, 1]
            ),
            yaxis=dict(
                title="Consommation",
            ),
            yaxis2=dict(
                title='Température moyenne (°C)',
                overlaying="y",
                side="right",
                position=1,
                showgrid=False
            ),
        )
        fig.update_layout(
            autosize=False,
            width=500,
            height=700,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
        )
    return fig
