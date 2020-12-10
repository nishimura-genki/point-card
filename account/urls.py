from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('customer_signup/', views.CustomerSignUpView.as_view(),
         name='customer_signup'),
    path('shop_signup/', views.ShopSignUpView.as_view(), name='shop_signup'),
    path('mypage/', views.MyPage.as_view(), name='mypage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', TemplateView.as_view(template_name='registration/signup.html'), name='signup'),
    path('delete_confirm', views.DeleteView.as_view(), name='delete-confirmation'),
    path('delete_complete', TemplateView.as_view(
        template_name="registration/delete_complete.html"), name='delete-complete'),
    path('point_card_list/', views.PointCardListView.as_view(),
         name='point_card_list'),
    path('point_card_detail/<int:pk>/',
         views.PointCardDetailView.as_view(), name='point_card_detail'),
    path('qrcode/', views.QRCodeView.as_view(), name='qrcode'),
    path('customer_profile_update/', views.CustomerProfileUpDateView.as_view(),
         name='customer_profile_update'),
    path('shop_profile_update/', views.ShopProfileUpDateView.as_view(),
         name='shop_profile_update'),
    # path('make_point_card_form/', TemplateView.as_view(
    #    template_name='registration/make_point_card_form.html'), name='make-point-card-form'),

    path('make_point_card/<int:shop_user_id>', views.MakePointCardView.as_view(),
         name='make-point-card'),
    path('use_point/<int:customer_user_id>/',
         views.UsePointView.as_view(), name="use_point"),
    path('add_point/<int:customer_user_id>/',
         views.AddPointView.as_view(), name="add_point"),
    path('add_stamp/<int:customer_user_id>',
         views.AddStampView.as_view(), name='add_stamp'),
    path('cashier/<int:customer_user_id>/',
         views.CashierView.as_view(), name="cashier"),
    path('read_qr_code/', views.ReadQRCodeView.as_view(), name='read_qr_code'),
    path('process_qr_code/', views.ProcessQRCodeView.as_view(),
         name="process_qr_code"),
    path('point_card/<int:pk>/delete',
         views.DeletePointCardView.as_view(), name='delete_point_card'),
    path("point_card/delete/complete", TemplateView.as_view(
        template_name='account/delete_point_card_complete.html'), name="delete_point_card_complete"),
    path("does_not_have_point/", TemplateView.as_view(
        template_name='account/does_not_have_point.html'), name="does_not_have_point"),
    path("use_stamp/<int:customer_user_id>/",
         views.UseStampView.as_view(), name='use_stamp'),
    path('does_not_have_stamp/', TemplateView.as_view(
        template_name='account/does_not_have_stamp.html'), name='does_not_have_stamp'),
    path('customize_point_card/', views.CustomizePointCardView.as_view(),
         name='customize_point_card'),
]
