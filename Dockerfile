FROM jupyter/minimal-notebook

RUN conda install --yes \
    geopandas \
    mplleaflet \
    xlrd
