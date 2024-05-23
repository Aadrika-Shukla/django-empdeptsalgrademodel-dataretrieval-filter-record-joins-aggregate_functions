from django.shortcuts import render
from app.models import *
from django.db.models import * #importing all the aggregate functions
def inner_equi_join(request):
    JDED=Emp.objects.select_related('dept_no').all()
    '''
    JDED=Emp.objects.select_related('dept_no').filter(job='MANAGER')
    JDED=Emp.objects.select_related('dept_no').filter(job='SALESMAN')
    JDED=Emp.objects.select_related('dept_no').filter(sal__gte=2000)
    JDED=Emp.objects.select_related('dept_no').filter(job='SALESMAN')
    '''
    





    #####################  TO CHECK THE RESULT OF OUR AGGREGATE FUNCTIONS AFTER RUNNING SERVER WITH RESPECTIVE URL GO TO CMD   ######################################





    #QTD dept_no whose department average salary is greater than all the employees average salary
    #Display the dept details whose dept avg salary is greater than avg sal of all employees.
    #1st part-avg sal of all employees
    ASAE=Emp.objects.aggregate(A_S_A_E=Avg('sal'))['A_S_A_E'] 
    print(ASAE)
    
    #in sql having clause shows group of rows in ORM annotate+filter shows the same
    #in sql where clause shows a particular row in ORM values() shows the same
    #department average sal>employees avg salary
    GASGEAS=Emp.objects.values('dept_no').annotate(G_A_S=Avg('sal')).filter(G_A_S__gte=ASAE) 
    print(GASGEAS) 
    
    
    

    
    #Display the dept details whose dept avg salary is greater than dept 30 avg salary
    #dept 30 avg salary
    IDAS=Emp.objects.values('dept_no').annotate(G_A_S=Avg('sal')).filter(dept_no=30)[0]['G_A_S']
    print(IDAS)
    #dept avg sal >dept 30 avg sal
    DASIDS=Emp.objects.values('dept_no').annotate(G_A_S=Avg('sal')).filter(G_A_S__gte=IDAS) 
    print(DASIDS)
    

    
    
    d={'JDED':JDED}
    return render(request,'inner_equi_join.html',d)



def selfjoin(request):
    EMJD=Emp.objects.select_related('mgr').all()
    EMJD=Emp.objects.select_related('mgr').filter(ename__startswith='S')
    EMJD=Emp.objects.select_related('mgr').filter(ename__startswith='T')
    EMJD=Emp.objects.select_related('mgr').filter(mgr__sal__gte=1000)
    EMJD=Emp.objects.select_related('mgr').filter(sal__gte=1000)
    EMJD=Emp.objects.select_related('mgr').filter(mgr__isnull=True)
    EMJD=Emp.objects.select_related('mgr').filter(mgr__isnull=False)
    EMJD=Emp.objects.select_related('mgr').filter(emp_no__contains='3333')
    EMJD=Emp.objects.select_related('mgr').filter(mgr__ename__startswith='S')
    EMJD=Emp.objects.select_related('mgr').filter(mgr__ename__endswith='T')
    
    d={'EMJD':EMJD} 
    return render(request,'selfjoin.html',d)


def emp_mgr_dept(request):
    EMDJD=Emp.objects.select_related('mgr','dept_no').all()
    EMDJD=Emp.objects.select_related('mgr','dept_no').filter(mgr__isnull=False)
    EMDJD=Emp.objects.select_related('mgr','dept_no').filter(mgr__ename='SMITH')
    EMDJD=Emp.objects.select_related('mgr','dept_no').filter(mgr__ename='ALLEN',dept_no__dname='RESEARCH')
    #EMDJD=Emp.objects.select_related('mgr','dept_no').filter(mgr__ename__contains='ES',mgr__ename__contains='T')
    
    #here by using extra() we can execute raw sql queries
    EMDJD=Emp.objects.extra(where=["LENGTH(ename) = 5"])
    EMDJD=Emp.objects.extra(where=["ename like 'S%'"])
    EMDJD=Emp.objects.extra(where=["ename='SCOTT'"])
    EMDJD=Emp.objects.extra(where=["sal between 1000 and 3000"])

    
    
    d={'EMDJD':EMDJD}
    return render(request,'emp_mgr_dept.html',d)   


def update_emp(request):
    EMO=Emp.objects.all()
    d={'EMO':EMO}

    #using Update method
    Emp.objects.filter(ename='SCOTT',).update(sal=3000)
    Emp.objects.filter(ename='ROJA',).update(sal=3000)
    Emp.objects.filter(ename='SCOTT',).update(dept_no=100)#foreign key constrained failed
    DO=Dept.objects.get(dept_no=10)
    Emp.objects.filter(ename='SCOTT',).update(dept_no=DO)#give op(value is present in parent table)
    

    #using update_or_create method
    Emp.objects.update_or_create(ename='ALLEN',defaults={'comm':120})
    Emp.objects.update_or_create(job='CLERK',defaults={'comm':120})#It can't update multiple rows(error bcz od update_or_create method)
    Emp.objects.update_or_create(job='PAINTING',defaults={'dept_no':100})#error
    Emp.objects.update_or_create(job='PAINTING',defaults={'dept_no':10})#error (bcz of columns present in table(there may be columns having not null constraints))
    DO=Dept.objects.get(dept_no=10)
    Emp.objects.update_or_create(job='PAINTING',defaults={'dept_no':DO,'emp_no':8888,'ename':'ROJA','sal':10000,'comm':100,'hiredate':'2022-12-02'})#here we have provided object


   
    return render(request,'display_emp.html',d) 

#space for delete




















# Create your views here.
