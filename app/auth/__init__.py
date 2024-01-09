from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from wtforms import validators
from flask import redirect, url_for, request


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'admin', False)

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'admin', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('rent4u.index'))
    
class UserModelView(AdminModelView):
    column_exclude_list = ["pwdhash"]
    form_excluded_columns = ["pwdhash"]
    column_searchable_list = ["username", "email"]

class CustomerModelView(AdminModelView):
    column_list = ('full_name', 'phone_number', 'address', 'date_of_birth', 'created_at', 'updated_at')
    form_columns = ('full_name', 'phone_number', 'address', 'date_of_birth')
    column_searchable_list = ('full_name',)
    column_filters = ('created_at', 'updated_at', 'date_of_birth')

class CarModelView(AdminModelView):
    column_list = ('brand', 'model', 'type', 'transmission', 'seats', 'doors', 'luggage', 'availability', 'rental_rate', 'created_at', 'updated_at')
    form_columns = ('brand', 'model', 'type', 'transmission', 'seats', 'doors', 'luggage', 'availability', 'rental_rate', 'description', 'image_filename')
    column_searchable_list = ('brand', 'model', 'type')
    column_filters = ('availability', 'brand', 'type', 'transmission')
    form_args = {
        'brand': {
            'validators': [validators.DataRequired()]
        },
        'rental_rate': {
            'validators': [validators.NumberRange(min=0)]
        },
        'seats': {
            'validators': [validators.NumberRange(min=0)]
        },
        'doors': {
            'validators': [validators.NumberRange(min=0)]
        },
        'luggage': {
            'validators': [validators.NumberRange(min=0)]
        }
    }
# class CategoryModelView(MyModelView):
#     column_list = ('name',)  # Gösterilecek sütunlar
#     form_columns = ('name',)  # Düzenlenebilir sütunlar
#     column_searchable_list = ('name',)  # Aranabilir sütunlar
#     form_args = {
#         'name': {
#             'validators': [validators.DataRequired()]
#         }
#     }

class ReservationAdminView(AdminModelView):
    column_list = ('id', 'car', 'customer', 'pick_up_date', 'return_date', 'pick_up_location', 'return_location', 'created_at', 'updated_at')
    column_searchable_list = ('car.brand', 'customer.full_name', 'pick_up_location', 'return_location')
    column_filters = ('car.brand', 'customer.full_name', 'pick_up_location', 'return_location', 'created_at', 'updated_at')
    form_columns = ('car', 'customer', 'pick_up_date', 'return_date', 'pick_up_location', 'return_location')

    column_formatters = {
        'car': lambda view, context, model, name: f"{model.car.id}",
        'customer': lambda view, context, model, name: f"{model.customer.id}",
    }

    column_labels = {
        'car': 'Car Id',
        'customer': 'Customer Id',
        'pick_up_date': 'Pick Up Date',
        'return_date': 'Return Date',
        'pick_up_location': 'Pick Up Location',
        'return_location': 'Return Location',
        'created_at': 'Created At',
        'updated_at': 'Updated At',
    }
    
class ContactAdminView(AdminModelView):
    column_list = ('name', 'phone', 'email', 'message', 'created_at')
    column_searchable_list = ('name', 'email')
    column_filters = ('created_at',)