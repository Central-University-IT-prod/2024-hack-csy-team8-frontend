from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ShoppingList, ShoppingListProduct, Group, Membership
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ShoppingListForm, ShoppingListProductForm
from django.http import JsonResponse
# Отображение продуктов
@login_required
def product_list(request, group_id=None):
    if group_id:
        group = get_object_or_404(Group, id=group_id)
        products = Product.objects.filter(group=group)
    else:
        products = Product.objects.filter(added_by=request.user)

    return render(request, 'products/product_list.html', {'products': products, 'group': group if group_id else None})

# Добавление нового продукта
@login_required
def add_product(request, group_id=None):
    group = None
    if group_id:
        group = get_object_or_404(Group, id=group_id)  # Получаем группу, если указан group_id

    if request.method == 'POST':
        name = request.POST.get('name')
        expiration_date = request.POST.get('expiration_date')
        quantity = request.POST.get('quantity')

        # Если продукт добавляется в группу, привязываем его к группе
        product = Product.objects.create(
            name=name,
            expiration_date=expiration_date,
            quantity=quantity,
            added_by=request.user,
            group=group  # Привязываем продукт к группе, если она существует
        )

        # Перенаправление на список продуктов для группы или пользователя
        if group:
            return redirect('group_product_list', group_id=group.id)
        else:
            return redirect('product_list')

    return render(request, 'products/add_product.html', {'group': group})
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт успешно удален.')
        return redirect('product_list')


# Отображение списков покупок
@login_required
def shopping_list(request):
    lists = ShoppingList.objects.filter(user=request.user)
    return render(request, 'shopping_list/shopping_list.html', {'lists': lists})

# Добавление нового списка покупок
@login_required
def add_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        name = request.POST.get('name')
        shopping_list = ShoppingList(name=name, user=request.user)
        shopping_list.save()
        return redirect('shopping_list')
    return render(request, 'shopping_list/add_shopping_list.html')
@login_required
def profile_view(request):
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} успешно создан! Теперь можете войти.')
            return redirect('login')  # Перенаправляем пользователя на страницу логина
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')
        group_description = request.POST.get('description')
        group = Group.objects.create(name=group_name, description=group_description)

        # Добавляем текущего пользователя как администратора группы
        Membership.objects.create(user=request.user, group=group, role='admin')

        return redirect('group_list')
    return render(request, 'products/create_group.html')

@login_required
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        member_username = request.POST.get('username')
        role = request.POST.get('role')

        try:
            # Пытаемся получить пользователя
            user = User.objects.get(username=member_username)  # Изменяем get_object_or_404 на get
        except User.DoesNotExist:
            error = "Пользователь с таким именем не найден."
            return render(request, 'products/add_member.html', {'group': group, 'error': error})

        # Проверяем, состоит ли пользователь уже в группе
        if Membership.objects.filter(user=user, group=group).exists():
            error = "Этот пользователь уже является участником группы."
            return render(request, 'products/add_member.html', {'group': group, 'error': error})

        # Добавляем участника в группу
        Membership.objects.create(user=user, group=group, role=role)
        return redirect('group_detail', group_id=group.id)  # Перенаправляем на страницу группы

    return render(request, 'products/add_member.html', {'group': group})

@login_required
def group_list(request):
    groups = Group.objects.filter(participants=request.user)
    return render(request, 'products/group_list.html', {'groups': groups})
@login_required
def group_product_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    products = Product.objects.filter(group=group)  # Фильтрация продуктов по группе

    return render(request, 'products/group_product_list.html', {'group': group, 'products': products})
def create_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)  # Не сохраняем еще в базе данных
            shopping_list.user = request.user  # Присваиваем текущего пользователя
            shopping_list.save()  # Теперь сохраняем в базе данных
            return redirect('shopping_list_detail', shopping_list_id=shopping_list.id)
    else:
        form = ShoppingListForm()
    return render(request, 'shopping_list/create.html', {'form': form})

def add_product_to_shopping_list(request, shopping_list_id):
    shopping_list = ShoppingList.objects.get(id=shopping_list_id)
    if request.method == 'POST':
        form = ShoppingListProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            ShoppingListProduct.objects.update_or_create(
                shopping_list=shopping_list,
                product=product,
                defaults={'quantity': quantity}
            )
            return redirect('shopping_list_detail', shopping_list_id=shopping_list.id)
    else:
        form = ShoppingListProductForm()
    return render(request, 'shopping_list/add_product.html', {'form': form, 'shopping_list': shopping_list})
def shopping_list_detail(request, shopping_list_id):
    shopping_list = get_object_or_404(ShoppingList, id=shopping_list_id, user=request.user)  # Получаем список, принадлежащий текущему пользователю
    return render(request, 'shopping_list/detail.html', {'shopping_list': shopping_list})
@login_required
def delete_shopping_list(request, shopping_list_id):
    shopping_list = get_object_or_404(ShoppingList, id=shopping_list_id, user=request.user)  # Получаем список, принадлежащий текущему пользователю
    if request.method == 'POST':
        shopping_list.delete()  # Удаляем список
        return redirect('shopping_list')  # Перенаправляем на страницу со списками
    # Возвращаем 405 (Method Not Allowed), если кто-то пытается открыть этот URL через GET
    return render(request, '405.html')  # Показываем страницу ошибки или сообщение о невозможности действия


@login_required
def delete_product_from_shopping_list(request, shopping_list_id, product_id):
    shopping_list = get_object_or_404(ShoppingList, id=shopping_list_id, user=request.user)
    product_in_list = get_object_or_404(ShoppingListProduct, shopping_list=shopping_list, product_id=product_id)

    if request.method == 'POST':
        product_in_list.delete()  # Удаляем продукт из списка покупок
        return redirect('shopping_list_detail', shopping_list_id=shopping_list_id)

    return render(request, 'shopping_list/delete_product_confirm.html',
                  {'product': product_in_list.product, 'shopping_list': shopping_list})
@login_required
def update_product_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        product.quantity = new_quantity  # Обновляем количество
        product.save()  # Сохраняем изменения
        return JsonResponse({'success': True, 'new_quantity': product.quantity})

    return JsonResponse({'success': False}, status=400)
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_membership = Membership.objects.filter(user=request.user, group=group).first()

    # Проверяем, является ли текущий пользователь администратором группы
    current_user_is_admin = current_membership and current_membership.role == 'admin'

    return render(request, 'products/group_detail.html', {
        'group': group,
        'current_user_is_admin': current_user_is_admin
    })

@login_required
def remove_member(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)

    # Проверка, является ли текущий пользователь администратором группы
    membership = get_object_or_404(Membership, user=request.user, group=group)
    if membership.role != 'admin':
        return redirect('group_detail', group_id=group.id)  # Перенаправление, если не администратор

    member = get_object_or_404(Membership, user_id=user_id, group=group)

    if request.method == 'POST':
        member.delete()  # Удаляем участника
        return redirect('group_detail', group_id=group.id)  # Перенаправляем на страницу группы

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    membership = get_object_or_404(Membership, user=request.user, group=group)

    # Если пользователь администратор, проверим, что есть другие администраторы в группе
    if membership.role == 'admin':
        admin_count = Membership.objects.filter(group=group, role='admin').count()
        if admin_count <= 1:
            error = "Вы не можете покинуть группу, так как вы единственный администратор."
            return render(request, 'products/group_detail.html', {'group': group, 'error': error})

    # Удаляем участника из группы
    membership.delete()
    return redirect('group_list')
