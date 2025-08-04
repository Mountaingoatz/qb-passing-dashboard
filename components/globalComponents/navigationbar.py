from dash import html
import dash_bootstrap_components as dbc

navigation_bar = html.Div(
    dbc.NavbarSimple([
        dbc.NavLink('About This App', href='/home', active='exact', id='home-navlink'),
        dbc.NavLink("Interactive Dashboard", href="/dashboard", active='exact', id='dashboard-navlink'),
    ],
        dark=True,
        color='primary',
        brand='NFL QB Passing Tendencies Dashboard',
        brand_href='#',
        className='py-lg-0',
    )
) 