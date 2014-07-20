
from wtforms.validators import DataRequired, StopValidation


class ConditionalDataRequired(DataRequired):
    """
    WTForms validator that extends DataRequired, to only check required if form.data_required is set.
    Depends on form_mixins.ConditionalDataRequiredMixin.
    """

    def __call__(self, form, field):

        if not form.data_required:
            raise StopValidation()

        super(ConditionalDataRequired, self).__call__(form, field)
