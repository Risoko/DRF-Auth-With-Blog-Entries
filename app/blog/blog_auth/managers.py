from datetime import date

from django.db import models

class CreateUserProfilManager(models.Manager):
    
    def create_profile(self, **kwargs):
        kwargs['date_birth'] = date(
            year=kwargs.pop("birth_year"),
            month=kwargs.pop('birth_month'),
            day=kwargs.pop('birth_day')
        )
        personal_data = self.model(**kwargs)
        personal_data.save()
        return personal_data


        