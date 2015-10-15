from xadmin.sites import AdminSite, site as normal_site
from xadmin.views import BaseAdminView, CommAdminView, ListAdminView
from models import ModelA, ModelB, ModelPrimary, ModelSecondary


site = AdminSite('views_base')


class ModelAAdmin(object):
    test_model_attr = 'test_model'
    model_icon = 'flag'


class TestBaseView(BaseAdminView):
    pass


class TestCommView(CommAdminView):
    global_models_icon = {ModelB: 'test'}


class TestAView(BaseAdminView):
    pass


class OptionA(object):
    option_attr = 'option_test'


class ModelPrimaryAdmin(object):
    model = ModelPrimary


class ModelSecondaryAdmin(object):
    model = ModelSecondary


site.register_modelview(r'^list$', ListAdminView, name='%s_%s_list')

site.register_view(r"^test/base$", TestBaseView, 'test')
site.register_view(r"^test/comm$", TestCommView, 'test_comm')
site.register_view(r"^test/a$", TestAView, 'test_a')

site.register(ModelA, ModelAAdmin)
site.register(ModelB)
normal_site.register(ModelPrimary, ModelPrimaryAdmin)
normal_site.register(ModelSecondary, ModelSecondaryAdmin)