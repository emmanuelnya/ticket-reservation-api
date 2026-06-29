from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permesso che consente l'accesso a una prenotazione solo
    all'utente che l'ha creata (proprietario).
    """

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
