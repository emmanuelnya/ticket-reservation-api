from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato per la risorsa Event.

    - Lettura (GET, HEAD, OPTIONS): consentita a chiunque, anche utenti
      anonimi (in linea con il requisito "Anonymous: read-only access").
    - Scrittura (POST): consentita solo agli utenti autenticati con
      ruolo ORGANIZER.
    - Modifica/cancellazione di un evento specifico: consentita solo
      all'organizer che ha creato quell'evento.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_organizer", False)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer_id == request.user.id
