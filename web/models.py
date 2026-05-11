from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user(models.Model):
    firstname=models.CharField(max_length=255)
    Lastname=models.CharField(max_length=255)
    description =models.TextField(null=True, blank=True)

class tips(models.Model):
    name=models.CharField(max_length=200)  
    description=models.TextField(null=True, blank=True)

class group(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name 





class room(models.Model): 
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group=models.ForeignKey(group, on_delete=models.SET_NULL, null=True) 
    #Firstname = models.CharField(null=True, blank=True, max_length=200)
    FullName=models.CharField(max_length=255)
    #lastName = models.CharField(null=True, blank=True, max_length=200)
    Email = models.EmailField(null=True, blank=True, max_length=200)
    phone = models.CharField(null=True, blank=True, max_length=200)
    id_number= models.CharField(null=True, blank=True, max_length=255) 
    KANGOYA = 'KANGOYA'  
    KASPHAT = 'KASPHAT'  
    NGARA = 'NGARA'
    GRACE_FAMILY= 'GRACE_FAMILY'
    WHITE_HOUSE = 'WHITE_HOUSE'
    KASARANI= 'KASARANI'
    KIKUYU = 'KIKUYU'
    KENYATTA = 'KENYATTA'
    MUCATHA = 'MUCATHA'
    TRUTH_SEEKERS = 'TRUTH_SEEKERS'
    RUIRU = 'RUIRU'
    GACHIE = 'GACHIE'
    SHAMMAH = 'SHAMMAH'
    THINDIGUA = 'THINDIGUA'
    MOMBASA_RD = 'MOMBASA_RD'
    JAMHURI = 'JAMHURU'
    KAHAWA = 'KAHAWA'
    BLOOM_HILL_KAWAIDA = 'BLOOM_HILL_KAWAIDA'
    THIKA= 'THIKA'
    JUJA= 'JUJA'

    CHOICES = [
        (KANGOYA,'Kangoya'),
        (KASPHAT,'Kasphat'),
        (NGARA,'Ngara'),
        (GRACE_FAMILY ,'Grace_family'),
        (WHITE_HOUSE,'White_house'),
        (KASARANI,'Kasarani'),
        (KIKUYU ,'Kikuyu'),
        (KENYATTA, 'Kenyatta'),
        (MUCATHA ,'Mucatha'),
        (TRUTH_SEEKERS ,'Truth_seekers'),
        (RUIRU ,'Ruiru'),
        (GACHIE ,'Gachie'),
        (SHAMMAH,'Shammah'),
        (THINDIGUA ,'Thindigua'),
        (MOMBASA_RD,'Mombasa_rd'),
        (JAMHURI,'Jamhuri'),
        (KAHAWA,'Kahawa'),
        (BLOOM_HILL_KAWAIDA,'Bloom_hill_kawaida'),
        (THIKA,'Thika'),
        (JUJA,'juja'),
        

    ]
   # HBC = models.CharField(null=True, blank=True, max_length=100)  
    HBC = models.CharField(  
        max_length=100,  
        choices=CHOICES,  
        default=KANGOYA,  
    )

    Parent = models.CharField(null=True, blank=True, max_length=200)
    Child = models.CharField(null=True, blank=True, max_length=200)
    Spouse = models.CharField(null=True, blank=True, max_length=200)
    #description=models.TextField(null=True, blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
     return self.FullName if self.FullName is not None else "Unnamed"
    
class message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE) 
    room=models.ForeignKey(room, on_delete=models.CASCADE) 
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    

    class Meta:
          ordering = ['-updated', '-created']

    def __str__(self):
     return self.body or ""

    

class Msg(models.Model):
    sender=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(room, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True ,max_length=100)
    updated= models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
          ordering = ['-updated', '-created']

    def __str__(self):
     return self.body or ""

class MpesaTransaction(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True) 
    profile=models.ForeignKey(room, on_delete=models.CASCADE, blank=True,null=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ) 
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.CharField(max_length=50, blank=True, null=True)  # sometimes comes as int
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    result_code = models.IntegerField(blank=True, null=True)
    result_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']   # newest transactions first

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d')} - {self.full_name} - {self.phone_number} - {self.status}"


    
    
class update(models.Model):
        user_name= models.ForeignKey(User,on_delete=models.CASCADE)
        #last_name=models.ForeignKey(room,on_delete=models.CASCADE, null=True)
        #transaction=models.ForeignKey(MpesaTransaction, on_delete=models.CASCADE, null=True, blank=True)
        transaction = models.OneToOneField(MpesaTransaction, on_delete=models.CASCADE, null=True, blank=True)
        #code=models.CharField(max_length=100)
       # name=models.CharField(null=True, blank=True, max_length=100)
        #amount = models.DecimalField(max_digits=10, decimal_places=1)
        Select= 'Select' 
        bbf= 'bff (OCT 2024 - JUL 2025)' 
        JANUARY = 'JANUARY'  
        FEBRUARY = 'FEBRUARY'  
        MARCH = 'MARCH'
        APRIL= 'APRIL'
        MAY = 'MAY'
        JUNE = 'JUNE'
        JULY = 'JULY'
        AUGUST = 'AUGUST'
        SEPTEMBER = 'SEPTEMBER'
        OCTOBER = 'OCTOBER'
        NOVEMBER = 'NOVEMBER'
        DECEMBER = 'DECEMBER'

        CHOICES = [
        (Select,'select'),
        (bbf,'bbf'),
        (JANUARY,'January'),
        (FEBRUARY,'February'),
        (MARCH,'March'),
        (APRIL ,'April'),
        (MAY ,'May'),
        (JUNE ,'June'),
        (JULY  ,'July'),
        (AUGUST, 'August'),
        (SEPTEMBER ,'September'),
        (OCTOBER ,'October'),
        (NOVEMBER ,'November'),
        (DECEMBER ,'December'),

    ]
        month = models.CharField(null=True, blank=True, max_length=100)  
        choose = models.CharField(  
        max_length=100,  
        choices=CHOICES,  
        default=Select,  
    )
        select= 'Select' 
        year1 = '2022'  
        year2 = '2023'  
        year3 = '2024' 
        year4 = '2025' 
        year5 ='2026' 
        year6 = '2027' 
        year7 = '2028'
        year8 = '2029'
        year9 = '2030'
        

        CHOICES = [
        (year1 ,'2022'),
        (year2,'2023'),
        (year3,'2024'),
        (year4,'2025'),
        (year5 ,'2026'),
        (year6,'2027'),
        (year7,'2028'),
        (year8 ,'2029'),
        (year9, '2030'),
    
       

    ]
        Year = models.CharField(null=True, blank=True, max_length=100)  
        choice = models.CharField(  
        max_length=100,  
        choices=CHOICES,  
        default=2025, 
        )
        updated=models.DateTimeField(auto_now=True)
        created=models.DateTimeField(auto_now_add=True)

        class Meta:
          ordering = ['-updated', '-created']

        def __str__(self):
          return self.choose if self.choose is not None else "Unnamed"

class cash_expenditure(models.Model):
    Expense =models.CharField(max_length=100, blank=True)
    Date =models.CharField(max_length=20, blank=True)
    Amount=models.DecimalField(max_digits=10, decimal_places=2)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
     ordering = ['-updated', '-created']

    def __str__(self):
      return self.Expense or ""
    
class WhatsAppContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)  # Store as 2547XXXXXXX

    def __str__(self):
        return f"{self.name} ({self.phone})"

class BulkMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    recipients_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
class WelfareContribution(models.Model):
    member = models.ForeignKey(room, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()  # 1–12

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('member', 'year', 'month')



    

   
        




  
    






