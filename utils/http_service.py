from django.http import HttpRequest

def get_user_ip(request: HttpRequest):
    "Return user ip"
    http_x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if http_x_forwarded_for:
        return http_x_forwarded_for

    return request.META.get("REMOTE_ADDR")