from typing import Optional

import dash_core_components as dcc
import dash_html_components as html

import id


def settings_title(text: str):
    return html.H4(className="settings_title", children=text)


def settings_label(text: str):
    return html.P(className="settings_label", children=text)


def create_percentage_input(title: str, element_id: str, value: float,
                            frequency: str = "annual"):
    return html.Div(children=[
        settings_label(f"{title} ({frequency})"),
        html.Div(className="input-group", children=[
            dcc.Input(
                className="form-control percentage",
                id=element_id,
                type='number',
                value=value,
                min=-100, max=100, step=1,
                inputmode='numeric'
            ),
            html.Div(className="input-group-append", children=[
                html.Span(className="input-group-text", children="%"),
            ]),
        ])
    ])


def create_money_input(title: str, element_id: str, value: float, step: int = 50, disabled: bool = False,
                       frequency: Optional[str] = "monthly"):
    header = f"{title} ({frequency})" if frequency else title

    return html.Div(children=[
        settings_label(header),
        html.Div(className="input-group", children=[
            dcc.Input(
                className="form-control currency",
                id=element_id,
                type='number',
                value=value,
                min=0, max=1e9, step=step,
                inputmode='numeric',
                disabled=disabled,
            ),
            html.Div(className="input-group-append", children=[
                html.Span(className="input-group-text", children="$"),
            ]),
        ])
    ])


def rental_cost_settings():
    inflation_rate_input_group = create_percentage_input(
        "Inflation rate",
        element_id=id.input_inflation_rate,
        value=2,
    )
    initial_rent_input_group = create_money_input(
        "Rent payment",
        element_id=id.input_initial_rent,
        value=1500
    )
    return html.Div(className="row justify-content-start", children=[
        html.Div(className="col-md-auto", children=initial_rent_input_group),
        html.Div(className="col-md-auto", children=inflation_rate_input_group),
    ])


def purchase_costs_settings():
    property_value = create_money_input(
        "Sale Price",
        element_id=id.input_property_sale_price,
        value=500000,
        step=1000,
        frequency=None
    )

    welcome_tax = create_money_input(
        "Welcome tax",
        id.input_welcome_tax,
        value=8000,
        disabled=True,
        frequency=None
    )

    legal_fee = create_money_input(
        "Legal fee",
        id.input_legal_fee,
        value=1500,
        frequency=None
    )

    property_tax_input_group = create_money_input(
        title="Property tax",
        element_id=id.input_property_tax,
        value=650
    )

    condo_fee_input_group = create_money_input(
        title="Condo fee",
        element_id=id.input_condo_fee,
        value=100
    )

    insurance_input_group = create_money_input(
        title="Insurance",
        element_id=id.input_insurance,
        value=50
    )

    utility_input_group = create_money_input(
        title="Hydro, etc.",
        element_id=id.input_utility_cost,
        value=100
    )

    property_appreciation = create_percentage_input(
        "Appreciation rate",
        element_id=id.input_property_appreciation,
        value=3,
    )

    children = [
        property_value,
        welcome_tax,
        legal_fee,
        property_tax_input_group,
        condo_fee_input_group,
        insurance_input_group,
        utility_input_group,
        property_appreciation,
    ]
    children = list(map(lambda child: html.Div(className="col-md-auto", children=child), children))
    return html.Div(className="row justify-content-start", children=children)


def mortgage_settings():
    down_payment = create_money_input(
        "Down payment",
        id.input_mortgage_down_payment,
        value=100000,
        step=1000,
        frequency=None
    )

    load = create_money_input(
        "Loan",
        value=400000,
        element_id=id.input_mortgage_load,
        step=1000,
        disabled=True,
        frequency=None,
    )

    interest_rates = create_percentage_input(
        "Interest rate",
        element_id=id.input_mortgage_interest_rate,
        value=3,
    )

    amortization_period = html.Div(children=[
        settings_label("Amortization period"),
        dcc.Dropdown(
            id=id.input_mortgage_terms,
            options=[
                {'label': '25 Years', 'value': 25},
                {'label': '20 Years', 'value': 20},
                {'label': '15 Years', 'value': 15},
                {'label': '10 Years', 'value': 10},
            ],
            value=25,
            clearable=False,
        ),
    ])

    payment_frequency = html.Div(children=[
        settings_label("Payment frequency"),
        dcc.Dropdown(
            id=id.input_mortgage_payments_per_year,
            options=[
                {'label': 'Monthly', 'value': 12},
                {'label': 'Semimonthly', 'value': 24},
                {'label': 'Weekly', 'value': 52},
            ],
            value=12,
            clearable=False,
        )
    ])

    return html.Div(className="row", children=[
        html.Div(className="col-md-auto", children=down_payment),
        html.Div(className="col-md-auto", children=load),
        html.Div(className="col-md-auto", children=amortization_period),
        html.Div(className="col-md-auto", children=interest_rates),
        html.Div(className="col-md-auto", children=payment_frequency),
    ])


def other_investment_settings():
    inflation_rate_input_group = create_percentage_input(
        "ROI",
        element_id=id.other_investment_roi,
        value=3,
    )
    return html.Div(className="row justify-content-start", children=[
        html.Div(className="col-md-auto", children=inflation_rate_input_group),
    ])


def create_settings_panel():
    return [
        html.Table(children=[
            html.Tr(children=[
                html.Th(children=settings_title("Rent")),
                html.Th(children=rental_cost_settings()),
            ]),
            html.Tr(children=[
                html.Th(children=settings_title("Property")),
                html.Th(children=purchase_costs_settings())
            ]),
            html.Tr(children=[
                html.Th(children=settings_title("Mortgage")),
                html.Th(children=mortgage_settings()),
            ]),
            html.Tr(children=[
                html.Th(children=settings_title("Other Investments")),
                html.Th(children=other_investment_settings())
            ]),
        ]),
    ]
