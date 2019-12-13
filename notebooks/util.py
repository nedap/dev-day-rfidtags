from os.path import join, splitext

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import glob



def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def load_clean_epc_codes():
    clean_epcs = set()

    for labelset in glob.glob('../data/labelset*/samples_labels/'):
        labelset_readings = glob.glob(join(labelset, '*.csv'))
        labelset_epcs = (set(pd.read_csv(csv)['epc']) for csv in labelset_readings)
        clean_epcs.update(set.intersection(*labelset_epcs))
        
    return clean_epcs


def load_samples():
    all_samples = []

    for sample_csv in glob.glob('../data/labelset*/samples_location*/*.csv'):
        _, _, labelset_id, location_id, sample_id = sample_csv.split('/')
        sample_id = splitext(sample_id)[0]

        df_location = pd.read_csv(sample_csv)
        df_location['labelset_id'] = labelset_id
        df_location['location_id'] = location_id
        df_location['sample_id'] = sample_id
        all_samples.append(df_location)

    df_samples = pd.concat(all_samples, sort=True)
    return df_samples