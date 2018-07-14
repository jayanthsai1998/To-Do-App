from todolistapp.models import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from todolistapp.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class HomeRedirectView(View):
    def get(self, request):
        return redirect('todolists')


class ToDoListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ToDoList
    template_name = 'todo_list.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoListView, self).get_context_data(**kwargs)
        todolists = ToDoList.objects.filter(user=self.request.user)
        context.update({
            'title': 'TODO Lists',
            'todolists': list(
                map(lambda x: {'list':x, 'count':len(x.todolistitem_set.all())}, todolists)
            ),
        })
        return context


class ToDoListCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    model = ToDoList
    form_class = ToDoListForm
    permission_required = ('todolistapp.add_todolist')
    template_name = 'add_todolist.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoListCreateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Add Todo list'
        })
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        credit_card_form = ToDoListForm(request.POST)

        if credit_card_form.is_valid():
            credit_card = credit_card_form.save(False)
            credit_card.user = user
            credit_card.save()

        return redirect("todolists")


class ToDoListDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = '/login/'
    model = ToDoList
    context_object_name = 'todolist'
    template_name = 'todolist_details.html'
    permission_denied_message = "You don't have permissions to access the requested card."

    def has_permission(self):
        pk = self.kwargs.get('pk')
        credit_card = self.request.user.todolist_set.filter(pk=pk)
        if credit_card:
            return True
        else:
            self.raise_exception = True
            return False

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(ToDoListDetailView, self).handle_no_permission()

    def get_object(self, queryset=None):
        obj = get_object_or_404(ToDoList, **self.kwargs)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ToDoListDetailView, self).get_context_data(**kwargs)
        context.update({
            'title': 'List details',
        })
        return context


class ToDoListUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    model = ToDoList
    form_class = ToDoListForm
    template_name = 'add_todolist.html'
    permission_required = ('todolistapp.edit_todolist')
    success_url = reverse_lazy('todolists')

    def has_permission(self):
        pk = self.kwargs.get('pk')
        credit_card = get_object_or_404(ToDoList, pk=pk)
        if credit_card:
            return credit_card.user == self.request.user
        else:
            self.raise_exception = True
            return

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(ToDoListUpdateView, self).handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super(ToDoListUpdateView, self).get_context_data(**kwargs)
        context.update({
            'edit': True,
        })
        return context


class ToDoListDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    model = ToDoList
    template_name = 'confirm_delete.html'
    permission_required = ('manageapp.delete_creditcard')
    success_url = reverse_lazy('todolists')

    def has_permission(self):
        pk = self.kwargs.get('pk')
        todolist = get_object_or_404(ToDoList, pk=pk)
        if todolist:
            return todolist.user == self.request.user
        else:
            self.raise_exception = True
            return

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(ToDoListDeleteView, self).handle_no_permission()