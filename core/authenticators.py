from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


#In some cases end user might want to go back to add/remove some files and then again 
#return to the next screen which is not possible with csrf velidation
#we have to exempt csrf validation for these perticular apis in order to achive this functionality.
#This is achived using this-
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening