from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy

class PostListView(generic.ListView):
    model = Post
    print(Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date'))
    template_name = 'blog/post_list.html'

    """
    あらかじめ取得するデータのソート順を変えたり、フィルタリングして制御したい時もあるでしょう。
    その時は、get_querysetメソッドをオーバーライドします。
    """
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

post_list = PostListView.as_view()
print("post_list:")
print(post_list)

class PostDetailView(generic.DetailView):  ## DetailViewは、pkをデフォルトで取ってきてくれる
    model = Post
    template_name = 'blog/post_detail.html'

post_detail = PostDetailView.as_view()


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post:post_list") # 要変更
    template_name = 'blog/post_edit.html'


post_new = PostCreateView.as_view()


class PostUpdateView(generic.UpdateView):
    """
    編集のビューでは以下のように動作する
    GET 編集う画面
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def get_success_url(self, **kwargs):
        """
        PostCreateView同様にアップデート成功時リダイレクト先を指定したい。
        success_url = reverse_lazy('post:post_list')では pk を含むことができないため
        success_url のメソッドを上書きする必要がある
        self.object に今編集した post のオブジェクトが入っているので、それのidを指定すると良い
        """
        return reverse_lazy("post:post_new", kwargs={"pk": self.object.id})


post_edit = PostUpdateView.as_view()



# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     print(posts)
#     return render(request, 'blog/post_list.html', {'posts': posts})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})