from meshed import code_to_dag


@code_to_dag
def audio_anomalies():
    wf = get_audio(audio_source)
    model = train(learner, wf)
    results = apply(model, wf)


audio_anomalies.dot_digraph()

# --------------------------------------------------------------------------------------


from functools import partial
from math import sqrt

import numpy as np
from sklearn.svm import OneClassSVM

from i2 import Sig, FuncFactory

from dol import Pipe
from meshed import DAG
from slang import fixed_step_chunker, SpectralProjector

from meshed.util import conservative_parameter_merge
from omodel.outliers.pystroll import OutlierModel

# from omodel.outliers.outlier_model import StrollDyLib

from omodel.outliers.gmm_stroll import GmmStroll


def mk_featurizer(chk_size=2048, chk_step=None, n_features=4, log_factor: float = 2):
    return SpectralProjector.for_sizes(
        chk_size, n_features=n_features, log_factor=log_factor
    )


DFLT_N_FEATURES = 11


@FuncFactory.wrap(exclude='wf')
def mk_wf_to_fvs(
    wf, chk_size=2048, chk_step=None, n_features=DFLT_N_FEATURES, log_factor: float = 2
):
    chunker = partial(fixed_step_chunker, chk_size=chk_size, chk_step=chk_step)
    featurizer = mk_featurizer(chk_size, n_features=n_features, log_factor=log_factor)
    return list(map(featurizer, chunker(wf)))


# TODO: Make with meshed:
def auto_spectral_anomaly_learner(
    wf,
    chk_size=2048,
    chk_step=None,
    n_features=DFLT_N_FEATURES,
    n_centroids=None,
    log_factor: float = 2,
    learner=OutlierModel(),
    #     learner=GmmStroll(),
    #     learner=OneClassSVM(gamma='auto'),
):
    wf_to_fvs = mk_wf_to_fvs(
        chk_size=chk_size,
        chk_step=chk_step,
        n_features=n_features,
        log_factor=log_factor,
    )

    fvs = wf_to_fvs(wf)
    n_centroids = n_centroids or int(1 + sqrt(n_features))  # TODO: Be more scientific!
    model_obj = learner.fit(np.array(fvs))

    def model_runner(wf):
        fvs = wf_to_fvs(wf)
        if callable(model_obj):
            return np.array(list(map(model_obj, fvs)))
        else:
            return model_obj.predict(fvs)

    return model_runner


# --------------------------------------------------------------------------------------


from recode import decode_wav_bytes
from pathlib import Path
from operator import methodcaller, itemgetter
import numpy as np

file_to_bytes = Pipe(Path, methodcaller('read_bytes'))
wav_file_to_array = Pipe(
    file_to_bytes,
    decode_wav_bytes,
    itemgetter(0),
    np.array,
    np.transpose,
    itemgetter(0),
)

audio_anomalies = audio_anomalies.ch_funcs(
    get_audio=lambda audio_source: wav_file_to_array(audio_source),
    train=auto_spectral_anomaly_learner,
    #     train=lambda learner, wf: auto_spectral_anomaly_learner(wf, learner=learner),  # note: don't need lambda
    apply=lambda model, wf: model(wf),
)

# filepath = '/Users/thorwhalen/Dropbox/_odata/sound/engines/aircraft/Aircraft Engine 01.wav'
# filepath = '/Users/thorwhalen/Dropbox/_odata/sound/guns/01 Gunshot Pistol - Small Caliber - 18 Versions.wav'
#
# from omodel.outliers.pystroll import OutlierModel
#
# tt = audio_anomalies(filepath, learner=OutlierModel(n_centroids=5))
# tt.shape
