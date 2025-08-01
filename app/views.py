from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self,request):
        form=ResumeForm()
        candidates=Resume.objects.all()
        return render(request,'app/home.html',{'candidates':candidates ,'form':form})
    
    def post(self,request):
        form=ResumeForm(request.POST,request.FILES)
        form.save()
        return render(request,'app/home.html',{'form':form})
    


class candidateView(View):
    def get(self,request,pk):
        candidate=Resume.objects.get(pk=pk)
        return render(request,'app/candidate.html',{'candidate':candidate})