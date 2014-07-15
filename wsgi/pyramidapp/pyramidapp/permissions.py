from pyramidapp.models import DBSession

def has_permission(self, id):
    """Check out whether a user has a permission or not."""
    permission = Permission.query.filter_by(id=id).first()
    # if the permission does not exist or was not given to the user
    if not permission or not permission in permissions:
        return False
    return True

def grant_permission(self, id):
    """Grant a permission to a user."""
    permission = Permission.query.filter_by(id=id).first()
    if permission and permission in permissions:
        return

    with transaction.manager:
        if not permission:
            permission = Permission()
            permission.id = id
            DBSession.add(permission)
        permissions.append(permission)

def revoke_permission(self, id):
    """Revoke a given permission for a user."""
    permission = Permission.query.filter_by(id=id).first()
    if not permission or not permission in permissions:
        return
    with transaction.manager:
        permissions.remove(permission)