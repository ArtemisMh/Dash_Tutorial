# =====================================================
# ======= produced by: Zeynab Mohseni (Artemis) =======
# ======= Date: Tue 29 Jun 2021, LNU ==================     
# =====================================================   

# ======= Import the libraries =======
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output 
import plotly.express as px
import pandas as pd


# ======= Import the stylesheets =======
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ============= Launch the application ==============
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# ======= Import and preprocessing the datasets =======
df = pd.read_csv('https://plotly.github.io/datasets/iris.csv') 
df = df.rename(columns={"Name": "Species"}) 

opts1 = [{'label' : i, 'value' : i} for i in df.iloc[:,[0,1,2,3]]] 
opts3 = [{'label' : i, 'value' : i} for i in df.iloc[:,[0,1,2,3,4]]] 


# ======= builds the pie chart =======
pie_fig = px.pie(
    data_frame = df,
    names = df['Species'], 
    hole = .3, 
    height = 400,
    title = 'Iris Species (%)',
    color_discrete_sequence=px.colors.qualitative.Dark24 
)

# ======= builds the heatmap =======
heatmap_fig = px.imshow(df.corr(),
    height = 400,
    color_continuous_scale = px.colors.sequential.Bluyl, 
    title = 'Coorelation matrix of Iris variables'
)

# ======= defines all dcc and htmls =======
app.layout = html.Div( 
    children =[
        html.Div(
            className="twelve columns",
            children=[
                html.H2(
                    children='Iris Dataset Analysis Uisng Dash',
                    style={
                        'textAlign': 'center',
                        }
                    ),

                html.Div(
                    children='''
                        Dash: A web application framework for Python.
                    ''',
                    style={
                        'textAlign': 'center',
                        'color': 'gray'
                        }
                    ),
                html.Div([ 
                    html.Div(
                        className='two columns',
                        children=[
                            html.Label(["Select feature ofor X-axis:", 
                                dcc.Dropdown(
                                    id = 'opt1', 
                                    options = opts1, 
                                    value = 'SepalWidth')]),
                        ],
                    ),
                    html.Div(
                        className='four columns',
                        children=[
                            html.Label(["Select feature ofor Y-axis:", 
                                dcc.RadioItems(
                                    id = 'opt2', 
                                    options = opts1, 
                                    value = 'SepalLength', 
                                    labelStyle={'display': 'inline-block', 'text-align': 'justify'} )]),
                        ],   
                    ),
                ], 
                style={"margin": "50px 20px 20px 20px"} # Marign: TOP, RIGHT, BOTTOM, LEFT
                ),
                html.Div(
                    className="twelve columns",
                    children=
                    [
                        html.Div(
                            className='five columns',
                            children=[
                                dcc.Loading(id = "loading-icon1", 
                                children=[html.Div(dcc.Graph(id='line-chart'))], type="circle", color="#2c2c2e"), 
                            ],
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Div(dcc.Graph(id='pie-chart', figure = pie_fig))
                            ],   
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Div(dcc.Graph(id='heatmap-plot', figure = heatmap_fig))
                            ],   
                        ),

                    ],
                    style={"margin": "20px 20px 20px 20px"}
                ),
                html.Div(
                    className="twelve columns",
                    children=
                    [
                        html.Div(
                            className='two columns',
                            children=[
                                html.Label(["Select table columns:", 
                                    dcc.Checklist(
                                        id = 'opt3', 
                                        options = opts3, 
                                        value =  ['SepalWidth','Species'])]),
                            ],   
                        ),
                        html.Div(
                            className='nine columns',
                            children=[
                                html.Div(id='table1', style={"margin-left": "10px", "margin-right": "10px", "margin-botton": "60px"}) 
                            ],
                        ),
                    ],
                    style={"margin": "20px 20px 20px 20px"}
                ),

            ],
        )
])

# ======= defines callback to the table =======
@app.callback(
    Output('table1', 'children'),
    [Input('opt3', 'value')])
def update_table(input1):
    T = dash_table.DataTable(
            columns=[{"name": i, "id": i} 
                     for i in input1], 
            data=df.to_dict('records'), 
            style_cell={'minWidth': 40, 'maxWidth': 40, 'width': 40, 'font_family': 'Arial', 'font_size': '15px','text_align': 'left'},
            style_header=dict(backgroundColor="rgb(239, 243, 255)"),
            style_data=dict(backgroundColor="white"),
            page_size=7,
            fixed_rows={'headers': True},
            style_table={'overflowY': 'auto'},
        )
    return T

# ======= defines callback to the scatter plot =======
@app.callback(
    Output('line-chart', 'figure'),
    Input('opt1', 'value'),
    Input('opt2', 'value'))
def update_graph(input1, input2):

    fig1 = px.scatter(
        data_frame = df,
        x=input1,
        y=input2,
        color= df['Species'],
        height = 400,
        title = 'Clustering Iris Species',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)