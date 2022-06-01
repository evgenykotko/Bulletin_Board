from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bulletin, Author, Reply, Guild
from django.contrib.auth.models import User
from .filters import RepliesFilter

from .forms import AddBulletinForm, AddReplyBulletinForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models.signals import post_save


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class BulletinListView(ListView):
    model = Bulletin
    template_name = 'bulletin_list.html'
    context_object_name = 'bulletins'
    ordering = ['-id']
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'is_not_author': not self.request.user.groups.filter(name='author').exists(),
            'is_author': self.request.user.groups.filter(name='author').exists(),
        }


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
            # Отправляем письмо автору объявления
            send_mail(
                subject=f'Объявлению {add_rep.bulletin} добавлен новый отклик',
                message=f'Пользователь {add_rep.user_rep} добавил отклик к объявлению {add_rep.bulletin}',
                from_email='bulletin.board.test@yandex.ru',
                recipient_list=[bulletin.author_bul.user.email]
            )
        return redirect(bulletin.get_absolute_url())
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class AddBulletin(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    permission_required = ('board.add_bulletin')
    template_name = 'add_bulletin.html'
    form_class = AddBulletinForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            add_bul = form.save(commit=False)
            add_bul.author_bul = Author.objects.get(user=self.request.user)
            add_bul.save()
        return redirect(form.instance.get_absolute_url())


class UpdateBulletin(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    permission_required = ('board.change_bulletin')
    template_name = 'add_bulletin.html'
    form_class = AddBulletinForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Bulletin.objects.get(pk=id)

#
class DeleteBulletin(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    permission_required = ('board.delete_bulletin')
    template_name = 'deletebulletin.html'
    context_object_name = 'bulletin'
    queryset = Bulletin.objects.all()
    success_url = '/board'

class SearchReplies(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/accounts/login/'
    permission_required = ('board.view_reply')
    model = Reply
    template_name = 'replies_list.html'
    context_object_name = 'replies'
    ordering = ['-id']

    def get_filter(self):
        return RepliesFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        user = self.request.user
        author_r = Author.objects.get(user=user)
        return Reply.objects.filter(bulletin__author_bul=author_r)

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class DeleteReply(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    permission_required = ('board.delete_reply')
    template_name = 'deletereply.html'
    context_object_name = 'replies'
    queryset = Reply.objects.all()
    success_url = '/board/replies'

@login_required
def confirm_rep(request, pk):
    repl = Reply.objects.get(pk=pk)
    repl.confirm()
    send_mail(
        subject=f'Ваш отклик к объявлению {repl.bulletin} подтвержден',
        message=f'Пользователь {repl.bulletin.author_bul} подтвердил ваш отклик к объявлению {repl.bulletin}',
        from_email='bulletin.board.test@yandex.ru',
        recipient_list=[repl.bulletin.author_bul.user.email]
    )
    return redirect('/board/replies')

@login_required
def up_to_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/board')


