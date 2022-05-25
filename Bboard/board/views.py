from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bulletin, Author
from .forms import AddBulletinForm
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


class UpdateNews(UpdateView):
    # login_url = '/accounts/login/'
    # permission_required = ('newsportal.change_post')
    template_name = 'add_bulletin.html'
    form_class = AddBulletinForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Bulletin.objects.get(pk=id)
#
# class DeleteNews(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     login_url = '/accounts/login/'
#     permission_required = ('newsportal.delete_post')
#     template_name = 'deletenews.html'
#     context_object_name = 'newspost'
#     queryset = Post.objects.all()
#     success_url = '/news/search'