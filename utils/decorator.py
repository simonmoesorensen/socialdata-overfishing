from utils.config import colors, font


def style_plot(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            font_family=font,
        )
        return fig

    return wrapper