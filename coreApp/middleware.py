
class CheckIfUserIsConnected:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated:
            print("user is connected")
        else:
            print("user not connected")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response