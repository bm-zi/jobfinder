from django.db import models
from django.db.models import fields
from ckeditor.fields import RichTextField

# Create your models here.


class JobSearchFilter(models.Model):
    search_filter_name = models.TextField(unique=True, blank=True, null=True)
    with_all_of_these_words = models.TextField(blank=True, null=True)
    with_the_exact_phrase = models.TextField(blank=True, null=True)
    with_at_least_one_of_these_words = models.TextField(blank=True, null=True)
    with_none_of_these_words = models.TextField(blank=True, null=True)
    with_these_words_in_the_title = models.TextField(blank=True, null=True)
    from_this_company = models.TextField(blank=True, null=True)

    def serialize(self):
        # returns a dictionary
        return{
            "id": self.id,
            "search_filter_name": self.search_filter_name,
            "with_all_of_these_words": self.with_all_of_these_words,
            "with_the_exact_phrase": self.with_the_exact_phrase,
            "with_at_least_one_of_these_words": self.with_at_least_one_of_these_words,
            "with_none_of_these_words": self.with_none_of_these_words,
            "with_these_words_in_the_title": self.with_these_words_in_the_title,
            "from_this_company": self.from_this_company
        }


class Job(models.Model):
    title = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    is_applied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "is_applied": self.is_applied
        }


class JobHistory(models.Model):
    ttl = models.TextField(blank=True, null=True)
    lnk = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)

    def serialize(self):
        return{
            "id": self.id,
            "ttl": self.ttl,
            "lnk": self.lnk,
            "desc": self.desc
        }
