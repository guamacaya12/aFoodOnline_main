

# This file is designed to save helpfuls utilitys developed by the owner


# This function is helpful to identify if the user is a vendor or a customer.
def detectUser(user):
    if user.role==1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
         redirectUrl = '/admin'
