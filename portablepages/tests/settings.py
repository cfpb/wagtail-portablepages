DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "not needed"

ROOT_URLCONF = "portablepages.tests.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "portablepages.sqlite",
    },
}

WAGTAIL_APPS = (
    "wagtail.contrib.forms",
    "wagtail.contrib.settings",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.snippets",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.contrib.styleguide",
    "wagtail",
    "wagtail.test.testapp",
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {"WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea"},
    "custom": {"WIDGET": "wagtail.test.testapp.rich_text.CustomRichTextArea"},
}

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

INSTALLED_APPS = (
    (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "taggit",
    )
    + WAGTAIL_APPS
    + ("portablepages",)
)

STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
]

ROOT_URLCONF = "portablepages.tests.urls"
WAGTAIL_SITE_NAME = "Test Site"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"
