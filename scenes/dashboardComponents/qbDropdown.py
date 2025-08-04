from dash import dcc

qb_dropdown = dcc.Dropdown(
    id='qb-select', multi=False, placeholder='Select Quarterback...',
    options=[],
    searchable=True,
    clearable=False,
    value='J.Allen',  # Default to Josh Allen
    persistence=True,
    className='mb-3'
) 