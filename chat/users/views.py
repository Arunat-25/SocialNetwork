from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.urls import reverse

from .forms import CustomUserCreationForm
from .models import CustomUser, Message


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('show_friends_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {"form": form})


def show_friends_list(request):
    message = None
    if request.method == 'POST':
        try:
            friend = CustomUser.objects.get(username=request.POST['friends_username'])
            request.user.friends.add(friend)
            message = f"Пользователь {request.POST['friends_username']} добавлен в друзья"
        except CustomUser.DoesNotExist:
            message = f"Пользователя {request.POST['friends_username']} не существует"
    user = request.user
    friends = user.friends.all()
    return render(request, "friends_list.html", {"friends": friends, "user": user, "message": message})


def send_message(request, username):
    receiver = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        content = request.POST['content']
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()
        return redirect(reverse("send_message", args=[username]))

    sent_messages = Message.objects.filter(sender=request.user, receiver=receiver)

    received_messages = Message.objects.filter(sender=receiver, receiver=request.user)

    all_messages = list(sent_messages) + list(received_messages)
    all_messages.sort(key=lambda x: x.timestamp)

    formatted_messages = [
        f"{message.sender.username} ({message.timestamp.strftime('%Y-%m-%d %H:%M')}): {message.content}"
        for message in all_messages
    ]

    return render(request, 'send_message.html', {
        'receiver': receiver,
        'messages': formatted_messages
    })

def show_chats(request):
    user = request.user

    sent_chats = Message.objects.filter(sender=user)
    received_chats = Message.objects.filter(receiver=user)

    all_chats = list(sent_chats) + list(received_chats)

    unique_chats = []

    added_contacts = []

    all_chats.sort(key=lambda x: x.timestamp, reverse=True)

    for chat in all_chats:
        if chat.sender == user:
            contact = chat.receiver
        else:
            contact = chat.sender

        if contact not in added_contacts:
            unique_chats.append({'contact': contact, 'message': chat})
            added_contacts.append(contact)

    formatted_chats = [
        {
            'username': chat['contact'].username,
            'message': f"{chat['contact'].username} ({chat['message'].timestamp.strftime('%Y-%m-%d %H:%M')}): {chat['message'].content[:30]}"
        }
        for chat in unique_chats
    ]

    return render(request, 'chats.html', {'chats': formatted_chats})

