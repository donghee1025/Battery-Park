import os
import numpy as np
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

dash.register_page(
    __name__, name="CP Modeling", top_nav=True, path="/modeling-cells"
)

tabs_styles={
     'borderBottom': '1px solid #d6d6d6',
     'padding':'14px',
     'fontWeight':'bold',
     'backgroundColor':'rgb(234, 228, 228)',
     'font-size':'20px',
 }

tab_selected_style = {
     'borderTop':'3px solid rgb(60,28,204)',
     'borderBottom':'1px solid lightgray',
     'backgroundColor':'rgb(234, 228, 228)',#'#119DFF',
     'color':'black',
     'fontWeight':'bold',
     'padding':'14px',
     'font-size':'20px'
     }



tab1 = dbc.Row([
                 dbc.Row([
                     dcc.Markdown('* Estimation of Cycle Life', style={'marginTop':'40px','font-size':'25px','textAlign':'left','font-weight':'bold'}),
                     dcc.Markdown(" This is for estimating cycle life when cells cycle with a specific columbic efficiency each cycles."),
                     dbc.Col([
                         dbc.Row([
                             dcc.Markdown("Option 1: Estimiate Cycle Number ", style={'font-weight':'bold'}),
                             html.Div([html.P('Coulombic Efficiency (%)', style={"height":"auto","margin-bottom":"auto"}),
                                       dcc.Input(id="input_zz", type="number",value="99", step="0.01", multiple=True, style={"margin-bottom":"1em"})]),
                             html.Div([html.P('Capacity Retention (%)', style={"height":"auto","margin-bottom":"auto"}),
                                       dcc.Input(id="input_g", type="number", value="80", step="0.1", style={"margin-bottom":"1em"})]),
                             html.Br(),
                             html.Br(),
                             html.Span(id="option1_outcome", style={"font-size":"150%", "font-weight":"bold"}),
                             dcc.Markdown("Option 2: Estimate required Coulombic Efficiency (%) to achieve N cycle life",style={'font-weight':'bold'}),
                             html.Div([html.P('targeted capacity retention (%)', style={"height":"auto","margin-bottom":"auto"}),
                                       dcc.Input(id="input_cap2", type="number",value="80", step="0.01", multiple=True, style={"margin-bottom":"1em"})]),
                             html.Div([html.P('targeted cycle life', style={"height":"auto","margin-bottom":"auto"}),
                                       dcc.Input(id="input_cycle", type="number", value="100", step="1", style={"margin-bottom":"1em"})]),
                             html.Br(),
                             html.Br(),
                             html.Span(id="option2_outcome", style={"font-size":"150%", "font-weight":"bold"})
                         ],
                         style={"margin-left":"10px","margin-top":"50px"},
                         ),
                     ],
                     width={"size":"6"},
                     xs=12,sm=12, md=10, lg=6, xl=6,
                     ),
                 dbc.Col([
                     # dcc.Loading(
                         # id='loading', type='graph', children=[html.Div(id='cyclelife')]
                     # )
                      dbc.Row([
                          dcc.Graph(id='cyclelife',figure={}, style={"width":"120vh", "height":"50vh","margin-top":"0px"})
                      ])
                 ], width={"size":"6"}, xs=12, sm=12, md=10, lg=6, xl=6,),
                 ])
             ])

tab2=dbc.Row([
    dcc.Markdown('* Estimation of Cycle Life', style={'marginTop':'40px','font-size':'25px','textAlign':'left','font-weight':'bold'}),
    dcc.Markdown(" This is for estimating cycle life when cells cycle with a specific columbic efficiency each cycles."),
    dbc.Col([
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        html.H5('Cathode Parameters', style={"margin-bottom":"0em", "color":"red"}),
                        html.Div([dcc.Markdown('Electrode density (g/cm<sup>3</sup>)', dangerously_allow_html=True, style={"height": "1.3em", "margin-bottom": "auto"}),
                            dcc.Input(id="input-m", type="number", value='0.5', step='0.001', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Electrode thickness (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-n", type="number", value='50', step='0.01', style={"margin-bottom":"1em"}) ]),                      
                        html.Div([html.P('Active material loading ratio', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-o", type="number", value='0.8', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Discharge capacity of active material (mAh/g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-p", type="number", value='150', step='0.1', style={"margin-bottom":"1em"}) ]),
                        html.Div([dcc.Markdown('Electrode area (mm<sup>2</sup>)', dangerously_allow_html=True, style={"height": "1.3em", "margin-bottom": "auto"}),
                            dcc.Input(id="input-q", type="number", value='1500', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Number of layers', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-r", type="number", value='5', step='1', style={"margin-bottom":"1em"}) ]),
                        html.Br(),
                        html.Br(),
                        ],
                    style={'textAlign':'center'},
                    ),
                ],width={"size":3},
                xs=6, sm=6, md=6, lg=3, xl=3,
                ),
                dbc.Col([   
                    dbc.Row([
                        html.H5('Other parameters', style={"margin-bottom":"0.5em", "color":"Purple"}),
                        html.Div([html.P('Total Al foil weight (g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-x", type="number", value='0.7', step='0.001', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Total Cu foil weight (g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-y", type="number", value='1.2', step='0.001', style={"margin-bottom":"1em"}) ]),                      
                        html.Div([html.P('Total separator weight (g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-z", type="number", value='0.5', step='0.001', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Electrolyte weight (g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-ab", type="number", value='3', step='0.001', style={"margin-bottom":"1em"}) ]),              
                        html.Div([html.P('Other weight-Sum (g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-bc", type="number", value='1.1', step='0.001', style={"margin-bottom":"1em"}) ]),                                
                        html.Br(),
                        html.Br(),
                        ],
                    style={'textAlign':'center'},
                    ),
                    ], 
                width={"size":3}, style={'margin-left':'5px'},
                xs=6, sm=6, md=6, lg=3, xl=3,
                ),
                dbc.Col([
                    dbc.Row([
                        html.H5('Anode Parameters', style={"margin-bottom":"1em", "color":"blue"}),
                        html.Div([dcc.Markdown('Electrode density (g/cm<sup>3</sup>)', dangerously_allow_html=True, style={"height": "1.3em", "margin-bottom": "auto"}),
                            dcc.Input(id="input-i", type="number", value='2', step='0.001', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Electrode thickness (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-j", type="number", value='50', step='0.01', style={"margin-bottom":"1em"}) ]),                      
                        html.Div([html.P('Active material loading ratio', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-k", type="number", value='0.9', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Discharge capacity of active material (mAh/g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-l", type="number", value='500', step='0.1', style={"margin-bottom":"1em"}) ]),
                        html.Div([dcc.Markdown('Electrode area (mm<sup>2</sup>)', dangerously_allow_html=True, style={"height": "1.3em", "margin-bottom": "auto"}),
                            dcc.Input(id="input-w", type="number", value='1000', step='0.01', style={"margin-bottom":"1em"}) ]),        
                        html.Br(),
                        html.Br(),
                        ],
                        style={'textAlign':'center'},
                        ),
                        ],
                width={"size":3}, style={'margin-left':'5px'},
                xs=6, sm=6, md=6, lg=3, xl=3,
                ),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Span(id='outcome3', style={"font-size": "150%", "color": "grey", "margin-top": "1em",
                                                "width": "100%",
                                                "justify": "center", "text-align": "left"})),
                                                ],
                                                style = {"margin-top":"1em"}
                                                ),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Span(id='outcome4', style={"font-size": "150%", "color": "grey", "margin-top": "1em",
                                                "width": "100%", "justify": "center",
                                                "text-align": "left"})),
                    ],
                    ),
                ],
                width={"size":3}, style={'margin-left':'5px', "border":"5px black solid", "display":"inline-block", "border-radius":"1em"},
                xs=1, sm=5, md=6, lg=2, xl=2,
                ),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='plot3', style={"width":"100%", "height":"50vh","margin-top":"20px"})
                    ],
                width={"size":"6"},
                xs=6, sm=12, md=10, lg=6, xl=6,                    
                ),
                dbc.Col([    
                    dcc.Graph(id='plot4', style={"width":"100%", "height":"50vh","margin-top":"20px"})
                    ],
                width={"size":"6"},
                xs=6, sm=12, md=10, lg=6, xl=6,
                    ),
                ],
                ),
            ]),

tab3= dbc.Row([
    dbc.Row([
                dbc.Col([
                    html.H1(('Cell Calculator (Jelly-roll Design)'), 
                        style={'textAlign':'left', 'font-weight':'bold','color':'purple'}),
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(('- This calculator can be used to compute the metrics for the cylindrical cell consisting of a jelly-roll of cathode, anode, and separator sheets.'), 
                        style={'textAlign':'left', 'font-size':'20px'}),
                    dcc.Markdown(('- To calculate the cylindrical cell electrode length, Archimedean spiral with a polar coordinate can be used:'), 
                        style={'textAlign':'left', 'font-size':'20px'}),
                    dcc.Markdown(('- For the spiral length:'), 
                        style={'textAlign':'left', 'font-size':'20px', 'font-weight':'bold','margin-left':'40px'}),
                    dcc.Markdown('''$$
                                     L=\\frac{a}{2\pi}(\\frac{\phi_{1}}{2}\\sqrt{\phi_{1}^2+1}+\\frac{1}{2}ln(\phi_{1}+\\sqrt{\phi_{1}^2+1})-\\frac{\phi_{0}}{2}\\sqrt{\phi_{0}^2+1}-\\frac{1}{2}ln(\phi_{0}+\\sqrt{\phi_{0}^2+1}))
                                     $$
                                     ''', mathjax=True, style={'textAlign':'left','font-size':"20px"}),
                    dcc.Markdown(('- Number of windings:'), 
                        style={'textAlign':'left', 'font-size':'20px', 'font-weight':'bold','margin-left':'40px'}),
                    dcc.Markdown('''$$
                                     Nw=\\frac{\phi_{1}-\phi_{0}}{2\pi}
                                     $$
                                     ''', mathjax=True, style={'textAlign':'left','font-size':"20px"}),
                    dcc.Markdown('where $$\phi$$ = rotation angle and $$a$$ = electrode thickness (double-sided cathode thickness + double-sided anode thickness + 2*separator thickness)', mathjax=True, style={'textAlign':'left', 'font-size':'18px', 'font-weight':'bold', 'margin-left':'50px'}),              
                    dcc.Markdown('Note: cell outer diameter = $$\\frac{a}{\pi}\phi_{1}$$ & cell inner diameter = $$\\frac{a}{\pi}\phi_{0}$$', mathjax=True, style={'textAlign':'left', 'font-size':'18px', 'margin-left':'50px'}),              
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    ], width={"size":12},
                xs=8, sm=10, md=12, lg=10, xl=12,
                ),
                ],
            style={'justify':'center','text-align':'left'},
        ),
        dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        html.Div(html.Img(src='https://www.dropbox.com/scl/fi/l4b853tep0e9r52k7oun1/cylindrical-spiral_wcaption.png?rlkey=noe3s94xw0p7rxkhx772b53l9&raw=1', style={"width":"120%", "margin-bottom":"20px"})), 
                        html.Br(),
                        html.Br(),
                        ],
                    style={'textAlign':'center'},
                    ),
                ],width={"size":4},
                xs=6, sm=8, md=6, lg=3, xl=4,
                ),
                dbc.Col([
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        html.H5('Cathode Parameters', style={"margin-bottom":"0em", "color":"red"}),
                        html.Div([html.P('Coating thickness (Single-side) (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c1", type="number", value='60', step='0.001', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Al foil thickness (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c2", type="number", value='15', step='0.1', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Discharge capacity of active material (mAh/g)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c3", type="number", value='200', step='0.1', style={"margin-bottom":"1em"}) ]),                        
                        html.Div([dcc.Markdown('Density of electrode material (g/cm<sup>3</sup>)', dangerously_allow_html=True, style={"height": "1.3em", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c4", type="number", value='4.87', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Active material loading ratio', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c5", type="number", value='0.95', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Estimated porosity', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c6", type="number", value='0.2', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Electrode width (cm)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c7", type="number", value='5', step='0.01', style={"margin-bottom":"1em"}) ]),
                        html.Br(),
                        html.Br(),
                        ],
                    style={'textAlign':'center'},
                    ),
                ],width={"size":4},
                xs=6, sm=8, md=6, lg=5, xl=4,
                ),
                dbc.Col([   
                    dbc.Row([
                        html.H5('Other cell parameters', style={"margin-bottom":"0.5em", "color":"Purple"}),
                        html.Div([html.P('Anode coating thickness (Single-side) (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c8", type="number", value='50', step='0.01', style={"margin-bottom":"1em"}) ]),                      
                        html.Div([html.P('Cu foil thickness (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c9", type="number", value='10', step='0.1', style={"margin-bottom":"1em"}) ]),                      
                        html.Div([html.P('Separator thickness (um)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c10", type="number", value='25', step='0.1', style={"margin-bottom":"1em"}) ]),
                        html.Div([html.P('Outer diameter of the cell (mm)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c11", type="number", value='45', step='0.001', style={"margin-bottom":"1em"}) ]),              
                        html.Div([html.P('Cell Can thickness (mm)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c12", type="number", value='1.5', step='0.001', style={"margin-bottom":"1em"}) ]),              
                        html.Div([html.P('Inner diameter of the cell (mm)', style={"height": "auto", "margin-bottom": "auto"}),
                            dcc.Input(id="input-c13", type="number", value='2', step='0.001', style={"margin-bottom":"1em"}) ]),                                
                        html.Br(),
                        html.Br(),
                        ],
                    style={'textAlign':'center'},
                    ),
                    ], 
                width={"size":4}, style={'margin-left':'0px'},
                xs=6, sm=8, md=6, lg=5, xl=4,
                ),
            ]),
            dbc.Col([
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        html.Span(id='outcome9', style={"font-size":"150%", "color":"blue","margin-top":"2em"}),
                        html.Span(id='outcome10', style={"font-size":"150%", "color":"blue","margin-top":"0em"}),
                        html.Span(id='outcome11', style={"font-size":"150%", "color":"red","margin-top":"0em"}),
                        html.Span(id='outcome12', style={"font-size":"150%", "color":"red","margin-top":"0em"}),
                        ],
                        style={"margin-left":"80px","margin-top":"40px"},
                    ),
                    ],
                    style={'textAlign':'center'}, 
                width={"size":"12"},
                xs=8, sm=10, md=10, lg=12, xl=12,
            )
])

layout = html.Div([
     dcc.Markdown('This pages for giving simple numeric estmiation of cell performance.'),
     dcc.Tabs(id="tabs", value='tab-1', parent_className='custom-tabs', className='custom-tabs-container', children=[
         dcc.Tab(label='A Single Cell',value='tab-1', style=tabs_styles, selected_style=tab_selected_style),
         dcc.Tab(label="Stacked Cell", id='tab-2', style=tabs_styles,selected_style=tab_selected_style),       
         dcc.Tab(label="Jelly-Roll Cell", id='tab-3', style=tabs_styles,selected_style=tab_selected_style),
         ]),
     html.Div(id='tabsclasses')
 ])

@callback(
       Output('tabsclasses','children'),
       Input('tabs', 'value')
 )

def render_content(tab):
    if tab == 'tab-1':
        return tab1  
    elif tab == 'tab-2':
        return tab2
    elif tab == 'tab-3':
        return tab3
    

def option1(zz,g):
    fig=go.Figure()
    if zz and g is not None:
        opt1_cn= np.arange(1,3000,1)
        opt1_cap = np.power(float(zz)/100, opt1_cn)
        find_index = np.argmin(np.abs(np.array(opt1_cap)-(float(g)/100)))
        cycle_life = opt1_cn[find_index]
        cap = float(g)/100

        fig.add_trace(go.Scatter(x=opt1_cn, y=opt1_cap, mode='lines'))
        
        fig.add_trace(go.Scatter(x=[0,cycle_life], y=[0.8,0.8], mode='lines',line=dict(dash='dash',color="gray")))
        fig.add_trace(go.Scatter(x=[cycle_life, cycle_life], y=[0, 0.8], mode='lines',line=dict(dash='dash',color="gray")))
        fig.add_trace(go.Scatter(x=[cycle_life], y=[cap], mode='markers', marker_symbol='circle', marker_size=15))
        fig.update_layout(xaxis_range=[0,cycle_life+100])

        fig.update_layout(
            plot_bgcolor='rgb(234, 228, 228)',
            paper_bgcolor='rgb(211, 211, 211)',
            title=" Coulombic Efficiency vs Capacity Retention",
            title_x=0.5,
            xaxis_title="Coulombic Efficiency (%)",
            yaxis_title="Capacity Retention (%)",
            font=dict(
                family="arial, monospace",
                size=16,
                color="black"
            ),
            showlegend=False
        )
        return dcc.Markdown("The cell is expected to undergo **{}** cycles".format(cycle_life), dangerously_allow_html=True), fig
    else:
        return "",{}



@callback([Output('option1_outcome', 'children'),Output('cyclelife','figure')],[Input('input_zz','value'),Input('input_g','value')])
def update_figure(zz, g):
    if zz and g is not None:
        return option1(zz,g)
    else:
        return dcc.Markdown("It is not working, sorry ")


