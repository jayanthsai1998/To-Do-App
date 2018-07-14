from todolistapp.models import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from todolistapp.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ToDoListItemListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ToDoListItem
    template_name = 'todo_list_items.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoListItemListView, self).get_context_data(**kwargs)
        todolistitems = ToDoListItem.objects.filter(**self.kwargs)
        context.update({
            'title': 'TODO List items',
            'todolistitems': todolistitems,
            'todolist_id': self.kwargs.get('todolist_id'),
        })
        return context


class ToDoListItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    model = ToDoListItem
    form_class = ToDoListItemForm
    permission_required = ('todolistapp.add_todolistitem')
    template_name = 'add_todolistitem.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoListItemCreateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Add Todo list item'
        })
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        todolistitem_form = ToDoListItemForm(request.POST)
        todolist_id = self.kwargs.get('todolist_id')
        if todolistitem_form.is_valid():
            todolistitem = todolistitem_form.save(False)
            todolistitem.todolist = ToDoList.objects.get(id=todolist_id)
            todolistitem.save()

        return redirect("todolistitem_list", todolist_id=todolist_id)


class ToDoListItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    model = ToDoListItem
    form_class = ToDoListItemForm
    template_name = 'add_todolistitem.html'
    permission_required = ('todolistapp.edit_todolistitem')

    def get_success_url(self, **kwargs):
        return redirect('todolistitem_list', todolist_id=self.kwargs.get('todolist_id')).url

    def has_permission(self):
        pk = self.kwargs.get('pk')
        todolistitem = get_object_or_404(ToDoListItem, pk=pk)
        if todolistitem:
            return todolistitem.todolist.user == self.request.user
        else:
            self.raise_exception = True
            return

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(ToDoListItemUpdateView, self).handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super(ToDoListItemUpdateView, self).get_context_data(**kwargs)
        context.update({
            'edit': True,
        })
        return context


class ToDoListItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    model = ToDoListItem
    template_name = 'confirm_delete.html'
    permission_required = ('todolistapp.delete_todolistitem')

    def get_success_url(self, **kwargs):
        return redirect('todolistitem_list', todolist_id=self.kwargs.get('todolist_id')).url

    def has_permission(self):
        pk = self.kwargs.get('pk')
        todolistitem = get_object_or_404(ToDoListItem, pk=pk)
        if todolistitem:
            return todolistitem.todolist.user == self.request.user
        else:
            self.raise_exception = True
            return

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(ToDoListItemDeleteView, self).handle_no_permission()