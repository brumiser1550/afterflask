from registration.views import RegistrationView


class LoginView(RegistrationView):
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        # add your additional data here
        context['active'] = 0
        return context


class RegisterView(RegistrationView):
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        # add your additional data here
        context['active'] = 1
        return context


class ForgotView(RegistrationView):
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        # add your additional data here
        context['active'] = 2
        return context