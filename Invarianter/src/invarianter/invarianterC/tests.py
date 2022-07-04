from django.test import TestCase
from invarianterC.models import *
from invarianterC.views import *
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from django.contrib.auth.models import User

N = 10


def createRoot():
    Directory.objects.create(name='root')


class SimplePath(TestCase):
    def setUp(self):
        createRoot()
        parent = Directory.objects.get(name='root')
        for i in range(N):
            Directory.objects.create(name=str(i), parent=parent)
            parent = Directory.objects.get(name=str(i))
        File.objects.create(name=str(N), parent=parent)

    def testStructure(self):
        parent = Directory.objects.get(name='root')
        name = '~/'
        for i in range(N):
            name += str(i) + '/'
            parent = Directory.objects.get(parent=parent)
            self.assertEqual(name, parent.__str__())
        parent = File.objects.get(parent=parent)
        name += str(N)
        self.assertEqual(name, parent.__str__())
        removeObj(File.objects.get(name=str(N)))
        recList = getRecursiveList(AnonymousUser)
        self.assertEqual(len(recList), N)


class ViewsTest(TestCase):
    def setUp(self):
        createRoot()
        parent = Directory.objects.get(name='root')
        for i in range(N):
            Directory.objects.create(name=str(i), parent=parent)
            parent = Directory.objects.get(name=str(i))
        File.objects.create(name=str(N), parent=parent)

    def testStructure(self):
        removeObj(File.objects.get(name=str(N)))
        c = Client()
        response = c.get('/invarianterC/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/invarianterC/new/directory/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/new/file/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/delete/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/recover/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/plik/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/sections/sekcja/')
        self.assertEqual(response.status_code, 404)
        response = c.post('/login/', {'id_username': 'nowy', 'id_password': 'nowehasło'})
        print(response.status_code)
        removeObj(Directory.objects.get(name=str(0)))


class ViewsTestLogin(TestCase):
    def setUp(self):
        createRoot()
        parent = Directory.objects.get(name='root')
        for i in range(N):
            Directory.objects.create(name=str(i), parent=parent)
            parent = Directory.objects.get(name=str(i))
        File.objects.create(name=str(N), parent=parent)
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

    def testStructure(self):
        removeObj(File.objects.get(name=str(N)))
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        response = c.get('/invarianterC/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/invarianterC/new/directory/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/new/file/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/delete/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/recover/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/plik/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/invarianterC/sections/sekcja/')
        self.assertEqual(response.status_code, 404)


# Create your tests here.
