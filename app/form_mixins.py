
from flask_wtf import Form


class ConditionalDataRequiredMixin(Form):
    """
    WTForms.Form mixin that adds data_required parameter, to control if all fields require data or not.
    Intended to be used with validators.ConditionalDataRequired.
    """

    def __init__(self, *args, **kwargs):
        self.data_required = kwargs.pop('data_required', True)
        super(ConditionalDataRequiredMixin, self).__init__(*args, **kwargs)
