import datetime
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class SimpleLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log the request method and path
        print(f"[{datetime.datetime.now()}] Request URL: {request.path}")

    def process_response(self, request, response):
        # Log the response status code
        print(f"[{datetime.datetime.now()}] Response Status Code: {response.status_code}")
        return response

    # def process_exception(self, request, exception):
    #     # Log any exceptions that occur during request processing
    #     print(f"[{datetime.datetime.now()}] Exception occurred: {exception}")

class BlockingIPMiddleware(MiddlewareMixin):
    BLOCKED_IPS = ['192.168.1.1', '127.0.0.1']  # Example blocked IPs

    def process_request(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip in self.BLOCKED_IPS:
            return HttpResponse("Access Denied: Your IP is blocked.", status=403)