import json
import logging

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

import id
import views
from appstate import AppState
from investments import RentingCapital, PropertyValue
from mortgage import Mortgage
from rent import Rent
from variable_settings import create_settings_panel

external_scripts = [
]

external_stylesheets = [
    # Bootstrap
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
    # Loading state https://community.plot.ly/t/mega-dash-loading-states/5687/3
    'https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css'
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)
app.title = 'Buy vs Rent'

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

fileHandler = logging.FileHandler("Vancouver.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)

app.server.logger.handlers = []

app.server.logger.addHandler(consoleHandler)
app.server.logger.addHandler(fileHandler)

logger = app.server.logger
logger.setLevel(logging.DEBUG)

app.layout = html.Div(className='container', children=[
    html.H1(className="display-4", children='Buy vs Rent'),
    html.H1(className="display-7", children='The economy of home ownership'),
    html.Br(),
    html.Div(children=create_settings_panel()),
    html.Br(),
    html.Div(id=id.graph_rent_or_buy),
    html.Br(),
    views.create_insights_tabs(),
    html.Div(id=id.memory_state, style={'display': 'none'}),  # Invisible cache
    html.Br(),
    html.Br(),
])


@app.callback(
    Output(id.input_mortgage_load, 'value'),
    [
        Input(id.input_property_sale_price, 'value'),
        Input(id.input_mortgage_down_payment, 'value'),
    ]
)
def calculate_loan(property_sale_price: float, property_down_payment: float):
    logger.log(
        logging.INFO,
        msg=f"Calculate loan property_sale_price={property_sale_price}, property_down_payment={property_down_payment}"
    )
    return property_sale_price - property_down_payment


@app.callback(
    Output(id.input_welcome_tax, 'value'),
    [
        Input(id.input_property_sale_price, 'value'),
    ]
)
def calculate_welcome_tax(property_sale_price):
    logger.log(logging.INFO, msg=f"Calculate welcome tax\n\tproperty_sale_price={property_sale_price}")

    class Ladder(object):
        def __init__(self,
                     price_from_k: float,
                     price_to_k: float,
                     percentage: float):
            self.from_price = price_from_k * 1000
            self.to_price = price_to_k * 1000
            self.percentage = percentage / 100

    ladders = [
        Ladder(0, 50, 0.5),
        Ladder(50, 250, 1.0),
        Ladder(250, 500, 1.5),
        Ladder(500, 1000, 2.0),
        Ladder(1000, float("inf"), 2.5),
    ]

    result = 0
    for ladder in ladders:
        if property_sale_price < ladder.from_price:
            result += 0
        elif property_sale_price > ladder.to_price:
            result += (ladder.to_price - ladder.from_price) * ladder.percentage
        else:
            result += (property_sale_price - ladder.from_price) * ladder.percentage

    return result


@app.callback(
    Output(id.memory_state, 'children'),
    [
        # Rent
        Input(id.input_initial_rent, 'n_submit'), Input(id.input_initial_rent, 'n_blur'),
        Input(id.input_inflation_rate, 'n_submit'), Input(id.input_inflation_rate, 'n_blur'),
        # Property
        Input(id.input_property_sale_price, 'n_submit'), Input(id.input_property_sale_price, 'n_blur'),
        Input(id.input_property_tax, 'n_submit'), Input(id.input_property_tax, 'n_blur'),
        Input(id.input_condo_fee, 'n_submit'), Input(id.input_condo_fee, 'n_blur'),
        Input(id.input_insurance, 'n_submit'), Input(id.input_insurance, 'n_blur'),
        Input(id.input_utility_cost, 'n_submit'), Input(id.input_utility_cost, 'n_blur'),
        Input(id.input_property_appreciation, 'n_submit'), Input(id.input_property_appreciation, 'n_blur'),
        # Mortgage
        Input(id.input_mortgage_load, 'n_submit'), Input(id.input_mortgage_load, 'n_blur'),
        Input(id.input_mortgage_interest_rate, 'n_submit'), Input(id.input_mortgage_interest_rate, 'n_blur'),
        Input(id.input_mortgage_terms, 'value'),
        Input(id.input_mortgage_payments_per_year, 'value'),
        # Purchase Upfront Cost
        Input(id.input_mortgage_down_payment, 'n_submit'), Input(id.input_mortgage_down_payment, 'n_blur'),
        Input(id.input_welcome_tax, 'n_submit'), Input(id.input_welcome_tax, 'n_blur'),
        Input(id.input_legal_fee, 'n_submit'), Input(id.input_legal_fee, 'n_blur'),
        # Other investments
        Input(id.other_investment_roi, 'n_submit'), Input(id.other_investment_roi, 'n_blur'),
    ],
    [
        # Rent
        State(id.input_initial_rent, 'value'),
        State(id.input_inflation_rate, 'value'),
        # Property
        State(id.input_property_tax, 'value'),
        State(id.input_condo_fee, 'value'),
        State(id.input_insurance, 'value'),
        State(id.input_utility_cost, 'value'),
        State(id.input_property_appreciation, 'value'),
        # Mortgage
        State(id.input_mortgage_load, 'value'),
        State(id.input_mortgage_interest_rate, 'value'),
        # Purchase Upfront Cost
        State(id.input_mortgage_down_payment, 'value'),
        State(id.input_welcome_tax, 'value'),
        State(id.input_legal_fee, 'value'),
        # Other investments
        State(id.other_investment_roi, 'value'),
    ])
def update_output(
        # Rent
        initial_rent_n_submit, initial_rent_n_blur,
        inflation_rate_n_submit, inflation_rate_n_blur,
        # Property
        property_sale_price_n_submit, property_sale_price_n_blur,
        property_tax_n_submit, property_tax_n_blur,
        condo_fee_n_submit, condo_fee_n_blur,
        insurance_n_submit, insurance_n_blur,
        utility_cost_n_submit, utility_cost_n_blur,
        property_appreciation_n_submit, property_appreciation_n_blur,
        # Mortgage
        mortgage_load_n_submit, mortgage_load_n_blur,
        mortgage_interest_rate_n_submit, mortgage_interest_rate_n_blur,
        mortgage_terms,
        mortgage_payments_per_year,
        # Purchase Upfront Cost
        mortgage_down_payment_n_submit, mortgage_down_payment_n_blur,
        welcome_tax_n_submit, welcome_tax_n_blur,
        legal_fee_n_submit, legal_fee_n_blur,
        # Other investments
        investment_roi_n_submit, investment_roi_n_blur,
        initial_rent, inflation_rate,
        property_tax, condo_fee, insurance, utility_cost,
        property_appreciation,
        mortgage_loan,
        mortgage_interest_rate,
        mortgage_down_payment,
        welcome_tax,
        legal_fee,
        other_investment_roi,
):
    logger.log(
        logging.INFO,
        msg="Update output: " +
            f"\n\tinitial_rent={initial_rent}" +
            f"\n\tinflation_rate={inflation_rate}" +
            f"\n\tproperty_tax={property_tax}" +
            f"\n\tcondo_fee={condo_fee}" +
            f"\n\tinsurance={insurance}" +
            f"\n\tutility_cost={utility_cost}" +
            f"\n\tproperty_appreciation={property_appreciation}" +
            f"\n\tmortgage_loan={mortgage_loan}" +
            f"\n\tmortgage_interest_rate={mortgage_interest_rate}" +
            f"\n\tmortgage_terms={mortgage_terms}" +
            f"\n\tmortgage_payments_per_year={mortgage_payments_per_year}" +
            f"\n\tmortgage_down_payment={mortgage_down_payment}" +
            f"\n\twelcome_tax={welcome_tax}" +
            f"\n\tlegal_fee={legal_fee}" +
            f"\n\tother_investment_roi={other_investment_roi}"
    )

    inflation_rate = inflation_rate / 100
    mortgage_interest_rate = mortgage_interest_rate / 100
    property_appreciation = property_appreciation / 100
    other_investment_roi = other_investment_roi / 100

    number_of_years = mortgage_terms

    monthly_property_owning_cost = property_tax + condo_fee + insurance + utility_cost

    mortgage = Mortgage.create(
        loan=mortgage_loan,
        annual_interest_rate=mortgage_interest_rate,
        amortization_period=number_of_years,
        annual_payment_count=mortgage_payments_per_year
    )

    rent = Rent.create_rent(initial_monthly_rent=initial_rent, inflation_rate=inflation_rate,
                            number_of_years=number_of_years)

    initial_capital = mortgage_down_payment + welcome_tax + legal_fee
    renting_capital = RentingCapital.create(
        initial_capital=initial_capital,
        return_on_investment=other_investment_roi,
        monthly_property_owning_cost=monthly_property_owning_cost,
        mortgage=mortgage,
        rent=rent,
        number_of_years=number_of_years
    )

    property_initial_value = mortgage_down_payment + mortgage_loan
    property_value = PropertyValue.create(
        initial_value=property_initial_value,
        appreciation_rate=property_appreciation,
        mortgage=mortgage,
        number_of_years=number_of_years,
        real_estate_commission=0.05
    )

    cache = AppState(
        number_of_years=number_of_years,
        rent=rent,
        property_value=property_value,
        renting_capital=renting_capital,
        mortgage=mortgage
    )

    return cache.dump()


@app.callback(
    Output(id.graph_rent_or_buy, 'children'),
    [
        Input(id.memory_state, 'children')
    ]
)
def render_content(state_json):
    state = AppState.from_json(json.loads(state_json))
    return views.create_summary_graph(
        x_axis_years=state.x_axis_years,
        renting_capital=state.renting_capital,
        property_value=state.property_value
    )


@app.callback(
    Output(id.detailed_insights_tab_content, 'children'),
    [
        Input(id.detailed_insights_tab, 'value'),
        Input(id.memory_state, 'children'),
    ]
)
def render_content(tab, state_json):
    state_json = str(state_json)
    state = AppState.from_json(json.loads(state_json))

    logger.log(
        logging.INFO,
        msg=f"Choose tab \n\ttab={tab}"
    )

    if tab == id.TabValue.tab_value_rent:
        return views.create_rental_graph(state.x_axis_years, state.rent)
    elif tab == id.TabValue.tab_value_mortgage_payment:
        return views.create_mortgage_payment_graph(state.x_axis_years, state.mortgage)
    elif tab == id.TabValue.tab_value_remaining_mortgage:
        return views.create_mortgage_principle_graph(state.x_axis_years, state.mortgage)
    elif tab == id.TabValue.tab_value_equity_by_rent:
        return views.create_renting_investment_portfolio(
            state.x_axis_years,
            renting_capital=state.renting_capital
        )
    elif tab == id.TabValue.tab_value_asset_for_buy:
        return views.create_buying_investment_graph(state.x_axis_years, property_value=state.property_value)
    else:
        return None


if __name__ == '__main__':
    app.run_server()
