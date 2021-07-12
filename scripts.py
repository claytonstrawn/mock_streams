import numpy as np
import yt
import trident
import os
from datetime import datetime

def create_number_density_plots(ds):
    #filename with date/time creation to put plots in
    now = datetime.now()
    datestr = now.strftime("%m.%d.%Y %H:%M:%S")
    path = 'savedplots ' + datestr
    pathsave = path + '/'
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
        
    trident.add_ion_fields(ds, ions=['O VI', 'H I', 'NE VIII', 'C IV'], ftype="gas")
    
    yt.SlicePlot(ds, 'x', 'O_p5_number_density').save(pathsave)
    yt.SlicePlot(ds, 'y', 'O_p5_number_density').save(pathsave)
    yt.SlicePlot(ds, 'z', 'O_p5_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'x', 'O_p5_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'y', 'O_p5_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'z', 'O_p5_number_density').save(pathsave)

    yt.SlicePlot(ds, 'x', 'H_p0_number_density').save(pathsave)
    yt.SlicePlot(ds, 'y', 'H_p0_number_density').save(pathsave)
    yt.SlicePlot(ds, 'z', 'H_p0_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'x', 'H_p0_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'y', 'H_p0_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'z', 'H_p0_number_density').save(pathsave)

    yt.SlicePlot(ds, 'x', 'Ne_p7_number_density').save(pathsave)
    yt.SlicePlot(ds, 'y', 'Ne_p7_number_density').save(pathsave)
    yt.SlicePlot(ds, 'z', 'Ne_p7_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'x', 'Ne_p7_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'y', 'Ne_p7_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'z', 'Ne_p7_number_density').save(pathsave)

    yt.SlicePlot(ds, 'x', 'C_p3_number_density').save(pathsave)
    yt.SlicePlot(ds, 'y', 'C_p3_number_density').save(pathsave)
    yt.SlicePlot(ds, 'z', 'C_p3_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'x', 'C_p3_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'y', 'C_p3_number_density').save(pathsave)
    yt.ProjectionPlot(ds, 'z', 'C_p3_number_density').save(pathsave)
