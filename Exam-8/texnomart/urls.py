from django.urls import path, include
from texnomart import views
from rest_framework.routers import DefaultRouter
from texnomart import auth


router = DefaultRouter()
router.register('categories/', views.CategoryViewSet, basename='category'),

urlpatterns = [
    path('', views.ProductList.as_view()),
    # Categries
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view()),
    path('category/add-category/', views.CategoryAdd.as_view()),
    path('category/<slug:slug>/edit/', views.CategoryChange.as_view()),
    path('category/<slug:slug>/delete/', views.CategoryDelete.as_view()),
    # Product
    path('product/detail/<int:id>/', views.ProductDetailView.as_view()),
    path('product/<int:id>/edit/', views.ProductEdit.as_view()),
    path('product/<int:id>/delete/', views.ProductDelete.as_view()),
    # Attribute
    path('attribute-key/', views.AttributeView.as_view()),
    path('attribute-value/', views.AttributeValueView.as_view()),
    path('product/<int:product_id>/product-attributes/', views.ProductAttributesView.as_view(), name='product-attributes-by-product'),
    # Other
    path('images/', views.ImageListView.as_view(), name='image_list'),
    path('modelviewset/', include(router.urls)),
    # Authentication
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.UserRegisterAPIView().as_view(), name='register'),
    path("logout/", auth.UserLogoutAPIView.as_view(), name="user_logout"),

]
