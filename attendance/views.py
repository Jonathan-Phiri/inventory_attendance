from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Attendance, Student  # Assuming you have models for Attendance and Student
from datetime import datetime
from .models import Item  # Assuming you have an Item model
import json
import traceback
from django.views.decorators.csrf import csrf_exempt

# View to handle attendance (RFID or QR code scanning)
def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        time_in = request.POST.get('time_in')

        # Fetch student record
        student = get_object_or_404(Student, student_id=student_id)
        
        # Record attendance
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            date=datetime.now().date(),
            defaults={'time_in': time_in}
        )
        
        if not created:
            attendance.time_out = time_in  # Assuming time_in works for both in/out
            attendance.save()
        
        return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

# View to fetch attendance history
def attendance_history(request):
    student_id = request.GET.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    
    attendances = Attendance.objects.filter(student=student).values('date', 'time_in', 'time_out')
    
    return JsonResponse(list(attendances), safe=False)



# View to handle adding or updating items


@csrf_exempt
def add_update_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('id')
            name = data.get('name')
            quantity = data.get('quantity')
            
            if not item_id or not name:
                return JsonResponse({'status': 'error', 'message': 'Item ID and Name are required'}, status=400)
            
            try:
                quantity = int(quantity)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Quantity must be a number'}, status=400)
            
            item, created = Item.objects.update_or_create(
                id=item_id,
                defaults={'name': name, 'quantity': quantity}
            )
            action = 'added' if created else 'updated'
            return JsonResponse({'status': 'success', 'message': f'Item {action} successfully!'})
        except Exception as e:
            print(f"Error in add_update_item: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=405)

# View to fetch current inventory

@csrf_exempt
def get_inventory(request):
    try:
        items = Item.objects.all().values('id', 'name', 'quantity')
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print(f"Error in get_inventory: {error_message}")
        print(f"Traceback: {error_traceback}")
        return JsonResponse({'status': 'error', 'message': f'Error fetching inventory: {error_message}'}, status=500)

# View to fetch details for a specific item


def get_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({'id': item.id, 'name': item.name, 'quantity': item.quantity})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

# View to delete an item
@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('id')
            
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Item deleted successfully!'})
        except Exception as e:
            print(f"Error in delete_item: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=405)

def attendance(request):
    return render(request, 'attendance.html')

def inventory(request):
    return render(request, 'inventory.html')