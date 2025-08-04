from dash import dcc

time_filter = dcc.RangeSlider(
    id='time-filter',
    min=0,
    max=900,
    step=1,
    value=[0, 900],
    allowCross=False,
    marks={
        0: '0:00',
        225: '3:45',
        450: '7:30',
        675: '11:15',
        900: '15:00',
    },
    updatemode='drag',
    className='dashboard-range-slider'
) 