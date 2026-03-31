"""Sales forms."""

from django import forms
from .models import Supply, Demand


class SupplyForm(forms.ModelForm):
    """供应信息表单。"""
    
    class Meta:
        model = Supply
        fields = ['medicine_name', 'specification', 'quantity', 'location', 
                  'origin', 'price', 'contact_name', 'contact_phone', 'description']
        labels = {
            'medicine_name': '药材名称',
            'specification': '规格',
            'quantity': '供应量',
            'location': '库存地',
            'origin': '产地',
            'price': '价格',
            'contact_name': '联系人',
            'contact_phone': '联系电话',
            'description': '描述',
        }
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入药材名称'}),
            'specification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入规格'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入供应量，如：10吨'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入库存地'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入产地'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入价格，如：50元/公斤'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入联系人姓名'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入联系电话'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '请输入其他描述信息'}),
        }


class DemandForm(forms.ModelForm):
    """求购信息表单。"""
    
    class Meta:
        model = Demand
        fields = ['medicine_name', 'specification', 'quantity', 'location', 
                  'origin', 'price', 'contact_name', 'contact_phone', 'description']
        labels = {
            'medicine_name': '药材名称',
            'specification': '规格',
            'quantity': '求购量',
            'location': '库存地',
            'origin': '产地',
            'price': '价格',
            'contact_name': '联系人',
            'contact_phone': '联系电话',
            'description': '描述',
        }
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入药材名称'}),
            'specification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入规格'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入求购量，如：10吨'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入库存地'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入产地'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入价格，如：50元/公斤'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入联系人姓名'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入联系电话'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '请输入其他描述信息'}),
        }
