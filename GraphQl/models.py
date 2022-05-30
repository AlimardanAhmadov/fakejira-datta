from operator import mod
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import string, random

def id_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ShippingQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.task.delete()
        super(ShippingQuerySet, self).delete(*args, **kwargs)


class Shipping(models.Model):
    product = models.CharField(max_length=50, null=True, blank=True)
    customer = models.CharField(max_length=50, null=True, blank=True)
    shipping_status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']


class StateQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()
        super(StateQuerySet, self).delete(*args, **kwargs)


class State(models.Model):
    slug = models.SlugField(max_length=50, null=True, blank=True)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)

    # location on the workflow chart
    rect_loc = models.CharField(max_length=50, null=True, blank=True)
    connector_loc = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']
    
    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')

        if created:
            instance.slug = slugify(instance.label) 
            instance.save()
 
post_save.connect(State.post_save, sender=State)



class Issue(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    detail = models.CharField(max_length=500, null=True, blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter_assigne')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_assigne')
    issue_status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']
    

class FlowType(models.Model):
    title = models.CharField(max_length=50)
    states = models.ManyToManyField(State, related_name="states", null=True, blank=True)

    def __str__(self):
        return self.title
