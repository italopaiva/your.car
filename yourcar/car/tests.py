from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from .models import Car
from .forms import NewUserForm

class YourCarViewsTestCase(TestCase):

    RESPONSE_OK = 200

    def setUp(self):
        self.user1_password = 'chuck'
        self.user1 = User.objects.create_user(username='Chuck', password=self.user1_password)

    def test_signup_get_view(self):
        """ Test if the signup view respond correctly when using GET method """

        url_to_test = reverse('signup')

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        # Check if the new user form is present
        self.assertEqual(str(NewUserForm()), str(response.context['form']))

    def test_signup_post_view(self):
        """ Test if the signup view respond correctly when using GET method """

        url_to_test = reverse('signup')

        post_data = {
            'username': "testuser",
            'password': "testuser",
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        # Check if the user was registered
        user = User.objects.get(username=post_data['username'])
        self.assertEqual(user.username, post_data['username']) 
    
    def test_invalid_password_signup_post_view(self):
        """ Test if the signup view respond correctly when using POST method with invalid password """

        url_to_test = reverse('signup')

        post_data = {
            'username': "testuser",
            # Password greater than 10 chars is invalid
            'password': "testuser1233345",
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'password', ['Ensure this value has at most 10 characters (it has 15).'])

        # Check if the user was not registered
        try:
            user = User.objects.get(username=post_data['username'])
        except:
            user = False
        self.assertEqual(user, False)

    def test_invalid_username_signup_post_view(self):
        """ Test if the signup view respond correctly when using POST method with invalid username"""

        url_to_test = reverse('signup')

        post_data = {
            # Username with invalid chars
            'username': "testuser**&%$$%",
            'password': "testuser",
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'username',
                             [_('Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')])

        # Check if the user was not registered
        try:
            user = User.objects.get(username=post_data['username'])
        except:
            user = False
        self.assertEqual(user, False)

    def test_login_get(self):
        url_to_test = reverse('login')
        response = self.client.get(url_to_test)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

    def test_login_with_valid_user(self):
        
        url_to_test = reverse('login')

        post_data = {
            'username': self.user1.username,
            'password': self.user1_password
        }
        
        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertIn(str(_('Welcome')+', '+self.user1.username+"!"), str(response.content))

    def test_login_with_invalid_user(self):
        
        url_to_test = reverse('login')

        post_data = {
            'username': 'userthatdoesnotexists',
            'password': 'password'
        }
        
        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)
        self.assertIn(_('Please enter a correct username and password. Note that both fields may be case-sensitive.'), str(response.content))

    def test_new_car_view_post(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto",
            'year': "2014",
            'mileage': "300000",
            'name': "Fuscao preto"
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertNotEqual(False, car)

    def test_new_car_view_post_with_invalid_car_model(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca*&$%", # Invalid car_model
            'color': "Preto",
            'year': "2014",
            'mileage': "300000",
            'name': "Fuscao preto"
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'car_model', [_('Car model must have only alphanumeric characters')])

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertEqual(False, car)

    def test_new_car_view_post_with_invalid_color(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto43423", # Invalid color name
            'year': "2014",
            'mileage': "300000",
            'name': "Fuscao preto"
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'color', [_('Car color must have only alphabetical characters')])

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertEqual(False, car)

    def test_new_car_view_post_with_invalid_year(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto43423",
            'year': "204564", # Invalid year
            'mileage': "300000",
            'name': "Fuscao preto"
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'year', [_('Enter a whole number.')])

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertEqual(False, car)

    def test_new_car_view_post_with_invalid_mileage(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto43423",
            'year': "204564",
            'mileage': "-1", # Invalid mileage
            'name': "Fuscao preto"
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'mileage', [_('Ensure this value is greater than or equal to 0.')])

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertEqual(False, car)

    def test_new_car_view_post_with_invalid_name(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto43423",
            'year': "204564",
            'mileage': "-1",
            'name': "Fuscao76&&*(*&" # Invalid name
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        self.assertFormError(response, 'form', 'name', [_('Car name must have only alphanumeric characters')])

        try:
            car = Car.objects.get(owner=self.user1.pk, name="Fuscao preto")
        except:
            car = False
        self.assertEqual(False, car)

    def test_new_car_view_post_with_valid_blank_name(self):

        # Log in with user1
        logged = self.client.login(username=self.user1.username, password=self.user1_password)

        url_to_test = reverse('new_car')

        post_data = {
            'owner': self.user1.pk,
            'car_model': "Fusca",
            'color': "Preto",
            'year': "2014",
            'mileage': "30000",
            'name': "" # Valid blank name
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        try:
            car = Car.objects.get(owner=self.user1.pk, color='Preto')
        except:
            car = False
        self.assertNotEqual(False, car)