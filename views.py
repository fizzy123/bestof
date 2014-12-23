import random, math

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from bestof.models import Category, Nominee
from general.functions import json_response

def categories(request):
    if request.META['REQUEST_METHOD'] == 'GET':
        categories = Category.objects.all()
        return render(request, 'bestof/categories.html', {'categories': categories})
    elif request.META['REQUEST_METHOD'] == 'POST':
        category = Category(title = request.POST['title'],
                            caption = request.POST['caption'])
        category.save()
        return json_response({'category': category.build_category_dict()})

def judge(request, key):
    if request.META['REQUEST_METHOD'] == 'GET':
        context = {}
        context['category'] = Category.objects.get(pk = key)
        nominee_count = len(list(context['category'].nominee_set.all()))
        if nominee_count == 0 or nominee_count == 1:
            return HttpResponseRedirect(reverse('bestof:nominees', args=(key,)))
        else:
            return render(request, 'bestof/judge.html', context)

def nominees(request, key):
    if request.META['REQUEST_METHOD'] == 'GET':
        context = {}
        context['category'] = Category.objects.get(pk = key)
        context['nominees'] = sorted(context['category'].nominee_set.all(), key=lambda nominee: nominee.rating)
        return render(request, 'bestof/list.html', context)
    elif request.META['REQUEST_METHOD'] == 'POST':
        nominee = Nominee(title = request.POST['title'],
                          category = Category.objects.get(pk = key))
        nominee.save()
        return json_response({'nominee': nominee.build_nominee_dict()})


def compare(request, key):
    #gif_num = Gif.objects.count()
    if request.META['REQUEST_METHOD'] == 'GET':
        context = {}
        category = Category.objects.get(pk = key)
        nominees = list(Nominee.objects.all().filter(category=category))
        rand_int = random.randint(0, len(nominees)-1)
        context['nominee1'] = nominees[rand_int].build_nominee_dict()
        del nominees[rand_int]
        context['nominee2'] = nominees[random.randint(0, len(nominees)-1)].build_nominee_dict()
        return json_response(context)
    elif request.META['REQUEST_METHOD'] == 'POST':
        win_nominee=Nominee.objects.get(pk=request.POST['win_nominee'])
        lose_nominee=Nominee.objects.get(pk=request.POST['lose_nominee'])
        
        #Calculate new RD    
        c = 0.45
        t = 600000
        temp_win_rd = math.sqrt(math.pow(win_nominee.rating_deviation,2) + math.pow(c,2)*(timezone.now()-win_nominee.last_updated).seconds)
        if temp_win_rd >350:
            temp_win_rd = 350
        temp_lose_rd = math.sqrt(math.pow(lose_nominee.rating_deviation,2) + math.pow(c,2)*(timezone.now()-lose_nominee.last_updated).seconds)
        if temp_lose_rd > 350:
            temp_lose_rd = 350
        
        #Calculate new rating
        q = math.log(10)/400
        g_win = 1/(math.sqrt(1+3*math.pow(q,2)*math.pow(temp_win_rd,2)/math.pow(math.pi,2)))
        g_lose = 1/(math.sqrt(1+3*math.pow(q,2)*math.pow(temp_lose_rd,2)/math.pow(math.pi,2)))
        e_win = 1/(1+math.pow(10,g_win*(float(win_nominee.rating)-float(lose_nominee.rating))/(-400)))
        e_lose = 1/(1+math.pow(10,g_lose*(float(lose_nominee.rating)-float(win_nominee.rating))/(-400)))
        d2_win = 1/(math.pow(q,2)*math.pow(g_win,2)*e_win*(1-e_win))
        d2_lose = 1/(math.pow(q,2)*math.pow(g_lose,2)*e_win*(1-e_lose))
        win_nominee.rating = str(float(win_nominee.rating) + q/(math.pow(temp_win_rd,-2)+1/d2_win)*g_win*(1-e_win))
        lose_nominee.rating = str(float(lose_nominee.rating) + q/(math.pow(temp_lose_rd,-2)+1/d2_lose)*g_lose*(0-e_lose))

        #Calculate final RD
        win_nominee.rating_deviation = str(math.pow((math.pow(temp_win_rd,-2)+1/d2_win),-0.5))
        lose_nominee.rating_deviation = str(math.pow((math.pow(temp_lose_rd,-2)+1/d2_lose),-0.5))
        
        #save
        win_nominee.save()
        lose_nominee.save()

        return json_response({'success':True})

