import plotly.offline as py
import plotly.graph_objs as go
import charts_generator
import time


def get_annotations_from_patterns_info(patterns_info):
    annotations = list()

    if 'pinbar' in patterns_info:
        for pinbar in patterns_info['pinbar']:
            p_time = pinbar['time'].astimezone(charts_generator.CONVERT_TO_TIMEZONE)
            annotations.append({
                'x': p_time,
                'showarrow': True,
                'y': pinbar['highBid'] + 0.00005, 'xref': 'x', 'yref': 'y',
                'text': '{}'.format(pinbar['type'])
            })

    return annotations


def display_chart(data, patterns_info, title):
    layout = go.Layout(
        title=title,
        annotations=get_annotations_from_patterns_info(patterns_info),
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=True
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=True
        )
    )
    fig = go.Figure(data=[data], layout=layout)
    py.plot(fig)

