from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.utils.translation import ugettext_lazy as _
from foobar.wallet import api as wallet_api
from shop import api as shop_api
from moneyed import Money
from .exceptions import NotCancelableException
from . import models, api


class ReadOnlyMixin(object):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class PurchaseInline(ReadOnlyMixin, admin.TabularInline):
    model = models.Purchase
    fields = ('link', 'date_created', 'amount',)
    readonly_fields = ('link', 'date_created', 'amount')
    ordering = ('-date_created',)
    show_change_link = True

    def link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:foobar_purchase_change', args=(obj.id,)),
            obj.id
        )
    link.allow_tags = True


class PurchaseItemInline(ReadOnlyMixin, admin.TabularInline):
    model = models.PurchaseItem
    fields = ('link', 'product_ean', 'qty', 'amount',)
    readonly_fields = ('link', 'product_ean', 'qty', 'amount',)

    def product_name(self, obj):
        obj = shop_api.get_product(obj.product_id)
        if obj:
            return obj.name

    def product_ean(self, obj):
        obj = shop_api.get_product(obj.product_id)
        if obj:
            return obj.code

    def link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_product_change', args=(obj.product_id,)),
            self.product_name(obj)
        )
    link.allow_tags = True


@admin.register(models.Account)
class AccountAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'card_id', 'balance')
    readonly_fields = ('id', 'wallet_link', 'date_created', 'date_modified')
    inlines = (PurchaseInline,)
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'user',
                'name',
                'card_id',
            )
        }),
        ('Additional information', {
            'fields': (
                'wallet_link',
                'date_created',
                'date_modified',
            )
        })
    )

    class Media:
        css = {'all': ('css/hide_admin_original.css',)}

    def balance(self, obj):
        _, balance = wallet_api.get_balance(obj.id)
        return balance

    def wallet_link(self, obj):
        wallet_obj = wallet_api.get_wallet(obj.id)
        return '<a href="{}">{}</a>'.format(
            reverse('admin:wallet_wallet_change', args=(wallet_obj.id,)),
            self.balance(obj)
        )
    wallet_link.allow_tags = True


@admin.register(models.Purchase)
class PurchaseAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('id', 'account', 'status', 'amount', 'date_created',)
    readonly_fields = ('id', 'account', 'amount', 'date_created', 'status',
                       'date_modified')
    inlines = (PurchaseItemInline,)
    list_filter = ('status',)
    change_list_template = 'admin/purchase/list.html'
    date_hierarchy = 'date_created'
    actions = ['cancel_purchases']

    class Media:
        css = {'all': ('css/hide_admin_original.css',)}

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def cancel_purchases(self, request, queryset):
        failed = 0
        for obj in queryset:
            try:
                api.cancel_purchase(obj.id)
            except NotCancelableException:
                failed += 1
        count = queryset.count()
        if failed:
            msg = _('Canceled %d purchase(s) (%d failed).')
            msg = msg % (count - failed, failed)
        else:
            msg = _('Canceled %d purchase(s).') % count
        return self.message_user(request, msg)
    cancel_purchases.short_description = _('Cancel purchases')

    def aggregated_sum(self, qs):
        expr = ExpressionWrapper(
            F('items__amount') * F('items__qty'), output_field=DecimalField()
        )
        qs = qs.aggregate(total=Sum(expr))
        return Money(qs['total'], settings.DEFAULT_CURRENCY)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            qs = response.context_data['cl'].queryset
            extra_context = {
                'total_amount': self.aggregated_sum(qs)
            }
            response.context_data.update(extra_context)
        return response
