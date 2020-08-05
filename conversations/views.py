from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.http import Http404
from django.views.generic import View
from . import models
from users import models as user_models


def go_conversation(request, h_pk, g_pk):
    if h_pk is not None and g_pk is not None:
        try:
            host = user_models.User.objects.get(pk=h_pk)
            guest = user_models.User.objects.get(pk=g_pk)
        except user_models.User.DoesNotExist:
            return redirect(reverse("core:home"))
        if host is not None and guest is not None:
            # q = Q(participants=guest)
            # q.add(Q(participants=host), q.AND)
            try:
                c = models.Conversation.objects.filter(participants=host)
                if len(c) == 0:
                    raise models.Conversation.DoesNotExist
                (conversation,) = c.filter(participants=guest)
            except models.Conversation.DoesNotExist:
                conversation = models.Conversation.objects.create()
                conversation.participants.add(host)
                conversation.participants.add(guest)
            # print(conversation.messages.all)
            return redirect(
                reverse("conversations:detail", kwargs={"pk": conversation.pk})
            )
    else:
        # 예약 목록 페이지 완성하면 거기로 redirect
        return redirect(reverse("core:home"))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk", None)
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        # print(pk, conversation)
        if pk is not None and conversation is not None:
            return render(
                self.request,
                "conversations/conversation_detail.html",
                {"conversation": conversation},
            )
        else:
            return Http404()

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk", None)
        message = self.request.POST.get("message", None)
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if pk is not None and message is not None and conversation is not None:
            models.Message.objects.create(
                msg=message, user=self.request.user, chat_room=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
