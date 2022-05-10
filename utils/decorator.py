from utils.config import colors, font


def style_plot(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        width = 800 if fig.layout.width is None else fig.layout.width
        height = 600 if fig.layout.height is None else fig.layout.height
        xaxis_showgrid = False if fig.layout.xaxis.showgrid is None else fig.layout.xaxis.showgrid
        yaxis_showgrid = False if fig.layout.yaxis.showgrid is None else fig.layout.yaxis.showgrid

        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            font_family=font,
            font_size=20,
            margin=dict(
                t=100,
                pad=5
            ),
            width=width,
            height=height,
            xaxis=dict(
                showgrid=xaxis_showgrid
            ),
            yaxis=dict(
                showgrid=yaxis_showgrid
            )
        )
        return fig

    return wrapper