
from django.contrib.auth.models import User

from base import BaseTest
from django.core.urlresolvers import reverse
from xadmin.views import BaseAdminView, BaseAdminPlugin, ModelAdminView, ListAdminView

from models import ModelA, ModelB, ModelPrimary, ModelSecondary
from adminx import site, normal_site, ModelAAdmin, TestBaseView, TestCommView, \
    TestAView, OptionA, ModelSecondaryAdmin, ModelPrimaryAdmin
from xadmin.plugins.relate import RELATE_PREFIX

class BaseAdminTest(BaseTest):

    def setUp(self):
        super(BaseAdminTest, self).setUp()
        self.test_view_class = site.get_view_class(TestBaseView)
        self.test_view = self.test_view_class(self._mocked_request('test/'))

    def test_get_view(self):
        test_a = self.test_view.get_view(TestAView, OptionA, opts={'test_attr': 'test'})

        self.assertTrue(isinstance(test_a, TestAView))
        self.assertTrue(isinstance(test_a, OptionA))

        self.assertEqual(test_a.option_attr, 'option_test')
        self.assertEqual(test_a.test_attr, 'test')

    def test_model_view(self):
        test_model = self.test_view.get_model_view(ListAdminView, ModelA)

        self.assertTrue(isinstance(test_model, ModelAAdmin))
        self.assertEqual(test_model.model, ModelA)
        self.assertEqual(test_model.test_model_attr, 'test_model')

    def test_admin_url(self):
        test_url = self.test_view.get_admin_url('test')
        self.assertEqual(test_url, '/view_base/test/base')

    def test_model_url(self):
        test_url = self.test_view.get_model_url(ModelA, 'list')
        self.assertEqual(test_url, '/view_base/view_base/modela/list')

    def test_has_model_perm(self):
        test_user = User.objects.create(username='test_user')

        self.assertFalse(self.test_view.has_model_perm(ModelA, 'change', test_user))

        # Admin User
        self.assertTrue(self.test_view.has_model_perm(ModelA, 'change'))


class CommAdminTest(BaseTest):

    def setUp(self):
        super(CommAdminTest, self).setUp()
        self.test_view_class = site.get_view_class(TestCommView)
        self.test_view = self.test_view_class(self._mocked_request('test/comm'))

    def test_model_icon(self):  
        self.assertEqual(self.test_view.get_model_icon(ModelA), 'flag')
        self.assertEqual(self.test_view.get_model_icon(ModelB), 'test')


from django.test import Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
class RelatedPluginTest(BaseTest):
    urls = "normal_urls"

    def setUp(self):
        super(RelatedPluginTest, self).setUp()
        p1 = ModelPrimary()
        p1.name = "primary1"
        p1.save()

        p2 = ModelPrimary()
        p2.name = "primary2"
        p2.save()

        s1 = ModelSecondary()
        s1.name = "secondary1"
        s1.related = p1
        s1.save()

        s2 = ModelSecondary()
        s2.name = "secondary2"
        s2.related = p2
        s2.save()

        self.p1 = p1

        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username="admin", email="test@test.com", password="password")
        self.user.save()
        self.client = Client()
        self.client.login(username="admin", password="password")

    def test_related_filter(self):
        response = self.client.get("/xadmin/view_base/modelprimary/")
        url = reverse('xadmin:view_base_modelsecondary_changelist')
        lookup_name = "related__id__exact"
        lookup = RELATE_PREFIX + lookup_name

        self.assertContains(response, "href=\"%s?%s=%s\"" % (url, lookup, self.p1.pk))

