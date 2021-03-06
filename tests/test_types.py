import sqlalchemy as sa
from wtforms.fields import (
    TextField,
    DateTimeField,
    DateField,
    IntegerField,
    TextAreaField,
    BooleanField,
    FloatField,
    DecimalField,
)
from wtforms_alchemy import SelectField, null_or_unicode
from tests import ModelFormTestCase


class TestModelColumnToFormFieldTypeConversion(ModelFormTestCase):
    def test_unicode_converts_to_text_field(self):
        self.init()
        self.assert_type('test_column', TextField)

    def test_string_converts_to_text_field(self):
        self.init(type_=sa.String)
        self.assert_type('test_column', TextField)

    def test_integer_converts_to_integer_field(self):
        self.init(type_=sa.Integer)
        self.assert_type('test_column', IntegerField)

    def test_unicode_text_converts_to_text_area_field(self):
        self.init(type_=sa.UnicodeText)
        self.assert_type('test_column', TextAreaField)

    def test_boolean_converts_to_boolean_field(self):
        self.init(type_=sa.Boolean)
        self.assert_type('test_column', BooleanField)

    def test_datetime_converts_to_datetime_field(self):
        self.init(type_=sa.DateTime)
        self.assert_type('test_column', DateTimeField)

    def test_date_converts_to_date_field(self):
        self.init(type_=sa.Date)
        self.assert_type('test_column', DateField)

    def test_float_converts_to_float_field(self):
        self.init(type_=sa.Float)
        self.assert_type('test_column', FloatField)

    def test_numeric_converts_to_decimal_field(self):
        self.init(type_=sa.Numeric)
        self.assert_type('test_column', DecimalField)

    def test_enum_field_converts_to_select_field(self):
        choices = ['1', '2']
        self.init(type_=sa.Enum(*choices))
        self.assert_type('test_column', SelectField)
        form = self.form_class()
        assert form.test_column.choices == [(s, s) for s in choices]

    def test_nullable_enum_uses_null_or_unicode_coerce_func_by_default(self):
        choices = ['1', '2']
        self.init(type_=sa.Enum(*choices), nullable=True)
        field = self._get_field('test_column')
        assert field.coerce == null_or_unicode

    def test_custom_choices_override_enum_choices(self):
        choices = ['1', '2']
        custom_choices = [('2', '2'), ('3', '3')]
        self.init(type_=sa.Enum(*choices), info={'choices': custom_choices})
        form = self.form_class()
        assert form.test_column.choices == custom_choices

    def test_column_with_choices_converts_to_select_field(self):
        choices = [(u'1', '1'), (u'2', '2')]
        self.init(type_=sa.Integer, info={'choices': choices})
        self.assert_type('test_column', SelectField)
        form = self.form_class()
        assert form.test_column.choices == choices
