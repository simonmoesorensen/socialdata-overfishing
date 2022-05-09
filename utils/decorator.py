from utils.config import colors, font


def style_plot(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            font_family=font,
            font_size=20,
            margin=dict(
                t=100
            ),
            width=800,
            height=600,
        )
        return fig

    return wrapper