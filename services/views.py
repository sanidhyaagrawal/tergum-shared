from django.shortcuts import render, redirect
from services.models import Job
from common.models import Language, Quality, Content, Rate, Status
from django.contrib import messages

def create_order(request):
    '''
    Initiate a new order and rediect to step-1
    '''
    if request.user.is_active:
        job_obj = Job.objects.create(employeer=request.user)
        return redirect('/order/step-1/{}'.format(job_obj.job_id))
    else:
        return redirect("/login") 

from profiles.models import Profile
def order_step1(request, job_id):
    '''
    Reders page for step 1 of creating an order,
    '''
    if request.user.is_active:
        job_obj = Job.objects.get(job_id=job_id)
        print(job_obj.attachments.all())
        all_profile = Profile.objects.all()
        supported_from_langs = []
        for profile in all_profile:
            supported_from_langs.extend(profile.from_languages.all())


        return render(request, 'order/create_order_step1.html', {"job_obj": job_obj, "languages":supported_from_langs})
    else:
        return redirect("/login")  

# Render page for step 2 of creating an order
def order_step2(request, job_id):
    '''
    Reders page for step 2 of creating an order,
    '''
    if request.user.is_active:
        job_obj = Job.objects.get(job_id= job_id)
        #Fetches and sends all the data required to calculate 
        #price of an Job instantly on the client side
        all_profile = Profile.objects.all().filter(from_languages=job_obj.source_language)
        supported_to_langs = []
        for profile in all_profile:
            supported_to_langs.extend(profile.from_languages.all().exclude(pk=job_obj.source_language.pk)  )


        #languages = Language.objects.all().exclude(pk=job_obj.source_language.pk)  
        quality_types = Quality.objects.all()
        content_types = Content.objects.all()
        rates = Rate.objects.all().filter(source_language=job_obj.source_language)
        return render(request, 'order/create_order_step2.html', {"job_obj": job_obj, "languages":supported_to_langs, "quality_types":quality_types, "content_types":content_types, "rates":rates })        
    else:
        return redirect("/login")


def order_delete(request, job_id):
    '''
    delete the order DRAFT
    '''
    if request.user.is_active:
        try:
            job_obj = Job.objects.get(job_id= job_id)
        except: 
            #job draft alredy deleted, add message to be shown in dashboard
            messages.add_message(request, messages.INFO, 'Draft has been deleted.')
            return redirect('/')

        if job_obj.employeer == request.user:
            #delete the draft, add message to be shown in dashboard
            job_obj.delete()
            messages.add_message(request, messages.INFO, 'Draft has been deleted.')
        return redirect('/')        
    else:
        return redirect("/login")


from payment_gateway import verifiers
def order_success(request, job_id, token):
    """
    Stripe's redirect URL if the payment was "processed" successfully
    Marks the order "accepted" and sets it's status as PN --> PENDING
    Once the payment is confirmed via Stripe webhook, status is set to OP --> OPEN  
    """
    if request.user.is_active:
        job_obj = Job.objects.get(job_id= job_id)
        if job_obj.employeer == request.user:
            if verifiers.payment_token_is_valid(token, job_obj):
                if job_obj.accepted == False:
                    job_obj.status = Status.objects.create(status_name="PN", comment="Awaiting payment confirmation from Stripe, this might take a few minutes.")
                    job_obj.accepted = True
                    job_obj.save()
                
                messages.add_message(request, messages.INFO, 'Your order has been created.')
                return redirect('/')   
            else:
                #someone tries to manually enter the URL with wrong payment_token
                messages.add_message(request, messages.INFO, 'Something went wrong, try again later.') 
                return redirect("/")          
        else:
            #the person making the request is not the same as the person who created the job
            messages.add_message(request, messages.INFO, 'Something went wrong, try again later.') 
            return redirect("/")          
    else:
        return redirect("/login")



 
    