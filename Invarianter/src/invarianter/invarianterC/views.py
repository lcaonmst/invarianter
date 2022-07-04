from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponseNotAllowed
from django.template import loader
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from meta.views import MetadataMixin
from django.middleware.csrf import get_token
from django.template.loader import render_to_string


from .models import *

# Create your views here.


def index(request):
    recList = getRecursiveList(request.user)
    return render(
        request,
        'invarianterC/index.html',
        {
            'recList': recList,
            'file': ''
        }
    )


def success(request):
    return render(request, 'invarianterC/success.html')


def dirsView(request):
    recList = getRecursiveList(request.user)
    return render(
        request,
        'invarianterC/dirs.html',
        {
            'recList': recList,
        }
    )


def dirsViewDelete(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed
    recList = getRecursiveList(request.user)
    return render(
        request,
        'invarianterC/delete_dirs.html',
        {
            'recList': recList,
        }
    )


def recoverFiles(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed
    recover()
    return redirect('index')


def delete(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed
    recList = getRecursiveList(request.user)
    return render(
        request,
        'invarianterC/delete.html',
        {
            'recList': recList,
            'file': ''
        }
    )


def deleteCurrent(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed
    if kwargs['name'] == 'root':
        return Http404
    try:
        dir = Directory.objects.all().get(name=kwargs['name'])
        if dir.deleted:
            return Http404
        removeObj(dir)
        return redirect('index')
    except:
        try:
            file = File.objects.all().get(name=kwargs['name'])
            if file.deleted:
                return Http404
            removeObj(file)
            return redirect('index')
        except:
            return Http404


def getFile(request, *args, **kwargs):
    try:
        file = File.objects.all().get(name=kwargs['name'], deleted=False)
        f = open(file.text_file.path, "r")
        s = f.read()
        f.close()
        return HttpResponse(s, content_type='text/plain')
    except:
        return Http404


def getSections(request, *args, **kwargs):
    try:
        file = File.objects.all().get(name=kwargs['name'], deleted=False)
        f = open(file.text_file.path, "r")
        s = f.read()
        sections = s.split('\n')
        res = []
        ile = 0
        curr = ''
        for section in sections:
            curr += section + '\n'
            ile += 1
            if ile == 10:
                res.append(curr)
                curr = ''
                ile = 0
        if ile > 0:
            res.append(curr)
        txt = render_to_string('invarianterC/sections.html', {'sections': res})
        return HttpResponse(txt, content_type='text/plain')
    except:
        return Http404


def fileInfo(request, *args, **kwargs):
    if kwargs['name'] == 'root':
        return redirect('index')
    recList = getRecursiveList(request.user)
    try:
        file = File.objects.all().get(name=kwargs['name'])
        if file.deleted:
            return Http404
        f = open(file.text_file.path, "r")
        s = f.read()
        f.close()
        return render(
            request,
            'invarianterC/index.html',
            {
                'recList': recList,
                'file': s
            }
        )
    except:
        try:
            dir = Directory.objects.all().get(name=kwargs['name'])
            if dir.deleted:
                return Http404
            return render(
                request,
                'invarianterC/index.html',
                {
                    'recList': recList,
                    'file': ''
                }
            )
        except:
            return Http404


class DirectoryCreateView(LoginRequiredMixin, CreateView, MetadataMixin):
    model = Directory
    fields = ['name', 'description', 'parent']
    success_url = '/invarianterC/success'

    def form_valid(self, form):
        user = self.request.user
        parentUser = form.instance.parent.user
        if parentUser.is_authenticated and parentUser.username != user.username:
            raise ValidationError(_('Invalid parent'), code='invalid')
        if user.is_authenticated:
            form.instance.user = user
            return super().form_valid(form)
        else:
            raise ValidationError(_('Unauthenticated user'), code='invalid')


class FileCreateView(LoginRequiredMixin, CreateView, MetadataMixin):
    model = File
    fields = ['name', 'description', 'parent', 'text_file']
    success_url = '/invarianterC/success'

    def form_valid(self, form):
        user = self.request.user
        parentUser = form.instance.parent.user
        if parentUser is not None and parentUser.is_authenticated and parentUser.username != user.username:
            raise ValidationError(_('Invalid parent'), code='invalid')
        if user.is_authenticated:
            form.instance.user = user
            return super().form_valid(form)
        else:
            raise ValidationError(_('Unauthenticated user'), code='invalid')
