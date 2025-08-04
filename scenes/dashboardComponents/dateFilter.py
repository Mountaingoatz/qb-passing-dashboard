from dash import dcc
from datetime import date, datetime

date_filter = dcc.DatePickerRange(
    id='date-filter',
    display_format='MMM Do, Y',
    min_date_allowed=date(2022, 9, 1),
    max_date_allowed=date(2024, 2, 1),
    initial_visible_month=date(2022, 9, 1),
    start_date=date(2022, 9, 1),
    end_date=date(2024, 2, 1)
) 