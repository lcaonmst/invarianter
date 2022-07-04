from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from crequest.middleware import CrequestMiddleware
from django.db.models import Q


# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class UserDirectoryManager(models.Manager):
    def get_queryset(self):
        qs = super(UserDirectoryManager, self).get_queryset()
        request = CrequestMiddleware.get_request()
        user = None
        if request is not None:
            user = request.user
        if user is not None and not user.is_authenticated:
            user = None
        if user is None or not user.is_superuser:
            return qs.filter(Q(user=user) | Q(user__isnull=True))
        else:
            return qs


class Directory(Section):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, default=None)
    objects = UserDirectoryManager()

    def __str__(self):
        return getPath(self)


class File(Section):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE)
    text_file = models.FileField(upload_to='invarianterC/uploads/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, default=None)
    objects = UserDirectoryManager()

    def __str__(self):
        return getPath(self)


sectionCategories = (
    ('1', 'Procedure'),
    ('2', 'Property'),
    ('3', 'Lemma'),
    ('4', 'Assertion'),
    ('5', 'Invariant'),
    ('6', 'Precondition'),
    ('7', 'Postcondition'),
)


sectionStatuses = (
    ('1', 'Proved'),
    ('2', 'Invalid'),
    ('3', 'Counterexample'),
    ('4', 'Unchecked'),
)


class Subsection(Section):
    parent = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    parentSection = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sectionCategory = models.CharField(choices=sectionCategories, max_length=30)
    sectionStatus = models.CharField(choices=sectionStatuses, max_length=30)


def recover():
    for dir in Directory.objects.all():
        dir.deleted = False
        dir.save()
    for file in File.objects.all():
        file.deleted = False
        file.save()


def removeObj(givenObj):
    givenObj.deleted = True
    givenObj.save()
    if type(givenObj) is Directory:
        sons = Directory.objects.all().filter(parent=givenObj)
        for son in sons:
            removeObj(son)
        sons = File.objects.all().filter(parent=givenObj)
        for son in sons:
            removeObj(son)


def getPath(givenObj):
    path = givenObj.name
    if type(givenObj) is Directory:
        path += '/'
    while givenObj.parent is not None:
        givenObj = givenObj.parent
        path = givenObj.name + '/' + path
    return '~' + path[4:]


# def checkPath(path):
#     if len(path) == 0:
#         return None
#     parent = Directory.objects.all().get(name=path[0], parent=None)
#     if len(path) == 1:
#         return parent
#     for part in path[1:-1]:
#         parent = Directory.objects.all().get(name=part, parent=parent)
#     if Directory.objects.all().filter(name=path[-1], parent=parent).count() == 0:
#         return File.objects.all().get(name=path[-1], parent=parent)
#     return Directory.objects.all().get(name=path[-1], parent=parent)


def getRecursiveList(user):
    if Directory.objects.all().count() == 0:
        Directory.objects.create(name="root")
    if not user.is_authenticated:
        user = None

    root = Directory.objects.all().get(name='root')
    recList = []
    getDirChild(recList, root, -1, user)
    return recList


def getDirChild(recList, directory, h, user):
    if directory.name != "root":
        recList.append((directory, h, directory.name, '', 'directory'))
    sons = Directory.objects.all().filter(parent=directory)
    for son in sons:
        if not son.deleted:
            getDirChild(recList, son, h + 1, user)
    sons = File.objects.all().filter(parent=directory)
    for son in sons:
        if not son.deleted:
            getFileChild(recList, son, h + 1)


def getFileChild(recList, file, h):
    recList.append((file, h, file.name, file.text_file.path, 'file'))


