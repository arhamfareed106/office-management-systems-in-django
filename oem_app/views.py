from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()  # Query to get all employees
    context = {
        'emps': emps
    }
    print(context)  # Log the context for debugging
    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        # Extract data from the form POST request using .get()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        try:
            salary = int(request.POST.get('salary'))
        except (TypeError, ValueError):
            return HttpResponse('Invalid salary value.')
        
        bonus = int(request.POST.get('bonus', 0))  # Default bonus to 0 if not provided
        phone = request.POST.get('phone')  # No need to convert here if you expect a string
        try:
            dept = int(request.POST.get('dept'))
            role = int(request.POST.get('role'))
        except (TypeError, ValueError):
            return HttpResponse('Invalid department or role value.')

        # Create a new Employee instance
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept_id=dept,  # Assuming dept is ForeignKey
            role_id=role,  # Assuming role is ForeignKey
            hire_date=datetime.now()  # Correct usage of datetime.now()
        )

        # Save the new employee
        new_emp.save()

        return HttpResponse('Employee added successfully.')
    
    elif request.method == 'GET':
        return render(request, 'view_add_emp.html')  # Render form on GET request
    
    else:
        return HttpResponse('Invalid request method.')


def remove_emp(request, emp_id=0):
    if emp_id:
        emp_to_be_removed = get_object_or_404(Employee, id=emp_id)
        emp_to_be_removed.delete()
        return HttpResponse("Employee removed successfully.")
    
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        # Get search criteria from the POST request
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        # Initialize a query set to hold search results
        emps = Employee.objects.all()

        # Filter results based on provided search criteria
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        # Return the filtered results
        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'view_filter_emp.html')  # Render search form
    
    else:
        return HttpResponse("Invalid request method.")
