import hashlib
import random
import bleach
from django.core.urlresolvers import reverse
from django.db import models
from django.template import Context, Template
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField


class Story(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    template = models.TextField(null=False, blank=False)
    max_mutations = models.IntegerField(null=False, blank=False)
    min_mutations = models.IntegerField(null=False, blank=False, default=1)

    class Meta:
        verbose_name_plural = 'stories'

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
    body = JSONField(null=True, blank=True, default='{}')
    attribute = models.ForeignKey(Attribute, null=False, blank=False, related_name='options')

    def __str__(self):
        return '{0} | {1} | {2}'.format(self.attribute.story.title, self.attribute.name, self.body)


class Variant(MPTTModel):
    hash = models.CharField(primary_key=True, editable=False, max_length=350)
    story = models.ForeignKey(Story, null=False, blank=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    options = models.ManyToManyField(Option, related_name='variants')
    # denormalized fields, not to change variant already saved, when something changes in template or options
    template = models.TextField(null=False, blank=False)
    options_dict = JSONField(default='{}')

    def __str__(self):
        return '{0} | {1}'.format(self.story.title, self.hash)

    def get_template(self):
        return Template(self.template)

    def mutate(self):
        child = Variant(
            parent=self,
            story=self.story,
            template=self.story.template,
        )
        mutated_options = []
        options = list(self.options.all())
        attributes = list(self.story.attributes.all())

        if len(options) > self.story.max_mutations:
            for i in range(random.randint(self.story.min_mutations, self.story.max_mutations)):
                change_option = random.choice(options)
                options.remove(change_option)
                choose_from = list(change_option.attribute.options.all())
                choose_from.remove(change_option)
                mutated_options.append(random.choice(choose_from))

        all_options = mutated_options + options
        # this is for attributes that were not in parent story (possible new ones)
        used_attributes = [option.attribute for option in all_options]
        all_options += [random.choice(attribute.options.all()) for attribute in attributes if attribute not in used_attributes]

        child.options_dict = {option.attribute.name: option.body for option in all_options}
        child.hash = child.calculate_hash()

        try:
            return Variant.objects.get(story=self.story, hash=child.hash)
        except Variant.DoesNotExist:
            child.save()
            child.options.add(*all_options)
            return child

    def get_text(self):
        context = Context(self.options_dict)
        template = self.get_template()
        text = template.render(context)
        return bleach.clean(text)

    def calculate_hash(self):
        return hashlib.md5(self.get_text().encode('ascii')).hexdigest()

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'stories:variant',
            kwargs={
                'story_pk': self.story_id,
                'pk': self.hash,
            }
        )

    def get_share_url(self):
        return reverse(
            'share',
            kwargs={
                'story_pk': self.story_id,
                'pk': self.hash,
            }
        )
