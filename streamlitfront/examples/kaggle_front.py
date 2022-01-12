import os
import dill
from haggle import KaggleDatasets
import pandas as pd
import numpy as np
import streamlit as st
from slang.snippers import PcaChkToFv, LdaChkToFv
from slang.util import mk_callable

from odat.mdat.local_kgl import mk_dacc
from streamlitfront.session_state import _get_state

# TODO: Replace omodel models with open source ones
from omodel.outliers.outlier_model import OutlierModel as Stroll
from omodel.ml.scent import CentroidSmoothing

# TODO: Resolve the UnhashableTypeError: Cannot hash object of type _thread.Rlock, found in something.


DFLT_FEATURIZER = {'supervised': LdaChkToFv, 'unsupervised': PcaChkToFv}


def search_kaggle(
    keyword_search: str = '', num_to_display: int = 10, metadata: bool = False
):
    s = KaggleDatasets()
    results = s.search(keyword_search)
    if metadata:
        df = pd.DataFrame(results.values())[
            ['ref', 'title', 'subtitle', 'downloadCount', 'totalBytes']
        ]
        df = df.set_index('ref').sort_values('downloadCount', ascending=False)
        st.write(df.head(num_to_display))
    else:
        st.write(list(results)[:10])
    return results


def download_kaggle_dataset(
    state: type(_get_state()), kaggle_path, preview: bool = False
):
    s = KaggleDatasets()
    v = s[kaggle_path]
    if preview:
        st.write(v)
    return kaggle_path


def create_kaggle_dacc(
    # state: type(_get_state()),
    zip_path: type(lambda a: a),
    annots_path: str,
    wrangle_func: type(lambda a: a),
    extension: str = '.wav',
    key_path: str = '',
):
    wrangle_func = dill.load(wrangle_func)
    return mk_dacc(
        zip_path, annots_path, wrangle_func, extension=extension, key_path=key_path,
    )


def build_and_run_model(tag: str, state: type(_get_state())):
    dacc = state['Create Kaggle Dacc']
    chks, tags = zip(*dacc.chk_tag_gen(tag))
    scores, fvs, featurizer, model = produce_results(chks, tags)
    return str(
        'Percentage correct: '
        + str(sum(scores == tags) / len(tags))
        + ' vs. Random guessing: '
        + str(1 / len(set(tags)))
    )


def get_featurizer(chks, tags=None, **kwargs):
    proj_type = 'unsupervised' if (tags is None) else 'unsupervised'
    featurizer = mk_callable('transform')(DFLT_FEATURIZER[proj_type])(**kwargs)
    featurizer.fit(chks, tags)
    return featurizer


def get_outlier_model(fvs, **kwargs):
    # Stroll is already callable, on dim-1 fv
    model = Stroll(**kwargs)
    model.fit(fvs)
    return model


def get_classification_model(fvs, tags, **kwargs):
    CS = mk_callable('predict')(CentroidSmoothing)
    model = CentroidSmoothing(**kwargs)
    return model.fit(fvs, tags)


def produce_results(
    chks,
    tags=None,
    featurizer_kwargs=None,
    classification_model_kwargs=None,
    outlier_model_kwargs=None,
):
    featurizer_kwargs = featurizer_kwargs or {}
    classification_model_kwargs = classification_model_kwargs or {}
    outlier_model_kwargs = outlier_model_kwargs or {}

    featurizer = get_featurizer(chks, tags, **featurizer_kwargs)
    fvs = featurizer(chks)
    if tags is None:
        model = get_outlier_model(fvs, **outlier_model_kwargs)
        scores = np.array(list(map(model, fvs)))
    else:
        model = get_classification_model(fvs, tags, **classification_model_kwargs)
        scores = model(fvs)

    return scores, fvs, featurizer, model


funcs = [
    search_kaggle,
    download_kaggle_dataset,
    create_kaggle_dacc,
    build_and_run_model,
]

if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from streamlitfront.page_funcs import StatePageFunc

    print('file: {}'.format(os.path.realpath(__file__)))

    app = dispatch_funcs(funcs, configs={'page_factory': StatePageFunc})

    app()
