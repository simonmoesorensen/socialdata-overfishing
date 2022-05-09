from dash import Dash, dcc, html, Output, Input, callback_context
import sd_material_ui as sd


def button_array():
    return html.Div(className='button-array',
                    children=[
                        sd.Button('Production',
                                  id='btn-production',
                                  variant='outlined',
                                  n_clicks=0,
                                  style={
                                      'background-color': 'cornflowerblue',
                                      'color': 'var(--text-color-dark)'
                                  }),
                        sd.Button('Supply',
                                  id='btn-supply',
                                  variant='outlined',
                                  n_clicks=0,
                                  style={
                                      'background-color': 'forestgreen',
                                      'color': 'var(--text-color-dark)'
                                  }),
                        sd.Button('Import',
                                  id='btn-import',
                                  variant='outlined',
                                  n_clicks=0,
                                  style={
                                      'background-color': 'indianred',
                                      'color': 'var(--text-color-dark)'
                                  }),
                        sd.Button('Export',
                                  id='btn-export',
                                  variant='outlined',
                                  n_clicks=0,
                                  style={
                                      'background-color': 'rebeccapurple',
                                      'color': 'var(--text-color-dark)'
                                  }),
                    ])
