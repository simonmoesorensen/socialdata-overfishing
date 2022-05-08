from utils.config import colors

def style_plot(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
        return fig

    return wrapper