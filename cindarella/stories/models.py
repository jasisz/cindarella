import hashlib
from django.core.urlresolvers import reverse
from django.db import models
from django.template import Context, Template
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField


class Story(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    template = models.TextField(null=False, blank=False)

    class Meta:
        verbose_name_plural = 'stories'

    def get_template(self):
        return Template(self.template)

    def __str__(self):
        return self.title


class Attribute(models.Model):
    name = models.CharField(max_length=350, null=False, blank=False)
    story = models.ForeignKey(Story, null=False, blank=False, related_name='attributes')

    class Meta:
        unique_together = ('name', 'story')

    def __str__(self):
        return '{0} | {1}'.format(self.story.title, self.name)


class Option(models.Model):
    text = models.TextField(null=True, blank=True)
    attribute = models.ForeignKey(Attribute, null=False, blank=False, related_name='options')

    def __str__(self):
        return '{0} | {1} | {2}'.format(self.attribute.story.title, self.attribute.name, self.text)


class Variant(MPTTModel):
    hash = models.CharField(primary_key=True, editable=False, max_length=350)
    story = models.ForeignKey(Story, null=False, blank=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    options = models.ManyToManyField(Option, related_name='variants')
    # denormalized options, not to change story already saved, when options changes
    options_dict = JSONField(default='{}')

    def __str__(self):
        return '{0} | {1}'.format(self.story.title, self.hash)

    def get_text(self):
        context = Context(self.options_dict)
        template = self.story.get_template()
        return template.render(context)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = hashlib.sha256(self.get_text().encode('ascii')).hexdigest()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'stories:variant',
            kwargs={
                'story_pk': self.story_id,
                'hash': self.hash,
            }
        )
