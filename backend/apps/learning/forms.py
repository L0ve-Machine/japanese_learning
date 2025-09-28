from django import forms

class DataImportForm(forms.Form):
    file = forms.FileField(
        label='CSVまたはExcelファイル',
        help_text='問題データを含むCSVまたはExcelファイルをアップロードしてください',
        widget=forms.FileInput(attrs={
            'accept': '.csv,.xlsx,.xls',
            'class': 'form-control'
        })
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            if not file.name.endswith(('.csv', '.xlsx', '.xls')):
                raise forms.ValidationError('CSVまたはExcelファイルのみアップロード可能です。')
        return file