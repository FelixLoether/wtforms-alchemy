from wtforms_alchemy import SelectField
from wtforms_test import FormTestCase
from wtforms import Form
from werkzeug.datastructures import MultiDict


class Dummy(object):
    fruits = []


class TestSelectField(FormTestCase):
    choices = (
        ('Fruits', (
            ('apple', 'Apple'),
            ('peach', 'Peach'),
            ('pear', 'Pear')
        )),
        ('Vegetables', (
            ('cucumber', 'Cucumber'),
            ('potato', 'Potato'),
            ('tomato', 'Tomato'),
        ))
    )

    def init_form(self, **kwargs):
        class TestForm(Form):
            fruit = SelectField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_understands_nested_choices(self):
        form_class = self.init_form(choices=self.choices)
        form = form_class(
            MultiDict([('fruit', 'invalid')])
        )
        form.validate()

        assert len(form.errors['fruit']) == 1

    def test_understands_functions_as_choices(self):
        form_class = self.init_form(choices=lambda: [])
        form = form_class(
            MultiDict([('fruit', 'invalid')])
        )
        form.validate()

        assert len(form.errors['fruit']) == 1

    def test_option_selected(self):
        form_class = self.init_form(choices=self.choices)

        obj = Dummy()
        obj.fruit = 'peach'
        form = form_class(
            obj=obj
        )
        assert (
            '<option selected="selected" value="peach">Peach</option>' in
            str(form.fruit)
        )
