'''
Created on Jul 27, 2013

@author: josborne
'''
from django.utils import unittest
from resume.models import Resume, ResumeForm, DegreeForm, SkillForm, CertificationForm
from student.models import Student

class Test(unittest.TestCase):
    
    def setUp(self):
        self.student=Student.objects.create()
        self.resume=Resume(student=self.student)
    
    def testResumeFormNoObjective(self):
        form_data = {'student': self.student}
        form = ResumeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testResumeFormObjective(self):
        form_data = {'student': self.student,
                     'objective': 'My main objective is to be awesome'}
        form = ResumeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
         
    def testDegreeWithoutUniversity(self):
        form_data = {'resume': self.resume,
                     'major': 'Computer Science'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testDegreeWithoutMajor(self):
        form_data = {'resume': self.resume,
                     'university': 'Auburn University'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testDegreeWithoutResume(self):
        form_data = {'major': 'Computer Science',
                     'university': 'Auburn University'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testDegreeMajorMoreThan32Chars(self):
        form_data = {'resume': self.resume,
                     'major': '123456789012345678901234567890123',
                     'university': 'Auburn University'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testDegreeMajor32Chars(self):
        form_data = {'resume': self.resume,
                     'major': '12345678901234567890123456789012',
                     'university': 'Auburn University'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testDegreeUniversityMoreThan32Chars(self):
        form_data = {'resume': self.resume,
                     'university': '123456789012345678901234567890123',
                     'major': 'Computer Science'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
    def testDegreeUniversity32Chars(self):
        form_data = {'resume': self.resume,
                     'university': '12345678901234567890123456789012',
                     'major': 'Computer Science'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testDegree(self):
        form_data = {'resume': self.resume,
                     'university': 'Auburn',
                     'major': 'Computer Science',
                     'date': '12/31/2004',
                     'gpa': '4.0',
                     'honors': 'summa cum laude'}
        form = DegreeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testSkill(self):
        form_data = {'resume': self.resume,
                     'skill': 'Python'}
        form = SkillForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        
    def testCertification(self):
        form_data = {'resume': self.resume,
                     'certification': 'Linux+',
                     'expdate': '12/2015',
                     }
        form = SkillForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        