from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, CreateView, DetailView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Comment, Recipe
from .forms import PostCreateForm, RegistrationForm


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class PostsView(ListView):
    queryset = Recipe.objects.annotate(comments_count=Count('comments')).order_by('-created_at')
    paginate_by = 6
    template_name = 'bestRecipes/recipe_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query)).distinct()
        cat = self.request.GET.get('cat')
        if cat:
            queryset = queryset.filter(categories__icontains=cat)
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bestRecipes/recipe_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    queryset = Recipe.objects.all()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        slug = request.POST.get('slug')
        if comment and slug:
            post = get_object_or_404(Recipe, slug=slug)
            comment = Comment.objects.create(author=request.user, recipe=post, text=comment)
            comment.save()
        return redirect('detail', slug)
