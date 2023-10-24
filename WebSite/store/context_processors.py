from .models import Cart


def cart_render(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, complete=False)

        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'], complete=False)

    except:
        cart = {"num_of_items": 0}
    return {"cart": cart}
