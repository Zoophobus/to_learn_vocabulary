from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from django.views import View

import random
import re
import datetime

from .forms import DutchForm, EnglishForm, DateForm, TextForm, TranslationGroupForm, TranslationListForm, TranslationsForm
from .models import English, Dutch, Translation, TranslationGroup
# Create your views here.


def index(request):
    eng = EnglishForm(request.GET)
    dtch = DutchForm(request.GET)
    grp = TranslationGroupForm(request.GET)
    latest = Translation.objects.order_by('-creation_date')[:5]
    translations = [t.english.value + " - " + t.dutch.value for t in latest]
    return render(request,'learn/index.html',
            {   
                'english' : eng,
                'dutch' : dtch,
                'group' : grp,
                'recent' : translations,
                }
        )

def add(request):
    latest = Translation.objects.order_by('-creation_date')[:5]
    translations = [t.english.value + " - " + t.dutch.value for t in latest]
    if request.method == 'POST':
        entries = request.POST.getlist('value') # TODO try and develop a more robust approach
        engEntry = None
        dtchEntry = None
        category = None
        # first we try and either create or obtain the english entry
        try:
            # Create the entries and save them
            engEntry = English(value=entries[0],creation_date=timezone.now())
            engEntry.save()
        except:
            engEntry = English.objects.get(value=entries[0])
        try:
            dtchEntry = Dutch(value=entries[1],creation_date=timezone.now())
            dtchEntry.save()
        except:
            dtchEntry = Dutch.objects.get(value=entries[1])
        
        # then we try and bind them together, along with creating or obtaining the category
        group = TranslationGroupForm(request.POST)
        try: 
            category = TranslationGroup(groupName=group.data['groupName'],created=timezone.now())
            category.save()
        except IntegrityError:
            category = TranslationGroup.objects.get(groupName=group.data['groupName'])
        try:
            data = Translation(english=engEntry,dutch=dtchEntry,creation_date=timezone.now(),translation_key=engEntry.value + '---' + dtchEntry.value)
            data.save()
            data.translation_group.add(category)
            status = True
        except IntegrityError:
            status = False
        latest = Translation.objects.order_by('-creation_date')[:5]
        translations = [t.english.value + " - " + t.dutch.value for t in latest]
        return HttpResponseRedirect(reverse('index'),{
            'english' : EnglishForm(request.GET),
            'dutch' : DutchForm(request.GET),
            'group' : TranslationGroupForm(request.GET),
            'recent' : translations,
            'status' : status,
            })

def options(request):
    if request.method == 'GET':
        form_data = request.GET
        if 'learn_vocabulary' in form_data:
            request.GET.get
            return render(request,'learn/learn_vocabulary.html', 
                    {
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        }
                    )
        elif 'test_vocabulary' in form_data:
            return render(request,'learn/test.html',
                    {
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        }
                    )
        elif 'remove_translation' in form_data:
            return render(request,'learn/remove.html',
                    {
                        'by_groups' : TranslationListForm(request.GET),
                        'everything' : TranslationsForm(request.GET),
                })
    return render(request,'learn/index.html',
            {
                'english' : EnglishForm(request.GET),
                'dutch' : DutchForm(request.GET),
                'group' : TranslationGroupForm(request.GET),
                'recent' : translations,
                }
            )

class Learn(View):
    # this is a weird case where the following static variables
    # do not appear to have the same scope as the class, which
    # is what would normally be expected
    toLearn = list()
    finished = True 
    current_translation = None
    current = None
    def get(self,request):
        if 'return' in request.GET:
            self.finished = True
            latest = Translation.objects.order_by('-creation_date')[:5]
            translations = ', '.join([t.english.value + " - " + t.dutch.value for t in latest])
            return HttpResponseRedirect(reverse('index'),{
                'english' : EnglishForm(request.GET),
                'dutch' : DutchForm(request.GET),
                'group' : TranslationGroupForm(request.GET),
                'recent' : translations,
                })
        elif 'start' in request.GET:
            if self.finished:
                self.toLearn = list()
                if len(request.GET.getlist('translation_list')) > 0:
                    for group in request.GET.getlist('translation_list'):
                        self.toLearn += list(Translation.objects.filter(translation_group__groupName=group))
                elif 'date' in request.GET:
                    upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
                    self.toLearn = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
                else:
                    latest = Translation.objects.order_by('-creation_date')[:5]
                    translations = ', '.join([t.english.value + " - " + t.dutch.value for t in latest])
                    # add a shortened list with the five most recent entries
                    return HttpResponseRedirect(reverse('index'),{
                        'english' : EnglishForm(request.GET),
                        'dutch' : DutchForm(request.GET),
                        'group' : TranslationGroupForm(request.GET),
                        'recent' : translations,
                        })
                random.shuffle(self.toLearn)
                self.finished = False
            try:
                self.current = self.toLearn.pop()
                self.current_translation = self.current.choose()
            except:
                self.finished = True
            return render(request,'learn/learn_vocabulary.html',
                {   
                    'translation' : self.current_translation,
                    'response' : TextForm(request.GET),
                    'completed' : self.finished
                    })
        elif 'next' in request.GET:
            self.current = self.toLearn.pop()
            self.current_translation = self.current.choose()
            if len(self.toLearn) == 0:
                self.finished = True
            return render(request,'learn/learn_vocabulary.html',
                    {
                        'translation' : self.current_translation,
                        'response' : TextForm(request.GET),
                        'completed' : self.finished,
                        'date_form' : DateForm(request.GET),
                        })
        elif 'check' in request.GET:
            attempt = request.GET.getlist('check')[0]
            relevant = list()
            if self.current.english.value == self.current_translation:
                # we look up the attempt in dutch
                relevant = Translation.objects.filter(english=self.current.english)
                for dutch_translations in relevant:
                    if re.sub(r'^the ','',attempt) == re.sub('^the ','',dutch_translations.dutch.value):
                        relevant = relevant.exclude(dutch=dutch_translations.dutch)
                        if len(relevant) > 0:
                            return render(request,'learn/learn_vocabulary.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : [alt.dutch.value for alt in relevant],
                                    'completed' : self.finished,
                                    })
                        else:
                            return render(request,'learn/learn_vocabulary.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : False,
                                    'completed' : self.finished,
                                    })
            else:
                # we look up the attempt in english
                relevant = Translation.objects.filter(dutch=self.current.dutch)
                for english_translations in relevant:
                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',english_translations.english.value):
                        relevant = relevant.exclude(english=english_translations.english)
                        if len(relevant) > 0:
                            return render(request,'learn/learn_vocabulary.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : [alt.english.value for alt in relevant],
                                    'completed' : self.finished,
                                    })
                        else:
                            return render(request,'learn/learn_vocabulary.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : False,
                                    'completed' : self.finished,
                                    })
            return render(request,'learn/learn_vocabulary.html',
                {
                    'translation' : self.current_translation,
                    'response' : attempt,
                    'good_response' : False,
                    'alternatives' : relevant,
                    'completed' : self.finished,
                    })

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)



class Test(View):
    # this is a weird case where the following static variables
    # do not appear to have the same scope as the class, which
    # is what would normally be expected
    vocabularTestList = list()
    current_translation = None
    current = None
    successes=0
    attempts=0
    def get(self,request):
        if 'return' in request.GET:
            latest = Translation.objects.order_by('-creation_date')[:5]
            translations = ', '.join([t.english.value + " - " + t.dutch.value for t in latest])
            return HttpResponseRedirect(reverse('index'),{
                'english' : EnglishForm(request.GET),
                'dutch' : DutchForm(request.GET),
                'group' : TranslationGroupForm(request.GET),
                'recent' : translations,
                })
        elif 'start' in request.GET:
            self.attempts = 0
            self.successes = 0
            self.vocabularTestList = list()
            if len(request.GET.getlist('translation_list')) > 0:
                for group in request.GET.getlist('translation_list'):
                    self.vocabularTestList += list(Translation.objects.filter(translation_group__groupName=group))
            else:
                upperDate =  datetime.date.today().year.__str__() + "-" + datetime.date.today().month.__str__() +'-'+ str(datetime.date.today().day+1)
                self.vocabularTestList = list(Translation.objects.filter(creation_date__range=[request.GET['date'],upperDate]))
            self.current = self.vocabularTestList[random.randrange(0,len(self.vocabularTestList))]
            self.current_translation = self.current.choose()
            return render(request,'learn/test.html',
                {   
                    'translation' : self.current_translation,
                    'response' : TextForm(request.GET),
                    })
        elif 'next' in request.GET:
            self.current = self.vocabularTestList[random.randrange(0,len(self.vocabularTestList))]
            self.current_translation = self.current.choose()
            return render(request,'learn/test.html',
                    {
                        'translation' : self.current_translation,
                        'response' : TextForm(request.GET),
                        'date_form' : DateForm(request.GET),
                        })
        elif 'finish' in request.GET:
            return render(request,'learn/test.html',
                    {
                        'completed' : True,
                        'date_form' : DateForm(request.GET),
                        'by_groups' : TranslationListForm(request.GET),
                        'tried' : self.attempts,
                        'successes' : self.successes,
                        })
        elif 'check' in request.GET:
            attempt = request.GET.getlist('check')[0]
            self.attempts+=1
            relevant = list()
            if self.current.english.value == self.current_translation:
                # we look up the attempt in dutch
                relevant = Translation.objects.filter(english=self.current.english)
                for dutch_translations in relevant:
                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',dutch_translations.dutch.value):
                        self.successes+=1
                        relevant = relevant.exclude(dutch=dutch_translations.dutch)
                        if len(relevant) > 0:
                            return render(request,'learn/test.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : [alt.dutch.value for alt in relevant],
                                    })
                        else:
                            return render(request,'learn/test.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : False,
                                    })
            else:
                # we look up the attempt in english
                relevant = Translation.objects.filter(dutch=self.current.dutch)
                for english_translations in relevant:
                    if re.sub(r'^the ','',attempt) == re.sub(r'^the ','',english_translations.english.value):
                        self.successes+=1
                        relevant = relevant.exclude(english=english_translations.english)
                        if len(relevant) > 0:
                            return render(request,'learn/test.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : [alt.english.value for alt in relevant],
                                    })
                        else:
                            return render(request,'learn/test.html',
                                {
                                    'translation' : self.current_translation,
                                    'response' : attempt,
                                    'good_response' : True,
                                    'alternatives' : False,
                                    })
            return render(request,'learn/test.html',
                {
                    'translation' : self.current_translation,
                    'response' : attempt,
                    'good_response' : False,
                    'alternatives' : relevant,
                    })

    @classmethod
    def as_view(cls,request):
        return cls.get(cls,request)

def delete(request):
    if request.method == 'POST':
        trnsList = request.POST.getlist('translations')
        for key in trnsList:
            print(type(key))
            trnsl = Translation.objects.get(translation_key=key)
            trnsl.delete()
    return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET),
                })

def group(request):
    trnsLst = list()
    if request.method == 'GET':
        grp = request.GET.get('translation_list')[0]
        print(grp)
        return render(request,'learn/remove.html',
            {
                'by_groups' : TranslationListForm(request.GET),
                'everything' : TranslationsForm(request.GET,grp=grp),
                })
