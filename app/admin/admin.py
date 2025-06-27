from sqladmin import ModelView
from app.models.template import Template
from app.models.request_stats import RequestStats
from app.models.application import Application
from app.models.template import Template


class RequestStatsAdminView(ModelView, model=RequestStats):
    name = 'RequestStats'
    column_list = '__all__'


class ApplicationAdminView(ModelView, model=Application):
    name = 'Application'
    column_list = '__all__'


class TemplateAdminView(ModelView, model=Template):
    name = 'Template'
    column_list = '__all__'
