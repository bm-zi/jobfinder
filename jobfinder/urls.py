from django.urls import path
from .views import (
    home_view,
    history_list_view,
    history_detail_view,
    history_delete_view,
    history_all_delete_view,
    indeed_search_view,
    history_item_save_view,
    job_save_view,
    job_save_edit_view,
    job_list_view,
    job_detail_view,
    job_delete_view,
    jobs_all_delete_view,
    filter_jobs_view,
    filter_list_view,
    filter_detail_view,
    filter_delete_view,
    filters_all_delete_view,
    filter_edit_view,
    about_view,
)

urlpatterns = [
    path('', home_view, name="home_view"),
    path('history-list', history_list_view),
    path('history-detail/<int:history_id>', history_detail_view),
    path('history-delete/<int:history_id>', history_delete_view),
    path('history-all-delete', history_all_delete_view),
    path('indeed-search', indeed_search_view),
    path('history-item-save/<int:history_id>', history_item_save_view),
    path('job-save', job_save_view, name="job_save_view"),
    path('job-save-edit/<int:job_id>', job_save_edit_view, name="job_save_edit_view"),
    path('job-list', job_list_view),
    path('job-detail/<int:job_id>', job_detail_view),
    path('job-delete/<int:job_id>', job_delete_view),
    path('jobs-all-delete', jobs_all_delete_view),
    path('filter-jobs', filter_jobs_view, name="filter_jobs_view"),
    path('filter-list', filter_list_view),
    path('filter-detail/<int:filter_id>', filter_detail_view),
    path('filter-delete/<int:filter_id>', filter_delete_view),
    path('filters-all-delete', filters_all_delete_view),
    path('filter-edit/<int:filter_id>', filter_edit_view, name="filter_edit_view"),
    path('about', about_view, name="about_view"),
]