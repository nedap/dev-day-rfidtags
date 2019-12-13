FROM jupyter/datascience-notebook

ENV NB_USER=jovyan
COPY environment.yml /home/$NB_USER

RUN conda env create -f environment.yml

# activate new conda environment, install ipykernel within it (it won't be present by default)
# and add a new kernel to jupyter with that environment
RUN /bin/bash -c "source activate rfidtags \
  && pip install --quiet ipykernel autopep8 \
  && python -m ipykernel install --user \
      --name rfidtags --display-name \"Python (rfidtags)\""

# Install and enable Jupyter extensions (for plain notebooks)
RUN conda install -c conda-forge jupyter_contrib_nbextensions \
    && jupyter contrib nbextension install --user \
    && jupyter nbextension enable spellchecker/main \
    && jupyter nbextension enable nbextensions_configurator/tree_tab/main \
    && jupyter nbextension enable execute_time/ExecuteTime \
    && jupyter nbextension enable nbextensions_configurator/config_menu/main \
    && jupyter nbextension enable hide_input_all/main \
    && jupyter nbextension enable toc2/main \
