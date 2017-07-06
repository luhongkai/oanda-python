from dateutil import parser
import plotly.offline as py
import plotly.graph_objs as go


def get_annotations_from_patterns_info(patterns_info):
    annotations = list()

    if 'pinbar' in patterns_info:
        for pinbar in patterns_info['pinbar']:
            annotations.append({
                'x': parser.parse(pinbar['candle']['time']),
                'showarrow': True,
                'y': pinbar['candle']['highBid'] + 0.00005, 'xref': 'x', 'yref': 'y',
                'text': '{}'.format(pinbar['data']['type'])
            })

    return annotations


def display_chart(data, patterns_info, title):
    layout = go.Layout(title=title, annotations=get_annotations_from_patterns_info(patterns_info))
    fig = go.Figure(data=[data], layout=layout)

    py.plot(fig)
