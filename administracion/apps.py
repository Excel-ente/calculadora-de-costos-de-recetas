from django.apps import AppConfig


class AdministracionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administracion'

    def ready(self):
        # django-jazzmin 3.0.2 uses format_html(html_str) with no args.
        # Django 6 raises TypeError in that case, so patch locally.
        self._patch_jazzmin_format_html()
        import administracion.signals

    @staticmethod
    def _patch_jazzmin_format_html():
        try:
            from django.utils.safestring import mark_safe
            import jazzmin.templatetags.jazzmin as jazzmin_tags

            original_format_html = jazzmin_tags.format_html

            def compat_format_html(format_string, *args, **kwargs):
                if not args and not kwargs:
                    return mark_safe(format_string)
                return original_format_html(format_string, *args, **kwargs)

            jazzmin_tags.format_html = compat_format_html
        except Exception:
            # Avoid blocking app startup if jazzmin is unavailable.
            pass