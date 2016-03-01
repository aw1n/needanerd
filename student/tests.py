'''
Created on Jul 27, 2013

@author: josborne
'''
from django.utils import unittest
from student.models import StudentUserCreationForm
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

class Test(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testStudent(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testStudentInvalidEmail(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoeatgmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testNoFirstName(self):
        form_data = {'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testNoLastName(self):
        form_data = {'first_name': 'John',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testMajorTooManyChars(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': '123456789012345678901234567890123',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testStudentDuplicateUserName(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        form.save()
        form2 = StudentUserCreationForm(data=form_data)
        self.assertEqual(form2.is_valid(), False)
        
    def testStudentNewUserName(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe2',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        form.save()
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe3',
                     'password1': 'temppassword',
                     'password2': 'temppassword'}
        form2 = StudentUserCreationForm(data=form_data)
        if form2.is_valid():
            self.assertTrue(True)
        else:
            logger.error('Form2 Errors: ' + str(form2.errors))
            self.assertTrue(False)

    def testStudentPasswordMismatch(self):
        form_data = {'first_name': 'John',
                     'last_name': 'Doe',
                     'email': 'johndoe@gmail.com',
                     'currentmajor': 'Marketing',
                     'username': 'jdoe',
                     'password1': 'temppassword',
                     'password2': 'temppassword2'}
        form = StudentUserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)