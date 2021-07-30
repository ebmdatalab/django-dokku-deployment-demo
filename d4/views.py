from django.shortcuts import render

from .models import Thing


def index(request):
    ctx = {"things": Thing.objects.order_by("name")}
    return render(request, "d4/index.html", ctx)
