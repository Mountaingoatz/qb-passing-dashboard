from dash import dcc

playclock_filter = dcc.RangeSlider(
    id='playclock-filter',
    min=0, max=40,
    step=1, value=[0, 40],
    allowCross=False,
    marks={
        0: '0s', 5: '5s', 10: '10s', 15: '15s',
        20: '20s', 25: '25s', 30: '30s', 35: '35s',
        40: '40s',
    },
    updatemode='drag',
    className='dashboard-range-slider'
) 