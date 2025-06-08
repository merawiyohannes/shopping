from django.shortcuts import render,redirect
from item.models import Item
from .models import Conversation, Message
from .forms import MessageForm


def super_view(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    messages = Message.objects.filter(conversation=conversation)
    form = MessageForm()
    sent_time = ""
    for message in messages:
        sent_time = message.created_at.strftime("%I:%M%p")
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.conversation = conversation
            new_form.created_by = request.user
            new_form.save()
            return redirect('super_view', pk)
    else:
        form = MessageForm()
    return render(request, 'conversation/message_super.html', {
        "messages":messages,
        "sent_time":sent_time,
        "form":form,
        'room_id': pk
    })


def chat_view(request):
    conversations = Conversation.objects.filter(number__in=[request.user])
    messages_data = {}
    for conversation in conversations:
        message = Message.objects.filter(conversation=conversation).order_by('-created_at').first()
        if message:
            messages_data[conversation.id] = {
                "message": message.text,
                "sent_time": message.created_at.strftime("%I:%M%p"),
                "item": conversation.item
            }
        else:
            messages_data[conversation.id] = {
                "message": "No messages yet",
                "sent_time": "",
                "item": conversation.item
            }
    for conversation in conversations:
        conversation.message = messages_data[conversation.id].get("message")
        conversation.sent_time = messages_data[conversation.id].get("sent_time")
        conversation.item = messages_data[conversation.id].get("item")
        
    context = {
        'conversations':conversations, 
    }
   
    return render(request, 'conversation/chat_user.html', context)

def contact_view(request):
    conversations = Conversation.objects.filter(number__in=[request.user])
    messages_data = {}
    for conversation in conversations:
        message = Message.objects.filter(conversation=conversation).order_by('-created_at').first()
        if message:
            messages_data[conversation.id] = {
                "message": message.text,
                "sent_time": message.created_at.strftime("%I:%M%p"),
                "item": conversation.item
            }
        else:
            messages_data[conversation.id] = {
                "message": "No messages yet",
                "sent_time": "",
                "item": conversation.item
            }
    for conversation in conversations:
        conversation.message = messages_data[conversation.id].get("message")
        conversation.sent_time = messages_data[conversation.id].get("sent_time")
        conversation.item = messages_data[conversation.id].get("item")
        
    context = {
        'conversations':conversations, 
    }
   
    return render(request, 'conversation/chat_super.html', context)


def message_view(request, pk):
    item = Item.objects.get(pk=pk)
    conversation = Conversation.objects.filter(item=item, number__in=[request.user]).first()
    form = MessageForm()
    messages = Message.objects.filter(conversation=conversation)
    sent_time = ""
    for message in messages:
        sent_time = message.created_at.strftime("%I:%M%p")

    if request.method == "POST":
        form = MessageForm(request.POST)     
        if not conversation:
            conversation = Conversation.objects.create(item=item)
            conversation.number.add(request.user)
            conversation.number.add(item.created_by)
            conversation.save()
            
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.conversation = conversation
            new_form.created_by = request.user
            new_form.save()
            return redirect('message_view', pk)
    else:
        form = MessageForm()
    
    context = {"form":form,
               "messages":messages,
               "sent_time":sent_time,
               "room_id":pk}
        
    return render(request, 'conversation/message_user.html', context)