from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm
import os
# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                title=request.POST['title'],
                author=request.POST['author'],
                image=request.FILES['image'],
                description=request.POST['description'],
                price=request.POST['price']
                )
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})
    
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        old_img = photo.image.path
        if form.is_valid():
            # 기존 이미지 파일 삭제
            if os.path.exists(old_img):
                os.remove(old_img)
            # 새로운 이미지 파일 등록
            form.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'photo/photo_post.html', {'form': form})