from django.db import models

# Create your models here.

class StaticContent(models.Model):
    """
    All the static contents for the normal webpage
    """
    name = models.CharField("Name", max_length=100)
    content = models.TextField("Html-Inhalt", max_length=10000, default="")


    def __unicode__(self):
        return u"%s" %(self.name)


class Media(models.Model):
    """
    All the medias that mentioned ortoloco
    """
    mediafile = models.FileField("Datei", upload_to='medias')
    name = models.CharField("Titel", max_length=200)
    year = models.CharField("Jahr", max_length=4)


    def __unicode__(self):
        return u"%s" %(self.name)


class Download(models.Model):
    """
    All the downloads available on ortoloco.ch
    """
    mediafile = models.FileField("Datei", upload_to='downloads')
    name = models.CharField("Titel", max_length=200)


    def __unicode__(self):
        return u"%s" %(self.name)


class Link(models.Model):
    """
    All the links that are mentioned on ortoloco.ch
    """
    name = models.CharField("Link", max_length=200)
    description = models.CharField("Beschreibung", max_length=400)

    def __unicode__(self):
        return u"%s" %(self.name)

class Politoloco(models.Model):
    email = models.EmailField("E-Mail Adresse")

    def __unicode__(self):
        return u'Politoloco %s' % self.email