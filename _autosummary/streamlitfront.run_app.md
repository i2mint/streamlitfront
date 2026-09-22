# streamlitfront.run_app

Launch a streamlit app from a set of functions — the `run_app` entry point.

Functions (and configs) are dill-serialized so they can be passed across the
streamlit bootstrap boundary as command-line args.

### Functions

| `run_app`(funcs[, configs, convention])   |    |
|-------------------------------------------|----|
