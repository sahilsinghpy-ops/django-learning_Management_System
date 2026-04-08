from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsEventManager(BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_event_manager

class IsCustomer(BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_customer
