from django import forms

from dynamicForm.models import ProfileInterest, Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        interests = ProfileInterest.objects.filter(
            profile=self.instance
        )
        for i in range(len(interests) + 1):
            field_name = 'interest_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = interests[i].interest
            except IndexError:
                self.initial[field_name] = ""
        # create an extra blank field
        field_name = 'interest_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)
        self.fields[field_name] = ""

    def clean(self):
        interests = set()
        i = 0
        field_name = 'interest_%s' % (i,)
        while self.cleaned_data.get(field_name):
            interest = self.cleaned_data[field_name]
            if interest in interests:
                self.add_error(field_name, 'Duplicate')
            else:
                interests.add(interest)
            i += 1
            field_name = 'interest_%s' % (i,)

        self.cleaned_data["interests"] = interests

    def save(self, commit=True):
        profile = self.instance
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]

        profile.interest_set.all().delete()
        for interest in self.cleaned_data["interests"]:
            ProfileInterest.objects.create(
                profile=profile,
                interest=interest,
            )

    def get_interest_fields(self):
        for field_name in self.fields:
            if field_name.startswith('interest_'):
                yield self[field_name]

    class Meta:
        model = Profile
        fields = '__all__'


class MyForm(forms.Form):
    original_field = forms.CharField()
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.CharField()