def execute_pipe(pipe: Iterable):
    for step in pipe:
        inputs = step(**inputs)
    return 


if __name__ == '__main__':
    app = mk_app(
        [execute_pipe],
        config={
            APP_KEY: {'title': 'Pipeline Maker'},
            RENDERING_KEY: {
                Callable: {
                    'execution': {
                        'inputs': {
                            'pipe': {
                                ELEMENT_KEY: MultiSelect,
                                'options': [
                                    {'value': 'blue', 'name': 'Blue'},
                                    {'value': 'white', 'name': 'White'},
                                    {'value': 'red', 'name': 'Red'},
                                ],
                                'item_template': '''
                                    <div>
                                        <strong>{name} &#128512;</strong>
                                    </div>
                                ''',
                            }
                        }
                    }
                }
            },
        },
    )
    app()