from re import DEBUG
import string
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import LinearAxis,Range1d
import math
from bokeh.palettes import Spectral5
from bokeh.models import HoverTool
from pandas.core.frame import DataFrame
import logging
import sys


class Pareto:

    _umbral:float=None
    _dataset:pd.DataFrame=None
    _str_name_categories:string = None
    _str_name_values:string=None
    _str_name_percentageAccumulate = 'percentageAccumulate'
    _str_name_percentaje = 'percentaje'
    _tools = "hover, box_zoom, undo, crosshair, save"
    _p:figure = None
    _height =500
    _width = 500
    _title=''
    _x_axis_label:string= ""
    _y_axis_label:string= ""

    def __init__(self, Dataset: pd.DataFrame, categories_name: string, 
                 value_name: string, umbral: float = 0.8, width: int = 500, height: int = 500):
        self._dataset = Dataset.copy()
        self._str_name_categories = categories_name
        self._str_name_values = value_name
        self._umbral = umbral
        self._width = width
        self._height = height
        self._p = figure()
        self._calculation()
    
    def get_dataset_pareto(self)->pd.DataFrame:
        return self._dataset

    def _calculation(self):
        self._dataset[self._str_name_percentaje] = (self._dataset[self._str_name_values] /
                                                    self._dataset[self._str_name_values].sum() * 100).round(2)

        self._dataset[self._str_name_percentageAccumulate] = self._dataset[self._str_name_percentaje].cumsum()
        self._dataset['umbral'] = self._dataset[self._str_name_percentageAccumulate] <= self._umbral * 100
        self._dataset['umbral_str'] = self._dataset['umbral'].astype(str)
        self._dataset.reset_index(inplace=True)

    def set_axis_names(self, name_x, name_y)->None:
        self._x_axis_label=name_x
        self._y_axis_label=name_y
    
    def fit(self) -> figure:
        self._p = figure(
            x_range=self._dataset[self._str_name_categories],
            plot_width=self._width,
            plot_height=self._height,
            toolbar_sticky=False,
            tools=self._tools,
            toolbar_location="left",
            x_axis_label=self._x_axis_label,
            y_axis_label=self._y_axis_label
        )

        self._p.vbar(
            x=self._str_name_categories,
            top=self._str_name_values,
            width=0.9,
            source=self._dataset,
            line_color='white',
            fill_color=factor_cmap('umbral_str', palette=["red", "green"],
                                   factors=["False", "True"])
            )
        
        self._p.extra_y_ranges = {"percAccCase": Range1d(start=0, end=100)}
        
        self._p.add_layout(LinearAxis(y_range_name="percAccCase"), 'right')

        self._p.line(
            x=self._str_name_categories,
            y=self._str_name_percentageAccumulate,
            color='red',
            source=self._dataset,
            y_range_name='percAccCase'
            )

        hover = self._p.select(dict(type=HoverTool))
        hover.tooltips = [
            ("Cantidad", "@" + self._str_name_values),
            ("Porcentaje", "@"+self._str_name_percentaje),
            ("Porcentaje Accumulado", "@" + self._str_name_percentageAccumulate)]

        hover.mode = 'mouse'

        #p.legend.label_text_font_size = '6pt'
        #p.legend.location = "top_right"
        self._p.xaxis.major_label_orientation = math.pi/2
        #self._p.xaxis.axis_label_text_font_size = "4pt"
      

        return self._p
    

