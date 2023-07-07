# Add dropdowns
button_layer_1_height = 1.08


def updated_layout(fig):
    fig.update_layout(updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["ticker", "AAPL"],
                    label="Apple",
                    method="restyle"
                ),
                dict(
                    args=["ticker", "MSFT"],
                    label="Microsoft",
                    method="restyle"
                ),
                dict(
                    args=["ticker", "GOOG"],
                    label="Google",
                    method="restyle"
                ),
                dict(
                    args=["ticker", "TSLA"],
                    label="Tesla",
                    method="restyle"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
        dict(
            buttons=list([
                dict(
                    args=["chart_type", False],
                    label="Live",
                    method="restyle"
                ),
                dict(
                    args=["chart_type", True],
                    label="Historical",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.37,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
        dict(
            buttons=list([
                dict(
                    args=["period", "1d"],
                    label="1 Day",
                    method="restyle"
                ),
                dict(
                    args=["period", "2d"],
                    label="2 Day",
                    method="restyle"
                ),
                dict(
                    args=["period", "5d"],
                    label="5 Day",
                    method="restyle"
                ),
                dict(
                    args=["period", "7d"],
                    label="7 Day",
                    method="restyle"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.58,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
    ])

    fig.update_layout(annotations=[
        dict(text="Select Stock", x=0, xref="paper", y=1.06, yref="paper",
             align="left", showarrow=False),
        dict(text="Chart Type", x=0.25, xref="paper", y=1.07,
             yref="paper", showarrow=False),
        dict(text="Period", x=0.54, xref="paper", y=1.06, yref="paper",
             showarrow=False)
    ])

    return fig