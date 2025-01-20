{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password
{% endblock %}

{% block html %}
http://127.0.0.1:8000/accounts/reset-password/confirm/{{ token }}
{% endblock %}