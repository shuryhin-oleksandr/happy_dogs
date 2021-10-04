import calendar
from datetime import date
from django import forms


class BoardingFilterForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        first_month_day, last_month_day = calendar.monthrange(today.year, today.month)
        self.fields['start_date'].initial = today.replace(day=first_month_day)
        self.fields['end_date'].initial = today.replace(day=last_month_day)

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date is None:
            self.data['start_date'] = self.fields['start_date'].initial
            return self.fields['start_date'].initial
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date is None:
            self.data['end_date'] = self.fields['end_date'].initial
            return self.fields['end_date'].initial
        return end_date
