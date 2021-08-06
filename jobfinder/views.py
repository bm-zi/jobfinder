from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib import messages

from .forms import SaveJobForm, SearchFilterForm
from .models import Job, JobSearchFilter, JobHistory
from .indeed_job_search import indeed_search_filter
from django.forms.models import model_to_dict

ALLOWED_HOSTS = settings.ALLOWED_HOSTS



# Home Tab - views functions
# ..........................


def home_view(request, *args, **kwargs):
    """ url : / """

    qsf = JobSearchFilter.objects.all()
    filters_list = [x.serialize() for x in qsf]
    filters_name = []
    
    if len(filters_list) > 0:
        for f in filters_list:
            filters_name.append(f['search_filter_name'])
    
    qs = JobHistory.objects.all()
    history_list = [x.serialize() for x in qs]
    
    return render(request, 'home.html', 
                    context={'history_list': history_list, 
                                'filters_name': filters_name}
                    )


def history_list_view(request, *args, **kwargs):
    """ url : /history-list """

    qs = JobHistory.objects.all()
    history_list = [x.serialize() for x in qs]
    
    data = {
        "response": history_list
    }

    return JsonResponse(data)


def history_detail_view(request, history_id, *args, **kwargs):
    """ url : /history-detail/<history_id> """

    data = {"id": history_id }
    status = 200
    
    try:
        obj = JobHistory.objects.get(id=history_id)
        data['ttl'] = obj.ttl
        data['lnk'] = obj.lnk
        data['desc'] = obj.desc

    except:
        data['messgae'] = 'Not found'
        status = 404

    return JsonResponse(data, status=status)


def history_delete_view(request, history_id, *args, **kwargs):
    """ url : /history-delete/<history_id> """

    qs = JobHistory.objects.filter(id=history_id)

    if not qs.exists():
        return JsonResponse({}, status=404)

    obj = qs.first()
    obj.delete()

    return JsonResponse(
        {"message": "Job from history removed"}, status=200)


def history_all_delete_view(request, *args, **kwargs):
    """ url : /history-all-delete """

    if request.method == "POST":
        JobHistory.objects.all().delete()
    
    return JsonResponse({"message": "History has been cleaned up"}, 
                        status=200)


def indeed_search_view(request, *args, **kwargs):
    """ url : /indeed-search """
    
    try:
        filter_name = request.POST['filter_choice']
    
    except:
        return redirect('/')

    qs = JobSearchFilter.objects.filter(search_filter_name=filter_name)
    
    if not qs.exists():
        return JsonResponse({}, status=404)

    filter_selected = qs.first()
    obj = model_to_dict(filter_selected)
    

    with_all_of_these_words = obj['with_all_of_these_words']
    with_the_exact_phrase = obj['with_the_exact_phrase']
    with_at_least_one_of_these_words = obj['with_at_least_one_of_these_words']
    with_none_of_these_words = obj['with_none_of_these_words']
    with_these_words_in_the_title = obj['with_these_words_in_the_title']
    from_this_company = obj['from_this_company']
    
    
    try:
        search_result = indeed_search_filter(
                            with_all_of_these_words, 
                            with_the_exact_phrase, 
                            with_at_least_one_of_these_words,
                            with_none_of_these_words, 
                            with_these_words_in_the_title, 
                            from_this_company)

        if not search_result:
            messages.add_message(request, messages.INFO, 
                    'No job found for selected filter.')

        for el in search_result:
            JobHistory.objects.create(
                ttl=el[0],
                lnk=el[1],
                desc=el[2]
            )

    except Exception as e:
        return JsonResponse({'Message': e}, status=500)

    return redirect('/')


def history_item_save_view(request, history_id, *args, **kwargs):
    """ url : /history-item-save/1 """

    qs = JobHistory.objects.filter(id=history_id)
    if not qs.exists():
        return JsonResponse({}, status=404)

    obj = qs.first()
    title = getattr(obj, 'ttl')
    link = getattr(obj, 'lnk')
    description = getattr(obj, 'desc')
    
    Job.objects.create(
        title=title,
        link=link,
        description=description
    )
    
    obj.delete()

    return JsonResponse({"message": "Job saved"}, status=200)



# Save Jobs Tab - Views Functions
# ...............................

def job_save_view(request, *args, **kwargs):
    """ url : /job-save """

    qs = Job.objects.all()
    jobs_list = [x.serialize() for x in qs]
    saveJobForm = SaveJobForm(request.POST or None)
    next_url = request.POST.get("next") or None
    
    if saveJobForm.is_valid():
        obj = saveJobForm.save(commit=False)
        obj.save()
    
        if request.is_ajax():
            if request.method == 'POST':
                return JsonResponse(obj.serialize(),  status=201)
    
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        saveJobForm = SaveJobForm()
    
    return render(request, 'job_save.html', 
                    context={'saveJobForm': saveJobForm, 
                            'jobs_list': jobs_list})


def job_save_edit_view(request, job_id, *args, **kwargs):
    """ url : /job-save-edit/1 """
    
    qs1 = Job.objects.all()
    jobs_list = [x.serialize() for x in qs1]
    qs2 = Job.objects.filter(id=job_id)

    saveJobForm = SaveJobForm(request.POST or None, 
                                instance=qs2.first())

    next_url = request.POST.get("next") or None
    
    if saveJobForm.is_valid():
        obj = saveJobForm.save(commit=False)
        obj.save()
        saveJobForm = SaveJobForm()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
    
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        saveJobForm = SaveJobForm()

    return render(request, 'job_save_edit.html',
                    context={'saveJobForm': saveJobForm,
                    'jobs_list': jobs_list})


def job_list_view(request, *args, **kwargs):
    """ url : /job-list """

    qs = Job.objects.all()
    jobs_list = [x.serialize() for x in qs]
    data = {"response": jobs_list}
    return JsonResponse(data)


def job_detail_view(request, job_id, *args, **kwargs):
    """ url : /job-detail/1 """

    data = {"id": job_id}
    status = 200

    try:
        obj = Job.objects.get(id=job_id)
        data['title'] = obj.title
        data['link'] = obj.link
        data['description'] = obj.description
    
    except:
        data['messgae'] = 'Not found'
        status = 404
    
    return JsonResponse(data, status=status)



def job_delete_view(request, job_id, *args, **kwargs):
    """ url : /job_detail/1 """

    qs = Job.objects.filter(id=job_id)
    
    if not qs.exists():
        return JsonResponse({}, status=404)

    obj = qs.first()
    obj.delete()
    return JsonResponse({"message": "Job removed"}, status=200)


def jobs_all_delete_view(request, *args, **kwargs):
    """ url : /jobs-all-delete """

    if request.method == "POST":
        Job.objects.all().delete()
    
    return JsonResponse(
            {"message": "All saved jobs has been removed"}, 
            status=200)


# Filter Jobs Tab Views Functions
# ...............................

def filter_jobs_view(request, *args, **kwargs):
    """ url : /filter-jobs """

    qs = JobSearchFilter.objects.all()
    filters_list = [x.serialize() for x in qs]
    searchFilterForm = SearchFilterForm(request.POST or None)
    next_url = request.POST.get("next") or None
    
    if searchFilterForm.is_valid():
        obj = searchFilterForm.save(commit=False)
        obj.save()
    
        if request.is_ajax():
            # if request.method == 'POST':
            return JsonResponse(obj.serialize(),  status=201)
    
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        searchFilterForm = SearchFilterForm()

    return render(request, 'filter_jobs.html', 
                    context={'searchFilterForm': searchFilterForm, 
                             'filters_list': filters_list})


def filter_list_view(request, *args, **kwargs):
    """ url : /filter-list """

    qs = JobSearchFilter.objects.all()
    filters_list = [x.serialize() for x in qs]
    data = { "response": filters_list }
    return JsonResponse(data)


def filter_detail_view(request, filter_id, *args, **kwargs):
    """ url : /filter-detail/1 """
    data = {"id": filter_id}
    status = 200

    try:
        obj = JobSearchFilter.objects.get(id=filter_id)
        data = obj.serialize()
    
    except:
        data['messgae'] = 'Not found'
        status = 404
    
    return JsonResponse(data, status=status)


def filter_delete_view(request, filter_id, *args, **kwargs):
    """ url : /filter-delete/1 """

    qs = JobSearchFilter.objects.filter(id=filter_id)

    if not qs.exists():
        return JsonResponse({}, status=404)

    obj = qs.first()
    obj.delete()

    return JsonResponse({"message": "Search filter removed"}, 
                        status=200)



def filter_edit_view(request, filter_id, *args, **kwargs):
    """ url : /filter-edit/1 """
    
    qs1 = JobSearchFilter.objects.all()
    filters_list = [x.serialize() for x in qs1]
    qs2 = JobSearchFilter.objects.filter(id=filter_id)

    searchFilterForm = SearchFilterForm(request.POST or None, 
                                        instance=qs2.first())

    next_url = request.POST.get("next") or None

    if searchFilterForm.is_valid():
        obj = searchFilterForm.save(commit=False)
        obj.save()
        searchFilterForm = SearchFilterForm()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
    
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        searchFilterForm = SearchFilterForm()

    return render(request, 'filter_jobs_edit.html', 
                    context={'searchFilterForm': searchFilterForm, 
                    'filters_list': filters_list})


def filters_all_delete_view(request, *args, **kwargs):
    """ url : /filters-all-delete """

    if request.method == "POST":
        JobSearchFilter.objects.all().delete()
    
    return JsonResponse(
                {"message": "All search filters has been removed"},
                status=200)

def about_view(request, *args, **kwargs):
    """url: /about """

    return render(request, 'about.html')

