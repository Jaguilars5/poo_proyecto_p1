from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from core.forms import BrandForm, BrandForm, CategoryForm, ProductForm, SupplierForm
from core.models import Brand, Category, Product, Supplier

def signup(request):
    if request.method == 'GET':
        return render(request, 'core/autentification/signup.html', {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.is_staff = True  # Permite acceso al admin
                user.is_superuser = True  # Hace al usuario superusuario
                user.save()
                login(request, user)
                return redirect('core:signin')
            except IntegrityError:
                return render(request, 'core/autentification/signup.html', {"form": UserCreationForm(), "error": "Usuario ya existe!."})
        else:
            return render(request, 'core/autentification/signup.html', {"form": UserCreationForm(), "error": "Las contraseñas deben ser iguales."})
def signin(request):
    if request.method == 'GET':
        return render(request, 'core/autentification/signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'core/autentification/signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('core:home')
@login_required
def signout(request):
    logout(request)
    return redirect('core:signin')

@login_required
def home(request):
   user=request.user 
   data = {
        "title1":"Autor | TeacherCode",
        "title2":"Super Mercado Economico",
        "user":user
   }
   return render(request,'core/home.html',data)

@login_required
def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)
# crear un producto
@login_required
def product_create(request):
    data = {"title1": "Productos", "title2": "Ingreso De Productos"}
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                form.save_m2m()
                return redirect("core:product_list")
            except IntegrityError:
                data["error"] = "Ocurrió un error de integridad de datos. Por favor, revise su entrada."
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"] = "Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        data["form"] = ProductForm()
    return render(request, "core/products/form.html", data)
@login_required
def product_update(request,id):
    data = {"title1": "Productos","title2": ">Edicion De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:product_list")
            except IntegrityError:
                data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada."
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        form = ProductForm(instance=product)
        data["form"]=form
    return render(request, "core/products/form.html", data)

@login_required
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
    return render(request, "core/products/delete.html", data)
@login_required
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas de Productos"
    }
    brands = Brand.objects.all() # select * from Product
    data["brands"]=brands
    return render(request,"core/brands/list.html",data)
@login_required
def brand_create(request):
    data = {"title1": "Marcas","title2": "Ingreso de Marcas"}
    if request.method == "POST":
        #print(request.POST)
        form = BrandForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                brand = form.save(commit=False)
                brand.user = request.user
                brand.save()
                return redirect("core:brand_list")
            except IntegrityError:
                data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada."
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        data["form"] = BrandForm() # controles formulario sin datos

    return render(request, "core/brands/form.html", data)
@login_required
def brand_update(request,id):
    data = {"title1": "Brands","title2": "Edicion De Marcas"}
    brand = Brand.objects.get(pk=id)
    if request.method == "POST":
        form = BrandForm(request.POST,request.FILES, instance=brand)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:brand_list")
            except IntegrityError:
                data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada."
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        form = BrandForm(instance=brand)
        data["form"]=form
    return render(request, "core/brands/form.html", data)
@login_required
def brand_delete(request,id):
    brand = Brand.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Marca","brand":brand}
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
    return render(request, "core/brands/delete.html", data)
@login_required   
def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De proveedores"
    }
    supplier = Supplier.objects.all() # select * from Product
    data["supplier"]=supplier
    return render(request,"core/suppliers/list.html",data)
@login_required
def supplier_create(request):
    data = {"title1": "Proveedores","title2": "Ingreso de Proveedores"}
    if request.method == "POST":
            #print(request.POST)
        form = SupplierForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                supplier = form.save(commit=False)
                supplier.user = request.user
                supplier.save()
                return redirect("core:supplier_list")
            except IntegrityError:
               data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada." 
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        data["form"] = SupplierForm()
    return render(request, 'core/suppliers/form.html', data)

@login_required
def supplier_update(request,id):
    data = {"title1": "Supplier","title2": "Edicion De Provedores"}
    supplier = Supplier.objects.get(pk=id)
    if request.method == "POST":
        form = SupplierForm(request.POST,request.FILES, instance=supplier)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:supplier_list")
            except IntegrityError:
               data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada." 
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        form = SupplierForm(instance=supplier)
        data["form"]=form
    return render(request, "core/suppliers/form.html", data)
@login_required
def supplier_delete(request,id):
    supplier = Supplier.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Proveedor","supplier":supplier}
    if request.method == "POST":
        supplier.delete()
        return redirect("core:supplier_list")
    return render(request, "core/suppliers/delete.html", data)

@login_required
def category_List(request):
    data = {
        "title1": "Categorias",
        "title2": "Consulta De Categorias"
    }
    category = Category.objects.all() # select * from Product
    data["categorys"]=category
    return render(request,"core/categorys/list.html",data)
@login_required
def category_create(request):
    data = {"title1": "Categorias","title2": "Ingreso de Categorias"}
    if request.method == "POST":
        #print(request.POST)
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect("core:category_list")
            except IntegrityError:
                data["error"] = "Ocurrió un error de integridad de datos. Por favor, revise su entrada."
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"] = "Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        data["form"] = CategoryForm() # controles formulario sin datos
    return render(request, "core/categorys/form.html", data)
@login_required
def category_update(request,id):
    data = {"title1": "Categorias","title2": "Edicion De Categorias"}
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES, instance=category)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:category_list")
            except IntegrityError:
               data["error"]="Ocurrió un error de integridad de datos. Por favor, revise su entrada." 
            except Exception as e:
                data["error"] = str(e)
        else:
            data["error"]="Por favor, corrija los errores en el formulario."
        data["form"] = form
    else:
        form = CategoryForm(instance=category)
        data["form"]=form
    return render(request, "core/categorys/form.html", data)
@login_required
def category_delete(request,id):
    category = Category.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar la categoria","category":category}
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
    return render(request, "core/categorys/delete.html", data)

