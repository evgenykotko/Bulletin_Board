from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bulletin, Author, Reply
from django.contrib.auth.models import User

from .forms import AddBulletinForm, AddReplyBulletinForm
from django.shortcuts import render, redirect


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class BulletinListView(ListView):
    model = Bulletin
    template_name = 'bulletin_list.html'
    context_object_name = 'bulletins'
    ordering = ['-id']


class BulletinView(DetailView):
    model = Bulletin
    template_name = 'bulletin.html'
    context_object_name = 'bulletin'
    form_class = AddReplyBulletinForm

    def get_context_data(self, *args, **kwargs):
        # получение ID объявления
        id = self.kwargs.get('pk')
        # получение и добавление списка отзывов в контекст
        replies = Reply.objects.filter(bulletin__pk=id).values('text_rep', 'user_rep__username')
        # добавление формы отзыва в контекст
        bulletin = Bulletin.objects.get(pk=id)
        reply_form = self.form_class(instance=bulletin)
        return {
            **super().get_context_data(*args, **kwargs),
            'list_reps': replies,
            'reply_form': reply_form,
        }
    # Обработка формы отзыва.
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        id = self.kwargs.get('pk')
        bulletin = Bulletin.objects.get(pk=id)
        if form.is_valid():
            add_rep = form.save(commit=False)
            add_rep.bulletin = bulletin
            add_rep.user_rep = self.request.user
            add_rep.save()
        return redirect(bulletin.get_absolute_url())



class AddBulletin(CreateView):
    # permission_required = ('newsportal.add_post')
    template_name = 'add_bulletin.html'
    form_class = AddBulletinForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            add_bul = form.save(commit=False)
            add_bul.author_bul = Author.objects.get(user=self.request.user)
            add_bul.save()
        return redirect(form.instance.get_absolute_url())


class UpdateBulletin(UpdateView):
    # login_url = '/accounts/login/'
    # permission_required = ('newsportal.change_post')
    template_name = 'add_bulletin.html'
    form_class = AddBulletinForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Bulletin.objects.get(pk=id)

#
class DeleteBulletin(DeleteView):
    # login_url = '/accounts/login/'
    # permission_required = ('newsportal.delete_post')
    template_name = 'deletebulletin.html'
    context_object_name = 'bulletin'
    queryset = Bulletin.objects.all()
    success_url = '/board'

class SearchReplies(ListView):
    model = Reply
    template_name = 'replies_list.html'
    context_object_name = 'replies'
    ordering = ['-id']
    def get_context_data(self, *args, **kwargs):
        # получение ID объявления
        id = self.kwargs.get('pk')
        # получение и добавление списка отзывов в контекст
        repl = Reply.objects.filter(bulletin__pk=id).values('text_rep', 'user_rep__username')
        return {
            **super().get_context_data(*args, **kwargs),
            'list_reps': repl,
        }


class DeleteReply(DeleteView):
    # login_url = '/accounts/login/'
    # permission_required = ('newsportal.delete_post')
    template_name = 'deletereply.html'
    context_object_name = 'replies'
    queryset = Reply.objects.all()
    success_url = '/board/replies'

@login_required
def confirm_rep(request, pk):
    repl = Reply.objects.get(pk=pk)
    repl.confirm()
    return redirect('/board/replies')