from bokehviz.Pareto.Pareto import Pareto

import pandas as pd
from bokeh.io import push_notebook, show, output_notebook, output_file, save
from bokeh.layouts import row
from bokeh.plotting import figure


dfplot = dftrx.groupby(['createYear', 'createMonth', 'createYearMonth']).agg(
    {'size'})['id'].reset_index()




pareto = Pareto(dfplot, categories_name='submotivos',
                value_name='size', umbral=0.8, width=1020, height=1020)
pareto.set_axis_names(
    'categorias-Motivo-Submotivo de Reclamo', 'Cantidad de casos')
p = pareto.fit()
p.title = "Cantidad de casos de RECLAMO por categoria Motivo-Submotivo con historial completo"
show(p)
