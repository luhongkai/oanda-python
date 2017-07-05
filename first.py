import os
import plotly.offline as py
import plotly.graph_objs as go
from data_sources import oanda


def display_chart(data, annotations, title):
    layout = go.Layout(title=title, annotations=annotations)
    fig = go.Figure(data=[data], layout=layout)

    py.plot(fig)


def main():
    client = oanda.get_client(os.environ.get('OANDA_API_ACCESS_TOKEN'))

    how_many_hours_back = 48
    bars_in_hour = 4
    bars_count = int(bars_in_hour * how_many_hours_back)

    response = oanda.get_historical_data(client, instrument='EUR_USD', granularity='M15', count=bars_count)

    df, annotations = oanda.get_dataframe_and_annotations(response)

    display_chart(df, annotations, 'EUR/USD, 15min')


if __name__ == "__main__":
    main()
