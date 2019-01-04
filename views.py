import dash_core_components as dcc
import dash_html_components as html

from investments import RentingCapital, PropertyValue
from mortgage import Mortgage
from rent import Rent
from typing import List
import id


class Colors:
    rent_payment_color = "#9575cd"

    equity_rent_color = "#1976d2"
    reinvestment_for_rent = "#90caf9"

    mortgage_principle_payment_color = "#ef6c00"
    mortgage_interest_payment_color = "#ffb300"

    mortgage_principle_remain_color = "#5d4037"

    property_evaluation_color = "#a5d6a7"
    equity_buy_color = "#2e7d32"


def create_equity_comparison_graph(
        x_axis_years: List[int],
        renting_capital: RentingCapital,
        property_value: PropertyValue
):
    equity_summary = f"This shows how your equity grows comparing renting vs buying in the " \
        f"next {x_axis_years[-1]} years. "

    assert len(renting_capital.capitals) == len(property_value.equity_by_year)

    first_year_better_buy = -1
    for i in range(0, len(renting_capital.capitals)):
        if property_value.equity_by_year[i] > renting_capital.capitals[i]:
            first_year_better_buy = i
            break

    if first_year_better_buy > 0:
        equity_summary += f"If you are planning on selling the property after {first_year_better_buy + 1} years, " \
            f"it is better to buy. If you plan to sell before then, you'd better continue renting. "
    else:
        equity_summary += "Your equity is always higher to rent. You should keep renting. "

    annotations = [
        dict(
            x=first_year_better_buy + 1,
            # * 1.05 because we want some spacing because the bottom of the arrow to the top of the chart
            y=property_value.equity_by_year[first_year_better_buy] * 1.05,
            xref='x',
            yref='y',
            ax=0,
            ay=-30,
            text='Tipping Point',
            arrowhead=2,
            xanchor="middle",
            yanchor="bottom",
            arrowcolor='orange',
            arrowwidth=2,
            font=dict(
                size=18,
                color='orange'
            ),
        )
    ] if first_year_better_buy > 0 else None

    return html.Div(children=[
        dcc.Graph(
            id='id-graph-buy-or-rent',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': renting_capital.capitals,
                        'type': 'bar',
                        'name': 'Equity for Rent',
                        "marker": {
                            "color": Colors.equity_rent_color
                        }
                    },
                    {
                        'x': x_axis_years,
                        'y': property_value.equity_by_year,
                        'type': 'bar',
                        'name': 'Equity for Buy',
                        'legend': {'orientation': 'h'},
                        "marker": {
                            "color": Colors.equity_buy_color
                        }
                    },
                ],
                'layout': {
                    'title': 'Equity by year, buy vs rent',
                    'yaxis': {'title': 'Equity ($)'},
                    'xaxis': {'title': 'Year'},
                    'legend': {'orientation': 'h'},
                    "annotations": annotations,
                }
            }
        ),
        html.Div(children=equity_summary)
    ])


def create_insights_tabs():
    return html.Div(children=[
        html.H2('Insights', className="golden_subtitle"),
        dcc.Tabs(id=id.detailed_insights_tab, children=[
            dcc.Tab(label='Mortgage payments', value=id.TabValue.tab_value_mortgage_payment),
            dcc.Tab(label='Mortgage principle', value=id.TabValue.tab_value_remaining_mortgage),
            dcc.Tab(label='Rent payments', value=id.TabValue.tab_value_rent),
            dcc.Tab(label='Equity for rent', value=id.TabValue.tab_value_equity_by_rent),
            dcc.Tab(label='Equity for buy', value=id.TabValue.tab_value_asset_for_buy),
        ]),
        html.Div(id=id.detailed_insights_tab_content)
    ])


def create_rental_graph(x_axis_years: List[int], rent: Rent):
    return html.Div(children=[
        dcc.Graph(
            id='rent-payment-graph',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': rent.yearly_payments,
                        'type': 'bar',
                        'name': 'Rent Payments',
                        'marker': {
                            'color': Colors.rent_payment_color
                        }

                    },

                ],
                'layout': {
                    'title': 'Rent By Year',
                    'yaxis': {'title': 'Payment ($)'},
                    'xaxis': {'title': 'Year'},
                    'legend': {'orientation': 'h'},
                }
            }
        ),
        html.Div(children=rent.description),
    ])


def create_mortgage_payment_graph(x_axis_years: List[int], mortgage: Mortgage):
    return html.Div(children=[
        dcc.Graph(
            id='mortgage-payment-graph',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': mortgage.principal_payments_by_year,
                        'type': 'bar',
                        'name': 'Principal Payments',
                        "marker": {
                            "color": Colors.mortgage_principle_payment_color
                        }
                    },
                    {
                        'x': x_axis_years,
                        'y': mortgage.interest_payments_by_year,
                        'type': 'bar',
                        'name': 'Interest Payments',
                        "marker": {
                            "color": Colors.mortgage_interest_payment_color
                        }
                    },
                ],
                'layout': {
                    'title': 'Mortgage Payment By Year',
                    'yaxis': {'title': 'Payment ($)'},
                    'xaxis': {'title': 'Year'},
                    'barmode': 'stack',
                    'legend': {'orientation': 'h'},
                }
            }
        ),
        html.Div(children=mortgage.description),
    ])


def create_mortgage_principle_graph(x_axis_years: List[int], mortgage: Mortgage):
    mortgage_principle_description = f"This graph simply shows how the mortgage is being paid off year over year. " \
        "Notice that it does not go down linearly. " \
        "As time goes by, it is being paid off faster and faster. "

    return html.Div(children=[
        dcc.Graph(
            id='mortgage-principle-graph',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': mortgage.remaining_principles_by_year,
                        'type': 'bar',
                        'text': list(map(lambda x: f"{round(x) / 1000}k", mortgage.remaining_principles_by_year)),
                        'hoverinfo': 'text',
                        'name': 'Remaining Mortgage',
                        'marker': {
                            'color': Colors.mortgage_principle_remain_color
                        },
                    },
                ],
                'layout': {
                    'title': 'Remaining Mortgage Principle By Year',
                    'yaxis': {'title': 'Mortgage ($)'},
                    'xaxis': {'title': 'Year'},
                    'legend': {'orientation': 'h'},
                }
            }
        ),
        html.Div(children=mortgage_principle_description),
    ])


def create_buying_investment_graph(x_axis_years: [int], property_value: PropertyValue):
    return html.Div(children=[
        dcc.Graph(
            id='buying-investment-graph-value',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': property_value.value_by_year,
                        'type': 'bar',
                        'name': 'Property Value',
                        "marker": {
                            "color": Colors.property_evaluation_color,
                        },
                    },
                    {
                        'x': x_axis_years,
                        'y': property_value.equity_by_year,
                        'type': 'bar',
                        'name': 'Income by selling',
                        "marker": {
                            "color": Colors.equity_buy_color,
                        },
                    }
                ],
                'layout': {
                    'title': 'Equity Growth with Buying',
                    'yaxis': {'title': 'Value ($)'},
                    'xaxis': {'title': 'Year'},
                    'legend': {'orientation': 'h'},
                }
            }
        ),
        html.Div(children=property_value.description),
    ])


def create_renting_investment_portfolio(x_axis_years: [int], renting_capital: RentingCapital):
    return html.Div(children=[
        dcc.Graph(
            id='renting-investment-graph',
            figure={
                'data': [
                    {
                        'x': x_axis_years,
                        'y': renting_capital.investments,
                        'name': 'Reinvestment',
                        'type': 'bar',
                        "marker": {
                            "color": Colors.reinvestment_for_rent,
                        },
                    },
                    {
                        'x': x_axis_years,
                        'y': renting_capital.capitals,
                        'name': 'Equity',
                        'type': 'bar',
                        "marker": {
                            "color": Colors.equity_rent_color,
                        }
                    },

                ],
                'layout': {
                    'title': 'Equity Growth with Renting',
                    'yaxis': {'title': 'Value ($)'},
                    'xaxis': {'title': 'Year'},
                    'legend': {'orientation': 'h'},
                }
            }
        ),
        html.Div(children=renting_capital.description),
    ])


def create_summary_graph(
        x_axis_years: [int],
        renting_capital: RentingCapital,
        property_value: PropertyValue
):
    if renting_capital.capitals[-1] < property_value.equity_by_year[-1]:
        summary = "💰 You should BUY 💰"
    else:
        summary = "💵 You should RENT 💵"
    return [
        html.H2(children=summary, className="golden_subtitle", style={}),
        create_equity_comparison_graph(x_axis_years, renting_capital, property_value),
    ]
