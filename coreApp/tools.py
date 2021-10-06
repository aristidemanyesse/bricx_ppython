
def form_to_model(modelform, suffix = 'Form'):
    if suffix and modelform.endswith(suffix):
        return modelform[:-len(suffix)]
    return modelform