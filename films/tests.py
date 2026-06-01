from django.test import TestCase, RequestFactory, override_settings
from films import views


@override_settings(DEBUG=False)
class ErrorPageTests(TestCase):
    """
    Проверяем все 4 кастомных обработчика ошибок.
    DEBUG=False обязателен: при True Django игнорирует handler404/500/400/403
    и показывает свои отладочные страницы.
    """

    # ── 404 ──────────────────────────────────────────────────────────────────

    def test_404_status_code(self):
        """Несуществующий URL возвращает статус 404."""
        response = self.client.get('/url-which-does-not-exist/')
        self.assertEqual(response.status_code, 404)

    def test_404_uses_custom_template(self):
        """Django рендерит наш шаблон errors/404.html, а не стандартный."""
        response = self.client.get('/url-which-does-not-exist/')
        self.assertTemplateUsed(response, 'errors/404.html')

    def test_404_html_contains_code(self):
        """Страница 404 содержит цифру 404 в HTML."""
        response = self.client.get('/url-which-does-not-exist/')
        self.assertContains(response, '404', status_code=404)

    # ── 500 ──────────────────────────────────────────────────────────────────

    def test_500_status_code(self):
        """e_handler500 возвращает статус 500."""
        request = RequestFactory().get('/')
        response = views.e_handler500(request)
        self.assertEqual(response.status_code, 500)

    def test_500_uses_custom_template(self):
        """e_handler500 рендерит errors/500.html."""
        request = RequestFactory().get('/')
        response = views.e_handler500(request)
        self.assertIn(b'500', response.content)

    def test_500_html_not_empty(self):
        """Шаблон 500 не пустой (> 100 байт)."""
        request = RequestFactory().get('/')
        response = views.e_handler500(request)
        self.assertGreater(len(response.content), 100)

    # ── 400 ──────────────────────────────────────────────────────────────────

    def test_400_status_code(self):
        """e_handler400 возвращает статус 400."""
        request = RequestFactory().get('/')
        response = views.e_handler400(request, exception=Exception('bad request'))
        self.assertEqual(response.status_code, 400)

    def test_400_uses_custom_template(self):
        """e_handler400 рендерит errors/400.html."""
        request = RequestFactory().get('/')
        response = views.e_handler400(request, exception=Exception('bad request'))
        self.assertIn(b'400', response.content)

    def test_400_html_not_empty(self):
        """Шаблон 400 не пустой (> 100 байт)."""
        request = RequestFactory().get('/')
        response = views.e_handler400(request, exception=Exception('bad request'))
        self.assertGreater(len(response.content), 100)

    # ── 403 ──────────────────────────────────────────────────────────────────

    def test_403_status_code(self):
        """csrf_failure возвращает статус 403."""
        request = RequestFactory().get('/')
        response = views.csrf_failure(request, reason='CSRF token missing')
        self.assertEqual(response.status_code, 403)

    def test_403_uses_custom_template(self):
        """csrf_failure рендерит errors/403.html."""
        request = RequestFactory().get('/')
        response = views.csrf_failure(request, reason='CSRF token missing')
        self.assertIn(b'403', response.content)

    def test_403_html_not_empty(self):
        """Шаблон 403 не пустой (> 100 байт)."""
        request = RequestFactory().get('/')
        response = views.csrf_failure(request, reason='CSRF token missing')
        self.assertGreater(len(response.content), 100)