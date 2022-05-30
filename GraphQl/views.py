from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db import transaction
from django.db.models import Q

from .forms import AddShippingForm
from .models import Shipping, FlowType, State

import json


@login_required(login_url='/login/')
def workflows(request):
    context = {
        'flows': FlowType.objects.all()
    }
    return render(request, 'home/workflows.html', context)


@login_required(login_url='/login/')
def shipping_flows(request, pk):
    selected_flow = get_object_or_404(FlowType, id=pk)
    context = {
        'selected_flow': selected_flow
    }
    return render(request, 'home/shippingflows.html', context)


@login_required(login_url='/login/')
def view_flow(request, pk):
    selected_flow = get_object_or_404(FlowType, id=pk)
    context = {
        'selected_flow': selected_flow
    }
    return render(request, 'home/viewshippingflows.html', context)


@login_required(login_url='/login/')
def add_new_state(request, pk):
    state = request.POST.get('state[]') 
    rect_loc = request.POST.get('rect_loc[]') 
    connector_loc = request.POST.get('connector_loc[]')
    print(connector_loc)
    new_state = State.objects.create(
        label = state, 
        rect_loc = rect_loc,
        connector_loc = connector_loc
    )
    try:
        selected_flow = get_object_or_404(FlowType, id=pk)
        selected_flow.states.add(new_state)
        response_data = 'success'
    except FlowType.DoesNotExist:
        response_data = 'fail'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/login/')
def main(request):
    return render(request, 'home/shippings.html')


@login_required(login_url='/login/')
def states(request):
    return render(request, 'home/states.html')


@login_required(login_url='/login/')
def all_issues(request):
    return render(request, 'home/issues.html')


@login_required(login_url='/login/')
def selected_shipping(request, pk):
    shipping = get_object_or_404(Shipping, id=pk)
    return render(request, 'home/shippings.html', {'shipping': shipping})


@login_required(login_url='/login/')
def manage_users(request, q=None):
    page = request.GET.get('page', 10)
    users = User.objects.all().order_by('-id')
    if request.method=='GET':

        query = request.GET.get('q')

        product_lookup = Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)

        if query is not None:
            mathcing_items = User.objects.filter(product_lookup).order_by('-id')
        else:
            mathcing_items=users

        paginator = Paginator(mathcing_items, 10)

        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages) 


        if request.is_ajax():

            html = render_to_string(
                template_name="filter/users-results.html", 
                context={"results": user_list}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)
    else:
        paginator = Paginator(users, 10)
   
    try:
        users_list = paginator.page(page)
    except PageNotAnInteger:
        users_list = paginator.page(1)
    except EmptyPage:
        users_list = paginator.page(paginator.num_pages) 

    context = {
        'users': users_list
    }
    return render(request, 'manage_users.html', context)


@login_required(login_url='/login/')
def shippings(request, q=None):
    page = request.GET.get('page', 1)
    shippings = Shipping.objects.all()
    
    if request.method=='GET':

        query = request.GET.get('q')

        product_lookup = Q(product__icontains=query) | Q(customer__icontains=query) | Q(shipping_status__icontains=query)

        if query is not None:
            mathcing_items = Shipping.objects.filter(product_lookup)
        else:
            mathcing_items=shippings

        paginator = Paginator(mathcing_items, 10)

        try:
            shippings_list = paginator.page(page)
        except PageNotAnInteger:
            shippings_list = paginator.page(1)
        except EmptyPage:
            shippings_list = paginator.page(paginator.num_pages) 


        if request.is_ajax():

            html = render_to_string(
                template_name="filter/shippings-results.html", 
                context={"results": shippings_list}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)
    else:
        paginator = Paginator(shippings, 10)
   
    try:
        shippings_list = paginator.page(page)
    except PageNotAnInteger:
        shippings_list = paginator.page(1)
    except EmptyPage:
        shippings_list = paginator.page(paginator.num_pages) 

    context = {
        'shippings': shippings_list
    }
    return render(request, 'home/shippings.html', context)


@login_required(login_url='/login/')
def view_shipping(request, pk):
    try:
        selected_shipping=get_object_or_404(Shipping, id=pk)
    except Shipping.DoesNotExist:
        selected_shipping=None
        return redirect('shippings')
    
    context = {
        'shipping': selected_shipping
    }
    return render(request, 'selected_shipping.html', context)


@login_required(login_url='/login/')
def create_shipping(request):
    return render(request, 'shipping_create.html')


@login_required(login_url='/login/')
def add_new_shipping(request):
    with transaction.atomic():
        try:
            new_form = AddShippingForm(request.POST or None)
            if new_form.is_valid():
                product = new_form.cleaned_data.get('product') 
                customer = new_form.cleaned_data.get('customer') 
                shipping_status = new_form.cleaned_data.get('shipping_status') 

                new_shipping = Shipping(
                    product=product,
                    customer=customer,
                    shipping_status=shipping_status
                )
                new_shipping.save()

                print('Success!')
            else:
                transaction.set_rollback(True)

                response = JsonResponse({"success": False,"error": "Invalid Form! Please try again later"})
                response.status_code = 500
                return response

        except Exception as e:
            print(e)

            transaction.set_rollback(True)

            response = JsonResponse({"success": False,"error": "Something went wrong! Please try again later"})
            response.status_code = 500
            return response

    return JsonResponse({"success": True,"message": "Shipping has been successfully created"})


@login_required(login_url='/login/')
def update_shipping(request, pk):
    with transaction.atomic():
        try:
            selected_shipping = get_object_or_404(Shipping, id=pk)
            new_form = AddShippingForm(request.POST or None)
            if new_form.is_valid():
                product = new_form.cleaned_data.get('product') 
                customer = new_form.cleaned_data.get('customer') 
                shipping_status = new_form.cleaned_data.get('shipping_status') 

                selected_shipping.product = product
                selected_shipping.customer = customer
                selected_shipping.shipping_status = shipping_status
                selected_shipping.save()

                print('Success!')
            else:
                transaction.set_rollback(True)

                response = JsonResponse({"success": False,"error": "Invalid Form! Please try again later"})
                response.status_code = 500
                return response

        except Exception as e:
            print(e)

            transaction.set_rollback(True)

            response = JsonResponse({"success": False,"error": "Something went wrong! Please try again later"})
            response.status_code = 500
            return response

    return JsonResponse({"success": True,"message": "Shipping has been successfully updated"})


@login_required(login_url='/login/')
def delete_shipping(request, pk):
    with transaction.atomic():
        try:
            selected_shipping = get_object_or_404(Shipping, id=pk)
            selected_shipping.delete()

        except Exception as e:
            print(e)

            transaction.set_rollback(True)

            response = JsonResponse({"success": False,"error": "Something went wrong! Please try again later"})
            response.status_code = 500
            return response

    return JsonResponse({"success": True,"message": "Shipping has been successfully deleted"})


@login_required(login_url='/login/')
def bulk_delete_shippings(request): 
    if request.method == 'POST':
        with transaction.atomic():
            try:
                selected_products = request.POST.getlist('products[]')
                if len(selected_products) != 0:
                    products = Shipping.objects.filter(id__in=selected_products)
                    products.delete()
                
            except Exception as e:
                print(e)

                transaction.set_rollback(True)

                response = JsonResponse({"success": False,"error": "Something went wrong! Please try again later"})
                response.status_code = 500
                return response

    return JsonResponse({"success": True,"message": "Shippings have been successfully deleted"})
