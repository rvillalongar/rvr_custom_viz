import string
from pandas.core.frame import DataFrame
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Spectral10, Greys256, Category20_20
from bokeh.models import Legend


class TimelineGraph:
    _dataset: DataFrame=None
    _figure: figure=None
    _palettes: Spectral10
    _tools:string = "hover, box_zoom, undo, crosshair, save"
    _typeColumnName:string=""
    _width=500
    _height=500

    def __init__(self, dataset: DataFrame, typesColumnName: string, width: int = 500, height: int = 500) -> None:
        self._dataset = dataset
        self._figure= figure()
        self._typeColumnName=typesColumnName
        self._width=width
        self._height=height
    
    def fit(self):
        self._figure = figure(
            title='cantidad de tipos de casos en el tiempo',
            plot_width=self._width,
            plot_height=self._height,
            x_axis_label='Month/Year',
            y_axis_label='No Casos',
            y_range=(0, 3500),
            x_axis_type='datetime',
            tools=self._tools
        )
        TOOLTIPS = [("(x,y)", "($createYearMonth, $size)")]
        
        for i, v in enumerate(list(set(self._dataset[self._typeColumnName]))):
            self._figure.line(x='createYearMonth', y='size', legend_label=v, line_color=Category20_20[i],
                              source=self._dataset.loc[self._dataset[self._typeColumnName] == v, :], line_dash=[4, 4])

        
        self._figure.legend.label_text_font_size = '6pt'
        

        hover = self._figure.select(dict(type=HoverTool))
        hover.tooltips = [("value", "@size"), ("date", "@createYearMonth{%F}")]
        hover.formatters = {'@createYearMonth': 'datetime'}
        hover.mode = 'mouse'

        self._figure.add_layout(Legend(), 'right')
        self._figure.legend.click_policy = "hide"
        
        return self._figure

