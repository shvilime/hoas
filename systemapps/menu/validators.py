def is_authenticated(request):
    """
    Returns True if request.user authenticated else returns False
    """
    return request.user.is_authenticated

def is_staff(request):
    """
    Returns True if request.user is Staff else returns False
    """
    return request.user.is_staff