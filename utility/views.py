from django.shortcuts import render, redirect, get_object_or_404
import os 


from .forms import AddItemForm, EditForm
from item.models import Item


def delete_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.images and item.images.name != "default.png":
        item_path = item.images.path
        if os.path.isfile(item_path):
            os.remove(item_path)
    if request.method == "POST":
        item.delete()
        return redirect('home_view')
    return render(request, 'utility/delete.html', {"item": item})
      

def edit_view(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new = form.save(commit=False)
            new.created_by = request.user
            if not cleaned_data.get('images'):
                item.images = "item_images/default.png"
            form.save()
            return redirect('detail_view', item.id)
    else:
        form = EditForm(instance=item)
    return render(request, 'utility/edit.html', {"form":form})


def add_item_view(request):
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.created_by = request.user
            form.save()
            return redirect('home_view',)
        
    else:
        form = AddItemForm()
        
    return render(request, "utility/add.html", {"form":form})