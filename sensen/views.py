from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView,FormView
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class HomeView(TemplateView):
    template_name='home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_list'] = BlogPage.objects.all()
        return context
    

def RegistrationView(request):
    d={}
    if request.method=='GET':
        user = UserCreationForm()
        author = AuthorForm()
        d={'u':user,'a':author}
        return render(request, "register.html",context=d)
    elif(request.method=="POST"):
        user = UserCreationForm(request.POST)
        author = AuthorForm(request.POST)
        if (author.is_valid() and user.is_valid()):
            u= user.save()
            a=author.save(commit=False)
            a.user=u
            a.save()
            return HttpResponse("Author Registered Successfully......")
        else:
            return render(request, 'register.html',context=d)


# ------------------------------Login Page------------------------

def LoginView(request):
    d={}
    if request.method=="GET":
        fm_user = AuthenticationForm()
        d={'fm':fm_user}
        return render(request,'login.html',context=d)
    elif(request.method=="POST"):
        fm_user = AuthenticationForm(request=request,data= request.POST)
        if fm_user.is_valid():
            uname=fm_user.cleaned_data['username']
            upass= fm_user.cleaned_data['password']
            users= authenticate(username=uname,password=upass)
            if users is not None:
                login(request, users)
                return redirect('home')
        else:
            d={'fm':fm_user}
            return render(request, 'login.html',context=d)
            
# --------------------Logout--------------------------
def LogoutView(request):
    logout(request)
    return redirect('home')



# ----------------------------Add Blogs------------------
@login_required(login_url='login')
def AddNewBlog(request):
    d={}
    if request.method=='GET':
        blog = BlogPageForm()
        d={'b':blog}
        return render(request, "addblogs.html",context=d)
    elif(request.method=='POST'):
        blog = BlogPageForm(request.POST,request.FILES)
        if blog.is_valid():
            blog.save()
            return redirect('show')

# -----------------Show Blogs---------------------------------

login_required(login_url='login')
def ShowBlogs(request):
    d={}
    if request.method=="GET":
        # img=ImagesForm()
        img=BlogPage.objects.all()
        d={'img':img}
        return render(request, 'showblogs.html',context=d)
    elif(request.method=='POST'):
        img=BlogPageForm(request.POST,request.FILES)
        if img.is_valid():
            img.save()
            return redirect('show')
        
    else:
        d={'img':img}
        return render(request, 'showblogs.html',context=d)

# --------------------Delete ------------------------------

def DeleteView(request,id):
    blog = BlogPage.objects.get(id=id)
    blog.delete()
    return redirect('show')

# -----------------------Add or Show Blogs--------------------
@login_required(login_url='login')
def AddShow(request):
    return render(request, 'addnewblog.html')

# -----------------------Blog Details-------------------------
class BlogDetailView(TemplateView):
    template_name = "blogdetails.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        blog = BlogPage.objects.get(slug=url_slug)
        blog.view_count +=1
        blog.save()
        context['blog'] = blog
        return context

# -----------------------Search Pannel--------------------

class SearchView(TemplateView):
    template_name='search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = BlogPage.objects.filter(Q(title__icontains=kw) | Q(author_name__icontains=kw) | Q(blog_body__icontains=kw))
        context['results'] = results
        return context
    
# ----------------------------Profile------------------------------
class CustomerProfile(TemplateView):
    template_name='profile.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.author:
            pass
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.request.user.author
        context['author'] = author
        order = BlogPage.objects.all()
        context['order'] = order
        return context
    
# --------------------------password Reset--------------------------
class PasswordForgot(FormView):
    template_name= 'forgotpassword.html'
    form_class=PasswordForgotForm
    success_url= "forgot-password"
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        print(email,'----------------------')
        return super().form_valid(form)